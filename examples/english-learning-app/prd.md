# PRD: The Mirror — speech scoring on your own video lines

**Date:** 2026-11-04
**Status:** Draft for the captain's review
**Built from:** `data/english-app-problem-framing.md`, `data/english-app-journey-map.md`,
`data/english-app-problem-statement.md`, `data/listen-to-me-market-premise-research/report.md`
**Decomposed into stories:** `data/english-app-user-stories.md` (14 Gherkin stories, plus 4 behaviours
held back because they cannot yet be made testable)

> **This is a document, not a green light.** The captain's standing boundary (2026-11-04) is that no
> coding work begins on this app even after discovery is finished. Nothing here authorises a build.
>
> **Gap tags used throughout:** 🔶 **Assumption** — plausible but unvalidated.
> 🔵 **Open Question** — unknown, needs discovery.

---

## 1. Executive Summary

We are building **a mirror** — a way for a solo English learner working from videos they chose
themselves to find out whether their spoken attempt at a line actually matched the native speaker's.
Today the learner can land on a line and replay it, but nothing tells them how close *their own voice*
came, and there is no teacher to say. The capability is narrow and deliberate: line landing,
transcripts, translation, and looping all exist free elsewhere, so this product is only the missing
half — the feedback. Success is a learner who can tell improvement from mere repetition, instead of
practising on hope.

---

## 2. Problem Statement

### Who has this problem?

An English learner who studies **alone**, from **real videos they chose themselves** (Bilibili,
YouTube), and who **learns by ear** — reading fluency is not their bottleneck, speaking is.

### What is the problem?

They cannot find out whether their spoken attempt at a line was close to the native speaker's. They
can hear the line as many times as they like; replay plays the *speaker*, never *them*. Without a
teacher, "close enough" is a guess they make alone.

### Why is it painful?

- **User impact:** practice is unsupervised and unmeasurable. Months can pass repeating the same
  error with no signal. The learner cannot distinguish improvement from repetition.
- **Downstream impact:** unsupported practice decays into passive watching — the journey map ends
  Phase 6 with the learner giving up and returning to watching with nothing learned.

### Evidence

- **Reported behaviour (captain):** genuinely drills lines by dragging the progress bar; fails in five
  observed ways, three of them precision failures.
- **Reported emotion:** frustration and impatience; "it's tedious enough that I give up and go back to
  just watching"; pushing through costs too much time.
- **Market evidence (2026-11-04 partial survey):** no surveyed product scores the learner's speech
  against their own imported video. Language Reactor and Migaku have video but no scoring; ELSA Speak
  scores speech but has no video. The two halves exist separately and nowhere joined.
- 🔵 **Not evidenced:** any other learner's experience. The beginner-who-cannot-read persona in the
  journey map is entirely hypothesised.

### Supporting context

`data/english-app-journey-map.md` — current-state journey, six phases, ending in abandonment.

---

## 3. Target Users & Personas

### Primary persona — the solo self-directed learner (evidenced)

- **Level:** reads English well enough to follow subtitles; speaking is the gap
- **Content:** self-chosen long-form video from Bilibili / YouTube, not a course
- **Setting:** alone, at a desk, on their own machine; no teacher, no class, no feedback loop
- **Motivation:** comes from the content; if it stops being interesting, they stop
- **Current behaviour:** drags the progress bar, overshoots, loses the line, gives up
- **Goal:** say the line aloud, unaided, without the subtitles

### Secondary persona — the beginner who cannot read the transcript (hypothesised) 🔶

- Every cell is inference; **no such learner has been observed**
- Suspected inversion: for the primary persona subtitles are an *anchor*; for this learner they are a
  *wall*, presenting a barrier before any audio work begins
- The Chinese-meaning scaffold exists primarily for this persona
- 🔵 **Assumption to test before building anything for them**

### Jobs to be done

> When I hear a line I want to own, help me find out whether I can already say it the way the native
> speaker does — so I know whether to keep working or move on.

---

## 4. Strategic Context

### Business goals

**None, by design.** This is a personal tool: free, local, single user. There are no OKRs, no revenue
target, no retention metric, and inventing them would misrepresent the project.

A long-term ambition to serve other learners exists but **must not shape v1** — a standing decision
recorded in the framing document.

### Market opportunity

