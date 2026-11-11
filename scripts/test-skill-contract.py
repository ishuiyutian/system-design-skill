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
    "every critical flow ends at a named durable or final effect in Key Design Decisions",
    "every invariant has one enforcement authority",
    "every load-bearing dependency has a deadline, retry owner, and bounded backlog in Key Design Decisions",
    "every load-bearing authoritative store has an acknowledgement point, failure domain, RPO, and RTO in a plain-language C4 container description",
    "every load-bearing derived view names its reconstruction source and cursor in its C4 container description",
    "every candidate has a named first failure",
    "every recommendation has a falsifiable evidence chain",
    "every unresolved uncertainty is recorded as an assumption or measurement",
    "every required SAD section is present or marked `n/a` with a reason",
    "all artifacts pass structural, C4-validity, and diagram checks",
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


C4_ELEMENT = re.compile(
    r"^\s*(Person_Ext|Person|System_Ext|System|SystemDb_Ext|SystemDb|"
    r"SystemQueue_Ext|SystemQueue|Container_Ext|ContainerDb_Ext|"
    r"ContainerQueue_Ext|ContainerDb|ContainerQueue|Container)"
    r"\(\s*([A-Za-z0-9_]+)\s*,(.*)\)\s*$"
)
C4_REL = re.compile(
    r"^\s*(Rel(?:_[A-Za-z]+)?|BiRel(?:_[A-Za-z]+)?)"
    r"\(\s*([A-Za-z0-9_]+)\s*,\s*([A-Za-z0-9_]+)\s*,(.*)\)\s*$"
)
C4_BOUNDARY = re.compile(
    r'^\s*System_Boundary\(\s*([A-Za-z0-9_]+)\s*,\s*"([^"]*)"\s*\)\s*\{\s*$'
)


def c4_elements(block: str):
    out = []
    for line in block.splitlines():
        match = C4_ELEMENT.match(line)
        if match:
            args = re.findall(r'"([^"]*)"', match.group(3))
            out.append(
                {"keyword": match.group(1), "alias": match.group(2), "args": args}
            )
    return out


def c4_rels(block: str):
    out = []
    for line in block.splitlines():
        match = C4_REL.match(line)
        if match:
            args = re.findall(r'"([^"]*)"', match.group(4))
            out.append(
                {
                    "keyword": match.group(1),
                    "from": match.group(2),
                    "to": match.group(3),
                    "args": args,
                }
            )
    return out


def c4_rel_pairs(block: str):
    return {(rel["from"], rel["to"]) for rel in c4_rels(block)}


def c4_aliases(block: str):
    return {
        element["alias"]
        for element in c4_elements(block)
        if element["keyword"].startswith("Container")
        or element["keyword"]
        in {"System_Ext", "SystemDb_Ext", "SystemQueue_Ext"}
    }


def c4_metadata(block: str):
    scope = re.search(r"%%\s*system-in-scope:\s*([A-Za-z0-9_]+)", block)
    level = re.search(r"%%\s*c4-level:\s*(L1|L2)\b", block)
    return (scope.group(1) if scope else None, level.group(1) if level else None)


def c4_boundary(block: str):
    for line in block.splitlines():
        match = C4_BOUNDARY.match(line)
        if match:
            return match.group(1), match.group(2)
    return None, None


def c4_external_aliases(elements):
    return {
        element["alias"]
        for element in elements
        if element["keyword"]
        in {
            "Person",
            "Person_Ext",
            "System_Ext",
            "SystemDb_Ext",
            "SystemQueue_Ext",
            "Container_Ext",
            "ContainerDb_Ext",
            "ContainerQueue_Ext",
        }
    }


def c4_external_system_aliases(elements):
    return {
        element["alias"]
        for element in elements
        if element["keyword"]
        in {
            "System_Ext",
            "SystemDb_Ext",
            "SystemQueue_Ext",
            "Container_Ext",
            "ContainerDb_Ext",
            "ContainerQueue_Ext",
        }
    }


