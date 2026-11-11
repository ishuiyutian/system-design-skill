#!/usr/bin/env python3
"""Structural contract for the system-design skill's progressive disclosure."""

import json
import re
from pathlib import Path


def description_value(frontmatter_text: str) -> tuple[str, bool]:
    """Return (description, yaml_checked).

    The installer parses this field with a YAML parser, so an unquoted plain
    scalar containing ': ' breaks installation. PyYAML is optional for
    stdlib-only checkouts; the fallback handles the block/quoted forms this
    repository uses and rejects exactly that failure shape.
    """
    try:
        import yaml
    except ImportError:
        yaml = None
    if yaml is not None:
        data = yaml.safe_load(frontmatter_text)
        assert isinstance(data, dict), "frontmatter must parse to a mapping"
        value = data.get("description")
        assert isinstance(value, str) and value.strip(), (
            "frontmatter description must be a nonempty string"
        )
        return value, True

    lines = frontmatter_text.splitlines()
    start = next(
        (index for index, line in enumerate(lines) if line.startswith("description:")),
        None,
    )
    assert start is not None, "frontmatter has no description"
    head = lines[start][len("description:"):].strip()
    if head in (">-", ">", "|", "|-", ">+", "|+"):
        collected = []
        for following in lines[start + 1:]:
            if following and not following[:1].isspace():
                break
            collected.append(following.strip())
        return " ".join(part for part in collected if part), False
    if head[:1] in ('"', "'"):
        return head[1:].rstrip(head[0]), False
    remainder = " ".join(
        [head] + [line.strip() for line in lines[start + 1:] if line[:1].isspace()]
    )
    assert ": " not in remainder, (
        "unquoted description contains ': ', which breaks YAML installation"
    )
    return remainder, False


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "system-design"
PACK_LINKS = (
    "archetypes/authoritative-state.md",
    "archetypes/derived-serving.md",
    "archetypes/realtime-sync.md",
    "archetypes/traffic-work.md",
    "archetypes/control-security.md",
    "archetypes/data-delivery.md",
)
COMPLETION_MARKERS = (
    "every critical flow ends at a named durable or final effect",
    "every invariant has one enforcement authority",
    "every dependency has a deadline, retry owner, and bounded backlog",
    "every authoritative store has an acknowledgement point, failure domain, RPO, and RTO",
    "every derived view names its reconstruction source and cursor",
    "every candidate has a named first failure",
    "every recommendation has a falsifiable evidence chain",
    "every unresolved uncertainty is recorded as an assumption or measurement",
    "all artifacts pass structural and diagram checks",
)
EXAMPLE_TOPICS = (
    "Scale vs skew",
    "Replication vs backup",
    "Quorum overlap vs freshness",
    "Queue vs log",
    "Idempotent request vs idempotent external effect",
    "Failover vs ownership transfer",
    "Cache freshness vs correctness",
    "Architecture candidate vs database substitution",
)


def mermaid_kind(block: str) -> str:
    head = block.lstrip().split(None, 1)[0] if block.strip() else ""
    if head.startswith("C4"):
        return "c4"
    if head in {"flowchart", "graph"}:
        return "flowchart"
    if head == "sequenceDiagram":
        return "sequence"
    return head or "empty"


def frontmatter(text: str) -> str:
    match = re.match(r"---\n(.*?)\n---", text, re.DOTALL)
    assert match, "SKILL.md has no frontmatter"
    return match.group(1)