**Deliberately not sized.** TAM/SAM/SOM are meaningless for a tool with no commercial intent. What
matters instead is coverage, and that has been measured:

| Requirement | Status in the market (verified 2026-11-04) |
|---|---|
| Import own video | Language Reactor: free, verified live. Migaku: paid |
| Auto subtitles | Both. Language Reactor free, no sign-in |
| Land on a line | Language Reactor: verified, precise |
| Loop a selection until stopped | **Not found anywhere** |
| Score own speech on own video | **Not found anywhere** |
| Chinese meaning on demand | Language Reactor renders it, but shown by default |

### Competitive landscape

- **Language Reactor** — free, closest overall; covers four requirements; no speech scoring, no loop
- **Migaku** — paid ($10–15/mo); local video + subtitles; single-line repeat; no scoring
- **ELSA Speak** — best-in-class per-sound scoring; no video, no own content
- **LingQ** — imports captions as text, not video; thin evidence
- 🔵 **Incomplete:** roughly half the named candidates and the entire Chinese-language market were
  never surveyed

### Why now?

**Personal motivation, not a market window.** The captain wants to fix specific sounds in his accent
now, and has not found anything that does it. The round-one "it's new" argument was **refuted** —
sentence-level replay is years-old technology — and is not used here.

The one factual advantage worth stating: **no existing tool is free, local, and scores the learner's own
imported video at the same time.**

| Product | Free | Accepts your own video | Scores your own speech |
|---|---|---|---|
| Language Reactor | yes | yes | **no** |
| Migaku | no | yes | **no** |
| ELSA Speak | no | n/a | yes, but **no video** |

Each product holds two of the three. None holds all three. (Language Reactor and Migaku run in a
browser and process your file there; "free and local" here means no account, no subscription, and your
own file rather than a vendor catalog — not that nothing leaves the machine.)

### The uncomfortable strategic fact

**This product knowingly duplicates capability that is already free.** Line landing, transcription,
and translation all exist. The only genuine gaps are speech scoring and a real selection loop. Any
plan must say so out loud rather than quietly rebuilding a video player.

---

## 5. Solution Overview

An addition to the existing `listen-to-me` app — not a new product. That app already imports a local
video, auto-transcribes it with Whisper, shows a synced sentence list, seeks to a clicked line, and
loops one sentence. What it lacks is the mirror.

**How it works:**

1. The learner imports or opens a video and gets its sentence-split transcript (already works today)
2. They pick a line — or a run of consecutive lines — and loop it by ear
3. They record an attempt by speaking the line
4. The attempt is compared against **that line's own audio from the video** — the native speaker
   saying exactly that sentence
5. Feedback names the substitution per phoneme — "you said /s/ where /θ/ was expected" — and reports
   a match count, "8 of 10 sounds matched", with no percentage and no grade
6. The learner decides whether to keep working or move on. **The score never gates them.**

**The design insight that makes this achievable:** the reference already exists in the learner's own
file. No text-to-speech, no cloud service, no synthetic reference speaker. Both the reference and the
attempt go through the same local model, and the comparison is between two recordings of the same
sentence.

**The model, settled by probe:** `facebook/wav2vec2-lv-60-espeak-cv-ft` — a true **IPA phoneme**
recogniser with a 392-token vocabulary (`θ ð ʃ ʒ ŋ æ ɹ ɾ ʔ ɑː ɔː aɪ aʊ dʒ tʃ`). It ships as PyTorch
only, so it must be converted to ONNX **once** at build time; at runtime it loads in 356 ms and scores
2 seconds of audio in 81 ms on CPU. A lighter character-level alternative (`Xenova/wav2vec2-base-960h`,
95 MB, official ONNX) exists as a fallback that needs no conversion. Evidence:
`data/english-app-probe-phoneme-model.md`.

**Key features:**

- Record-and-score one line, or a run of lines, at a time
- Per-sound feedback presented as detail, never as pass/fail
- Attempt history per line, so improvement is visible across tries
- Chinese meaning per line on demand, never default-on
- Everything local: no upload, no account, no cost

🔵 **Not yet specified:** what per-sound feedback *looks like*, what counts as "close", and which
model performs the comparison. These are the three things standing between this document and a plan.

---

## 6. Success Metrics

There are no users to instrument and no analytics, so these are **personal and observable**, not
product metrics.

### Primary metric

