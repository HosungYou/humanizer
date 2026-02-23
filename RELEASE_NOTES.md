# Release Notes — Humanizer MCP Server v2.1.0

**Date**: 2026-02-23
**Title**: MCP Server — Precise Stylometric Computation for Humanization Pipeline

---

## Highlights

- **Python MCP server** with 4 tools replacing LLM estimation with exact computation
- **Burstiness CV, MTLD, Fano Factor** calculated algorithmically — no more approximation
- **Feedback loop**: `humanizer_verify` returns `needs_another_pass` with specific recommendations
- **Discipline calibration**: psychology, management, education profiles with field-specific thresholds
- **Regression detection**: flags when humanization accidentally decreases burstiness or opener diversity
- **Hedge density tracking**: counts hedging language per sentence for manual review
- **120 tests passing** (84 existing pipeline + 36 new MCP server tests)

---

## What's New

### MCP Server (4 Tools)

The humanizer MCP server provides precise quantitative metrics via `stdio` transport, replacing LLM estimation in the G5/G6/F5 pipeline. LLMs are poor at counting words per sentence, computing standard deviations, and iterating MTLD algorithms — this server handles those computations exactly.

| Tool | Purpose | Pipeline Stage |
|------|---------|---------------|
| `humanizer_metrics` | Full stylometric analysis | G5 Analysis (Stage 2) |
| `humanizer_verify` | Before/after comparison with regression detection | After each G6 pass |
| `humanizer_diff` | Per-metric delta report with improvement percentages | Checkpoint reports |
| `humanizer_status` | Readiness assessment with discipline calibration | Pipeline start |

### `humanizer_metrics`

Computes all quantitative metrics for input text:

| Metric | Algorithm | Human Baseline | AI Typical |
|--------|-----------|---------------|------------|
| Burstiness CV | SD / Mean of sentence word counts | > 0.45 | < 0.30 |
| MTLD | Forward + backward pass, TTR threshold 0.72 | > 80 | < 60 |
| Fano Factor | Variance / Mean of sentence lengths | > 1 (super-Poissonian) | < 1 |
| Sentence Length Range | max - min word count | > 25 | < 15 |
| Paragraph Opener Diversity | unique first-3-words / total paragraphs | > 0.70 | < 0.50 |
| Hedge Density | hedge words / sentence count | varies | high |
| Composite Score | Weighted formula (pattern 60% + burstiness 20% + vocab 10% + structural 10%) | < 30% | > 60% |

Parameters: `text`, `pattern_score`, `structural_penalty`, `non_native`, `discipline`

### `humanizer_verify`

Compares metrics before and after humanization. Returns:
- Per-metric comparison (before/after values)
- `regressions` array with severity ratings (high/moderate/low)
- `needs_another_pass: bool` — true if composite > 30% or any metric regressed
- `recommendations` array with specific guidance for the next pass

Resolves **Gap 1** (feedback loop) and **Gap 6** (pattern recovery detection) from v2.0.

### `humanizer_diff`

Generates a per-metric delta report:
- Delta values and improvement percentages for all 9 metrics
- Sentence length distribution comparison (before/after word count arrays)

Resolves **Gap 5** (diff visualization) from v2.0.

### `humanizer_status`

Pipeline readiness assessment:
- Per-metric pass/fail against discipline-specific thresholds
- Distance-to-target for each metric
- Overall `readiness: "ready" | "needs_work"`

Resolves **Gap 3** (discipline calibration) from v2.0.

### Discipline Calibration Profiles

| Discipline | Burstiness Threshold | MTLD Threshold |
|------------|---------------------|----------------|
| Default | 0.45 | 80 |
| Psychology | 0.40 | 75 |
| Management | 0.42 | 78 |
| Education | 0.43 | 76 |

Pass `discipline="psychology"` to any tool for field-specific thresholds.

### Sentence Tokenization

Pure Python tokenizer with protection for:
- Abbreviations: et al., Fig., Dr., Prof., etc.
- Decimal numbers: 0.45, p = .001
- Parenthetical citations: (Author, 2024).
- Minimum 3-word sentence filter to avoid fragments