def main() -> None:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    skill = (SKILL_DIR / "SKILL.md").read_text()
    skill_description, _yaml_checked = description_value(frontmatter(skill))
    check(
        len(skill_description) <= 700,
        f"description is {len(skill_description)} chars; keep it under 700 (hard limit 1024)",
    )
    check("USE for:" in skill_description, "description lacks a 'USE for:' routing block")
    check("SKIP for:" in skill_description, "description lacks a 'SKIP for:' routing block")
    lowered_description = skill_description.lower()
    for group in (
        ("repository",),
        ("greenfield",),
        ("sharding", "scaling"),
        ("consistency", "datastore"),
        ("caching",),
        ("capacity",),
        ("adr",),
        ("drift", "debt"),
        ("single choice",),
        ("workload numbers",),
    ):
        check(
            any(token in lowered_description for token in group),
            f"description lost a routing trigger: {' or '.join(group)}",
        )
    for jargon in (
        "answers in a paragraph",
        "overengineering gates",
        "structurally distinct",
        "chained evidence argument",
    ):
        check(
            jargon not in lowered_description,
            f"description carries execution detail that belongs in SKILL.md: {jargon!r}",
        )
    index = (SKILL_DIR / "ARCHETYPES.md").read_text()
    examples_path = SKILL_DIR / "EXAMPLES.md"
    check(examples_path.is_file(), "EXAMPLES.md does not exist")
    if examples_path.is_file():
        examples = examples_path.read_text()
        opening = "\n".join(examples.splitlines()[:5])
        check("](SKILL.md)" in opening, "EXAMPLES.md does not backlink SKILL.md in its opening lines")
        headings = re.findall(r"(?m)^## (.+)$", examples)
        check(tuple(headings) == EXAMPLE_TOPICS, "EXAMPLES.md must contain exactly the eight ordered contrasts")
        check(len(re.findall(r"(?m)^\*\*BAD:\*\*", examples)) == 8, "EXAMPLES.md must contain exactly eight BAD examples")
        check(len(re.findall(r"(?m)^\*\*GOOD:\*\*", examples)) == 8, "EXAMPLES.md must contain exactly eight GOOD examples")

    conditional_examples = (
        "](EXAMPLES.md)" in skill
        and "do not load examples by default" in skill.lower()
        and "only if a first-draft recommendation or interface remains generic" in skill.lower()
    )
    check(conditional_examples, "SKILL.md lacks the conditional EXAMPLES.md pointer")

    for link in PACK_LINKS:
        check(f"]({link})" in index, f"ARCHETYPES.md does not link {link}")
        pack_path = SKILL_DIR / link
        check(pack_path.is_file(), f"missing pack file: {link}")
        if pack_path.is_file():
            pack = pack_path.read_text()
            provenance_path = ROOT / "docs" / "provenance" / link
            check(provenance_path.is_file(), f"missing provenance pack file: {link}")
            if provenance_path.is_file():
                runtime_headings = set(re.findall(r"(?m)^## (.+)$", pack))
                provenance_headings = set(
                    re.findall(r"(?m)^## (.+)$", provenance_path.read_text())
                )
                check(
                    runtime_headings == provenance_headings,
                    f"{link}: runtime/provenance ## headings differ "
                    f"(runtime-only={sorted(runtime_headings - provenance_headings)}, "
                    f"provenance-only={sorted(provenance_headings - runtime_headings)})",
                )
            entries = re.split(r"(?m)^## ", pack)[1:]
            check(bool(entries), f"{link} has no archetype entries")
            for entry in entries:
                name = entry.splitlines()[0]
                check("Not when" in entry, f"{link}: {name} has no Not when")
                check("Anti-gate" in entry, f"{link}: {name} has no Anti-gate")

    selective_language = (
        "load only the selected pack" in skill.lower()
        and "do not load every pack" in skill.lower()
    )
    check(selective_language, "SKILL.md does not require selective pack loading")
    schema_language = (
        "database schemas" in skill.lower()
        and "fields" in skill.lower()
        and "indexes" in skill.lower()
        and "relationships" in skill.lower()
        and "no executable ddl" in skill.lower()
    )
    check(schema_language, "SKILL.md does not require intuitive non-executable database schemas")
    check("Diagram kind:" in skill, "SKILL.md does not require recording the diagram kind")
    check("ask the user" in skill.lower(), "SKILL.md does not allow asking the user to choose a diagram kind")
    audit_path = SKILL_DIR / "AUDIT.md"
    check(audit_path.is_file(), "AUDIT.md does not exist")
    if audit_path.is_file():
        audit = audit_path.read_text()
        check("](SKILL.md)" in "\n".join(audit.splitlines()[:5]),
              "AUDIT.md does not backlink SKILL.md in its opening lines")
        check("](AUDIT.md)" in skill, "SKILL.md does not link AUDIT.md at the audit step")
        audit_provenance = ROOT / "docs" / "provenance" / "AUDIT.md"
        check(audit_provenance.is_file(), "missing provenance pack: AUDIT.md")
        if audit_provenance.is_file():
            runtime = set(re.findall(r"(?m)^## (.+)$", audit))
            recorded = set(re.findall(r"(?m)^## (.+)$", audit_provenance.read_text()))
            # A subset, not equality: the runtime file carries a Contents block
            # that has nothing to cite, and every other section must be covered.
            check(recorded <= runtime,
                  f"provenance/AUDIT.md has sections AUDIT.md does not: {sorted(recorded - runtime)}")
            check(not (runtime - recorded - {"Contents"}),
                  f"AUDIT.md sections with no provenance: {sorted(runtime - recorded - {'Contents'})}")
        categories = re.findall(r"(?m)^### ([a-z-]+) — ", audit)
        check(len(categories) == 7, f"AUDIT.md must define exactly seven categories, found {len(categories)}")
        patterns = re.findall(r"(?m)^\| `([a-z-]+)` \|(.*)$", audit)
        check(bool(patterns), "AUDIT.md defines no debt patterns")
        for name, row in patterns:
            # signature | remedy | not-when, the leading cells already consumed.
            # Without a disqualifier a pattern gets matched against a system it
            # does not fit, which is the failure the suppression list exists for.
            cells = [cell.strip() for cell in row.split("|")]
            check(len(cells) >= 3 and cells[2] not in ("", "—"),
                  f"AUDIT.md pattern has no Not when: {name}")
        for level in ("blocking", "high", "medium", "low"):
            check(f"`{level}`" in audit, f"AUDIT.md does not define severity {level}")
        check("`note` is not a severity" in audit,
              "AUDIT.md does not separate observations from severities")
        # Severity has exactly one source. A lens that writes it directly makes
        # the protocol non-deterministic, because stage 4 re-derives afterwards.
        check("severity` has exactly one source" in audit,
              "AUDIT.md does not state that severity has a single source")
        kill_rules = audit.split("### Kill rules")[-1].split("###")[0]
        for verdict in ("Demote to", "Demote to `low`", "set `severity`"):
            check(verdict not in kill_rules,
                  f"a kill rule writes severity directly instead of moving an input: {verdict!r}")
        for banned in ("debt score", "debt index", "remediation hours"):
            check(banned not in audit.lower(), f"AUDIT.md reintroduces a rejected measure: {banned}")

    design_format_path = SKILL_DIR / "DESIGN-FORMAT.md"
    check(design_format_path.is_file(), "DESIGN-FORMAT.md does not exist")
    if design_format_path.is_file():
        design_format = design_format_path.read_text()
        check(
            "](SKILL.md)" in "\n".join(design_format.splitlines()[:5]),
            "DESIGN-FORMAT.md does not backlink SKILL.md in its opening lines",
        )
        lowered_format = design_format.lower()
        for phrase in (
            "DESIGN.md is the source of truth",
            "one diagram kind for the whole design",
            "Diagram kind:",
            "ask the user",
            "C4 structure",
            "flowchart",
            "sequence",
            "the debt register",
        ):
            check(
                phrase.lower() in lowered_format,
                f"DESIGN-FORMAT.md lacks required contract language: {phrase!r}",
            )
        for term in ("finding", "debt", "severity", "remedy", "evidence"):
            check(
                term in design_format.split("## Vocabulary")[-1],
                f"DESIGN-FORMAT.md vocabulary omits {term!r}",
            )

    for forbidden in (
        SKILL_DIR / "HTML-REPORT.md",
        SKILL_DIR / "RUNTIME.md",
        SKILL_DIR / "scripts" / "render_report.py",
        SKILL_DIR / "scripts" / "design_session.py",
        SKILL_DIR / "assets" / "report-template.html",
    ):
        check(
            not forbidden.exists(),
            f"obsolete artifact still present: {forbidden.relative_to(ROOT)}",
        )
    for filename in ("SKILL.md", "DESIGN-FORMAT.md", "HEURISTICS.md", "AUDIT.md"):
        text = (SKILL_DIR / filename).read_text().lower()
        for banned in ("render_report", "report-template", "design_session", "runtime.md", "html-report.md"):
            check(banned not in text, f"{filename} still references removed artifact: {banned}")

    example = ROOT / "examples" / "design-ticketing" / "DESIGN.md"
    check(example.is_file(), "example DESIGN.md does not exist")
    if example.is_file():
        example_text = example.read_text()
        for heading in (
            "## Requirements",
            "## Core entities and invariants",
            "## Data and consistency model",
            "## Database schemas",
            "## System interfaces",
            "## Estimates",
            "## Architectures",
            "## Comparison and recommendation",
            "## Critical deep dives",
            "## Operations and rollout",
            "## Risks and what breaks first",
            "## Measurements that could overturn the decision",
            "## Next steps",
            "## Notes",
        ):
            check(f"{heading}\n" in example_text, f"example DESIGN.md lacks {heading}")
        blocks = re.findall(r"```mermaid\n(.*?)```", example_text, re.DOTALL)
        check(bool(blocks), "example DESIGN.md has no Mermaid diagram")
        kinds = {mermaid_kind(block) for block in blocks}
        check(
            len(kinds) == 1,
            f"example DESIGN.md mixes diagram kinds: {sorted(kinds)}",
        )
        recorded = re.search(r"(?m)^Diagram kind:\s*(.+?)\s*$", example_text)
        check(bool(recorded), "example DESIGN.md does not record its diagram kind")
        if recorded:
            value = recorded.group(1).strip().lower()
            expected = {
                "c4": "c4",
                "c4 structure": "c4",
                "flowchart": "flowchart",
                "sequence": "sequence",
            }.get(value)
            check(
                expected is not None,
                f"example DESIGN.md records an unknown diagram kind: {recorded.group(1)!r}",
            )
            if expected is not None:
                check(
                    kinds == {expected},
                    f"example records {value!r} but uses {sorted(kinds)}",
                )

    completion_match = re.search(
        r"A design is complete only when:\n\n(.*?)(?=\n\nBefore writing, verify:)",
        skill,
        re.DOTALL,
    )
    check(bool(completion_match), "SKILL.md lacks completion contract")
    completion = completion_match.group(1) if completion_match else ""
    check(len(re.findall(r"(?m)^- ", completion)) == 9, "completion contract must contain exactly nine items")
    for marker in COMPLETION_MARKERS:
        check(marker in completion, f"SKILL.md lacks completion marker: {marker}")

    skill_version = re.search(r'(?m)^  version: "([^"]+)"$', frontmatter(skill))
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    check(bool(skill_version), "SKILL.md metadata.version is missing")
    if skill_version:
        check(
            skill_version.group(1) == plugin.get("version"),
            "SKILL.md and plugin.json versions disagree",
        )
        marketplace_versions = {
            entry.get("version")
            for entry in marketplace.get("plugins", [])
            if entry.get("name") == plugin.get("name")
        }
        check(
            marketplace_versions == {skill_version.group(1)},
            "SKILL.md and marketplace plugin version disagree",
        )

    fixture_path = ROOT / "docs" / "evaluations" / "invocation-cases.json"
    check(fixture_path.is_file(), "invocation fixtures do not exist")
    if fixture_path.is_file():
        fixtures = json.loads(fixture_path.read_text())
        required = {
            "full-process", "direct-answer", "non-invocation", "repository",
            "greenfield", "resume", "contradiction", "debugging",
        }
        labels = {case.get("label") for case in fixtures}
        check(len(labels) == len(fixtures), "invocation fixture labels are not unique")
        check(required <= labels, f"invocation fixtures lack labels: {sorted(required - labels)}")
        for case in fixtures:
            check(bool(case.get("prompt")), f"fixture {case.get('label')} lacks an exact prompt")
            check("expectedInvocation" in case, f"fixture {case.get('label')} lacks expectedInvocation")
            check("expectedMode" in case, f"fixture {case.get('label')} lacks expectedMode")
        check(any(case.get("expectedInvocation") is True for case in fixtures), "no positive invocation case")
        check(any(case.get("expectedMode") == "direct-answer" for case in fixtures), "no direct-answer case")
        check(any(case.get("expectedInvocation") is False for case in fixtures), "no negative invocation case")
        cache_cases = {
            case.get("label"): (case.get("expectedInvocation"), case.get("expectedMode"))
            for case in fixtures
        }
        expected_cache_cases = {
            "cache-explanation": (False, "none"),
            "cache-choice": (True, "direct-answer"),
            "global-cache-design": (True, "full-process"),
            "cache-debugging": (False, "none"),
        }
        for label, expected in expected_cache_cases.items():
            check(cache_cases.get(label) == expected, f"invocation boundary case is missing or wrong: {label}")

    if failures:
        raise AssertionError("\n- " + "\n- ".join(failures))
    print("skill contract: ok")


if __name__ == "__main__":
    main()