**A specific substitution disappears and stays gone.**
- Definition: an error pattern present in early attempts on a line — e.g. /s/ produced where /θ/ was
  expected — stops appearing in later attempts on that line **and is still absent about a week later**
- Baseline: **never measured** — nothing records attempts today
- How observed: the retained results per line (all results are kept; only the latest recording per line
  is stored), read back against the substitution list
- Why this and not a score: a rising match count can move by luck, "can say it unaided" measures
  memory rather than pronunciation, and "any improvement counts" would make the product unfalsifiable

### Secondary metrics

- **Scoring agreement** — does the feedback match the learner's own judgement of their attempt?
  **A quality check, not a target:** the learner stays the authority, so disagreement signals a problem
  with the feedback, not with the learner
- **Attempts per line** — a proxy for whether the loop is being used or abandoned
- **Time from wanting a line to drilling it** — the journey map's Phase 3–4 cost; today it is dominated
  by bar-fighting

### Guardrail metrics

- **The score must never gate.** No pass/fail, no automatic progression. Violating this breaks the
  standing decision recorded in the framing document
- **No learner audio leaves the machine.** Ever
- **Existing transcription must keep working** — the Whisper path is cached and functional; the change
  must not break it
- **Free and offline.** No subscription, no account, no network dependency after setup

---

## 7. User Stories & Requirements

### Epic hypothesis

> We believe that adding per-sound speech feedback on the learner's own video lines will let a solo
> learner tell improvement from repetition, because today they can replay the native speaker but never
> hear themselves compared — and we will know it works when the learner can name specific sounds they
> fixed and reports that the score matches their own judgement.

### Story 1 — Loop a line or a run of lines

As a learner, I want to select one line or several consecutive lines and have them repeat until I
stop, so I can drill by ear without fighting the progress bar.

*(Note: a run loops for listening only. Scoring always applies to one line — §10b Q6.)*

**Acceptance criteria**
- [ ] Playback defaults to starting at the first line
- [ ] Clicking any line seeks to exactly that line's start
- [ ] A selection can be one line or a run of consecutive lines
- [ ] The selection repeats continuously until the learner stops it
- [ ] Stopping holds position rather than restarting the video

### Story 2 — Record an attempt at the selected line

As a learner, I want to record myself saying the line, so there is something to compare.

**Acceptance criteria**
- [ ] Recording starts and stops on an explicit control
- [ ] The learner can hear their own recording back before scoring
- [ ] Recording is stored locally only
- [ ] A failed or empty recording reports clearly rather than producing a misleading score

### Story 3 — Score the attempt against the video's own line audio

As a learner, I want my attempt compared to the native speaker saying that exact line, so the feedback
reflects the right target.

**Acceptance criteria**
- [ ] The reference is the line's own audio sliced from the video — not TTS, not a stock voice
- [ ] The comparison runs locally
- [ ] If the reference audio is unusable (music, noise, silence), the app says so instead of scoring
- [ ] The score never blocks the learner from continuing

### Story 4 — See per-phoneme detail, named

As a learner, I want to be told which sound I substituted and for what, so I know which habit to fix.

**Acceptance criteria**
- [ ] Feedback names the substitution per phoneme — "you said /s/ where /θ/ was expected"
- [ ] The overall result is a match count — "8 of 10 sounds matched" — with no percentage, grade, or
      pass mark
- [ ] Dissimilarity is shown as information, never as a failure state

### Story 5 — Reveal Chinese meaning on demand

As a learner, I want the Chinese meaning of a line available on a button, so I can check sense without
reading being the default.

**Acceptance criteria**
- [ ] Translation is hidden by default for every line
- [ ] One control per line reveals it
- [ ] Revealing one line does not reveal others

### Story 6 — Keep a record of attempts per line

As a learner, I want to see my past attempts on a line, so improvement is visible across tries.

**Acceptance criteria**
- [ ] Every result is retained per line — a few hundred bytes each
- [ ] Only the latest recording per line is kept; earlier audio is discarded after scoring
- [ ] The learner can read an earlier result beside a later one to see a substitution stop appearing

### Constraints & edge cases

- **Platform:** the existing app is macOS + Node 22.12+; it runs a local server with a browser UI.
  Phone and tablet access means pointing a browser at that server — not a native app