### Non-Native Speaker Calibration

When `non_native=True`, burstiness threshold lowers from 0.45 to 0.35 (based on Liang et al., 2023).

---

## Gaps Resolved from v2.0

| Gap | v2.0 Status | v2.1 Resolution |
|-----|-------------|-----------------|
| Gap 1: Feedback loop | No automatic retry | `humanizer_verify` returns `needs_another_pass` with recommendations |
| Gap 3: Discipline calibration | Generic thresholds | `humanizer_status` with discipline-specific profiles |
| Gap 5: Diff visualization | No side-by-side | `humanizer_diff` with per-metric deltas |
| Gap 6: Pattern recovery | Flag only | `humanizer_verify` detects opener diversity regression |
| Gap 7: Hedge calibration | No measurement | `humanizer_metrics` returns `hedge_density` |

---

## Files

**6 new files (~500 LOC production, ~320 LOC tests)**

| File | Description |
|------|-------------|
| `pyproject.toml` | Package config with hatchling backend, pytest config |
| `src/humanizer_mcp/__init__.py` | Package init, version 2.1.0 |
| `src/humanizer_mcp/metrics.py` | Core algorithms (~280 LOC) |
| `src/humanizer_mcp/server.py` | FastMCP server with 4 tools (~150 LOC) |
| `tests/test_metrics.py` | 28 unit tests across 9 test classes |
| `tests/test_server.py` | 8 integration tests for all 4 tools |

---

## Agent Integration

The following Diverga agents are updated to call MCP tools when available:

| Agent | Tool Used | Fallback |
|-------|-----------|----------|
| G5 (Academic Style Auditor) | `humanizer_metrics`, `humanizer_status` | LLM estimation |
| G6 (Academic Style Humanizer) | `humanizer_verify`, `humanizer_diff` | LLM estimation |
| F5 (Humanization Verifier) | `humanizer_verify` | LLM estimation |

---

## Installation

```bash
cd /Users/hosung/humanizer
pip install -e .
```

MCP server registration in `~/.claude/settings.json`:
```json
"humanizer": {
  "command": "/Users/hosung/humanizer/.venv/bin/python",
  "args": ["-m", "humanizer_mcp.server"],
  "cwd": "/Users/hosung/humanizer"
}
```

---

## Test Results

```
120 passed in 0.29s
  - 84 existing pipeline tests (test_pipeline_v2.py)
  - 28 metrics unit tests (test_metrics.py)
  - 8 server integration tests (test_server.py)
```

---

## Breaking Changes

None. v2.1 is additive — the MCP server is a new component that agents use when available, with graceful LLM estimation fallback.

---

*Humanizer v2.1.0 — Released 2026-02-23*
*Diverga v9.2.0 — MCP Tool Integration*
*Repository: https://github.com/HosungYou/humanizer*
*Diverga plugin: https://github.com/HosungYou/Diverga*

---
---

# Release Notes — Diverga Humanization Pipeline v2.0.0

**Date**: 2026-02-22
**Title**: Humanization Pipeline v2.0 — Multi-Pass Iterative Architecture

---

## Highlights

- **Multi-pass pipeline** replacing single-pass: Pass 1 (Vocabulary), Pass 2 (Structural), Pass 3 (Polish, optional)
- **4 new structural detection patterns** (S7–S10) discovered through empirical humanization rounds
- **Quantitative stylometric metrics**: burstiness CV, MTLD, sentence length range, paragraph opener diversity
- **Composite AI probability scoring formula** combining pattern-based and quantitative signals: `AI_Probability = (0.60 × pattern_score) + (0.20 × burstiness_penalty) + (0.10 × vocab_diversity_penalty) + (0.10 × structural_penalty)`
- **Section-aware mode escalation**: per-section transformation intensity based on G5 section scores
- **Score target presets**: `journal_safe` (30%), `conference` (40%), `working_paper` (50%)
- **F5 Verifier expanded to 7 domains**: burstiness, structural pattern delta, cross-section coherence — up from 4 domains in v1.0
- Full research documentation at https://github.com/HosungYou/humanizer