def c4_internal_aliases(elements):
    return {
        element["alias"]
        for element in elements
        if element["keyword"]
        in {"Container", "ContainerDb", "ContainerQueue"}
    }


def c4_boundary_pairs(block: str, scope: str):
    elements = c4_elements(block)
    external = c4_external_aliases(elements)
    pairs = set()
    for left, right in c4_rel_pairs(block):
        if left in external and right not in external:
            pairs.add((left, scope))
        elif right in external and left not in external:
            pairs.add((scope, right))
    return pairs


def c4_text_values(block: str):
    for element in c4_elements(block):
        for value in element["args"]:
            yield value
    for rel in c4_rels(block):
        for value in rel["args"]:
            yield value


C4_TRANSPORTS = {
    "HTTPS", "HTTP", "gRPC", "GraphQL", "WebSocket", "SQL", "key read",
    "log read", "log append", "log read/append", "object read", "object write",
    "object read/write", "queue", "filesystem", "in-process", "IPC", "AMQP",
}
C4_BARE_ROLES = {"service", "worker", "store", "database", "queue", "cache", "log", "server"}
C4_BANNED_RELATION_VERBS = (
    "uses", "talks to", "communicates with", "interacts with", "connects to",
    "handles", "sends data",
)
C4_BANNED_DESCRIPTION_TERMS = (
    "stdout", "stderr", "spawn", "column", "pointer", "directory", "class ", "function ",
)
C4_READ_VERBS = ("read", "load", "fetch", "query", "scan", "consume", "get", "list")
C4_WRITE_VERBS = ("write", "append", "publish", "store", "record", "capture", "create", "update", "delete", "put")


def c4_title(block: str):
    match = re.search(r"(?m)^\s*title\s+(.+)$", block)
    return match.group(1).strip() if match else None


def c4_legend(block: str):
    match = re.search(r"(?m)^\s*%%\s*legend:\s*(.+)$", block)
    return match.group(1).strip() if match else None


def c4_internal_stores(elements):
    return {
        element["alias"]
        for element in elements
        if element["keyword"] in {"ContainerDb", "ContainerQueue"}
    }


def c4_archive_only(block: str, alias: str) -> bool:
    return re.search(rf"%%\s*archiveOnly:\s*{re.escape(alias)}\b", block) is not None


def c4_exception(block: str, source: str, target: str) -> bool:
    for line in block.splitlines():
        if line.strip().startswith("%% exception:") and source in line and target in line:
            return True
    return False


def c4_store_paths(block: str, alias: str):
    reads = writes = False
    for rel in c4_rels(block):
        if alias not in {rel["from"], rel["to"]}:
            continue
        text = " ".join(rel["args"]).lower()
        reads = reads or any(verb in text for verb in C4_READ_VERBS)
        writes = writes or any(verb in text for verb in C4_WRITE_VERBS)
    return reads, writes


def c4_store_path_errors(block: str):
    errors = []
    for store in c4_internal_stores(c4_elements(block)):
        if c4_archive_only(block, store):
            continue
        reads, writes = c4_store_paths(block, store)
        if not (reads and writes):
            errors.append(store)
    return errors


def c4_boundary_rels(block: str):
    elements = c4_elements(block)
    external = c4_external_aliases(elements)
    internal = c4_internal_aliases(elements)
    return [
        rel for rel in c4_rels(block)
        if (rel["from"] in external and rel["to"] in internal)
        or (rel["from"] in internal and rel["to"] in external)
    ]


def c4_transport_ok(technology: str) -> bool:
    base = technology.split(";", 1)[0].strip()
    parts = base.split(None, 1)
    return len(parts) == 2 and parts[0] in {"sync", "async"} and parts[1] in C4_TRANSPORTS