- **Reference quality:** a line sung, whispered, or over music cannot be a fair target
- **Microphone variance:** built-in mic versus headset produces different scores for the same attempt 🔶
- **Partial attempts:** the learner may say half the line; the comparison must not silently reward it
- **Multi-line selections:** scoring a run of lines raises a design question — score per line, or the
  run as a whole? 🔵 undecided

---

## 8. Out of Scope

**Not in this release:**

- **Accounts, sign-in, multi-device sync** — the app is local and single-user. Long-term product
  ambitions must not shape v1
- **Hosted scoring, cloud speech APIs, any upload of learner audio** — contradicts free, local, and
  private
- **Cloud-drive import** (Google Drive, Baidu, Tencent) — a separate queued item, gated on the
  captain's own developer credentials
- **Languages other than English**
- **Advanced-specific coaching** — dedicated accent drills, phoneme practice modes
- **Score-gated progression** — never; the score is a coach
- **Building a new player, transcript pipeline, or translation system** — `listen-to-me` already has
  them, and Language Reactor offers them free
- **Native mobile apps**
- **Scoring a run of lines as one unit** — scoring is per line (§10b Q6). Run-level scoring needs
  automatic segmentation of the learner's recording and may follow once single-line scoring is proven

---

## 9. Dependencies & Risks

### Dependencies

- **`listen-to-me`** as the host app, with its Fastify server, React + Vite frontend, SQLite storage,
  `ffmpeg-static` audio extraction, and `@huggingface/transformers` + `onnxruntime-node` runtime — all
  already installed and proven able to run ONNX models locally
- **Whisper transcription** for the sentence-split transcript — already cached locally (75 MB) and
  working
- **A speech-comparison model** — **identified and proven runnable.**
  `facebook/wav2vec2-lv-60-espeak-cv-ft` from ModelScope, converted to ONNX once at build time. Needs a
  Python toolchain (torch + transformers + onnxscript) **to produce** the artifact; the app itself needs
  only Node (`data/english-app-probe-phoneme-model.md`)
- **ModelScope** as the download route — the working replacement for Hugging Face
  (`https://modelscope.cn/models/<org>/<name>/resolve/master/<file>`)

### Risks and mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| ~~**Model download path is broken**~~ | ~~BLOCKER~~ **RESOLVED** | **ModelScope works** — 95 MB in 9 s, mirrors the Xenova ONNX repos. Route the app at it (`data/english-app-probe-speech-model.md`) |
| **Local speech scoring may not be accurate enough** on real speech | **HIGH** | The probe proved *mechanics* on synthetic tones only: download, local execution, and alignment all work, and a near-miss separates from an unrelated signal by 3.44×. Accuracy on real human speech is still unproven — record one real line before any wider plan |
| ~~**Per-sound detail is only character-level**~~ | ~~MEDIUM~~ **RESOLVED** | A true phoneme model was found, converted and run locally (`data/english-app-probe-phoneme-model.md`). Cost is a 1.26 GB download plus a one-time conversion; quantisation still to do |
| Scoring disagrees with the learner's own judgement often enough to be untrustworthy | HIGH | Measure agreement early; a score that misleads is worse than none |
| Building a duplicate of free capability | MEDIUM | Keep scope to scoring and the loop; do not rebuild the player or the transcript |
| The beginner persona is invented | MEDIUM | Observe one real beginner before building anything for them |
| Duplicate work across `listen-to-me` and this scope | LOW | One app; replace parts rather than forking |

---

## 10. Open Questions

**Corrected 2026-11-04.** The first draft of this section listed only seven questions, while the body of
the document carried several more tagged inline. All twelve are consolidated here, grouped by what
would actually answer each one. **None is answered.**

### 10a — Probe questions — **1 and 2 ANSWERED 2026-11-04**

Full evidence: `data/english-app-probe-speech-model.md`

1. ~~**Which model performs the comparison**, and does a usable one exist that this machine can run
   offline?~~ **ANSWERED — YES, at phoneme level.**
   `facebook/wav2vec2-lv-60-espeak-cv-ft` (IPA vocabulary, 392 tokens) was downloaded from ModelScope,
   converted to ONNX, and run locally: **356 ms load, 81 ms inference for 2 s of audio on CPU.**
   `Xenova/wav2vec2-base-960h` (95 MB, character-level) remains a lighter fallback that needs no
   conversion. Evidence: `data/english-app-probe-speech-model.md` and
   `data/english-app-probe-phoneme-model.md`.