---

## What's New

### G5 Academic Style Auditor v2.0

G5 now operates on **28 pattern categories** — the original 24 from Wikipedia's AI Cleanup initiative plus four empirically-discovered structural patterns (S7–S10). Detection accuracy is supplemented by a new quantitative metrics dashboard that captures statistical properties of the text that pattern matching alone cannot reliably measure.

#### New Structural Patterns (S7–S10)

These four patterns were identified during Round 3 humanization of two academic papers. After vocabulary-level cleanup drove scores from ~80% to ~60%, structural fingerprints accounted for the remaining AI signal. They are the hardest patterns to address because they operate at paragraph and section level rather than word level.

| Pattern | Weight | Risk | Description |
|---------|--------|------|-------------|
| **S7: Enumeration as Prose** | 12 | HIGH | "First...Second...Third..." ordinal markers embedded in flowing paragraph text (not formatted lists). One of the most persistent AI structural fingerprints. |
| **S8: Repetitive Paragraph Openers** | 10 | HIGH | More than 3 paragraphs in the same section opening with the same syntactic pattern, most commonly "The [noun]..." (e.g., "The results...", "The analysis...", "The findings..."). |
| **S9: Formulaic Section Structure** | 8 | MEDIUM | Discussion section following a rigid template: restate findings → compare to literature → state implications → acknowledge limitations → suggest future research, with no structural deviation. |
| **S10: Hypothesis Checklist Pattern** | 10 | HIGH | Sequential hypothesis confirmation statements in mechanical list format: "H1 was supported. H2 was partially supported. H3 was not supported." |

#### Quantitative Metrics Dashboard

G5 v2.0 calculates four stylometric metrics alongside pattern detection:

| Metric | Method | Human Baseline | AI Typical | Composite Weight |
|--------|--------|---------------|------------|-----------------|
| **Burstiness (CV)** | SD / Mean of sentence lengths | CV > 0.45 | CV < 0.30 | 15 |
| **MTLD** | Mean length of sequential strings maintaining TTR ≥ 0.72 (McCarthy & Jarvis, 2010) | MTLD > 80 | MTLD < 60 | 10 |
| **Sentence Length Range** | max − min word count per sentence | Spread > 25 words | Spread < 15 words | 5 |
| **Paragraph Opener Diversity** | unique first-3-words / total paragraphs | Ratio > 0.70 | Ratio < 0.50 | 8 |

#### Composite Scoring Formula

```
AI_Probability = (0.60 × pattern_score)
              + (0.20 × burstiness_penalty)
              + (0.10 × vocab_diversity_penalty)
              + (0.10 × structural_penalty)
```

Where:
- `pattern_score` = existing G5 pattern algorithm, normalized 0–100
- `burstiness_penalty` = `max(0, (0.45 − CV) / 0.45 × 100)` — zero if CV > 0.45
- `vocab_diversity_penalty` = `max(0, (80 − MTLD) / 80 × 100)` — zero if MTLD > 80
- `structural_penalty` = S7 + S8 + S9 + S10 weighted scores, normalized 0–100

Burstiness carries the highest quantitative weight (20%) because sentence length variance is one of the most reliable discriminators between human and AI text.

#### Non-Native Speaker Calibration (Opt-In)

Based on Liang et al. (2023), who found that over 61% of TOEFL essays were misclassified as AI-generated by at least one detector. When enabled by the user, G5 applies adjusted thresholds:

- Vocabulary flagging weight reduced by 30%
- Verbose phrase flagging weight reduced by 20%
- Burstiness threshold lowered from 0.45 to 0.35

This opt-in calibration must be explicitly requested and is never applied by default.

---

### G6 Academic Style Humanizer v2.0

G6 now operates in three transformation layers. Layer 1 (vocabulary substitution) and Layer 2 (phrase restructuring) are carried over from v1.0. Layer 3 is new.