def c4_has_auth(technology: str) -> bool:
    return re.search(r";\s*auth=\S", technology) is not None



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
    check("Structure diagram:" in skill, "SKILL.md does not require recording the structure diagram role")
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
            "Structure diagram: C4Context + C4Container",
            "C4Context",
            "C4Container",
            "System_Boundary",
            "plain business sentence",
            "Key Design Decisions",
            "the debt register",
            "Context & Background",
            "Security & Regulatory Compliance",
            "Guiding Principles",
            "Business Function Impact",
            "Scope & Requirements",
            "Solution Design",
            "Data Sets & Data Model",
            "Key Design Decisions",
            "Technology Impacts",
            "Data Classifications",
            "Glossary & References",
            "Appendix — Evidence and open questions",
            "Appendix — Architectural debt",
            "Appendix — Critical deep dives",
            "Appendix — Measurements that could overturn the decision",
            "n/a — <reason>",
            "the c4container diagram is the component record",
            "do not add a component table",
            "load-bearing",
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

    c4_rules_path = SKILL_DIR / "C4" / "RULES.md"
    c4_profile_path = SKILL_DIR / "C4" / "PROFILE.md"
    c4_constraints_path = SKILL_DIR / "C4" / "CONSTRAINTS.md"
    check(c4_rules_path.is_file(), "C4/RULES.md does not exist")
    check(c4_profile_path.is_file(), "C4/PROFILE.md does not exist")
    check(c4_constraints_path.is_file(), "C4/CONSTRAINTS.md does not exist")
    for c4_path in (c4_rules_path, c4_profile_path, c4_constraints_path):
        if c4_path.is_file():
            opening = "\n".join(c4_path.read_text().splitlines()[:6])
            check("](../SKILL.md)" in opening, f"{c4_path.name} does not backlink SKILL.md")
    check("](C4/RULES.md)" in skill, "SKILL.md does not link C4/RULES.md at the structure step")
    check("](C4/PROFILE.md)" in skill, "SKILL.md does not link C4/PROFILE.md at the structure step")
    check("](C4/CONSTRAINTS.md)" in skill, "SKILL.md does not link C4/CONSTRAINTS.md at the structure step")
    check("](C4/RULES.md)" in design_format, "DESIGN-FORMAT.md does not link C4/RULES.md")
    check("](C4/PROFILE.md)" in design_format, "DESIGN-FORMAT.md does not link C4/PROFILE.md")
    check("](C4/CONSTRAINTS.md)" in design_format, "DESIGN-FORMAT.md does not link C4/CONSTRAINTS.md")
    check("Container_Boundary` only when" not in design_format, "DESIGN-FORMAT.md still allows Container_Boundary")

    for runtime_path in (c4_rules_path, c4_profile_path, c4_constraints_path):
        provenance_path = ROOT / "docs" / "provenance" / "C4" / runtime_path.name
        check(provenance_path.is_file(), f"missing provenance pack: C4/{runtime_path.name}")
        if provenance_path.is_file():
            runtime_headings = set(re.findall(r"(?m)^## (.+)$", runtime_path.read_text()))
            provenance_headings = set(re.findall(r"(?m)^## (.+)$", provenance_path.read_text()))
            check(
                provenance_headings <= runtime_headings,
                f"provenance/C4/{runtime_path.name} has headings the runtime file lacks",
            )
            check(
                not (runtime_headings - provenance_headings),
                f"C4/{runtime_path.name} sections with no provenance: {sorted(runtime_headings - provenance_headings)}",
            )

    readme_text = (ROOT / "README.md").read_text()
    check("skills/system-design/C4/RULES.md" in readme_text, "README.md does not reference C4/RULES.md")
    check("skills/system-design/C4/PROFILE.md" in readme_text, "README.md does not reference C4/PROFILE.md")
    check("skills/system-design/C4/CONSTRAINTS.md" in readme_text, "README.md does not reference C4/CONSTRAINTS.md")

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
        sad_headings = (
            "## Context & Background",
            "## Security & Regulatory Compliance",
            "## Guiding Principles",
            "## Business Function Impact",
            "## Scope & Requirements",
            "## Solution Design",
            "## Data Sets & Data Model",
            "## Key Design Decisions",
            "## Technology Impacts",
            "## Data Classifications",
            "## Next Steps",
            "## Glossary & References",
            "## Appendix — Evidence and open questions",
            "## Appendix — Critical deep dives",
            "## Appendix — Measurements that could overturn the decision",
            "## Notes",
        )
        for heading in sad_headings:
            check(f"{heading}\n" in example_text, f"example DESIGN.md lacks {heading}")
        positions = []
        for heading in sad_headings:
            if f"{heading}\n" in example_text:
                positions.append(example_text.index(f"{heading}\n"))
        check(
            positions == sorted(positions),
            "example DESIGN.md SAD headings are out of order",
        )
        check(
            "## Appendix — Architectural debt" not in example_text,
            "greenfield example DESIGN.md must omit the debt appendix",
        )
        for heading in sad_headings:
            if heading == "## Notes":
                continue
            marker = f"{heading}\n"
            if marker not in example_text:
                continue
            start = example_text.index(marker) + len(marker)
            next_heading = example_text.find("\n## ", start)
            content = example_text[start:next_heading if next_heading != -1 else None].strip()
            check(bool(content), f"example DESIGN.md has an empty section: {heading}")
        check(
            re.search(r"`n/a — [^`]+`", example_text) is not None,
            "example DESIGN.md does not show an n/a reason",
        )
        for forbidden in (
            "| id | name | kind | zone | tech | note | state contract |",
            "| from | to | kind | label | deadline | retry owner | backlog bound |",
            "| seq | from | to | label | note |",
            "**Components.**",
            "**Edges and contracts.**",
            "**Flows.**",
        ):
            check(
                forbidden not in example_text,
                f"example DESIGN.md still carries a removed candidate table: {forbidden!r}",
            )
        check(
            example_text.count("**Structure.**") == 3,
            "example DESIGN.md must carry one Structure section per candidate",
        )
        check(
            "**Critical flows.**" not in example_text,
            "example DESIGN.md must not carry a critical-flow section",
        )
        check(
            re.search(r"(?m)^Structure diagram:\s*C4Context \+ C4Container\s*$", example_text) is not None,
            "example DESIGN.md does not record C4Context + C4Container for structure",
        )
        structure_blocks = re.findall(
            r"\*\*Structure\.\*\*\n\n```mermaid\n(.*?)```",
            example_text,
            re.DOTALL,
        )
        check(len(structure_blocks) == 3, "example DESIGN.md must have three structure diagrams")
        check(
            all(mermaid_kind(block) == "c4" and "C4Container" in block for block in structure_blocks),
            "example structure diagrams must all be C4Container blocks",
        )
        check(
            all('System_Boundary(ticketing, "Ticketing system")' in block for block in structure_blocks),
            "every C4Container must wrap the business system in System_Boundary",
        )
        check(
            all("Container_Boundary" not in block for block in structure_blocks),
            "example C4Container diagrams must not invent generic Container_Boundary systems",
        )
        blocks = re.findall(r"```mermaid\n(.*?)```", example_text, re.DOTALL)
        check(bool(blocks), "example DESIGN.md has no Mermaid diagram")
        kinds = {mermaid_kind(block) for block in blocks}
        check(
            kinds == {"c4"},
            f"example DESIGN.md must use C4 structure only, found {sorted(kinds)}",
        )
        check(
            "sequenceDiagram" not in example_text and "flowchart" not in example_text,
            "example DESIGN.md must not contain a flow diagram",
        )
        c4_blocks = [block for block in blocks if mermaid_kind(block) == "c4"]
        check(
            sum("C4Context" in block for block in c4_blocks) == 1,
            "example DESIGN.md must contain exactly one C4Context diagram",
        )
        check(
            sum("C4Container" in block for block in c4_blocks) == 3,
            "example DESIGN.md must contain one C4Container diagram per candidate",
        )
        for block in c4_blocks:
            for jargon in ("RPO", "RTO", "WAL fsync", "fenced promotion", "failure domain"):
                check(
                    jargon not in block,
                    f"C4 container descriptions must stay business-readable; found {jargon!r}",
                )

        l1_blocks = [block for block in c4_blocks if block.lstrip().startswith("C4Context")]
        check(len(l1_blocks) == 1, "example DESIGN.md must contain one C4Context block")
        l1 = l1_blocks[0] if l1_blocks else ""
        l1_scope, l1_level = c4_metadata(l1)
        check(bool(l1_scope) and l1_level == "L1", "C4Context must carry L1 metadata")
        l1_elements = c4_elements(l1)
        l1_systems = [e for e in l1_elements if e["keyword"] == "System"]
        check(len(l1_systems) == 1, "C4Context must have exactly one System in scope")
        check(
            not any(
                e["keyword"].startswith("Container")
                or e["keyword"] in {"SystemDb", "SystemQueue"}
                for e in l1_elements
            ),
            "C4Context must not contain containers or deployment elements",
        )
        check(
            not re.search(r"\bcdn\b", l1, re.IGNORECASE),
            "C4Context must not contain a CDN; record it in Technology Impacts",
        )
        check(
            all(len(rel["args"]) == 1 for rel in c4_rels(l1)),
            "C4Context relationships must carry intent only, with no protocol or technology",
        )
        check(len(l1_elements) <= 10, "C4Context exceeds the ten-element budget")
        check(len(c4_rels(l1)) <= 12, "C4Context exceeds the twelve-relationship budget")
        l1_label = l1_systems[0]["args"][0] if l1_systems and l1_systems[0]["args"] else None
        l1_externals = {
            e["alias"]: tuple(e["args"][:2])
            for e in l1_elements
            if e["alias"] in c4_external_aliases(l1_elements) and e["args"]
        }
        l1_rels = c4_rel_pairs(l1)
        realised_pairs = set()

        for block in structure_blocks:
            scope, level = c4_metadata(block)
            check(scope == l1_scope and level == "L2", "C4Container must carry matching L2 metadata")
            boundary_alias, boundary_label = c4_boundary(block)
            check(
                boundary_alias == l1_scope and boundary_label == l1_label,
                "C4Container System_Boundary must match the C4Context scope alias and label",
            )
            check(
                block.count("System_Boundary") == 1,
                "C4Container must have exactly one top-level System_Boundary",
            )
            nested = re.sub(r"System_Boundary", "", block)
            check(
                not re.search(r"\b(?:Container_Boundary|Enterprise_Boundary|Boundary)\b", nested),
                "C4Container must not contain a nested boundary",
            )
            check(
                not re.search(r"\bC4(?:Component|Deployment)\b", block),
                "C4Container must not use a component or deployment diagram",
            )
            elements = c4_elements(block)
            check(
                not any(e["keyword"] == "System" for e in elements),
                "C4Container must not redeclare the context System",
            )
            lines = block.splitlines()
            start = next(
                (i for i, line in enumerate(lines) if C4_BOUNDARY.match(line)),
                None,
            )
            end = next(
                (i for i in range(len(lines) - 1, -1, -1) if lines[i].strip() == "}"),
                None,
            )
            inside = "\n".join(lines[start + 1:end]) if start is not None and end is not None else ""
            inside_elements = c4_elements(inside)
            check(
                not any(e["keyword"].startswith("Person") for e in inside_elements),
                "C4Container must not put a Person inside the boundary",
            )
            internal = c4_internal_aliases(elements)
            check(
                internal <= {e["alias"] for e in inside_elements},
                "C4Container containers must sit inside the System_Boundary",
            )
            check(len(internal) <= 12, "C4Container exceeds the twelve-container budget")
            check(len(c4_rels(block)) <= 18, "C4Container exceeds the eighteen-relationship budget")
            check(len(elements) <= 15, "C4Container exceeds the fifteen-node budget")
            check(
                len(c4_boundary_rels(block)) <= 6,
                "C4Container exceeds six boundary-crossing relationships",
            )
            for element in elements:
                if element["keyword"].startswith("Container"):
                    check(
                        len(element["args"]) == 3
                        and all(element["args"][:3]),
                        f"{element['alias']} must declare label technology and responsibility",
                    )
                elif element["keyword"] in {
                    "Person", "Person_Ext", "System_Ext", "SystemDb_Ext", "SystemQueue_Ext"
                }:
                    check(
                        len(element["args"]) == 2 and all(element["args"]),
                        f"{element['alias']} must declare a label and description",
                    )
            for element in elements:
                if element["alias"] in c4_external_aliases(elements):
                    check(
                        l1_externals.get(element["alias"]) == tuple(element["args"][:2]),
                        f"{element['alias']} must match its C4Context alias label and description",
                    )
            candidate_pairs = c4_boundary_pairs(block, scope)
            realised_pairs |= candidate_pairs
            for pair in candidate_pairs:
                check(
                    pair in l1_rels,
                    f"L2 boundary crossing {pair} has no matching L1 relationship",
                )

        for pair in l1_rels:
            if l1_scope in pair:
                check(
                    pair in realised_pairs,
                    f"L1 relationship {pair} is not realised by any candidate",
                )

        external_meta: dict[str, list[tuple[str, ...]]] = {}
        internal_seen: set[str] = set()
        external_seen: set[str] = set()
        l2_external_seen: set[str] = set()

        for block in c4_blocks:
            level = c4_metadata(block)[1]
            elements = c4_elements(block)
            stores = c4_internal_stores(elements)
            external_systems = c4_external_system_aliases(elements)
            people = {
                element["alias"]
                for element in elements
                if element["keyword"].startswith("Person")
            }
            for element in elements:
                alias = element["alias"]
                if alias in c4_external_aliases(elements):
                    external_seen.add(alias)
                    external_meta.setdefault(alias, []).append(tuple(element["args"][:2]))
                    if level == "L2":
                        l2_external_seen.add(alias)
                if alias in c4_internal_aliases(elements):
                    internal_seen.add(alias)

            check(
                not re.search(r"[^\x00-\x7F]", block),
                "C4 text must be ASCII",
            )
            title = c4_title(block)
            check(bool(title), "C4 block must carry a title")
            if title and l1_label:
                if level == "L1":
                    check(
                        title.startswith("Context view - ") and l1_label in title,
                        f"[S3 B] C4Context title {title!r} must name the level and scope",
                    )
                elif level == "L2":
                    check(
                        title.startswith("Container view - ")
                        and l1_label in title
                        and "Candidate" in title,
                        f"[S3 B] C4Container title {title!r} must name the level scope and candidate",
                    )
            legend = c4_legend(block)
            check(bool(legend), "[F5 M] C4 block must carry a %% legend: line")
            if legend:
                lowered = legend.lower()
                check(
                    "arrow" in lowered and ("owned" in lowered or "owner" in lowered),
                    "[B1 B] C4 legend must state the arrow convention and ownership rule",
                )
            check("Container_Boundary" not in block, "C4 block must not use Container_Boundary")
            check(
                not re.search(r"\bC4(?:Component|Deployment)\b", block),
                "C4 block must not use a component or deployment diagram",
            )
            aliases = [element["alias"] for element in c4_elements(block)]
            check(len(aliases) == len(set(aliases)), "C4 aliases must be unique within a block")
            display_names = [element["args"][0] for element in elements if element["args"]]
            check(
                len(display_names) == len(set(display_names)),
                "[E5 M] C4 display names must be unique within a block",
            )
            boundary_alias, _ = c4_boundary(block)
            declared = set(aliases) | ({boundary_alias} if boundary_alias else set())
            for rel in c4_rels(block):
                check(
                    rel["from"] in declared and rel["to"] in declared,
                    f"C4 relationship {rel['from']}->{rel['to']} names an undeclared alias",
                )
                check(rel["from"] != rel["to"], f"[R7 M] C4 relationship {rel['from']}->{rel['to']} is a self-loop")
            signatures = [
                (rel["from"], rel["to"], rel["args"][0].lower() if rel["args"] else "")
                for rel in c4_rels(block)
            ]
            check(
                len(signatures) == len(set(signatures)),
                "[R7 M] C4 relationships must not duplicate an ordered pair with the same label",
            )
            for element in c4_elements(block):
                alias = element["alias"]
                check(
                    re.fullmatch(r"[a-z][A-Za-z0-9]*", alias) is not None,
                    f"C4 alias {alias!r} is not semantic camelCase",
                )
                check(bool(element["args"]), f"C4 element {alias} has no label")
                if not element["args"]:
                    continue
                label = element["args"][0]
                check(0 < len(label) <= 40, f"C4 label {label!r} exceeds forty characters")
                check(len(label.split()) <= 4, f"[F4 m] C4 label {label!r} exceeds four words")
                if element["keyword"].startswith("Container"):
                    technology = element["args"][1] if len(element["args"]) > 1 else ""
                    description = element["args"][2] if len(element["args"]) > 2 else ""
                    check(
                        0 < len(technology) <= 40,
                        f"C4 technology {technology!r} exceeds forty characters",
                    )
                    check(
                        technology.strip().lower() not in C4_BARE_ROLES,
                        f"[F2 M] C4 technology {technology!r} is a bare role rather than a runtime or store type",
                    )
                else:
                    description = element["args"][1] if len(element["args"]) > 1 else ""
                check(
                    0 < len(description) <= 140,
                    f"C4 description {description!r} exceeds one hundred forty characters",
                )
                check(
                    len(description.split()) <= 24,
                    f"[F4 m] C4 description {description!r} exceeds twenty-four words",
                )
                check(
                    not any(term in description.lower() for term in C4_BANNED_DESCRIPTION_TERMS),
                    f"[F1 B] C4 description {description!r} contains implementation or schema detail",
                )
            for rel in c4_rels(block):
                check(bool(rel["args"]), f"C4 relationship {rel['from']}->{rel['to']} has no label")
                if not rel["args"]:
                    continue
                label = rel["args"][0]
                check(0 < len(label) <= 60, f"C4 relationship label {label!r} exceeds sixty characters")
                check(len(label.split()) <= 8, f"[F4 m] C4 relationship label {label!r} exceeds eight words")
                check(not re.search(r"\d", label), f"C4 relationship label {label!r} contains a number")
                lowered = label.lower()
                check(
                    not any(verb in lowered for verb in C4_BANNED_RELATION_VERBS),
                    f"[R4 M] C4 relationship {rel['from']}->{rel['to']} uses a banned verb",
                )
                check(
                    not re.search(r"\b(?:then|after|before|first|next)\b", lowered),
                    f"[S5 M] C4 relationship {rel['from']}->{rel['to']} contains a temporal connective",
                )
                if len(rel["args"]) > 1:
                    technology = rel["args"][1]
                    check(
                        0 < len(technology) <= 40,
                        f"C4 relationship technology {technology!r} exceeds forty characters",
                    )
                    if level == "L2":
                        check(
                            c4_transport_ok(technology),
                            f"[R2 B] C4 relationship {rel['from']}->{rel['to']} must name sync or async and a transport",
                        )
            for rel in c4_boundary_rels(block):
                technology = rel["args"][1] if len(rel["args"]) > 1 else ""
                check(
                    bool(technology) and c4_has_auth(technology),
                    f"[R11 M] C4 boundary relationship {rel['from']}->{rel['to']} must declare auth posture",
                )
            for rel in c4_rels(block):
                source, target = rel["from"], rel["to"]
                if source in people and target in stores:
                    check(False, f"[R9 B] C4 Person {source} must not connect to internal store {target}")
                if target in people and source in stores:
                    check(False, f"[R9 B] C4 Person {target} must not connect to internal store {source}")
                if source in external_systems and target in stores:
                    check(
                        c4_exception(block, source, target),
                        f"[R10 M] C4 external system {source} needs a recorded exception to write {target}",
                    )
                if target in external_systems and source in stores:
                    check(
                        c4_exception(block, source, target),
                        f"[R10 M] C4 external system {target} needs a recorded exception to receive from {source}",
                    )
            for store in c4_store_path_errors(block):
                check(
                    False,
                    f"[C2 B] C4 store {store} needs an inbound read and write path or archiveOnly",
                )
            related = {alias for pair in c4_rel_pairs(block) for alias in pair}
            check(
                set(aliases) <= related,
                f"[C1 B] C4 block has orphan elements: {sorted(set(aliases) - related)}",
            )
            for value in c4_text_values(block):
                check(
                    not re.search(r"[,()<>]", value),
                    f"C4 text {value!r} contains a comma parenthesis or HTML bracket",
                )

        for alias, metas in external_meta.items():
            check(
                len(set(metas)) == 1,
                f"[V1 M] C4 shared external {alias} drifts across context and candidates",
            )
        check(
            not (internal_seen & external_seen),
            f"[X7 B] C4 alias flips between internal and external: {sorted(internal_seen & external_seen)}",
        )
        check(
            set(l1_externals) <= l2_external_seen,
            f"[X4 M] C4Context externals absent from every candidate: {sorted(set(l1_externals) - l2_external_seen)}",
        )

        negative_store_block = '''
C4Container
  Container(app, "App", "Go service", "Serves requests")
  ContainerDb(store, "Store", "Postgres", "Stores state")
  Rel(app, store, "Writes state", "sync SQL")
'''
        check(
            bool(c4_store_path_errors(negative_store_block)),
            "[C2 B] negative fixture: a write-only store must fail the read and write path check",
        )
        check(
            not c4_store_path_errors(
                negative_store_block.replace(
                    'Rel(app, store, "Writes state", "sync SQL")',
                    'Rel(app, store, "Reads and writes state", "sync SQL")',
                )
            ),
            "negative fixture: a store with both paths must pass",
        )

        candidate_sections = re.split(r"(?m)^#### [ABC] — ", example_text)[1:]
        check(len(candidate_sections) == 3, "example DESIGN.md must contain three candidate sections")
        for index, section in enumerate(candidate_sections):
            label = "ABC"[index]
            structure_match = re.search(
                r"\*\*Structure\.\*\*\n\n```mermaid\n(.*?)```",
                section,
                re.DOTALL,
            )
            check(bool(structure_match), f"candidate {label} has no structure diagram")
            if not structure_match:
                continue
            structure = structure_match.group(1)
            rels = c4_rel_pairs(structure)
            aliases = c4_aliases(structure)
            related = {alias for pair in rels for alias in pair}
            check(
                aliases <= related,
                f"candidate {label} has an orphan C4 container: {sorted(aliases - related)}",
            )


    completion_match = re.search(
        r"A design is complete only when:\n\n(.*?)(?=\n\nBefore writing, verify:)",
        skill,
        re.DOTALL,
    )
    check(bool(completion_match), "SKILL.md lacks completion contract")
    completion = completion_match.group(1) if completion_match else ""
    check(len(re.findall(r"(?m)^- ", completion)) == 10, "completion contract must contain exactly ten items")
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