2. ~~**Can a reliable model download source be established at all?**~~ **ANSWERED — YES.**
   **ModelScope works**: `https://modelscope.cn/models/<org>/<name>/resolve/master/<file>`, 95 MB in
   9 seconds, and it mirrors the Xenova ONNX repos this app already uses. Both `huggingface.co` and
   `hf-mirror.com` remain unusable.
3. ~~**Is the reference the video's own line audio, or phonemes derived from the transcript?**~~
   **ANSWERED 2026-11-04 — the video's own line audio.** The native speaker saying that exact sentence
   is the reference. The model consumes raw float32 audio directly, so no phoneme dictionary is needed
   and both sides pass through one model as two recordings of the same line. This settles §5's design
   insight as the implemented path. Phoneme-from-transcript is not only less honest, it is currently
   impossible with the character-level model alone. **Superseded by the phoneme probe below: a true
   phoneme model was found and run, so phoneme-level scoring is back on the table.**

**Per-sound detail: RESOLVED IN THE CAPTAIN'S FAVOUR.** A second probe
(`data/english-app-probe-phoneme-model.md`) found that a true phoneme model **is** reachable and
runnable:

- `facebook/wav2vec2-lv-60-espeak-cv-ft` is mirrored on **ModelScope** (1.26 GB PyTorch weights)
- Its vocabulary is genuine IPA — `θ ð ʃ ʒ ŋ æ ɹ ɾ ʔ ɑː ɔː aɪ aʊ dʒ tʃ` — 392 tokens
- **No ONNX export exists**, so it was converted here with `torch.onnx.export` (torch 2.15,
  transformers 5.22, opset 17)
- Verified locally: **load 356 ms, inference 81 ms for 2 s audio on CPU**, emitting IPA tokens

So **per-phoneme detail, as originally chosen, is achievable.** The cost is one large download plus a
one-time Python conversion step — not a per-use cost.

**CAPTAIN'S DECISION 2026-11-04: adopt the per-phoneme model.** Per-sound detail stands as originally
chosen, at true phoneme granularity. Consequences:

- The scoring model is `facebook/wav2vec2-lv-60-espeak-cv-ft`, converted to ONNX once at build time
- A Python toolchain (torch + transformers + onnxscript) is required **to produce** the artifact, not
  to run the app
- **Open sub-task:** int8 quantisation to bring 1.26 GB fp32 down to roughly 320 MB
- **Open sub-task:** accuracy on real speech against a real video line, still unproven
- `Xenova/wav2vec2-base-960h` (95 MB, character-level, official ONNX) is no longer the plan, but stays
  available as a fallback if the phoneme artifact proves impractical to ship

### 10b — Need a decision from the captain

4. ~~**What counts as "close"?**~~ **ANSWERED 2026-11-04 — named substitution.** Feedback reports
   *what the learner actually said instead of the expected phoneme* — e.g. "you said /s/ where /θ/ was
   expected" — rather than a pass mark or a bare number. Chosen because the mistakes an accent learner
   makes are **systematic substitutions** (`θ`→`s`/`f`, `l`/`n` merging), and naming the habit is
   actionable in a way that "67%" is not. Rejected alternatives: binary match (too blunt), graded
   value alone (a number tells you something went wrong but not what to fix).
   **Follow-up ANSWERED 2026-11-04 — match count, not a score.** The result is expressed as
   **"N of M sounds matched, and here are the substitutions"** — e.g. "8 of 10 sounds matched: you said
   /s/ for /θ/, and /n/ for /l/". No 0–100 scale: it would be arbitrary, would invite being read as a
   grade, and would violate the standing rule that the score never gates. This also becomes the
   quantity the primary metric measures — **sounds no longer substituted** — which is the thing the
   learner is actually working on.