#### Layer 3: Deep Structural Transformation

Addresses patterns that survive vocabulary substitution and phrase restructuring. Based on Round 3 humanization experience, where structural changes drove scores from approximately 60% to under 30%.

**S7 Enumeration Dissolution** — Converts numbered enumerations embedded in prose into flowing narrative by removing ordinal markers and replacing them with varied transitional devices.

Before:
> First, education significantly predicted AI concern. Second, partisan identity showed the strongest association. Third, age interacted with awareness to shape attitudes.

After:
> Education emerged as a reliable predictor of AI concern, but partisan identity dwarfed its effect — a finding that persisted even after adjusting for demographic covariates. Age told a more complicated story, one that depended heavily on whether respondents had heard of ChatGPT before the survey.

**S8 Paragraph Opener Variation** — Ensures no more than two consecutive paragraphs begin with the same syntactic pattern. Eliminates repetitive "The [X]..." or "This [X]..." openers through syntactic reframing.

**S9 Discussion Architecture Breaking** — Opens Discussion sections with compelling hooks, questions, or surprising findings instead of formulaic "The present study examined..." restatements.

Before:
> The present study examined... Our findings are consistent with...

After:
> Why do Democrats and Republicans — who agree on almost nothing — both worry about AI at nearly identical rates?

**S10 Hypothesis Narrative Conversion** — Converts hypothesis confirmation checklists into thematic narrative anchored by concrete effect sizes and notable non-findings.

Before:
> H1 was supported (p < .001). H2 was partially supported. H3 was not supported.

After:
> The partisan divide we predicted materialized clearly — Republicans were 14 percentage points more likely to express concern (AME = 0.14, p < .001). But the education gradient surprised us: rather than a simple linear relationship, the effect flattened above a bachelor's degree.

#### Burstiness Enhancement

G6 v2.0 deliberately varies sentence length to increase the coefficient of variation (CV) of sentence lengths, targeting CV > 0.45. Strategies include:

1. Insert 2–5 word declarative sentences at impact points ("That gap is real.")
2. Allow 1–2 complex sentences per section to reach 40–60 words
3. Break medium-length sentences (15–25 words) into either shorter or longer forms
4. Use sentence fragments strategically for emphasis
5. Alternate paragraph length: 2-sentence and 6-sentence paragraphs

#### Section-Aware Mode Escalation

Replaces the single-mode-for-entire-document approach. G6 v2.0 automatically applies per-section transformation intensity based on G5 section scores:

| Section | Base Mode | Escalation Trigger | Escalates To |
|---------|-----------|-------------------|--------------|
| Abstract | Conservative | section_score > 50 | Balanced |
| Introduction | Balanced | — | No escalation |
| Methods | Conservative | Never | Conservative |
| Results | Conservative | section_score > 60 (framing language only) | Balanced |
| Discussion | Balanced | section_score > 50 | Aggressive |
| Conclusion | Balanced | section_score > 50 | Aggressive |

Methods sections are never escalated beyond conservative to preserve IMRAD structural integrity and methodological precision.

---

### F5 Humanization Verifier v2.0

F5 expands from 4 to **7 verification domains** and introduces two distinct verification modes to match the multi-pass pipeline structure.

#### Verification Domains

| Domain | Severity | Description |
|--------|----------|-------------|
| 1. Citation Integrity | Critical | Author names, years, page numbers, DOIs unchanged |
| 2. Statistical Accuracy | Critical | Numbers, p-values, effect sizes exact match |
| 3. Meaning Preservation | Major | Core arguments, causal claims, hedging, conclusions intact |
| 4. AI Pattern Reduction | Standard | Probability decreased; no new patterns introduced by G6 |
| 5. Burstiness Verification | Major | CV must not decrease after humanization; flags if still < 0.35 |
| 6. Structural Pattern Check | Major | S7–S10 counts before/after; flags regressions |
| 7. Cross-Section Coherence | Minor | Terminology consistency, internal references, section transitions |

#### Verification Modes