5. ~~**What does per-sound feedback look like?**~~ **ANSWERED 2026-11-04.** Per phoneme, the feedback
   names the substitution ("you said /s/ for /θ/"); overall it reports a **match count** ("8 of 10
   sounds matched") plus the substitution list. No percentage, no grade, no pass mark.
6. ~~**Do we score a run of lines as a unit, or per line?**~~ **ANSWERED 2026-11-04 — one line at a
   time.** A run may still loop for listening by ear, but scoring applies to a single chosen line.
   Reason: named substitutions are only actionable when they point at one line's sounds; mixing three
   lines into one recording keeps the finding but loses its location. Run-level scoring may come later,
   after single-line scoring is proven, and needs automatic segmentation that could fail in its own
   ways. **This unblocks the withheld multi-line story, rewritten as loop-only.**
7. ~~**What is the retention policy for recorded attempts** — kept forever, or pruned?~~ **ANSWERED
   2026-11-04 — all results forever, only the latest recording per line.** Results are a few hundred
   bytes each, so progress history costs nothing; recordings are the bulk and lose most of their value
   once scored. The learner can still hear their most recent attempt beside the original. **This
   unblocks the withheld progress-over-time story.**
8. ~~**What target for the primary metric**, and **how much agreement between the score and the
   learner's own judgement is acceptable?**~~ **ANSWERED 2026-11-04 — a substitution disappears and
   stays gone.** The product works when a specific error pattern, e.g. /s/ for /θ/, stops appearing in
   the learner's attempts on a line **and does not return a week later**. Rejected: a rising match
   count (can move by luck without learning), "can say it unaided" (measures memory, not
   pronunciation), and "any of the above" (makes the product unfalsifiable). Agreement between score
   and the learner's own judgement remains a **quality check, not a target** — the score is a coach, so
   the learner's judgement stays authoritative and disagreement is a signal to fix the feedback, not
   the learner.
9. ~~**Is the market survey complete enough to justify building at all?**~~ **ANSWERED 2026-11-04 —
   no further survey; proceed knowingly.** The captain chose not to finish it. The gap is recorded
   rather than closed: eJOY, Toucan, FluentU, Yabla and the video players were never examined, and the
   entire Chinese-language market — 每日英语听力, 有道, Bilibili-adjacent tools — was not reached at all,
   which is the largest blind spot given the content source. Accepted risk: something already doing
   self-imported video plus phoneme scoring may exist and would have been cheaper than building. That
   risk is now a known, accepted one rather than an unknown.
10. ~~**"Why now?"**~~ **ANSWERED 2026-11-04 — personal motivation, plus one factual advantage.**
    The reason is personal: the captain wants to fix specific sounds in his accent now, and nothing he
    has found does it. The factual advantage, not a market thesis: no existing tool is **free, local,
    and scores the learner's own imported video at once** — Language Reactor is free and local-ish but
    scores nothing; Migaku scores nothing and costs money; ELSA scores speech but takes no video.
    §4 should state this plainly instead of implying a market window.

### 10c — Need observation, not reasoning

11. ~~**Does the beginner-who-cannot-read persona exist as described?**~~ **DISPOSITION AGREED
    2026-11-04 — kept, permanently labelled unvalidated.** The captain chose to keep it as a clearly
    marked hypothesis. Nothing is built specifically for it, and the Chinese-meaning button stays in
    scope because he wants it regardless. The inversion it rests on — subtitles as anchor for one
    learner, a wall for another — remains **untested** and must never be cited as research. Observing
    one real beginner is still the only thing that would promote it.
12. ~~**Are the three inferred emotions in the problem statement real?**~~ **ANSWERED 2026-11-04 — all
    three confirmed by the captain.** "Uncertain", "uneasy" and "resigned" all hold. They stay labelled
    with their origin (reasoned first, confirmed after) rather than being rewritten as initial
    research findings.

### Settled

- **Where it lives:** inside `listen-to-me`, replacing parts as needed. Only the mechanical surgery
  remains, which is engineering detail rather than an open question.

## Self-assessment

**Strongest section:** §4 Strategic Context — unusual for a PRD, because instead of inventing business
justification it records the coverage evidence and states plainly that this product deliberately
duplicates free capability. **Weakest section:** §6 Success Metrics — every target is undefined,
because nothing has ever been measured.

**Top assumptions to validate, in order:**

1. **Local speech scoring is achievable on this machine at all** — currently blocked on model download
2. **"Close" can be defined** well enough that the score is trustworthy
3. **The beginner persona exists** as described — presently pure invention

**Recommended next step before this PRD is shared or acted on:** settle the model-download blocker and
prove **one line, end to end** — record an attempt, compare it to that line's audio, show a result.
That single experiment answers questions 1, 2 and 3 at once, and it is the cheapest way to find out
whether this product can exist.

**Standing boundary, restated:** none of this authorises coding work. This is a draft for the
captain's review.