| Mode | When Applied | Domains Checked |
|------|-------------|-----------------|
| **Quick Verify** | After Pass 1 (vocabulary) | Domains 1–2 only (citation + statistics) |
| **Full Verify** | After Pass 2/3 (structural/polish) | All 7 domains |

Quick Verify is lightweight by design — after a vocabulary pass, the primary integrity risk is inadvertent citation or statistic modification. Structural and coherence checks are deferred to Full Verify after structural transformation has occurred.

---

### Pipeline v2.0 Architecture

#### Multi-Pass Flow

```
G5 Analysis
    |
    v
[CP_HUMANIZATION_REVIEW]
    |
    v
Pass 1: G6 Vocabulary Transformation
    |
    v
F5 Quick Verify (Domains 1-2)
    |
    v
[CP_PASS1_REVIEW]
    |
    v
Pass 2: G6 Structural Transformation (Layer 3 + Burstiness)
    |
    v
F5 Full Verify (All 7 Domains)
    |
    v
[CP_PASS2_REVIEW]
    |
    v
[Optional] Pass 3: G6 Polish
    |
    v
F5 Full Verify (All 7 Domains)
    |
    v
[CP_FINAL_REVIEW]
    |
    v
Export
```

#### New Checkpoints (5 added)

| Checkpoint | Level | When |
|------------|-------|------|
| CP_HUMANIZATION_REVIEW | Recommended | After G5 audit, before any transformation |
| CP_PASS1_REVIEW | Recommended | After vocabulary pass, before structural pass |
| CP_PASS2_REVIEW | Recommended | After structural pass, before optional polish |
| CP_FINAL_REVIEW | Optional | After polish pass, before export |
| CP_HUMANIZATION_VERIFY | Optional | Post-humanization verification review |

#### Expanded Finite State Machine

The pipeline FSM expanded from 7 states (v1.0) to **17 states** (v2.0) to represent the multi-pass stages, per-pass verification, checkpoint gates, and optional polish branch.

#### Score Target System

| Preset | Target | Recommended For |
|--------|--------|----------------|
| `journal_safe` | 30% | High-impact journal submissions |
| `conference` | 40% | Conference papers and proceedings |
| `working_paper` | 50% | Working papers and preprints |

Custom targets can be specified directly: "Humanize to target: 35%"

---

## Files Changed

**13 files total: 10 updated, 3 new — approximately 2,728 lines added, 240 removed**

### Updated Files (10)

| File | Change Summary |
|------|----------------|
| `agents/g5.md` | v2.0 agent definition — quantitative metrics, S7–S10 structural patterns, composite scoring, non-native calibration |
| `agents/g6.md` | v2.0 agent definition — Layer 3 structural transformation, burstiness enhancement, section-aware escalation |
| `agents/f5.md` | v2.0 agent definition — 7 verification domains, Quick Verify / Full Verify modes |
| `.claude/references/agents/g5/detection-rules.md` | S7–S10 category definitions, composite scoring algorithm, non-native calibration thresholds |
| `.claude/references/agents/g6/transformations/balanced.yaml` | Structural transformation rules (S7–S10), burstiness enhancement directives |
| `.claude/references/agents/g6/transformations/aggressive.yaml` | Structural transformation rules (S7–S10), burstiness target values |
| `.claude/references/agents/g6/academic-exceptions.md` | Structural transformation exceptions (Methods section IMRAD preservation) |
| `.claude/references/agents/research-coordinator/core/humanization-pipeline.md` | Multi-pass v2.0 architecture, replacing single-pass v1.0 |
| `.claude/checkpoints/checkpoint-definitions.yaml` | 5 new checkpoint definitions (CP_PASS1_REVIEW, CP_PASS2_REVIEW, CP_FINAL_REVIEW, CP_HUMANIZATION_VERIFY, CP_HUMANIZATION_REVIEW) |
| `CLAUDE.md` | v8.1.0 changelog entry, updated humanization pipeline commands, updated agent descriptions |

### New Files (3)

| File | Description |
|------|-------------|
| `.claude/references/agents/g5/structural-patterns.md` | Detailed definitions, detection logic, and examples for S7–S10 |
| `.claude/references/agents/g5/quantitative-metrics.md` | Burstiness CV, Fano Factor, MTLD, sentence length range — calculation methods and baselines |
| `.claude/references/agents/g6/transformations/structural.yaml` | Layer 3 transformation rules reference — S7 dissolution, S8 variation, S9 architecture, S10 narrative |

---

## Breaking Changes

None. v2.0 is fully backward-compatible with v1.0 workflows.

The single-pass pipeline continues to function and is treated as Pass 1 (vocabulary) only. All existing humanization commands work without modification.

---

## Migration Guide

No migration steps are required. Existing humanization workflows continue to operate as before.

### New Commands Available

| Command | Description |
|---------|-------------|
| `"Humanize (multi-pass)"` | Explicit multi-pass with all inter-pass checkpoints |
| `"Humanize to target: 30%"` | Target-based multi-pass until score threshold met |
| `"Humanize (journal_safe)"` | Preset: 30% target |
| `"Humanize (conference)"` | Preset: 40% target |
| `"Humanize (working_paper)"` | Preset: 50% target |

### Behavior Change for Existing Commands

`"Humanize my draft"` now uses the multi-pass pipeline by default (Pass 1 + Pass 2, with optional Pass 3 if the score target is not met). The checkpoint sequence gives users control at each stage. To retain the v1.0 single-pass behavior, use `"Humanize (conservative)"`.

---

## Research Background

This release is grounded in a 3-round empirical humanization study on two academic papers submitted to high-impact journals.

| Paper | Topic | Target Journal | Round 1 | Round 2 | Round 3 |
|-------|-------|----------------|---------|---------|---------|
| Paper 1 | Occupational Identity Threat | TFSC (IF ~12.0) | 80% | 62% | 31% |
| Paper 2 | Epistemic Cognition | IJAIED (IF ~4.7) | 82% | 61% | 22% |

Rounds 1 and 2 applied vocabulary-level and phrase-level transformation (equivalent to G6 Layer 1 and Layer 2). Scores plateaued around 60% despite comprehensive vocabulary cleanup. Round 3 introduced manual structural deconstruction — enumeration dissolution, paragraph opener variation, discussion architecture reframing, and hypothesis narrative conversion — which drove scores below 30%.

**Key finding**: After vocabulary cleanup, structural fingerprints (S7–S10) account for the majority of the remaining AI detection signal. These patterns operate at paragraph and section level and are invisible to word-level humanizers. The v2.0 pipeline automates the Round 3 structural intervention.

Full research discussion and analysis documents: https://github.com/HosungYou/humanizer

---

## Known Gaps and Future Work

The following limitations were identified during architecture analysis and are candidates for future releases:

| Gap | Description |
|-----|-------------|
| Iterative refinement feedback loop | No automatic retry with modified parameters when F5 detects >10% unresolved patterns after Pass 2 |
| Discipline-specific calibration | Generic 28-pattern model applied uniformly; Psychology and Management may have different baseline values |
| Custom preservation lists | Users cannot protect domain-specific terminology without code modification |
| Before/after diff visualization | No visual side-by-side highlighting of changes |
| AI pattern recovery detection | G6 may introduce new AI patterns while removing existing ones; F5 flags this but does not auto-correct |
| Hedge appropriateness calibration | No validation that remaining hedges match evidence strength |

---

## Ethics Note

Humanization assists researchers in expressing ideas naturally and reducing inadvertent AI stylistic patterns. It does not make AI use "undetectable" in any absolute sense, nor is it intended to circumvent journal or institutional disclosure policies. Researchers are responsible for following applicable AI disclosure requirements.

See: `.claude/skills/research-coordinator/ethics/ai-writing-ethics.md`

---

*Diverga v8.1.0 — Released 2026-02-22*
*Research documentation: https://github.com/HosungYou/humanizer*
*Diverga plugin: https://github.com/HosungYou/Diverga*
