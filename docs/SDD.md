# Software Design Document: Diverga Humanization Pipeline v2.0

**Document ID**: SDD-HUMANIZE-2.0
**Version**: 2.0.0
**Date**: 2026-02-22
**Standard**: IEEE 1016-2009 (adapted)
**Status**: Reference
**Repository**: https://github.com/HosungYou/humanizer

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Overview](#2-system-overview)
3. [Architecture Design](#3-architecture-design)
4. [Component Design](#4-component-design)
5. [State Machine Design](#5-state-machine-design)
6. [Interface Design](#6-interface-design)
7. [Configuration Schema](#7-configuration-schema)
8. [Algorithm Specifications](#8-algorithm-specifications)
9. [Checkpoint Integration](#9-checkpoint-integration)
10. [Non-Functional Requirements](#10-non-functional-requirements)
11. [Appendices](#11-appendices)

---

## 1. Introduction

### 1.1 Purpose

This Software Design Document (SDD) describes the architecture, components, algorithms, and interfaces of the Diverga Humanization Pipeline v2.0. It serves as the authoritative technical reference for developers extending, maintaining, or integrating with the pipeline.

The pipeline transforms AI-generated academic text into natural, human-sounding prose while preserving scholarly integrity (citations, statistics, methodology, technical terminology). It is implemented as a multi-agent subsystem within the Diverga Research Assistant (v8.1+), coordinating three specialized agents through a multi-pass iterative architecture.

### 1.2 Scope

This document covers:

- The three-agent pipeline (G5 Auditor, G6 Humanizer, F5 Verifier) and their interactions
- The multi-pass iterative architecture (Pass 1: Vocabulary, Pass 2: Structural, Pass 3: Polish)
- The composite AI probability scoring formula and its four component algorithms
- The 28-category pattern detection system (24 original + S7-S10 structural)
- The quantitative stylometric metrics (burstiness CV, MTLD, sentence length range, paragraph opener diversity)
- The three transformation configurations (conservative, balanced, aggressive)
- The finite state machine governing pipeline execution (17 states)
- Human checkpoint integration (5 checkpoints)
- Section-aware mode escalation logic
- Non-native speaker calibration

This document does NOT cover the broader Diverga research assistant framework, the MCP server infrastructure, or agents outside the humanization subsystem.

### 1.3 Definitions and Abbreviations

| Term | Definition |
|------|-----------|
| AI Probability | Composite score (0-100) estimating the likelihood that text was AI-generated |
| Burstiness | Coefficient of variation (CV) of sentence lengths; measures rhythm variation |
| CV | Coefficient of Variation = SD / Mean |
| Fano Factor | Variance / Mean of sentence lengths; supplementary diagnostic metric |
| G5 | Academic Style Auditor v2.0 agent |
| G6 | Academic Style Humanizer v2.0 agent |
| F5 | Humanization Verifier v2.0 agent |
| IMRAD | Introduction, Methods, Results, and Discussion (standard academic structure) |
| L1/L2/L3 | Transformation layers: vocabulary, phrase, structural |
| MTLD | Measure of Textual Lexical Diversity (McCarthy & Jarvis, 2010) |
| Pass | One complete cycle of G6 transformation followed by G5 re-scan and F5 verification |
| S7-S10 | Structural detection patterns added in v2.0 |
| TTR | Type-Token Ratio |
| VS | Verbalized Sampling methodology |

### 1.4 References

| Reference | Description |
|-----------|-------------|
| Wikipedia AI Cleanup Initiative | Source for original 24 pattern categories |
| McCarthy & Jarvis (2010) | MTLD validation study, *Behavior Research Methods* 42(2), 381-392 |
| Liang et al. (2023) | Non-native speaker false positive rates (>61% for TOEFL essays) |
| GPTZero | Perplexity + burstiness as primary detection signals |
| IEEE 1016-2009 | Software Design Descriptions standard |
| Diverga CLAUDE.md | Parent system architecture and agent catalog |

### 1.5 Design Rationale

The v2.0 multi-pass architecture replaced the v1.0 single-pass pipeline based on empirical evidence from humanizing two academic papers:

- Paper 1 (Occupational Identity Threat, TFSC): 80% -> 62% -> 31% across 3 manual rounds
- Paper 2 (Epistemic Cognition, IJAIED): 82% -> 61% -> 22% across 3 manual rounds

The single-pass approach was unable to address structural patterns (S7-S10) that accounted for 60%+ of the remaining AI probability after vocabulary-level cleaning. The multi-pass architecture automates this progression through dedicated transformation layers.

---

## 2. System Overview

### 2.1 High-Level Description

The Humanization Pipeline is a subsystem of the Diverga Research Assistant that detects and transforms AI-typical patterns in academic text. It operates through three coordinated agents:

1. **G5-AcademicStyleAuditor v2.0** (Sonnet tier): Detects AI patterns across 28 categories and computes quantitative stylometric metrics. Produces a composite AI probability score.

2. **G6-AcademicStyleHumanizer v2.0** (Opus tier): Transforms detected patterns through three layers -- vocabulary substitution, phrase restructuring, and deep structural transformation. Enhances burstiness and applies section-aware mode escalation.

3. **F5-HumanizationVerifier v2.0** (Haiku tier): Validates that transformations preserve citation integrity, statistical accuracy, meaning, and cross-section coherence. Verifies burstiness improvement and structural pattern reduction.

The pipeline processes text through up to three iterative passes, with mandatory G5 re-scans and human checkpoints between passes.

### 2.2 System Context

```
+-------------------------------------------------------------------+
|                    DIVERGA RESEARCH ASSISTANT                      |
|                                                                    |
|  +------------------+    +------------------+                      |
|  | G2-Academic      |    | G3-Peer Review   |                      |
|  | Communicator     |    | Strategist       |                      |
|  +--------+---------+    +--------+---------+                      |
|           |                       |                                |
|           +----------+------------+                                |
|                      |                                             |
|                      v                                             |
|  +====================================================+           |
|  ||         HUMANIZATION PIPELINE v2.0                ||           |
|  ||                                                   ||           |
|  ||  G5 (Audit) --> G6 (Transform) --> F5 (Verify)   ||           |
|  ||       ^                |                          ||           |
|  ||       +----------------+  (iterative re-scan)     ||           |
|  ||                                                   ||           |
|  +====================================================+           |
|                      |                                             |
|                      v                                             |
|  +------------------+    +------------------+                      |
|  | Word Export      |    | PDF Export       |                      |
|  +------------------+    +------------------+                      |
+-------------------------------------------------------------------+
```

### 2.3 Design Constraints

1. **Preservation invariants**: Citations, statistics, technical terms, direct quotes, and proper nouns must NEVER be altered, regardless of transformation mode.
2. **Human-in-the-loop**: Every pass boundary requires a human checkpoint. The pipeline cannot autonomously complete multiple passes.
3. **Idempotency**: Re-running G5 on the same text must produce the same score (within rounding tolerance).
4. **Model tier alignment**: G5 (Sonnet) for detection speed, G6 (Opus) for transformation quality, F5 (Haiku) for verification cost efficiency.
5. **Ethical boundary**: The pipeline helps express ideas naturally. It does not make AI use "undetectable" or substitute for AI disclosure.

---

## 3. Architecture Design

### 3.1 Component Diagram

```
+---------------------------------------------------------------------+
|                  HUMANIZATION PIPELINE v2.0                          |
|                                                                      |
|  +-----------------------+                                           |
|  |   INPUT               |                                           |
|  |   - Raw academic text |                                           |
|  |   - Section labels    |                                           |
|  |   - Target score      |                                           |
|  |   - Mode override     |                                           |
|  +-----------+-----------+                                           |
|              |                                                       |
|              v                                                       |
|  +-----------------------+     +---------------------------+         |
|  |  G5 v2.0              |     | Reference Data            |         |
|  |  Academic Style       |<--->| - detection-rules.md      |         |
|  |  Auditor              |     | - structural-patterns.md  |         |
|  |                       |     | - quantitative-metrics.md |         |
|  | Outputs:              |     +---------------------------+         |
|  |  - Pattern report     |                                           |
|  |  - Quantitative       |                                           |
|  |    metrics            |                                           |
|  |  - Composite score    |                                           |
|  |  - Section scores     |                                           |
|  |  - Risk class         |                                           |
|  +-----------+-----------+                                           |
|              |                                                       |
|              v                                                       |
|  +---------------------------+                                       |
|  | CP_HUMANIZATION_REVIEW    |  <-- Human decision point             |
|  | (mode selection)          |                                       |
|  +-------------+-------------+                                       |
|                |                                                     |
|       +--------+--------+                                            |
|       |                 |                                            |
|    [mode]            [skip]---> EXIT                                 |
|       |                                                              |
|       v                                                              |
|  +===========================================================+      |
|  ||  PASS LOOP (max 3 iterations)                            ||      |
|  ||                                                          ||      |
|  ||  +--------------------+    +-------------------------+   ||      |
|  ||  | G6 v2.0            |    | Transformation Configs  |   ||      |
|  ||  | Academic Style     |<-->| - balanced.yaml         |   ||      |
|  ||  | Humanizer          |    | - aggressive.yaml       |   ||      |
|  ||  |                    |    | - structural.yaml       |   ||      |
|  ||  | Layers:            |    | - academic-exceptions.md|   ||      |
|  ||  |  L1: Vocabulary    |    +-------------------------+   ||      |
|  ||  |  L2: Phrase        |                                  ||      |
|  ||  |  L3: Structural    |                                  ||      |
|  ||  +---------+----------+                                  ||      |
|  ||            |                                             ||      |
|  ||            v                                             ||      |
|  ||  +--------------------+                                  ||      |
|  ||  | G5 Re-Scan         | <-- MANDATORY after every pass   ||      |
|  ||  | (delta or full)    |                                  ||      |
|  ||  +---------+----------+                                  ||      |
|  ||            |                                             ||      |
|  ||            v                                             ||      |
|  ||  +--------------------+                                  ||      |
|  ||  | F5 v2.0            |                                  ||      |
|  ||  | Humanization       |                                  ||      |
|  ||  | Verifier           |                                  ||      |
|  ||  |                    |                                  ||      |
|  ||  | Modes:             |                                  ||      |
|  ||  |  Quick (Pass 1)    |                                  ||      |
|  ||  |  Full  (Pass 2/3)  |                                  ||      |
|  ||  +---------+----------+                                  ||      |
|  ||            |                                             ||      |
|  ||            v                                             ||      |
|  ||  +--------------------+                                  ||      |
|  ||  | CP_PASSn_REVIEW    | <-- Human checkpoint             ||      |
|  ||  | [continue/accept]  |                                  ||      |
|  ||  +---------+----------+                                  ||      |
|  ||            |                                             ||      |
|  ||     [continue]---> next pass                             ||      |
|  ||     [accept]----> EXIT LOOP                              ||      |
|  ||                                                          ||      |
|  +===========================================================+      |
|              |                                                       |
|              v                                                       |
|  +-----------------------+                                           |
|  |   OUTPUT              |                                           |
|  |   - Humanized text    |                                           |
|  |   - Score progression |                                           |
|  |   - Audit trail       |                                           |
|  |   - F5 report         |                                           |
|  +-----------------------+                                           |
+---------------------------------------------------------------------+
```

### 3.2 Multi-Pass Pipeline Architecture

The pipeline executes up to three passes, each targeting a different transformation layer:

```
BASELINE       PASS 1           PASS 2            PASS 3
(Original)     (Vocabulary)     (Structural)      (Polish)
                                                   [optional]
  80%  -------> 55% ----------> 30% ------------> 25%
                 |                |                  |
           L1: AI vocab     L3: S7-S10        Micro-fixes
           L1: Meta-comm    L3: Burstiness    Remaining hedging
           L1: Inflation    L3: Openers       Opener diversity
                 |                |                  |
           F5: Quick        F5: Full          F5: Full
           (checks 1-2)    (checks 1-7)      (checks 1-7)
                 |                |                  |
           CP_PASS1         CP_PASS2          CP_FINAL
           _REVIEW          _REVIEW           _REVIEW
```

**Pass 1 -- Vocabulary (Conservative layer)**
- Target: Word-level and phrase-level AI patterns
- G5 scan type: Full (establishes baseline)
- G6 transformations: L1 vocabulary (Tier 1 + Tier 2), M1 chatbot artifacts, C1 significance inflation
- F5 verification: Quick verify (citation integrity + statistical accuracy)
- Expected reduction: 15-25 percentage points

**Pass 2 -- Structural (Balanced layer)**
- Target: Structural patterns and sentence-level rhythm
- G5 scan type: Delta (measures improvement, identifies remaining structural patterns)
- G6 transformations: S7 enumeration dissolution, S8 paragraph opener variation, S9 discussion architecture, S10 hypothesis narrative, burstiness CV enhancement
- F5 verification: Full verify (all 7 domains)
- Expected reduction: 10-20 additional percentage points

**Pass 3 -- Polish (Optional)**
- Target: Remaining micro-patterns and fine-tuning
- G5 scan type: Full audit (comprehensive final check)
- G6 transformations: Remaining hedging, paragraph opener diversity, sentence length outliers
- F5 verification: Full verify (all 7 domains)
- Expected reduction: 5-10 additional percentage points
- Trigger: Only if score target not met after Pass 2, or user-requested

### 3.3 Data Flow

```
                        +-------------------+
                        |   Raw Text Input  |
                        +---------+---------+
                                  |
                   +--------------v--------------+
                   |  G5: Pattern Scan (Phase 1) |
                   |  G5: Quantitative (Phase 2) |
                   |  G5: Structural  (Phase 3)  |
                   |  G5: Composite   (Phase 4)  |
                   +--------------+--------------+
                                  |
                     PatternReport + CompositeScore
                     + SectionScores + Metrics
                                  |
                   +--------------v--------------+
                   | CP_HUMANIZATION_REVIEW       |
                   | User selects: mode + target  |
                   +--------------+--------------+
                                  |
              +-------------------v-------------------+
              |          PASS N (1..3)                 |
              |                                       |
              |  Input: text + PatternReport           |
              |         + mode + section_escalation    |
              |                                       |
              |  +----------------------------------+ |
              |  | G6: Apply transformations per     | |
              |  |     layer and mode config         | |
              |  +----------------+-----------------+ |
              |                   |                   |
              |          TransformedText               |
              |                   |                   |
              |  +----------------v-----------------+ |
              |  | G5: Re-scan (delta or full)       | |
              |  +----------------+-----------------+ |
              |                   |                   |
              |          UpdatedScore + NewPatterns    |
              |                   |                   |
              |  +----------------v-----------------+ |
              |  | F5: Verify (quick or full)        | |
              |  +----------------+-----------------+ |
              |                   |                   |
              |          VerificationReport            |
              |                   |                   |
              |  +----------------v-----------------+ |
              |  | CP_PASSn_REVIEW                   | |
              |  | [continue / accept / revert]      | |
              |  +----------------+-----------------+ |
              +-------------------+-------------------+
                                  |
                   +--------------v--------------+
                   |   Final Output Package       |
                   |   - Humanized text           |
                   |   - Score: baseline -> final |
                   |   - Audit trail              |
                   |   - F5 verification report   |
                   +-----------------------------+
```

### 3.4 Layer Ordering Rationale

Transformations are applied in strict order: Layer 1 (vocabulary) -> Layer 2 (phrase) -> Layer 3 (structural). This ordering is mandatory because:

1. Vocabulary changes may resolve some structural issues, reducing unnecessary structural rewrites.
2. Structural rewriting performed first can reintroduce AI vocabulary that would then need a second vocabulary pass.
3. The structural layer can optimize sentence length variation after all word-level changes are settled.
4. Post-structural verification checks that no new L1 vocabulary was introduced during structural rewriting.

---

## 4. Component Design

### 4.1 G5-AcademicStyleAuditor v2.0

**Agent ID**: G5
**Category**: G -- Publication & Communication
**Model Tier**: MEDIUM (Sonnet)
**Tools**: Read, Glob, Grep

#### 4.1.1 Pattern Detection System (28 Categories)

The detection system comprises 24 original categories from the Wikipedia AI Cleanup initiative plus 4 structural patterns (S7-S10) discovered through empirical humanization rounds.

**Category Taxonomy**:

| Category Code | Category Name | Pattern Count | Description |
|---------------|---------------|---------------|-------------|
| C | Content | 6 (C1-C6) | Significance inflation, notability claims, promotional language, vague attributions |
| L | Language | 6 (L1-L6) | AI vocabulary (tiered), copula avoidance, negative parallelism, elegant variation, false ranges |
| S (original) | Style | 6 (S1-S6) | Em dash overuse, boldface, inline-header lists, title case, emoji, quote inconsistency |
| S (structural) | Style (Structural) | 4 (S7-S10) | Enumeration as prose, repetitive paragraph openers, formulaic section structure, hypothesis checklist |
| M | Communication | 3 (M1-M3) | Chatbot artifacts, knowledge disclaimers, sycophantic tone |
| H | Filler | 3 (H1-H3) | Verbose phrases, hedge stacking, generic conclusions |
| A | Academic | 6 (A1-A6) | Abstract template, methods boilerplate, discussion inflation, citation hedging, contribution enumeration, limitation disclaimers |
| **Total** | | **34 patterns** | 28 unique categories (L1 has sub-tiers) |

#### 4.1.2 Structural Detection Patterns (S7-S10)

These four patterns were discovered empirically: after vocabulary-level cleaning (Rounds 1-2), they accounted for the remaining 60%+ AI probability. They operate at paragraph/section level and resist word-level humanization.

**S7: Enumeration as Prose (Weight: 12, Risk: HIGH)**

Ordinal markers ("First,...Second,...Third,...") embedded within flowing paragraph text, creating a hidden numbered list disguised as prose. Detection scans for 3+ sequential ordinal markers within a single section or across consecutive paragraphs.

- English markers: First/Second/Third/Fourth/Finally, Additionally/Moreover/Furthermore as sequential connectors, "There are N key [noun]" preambles
- Korean markers: 첫째/둘째/셋째, 첫 번째로/두 번째로/세 번째로
- Aggravating factor (1.5x): 4+ sequential ordinals or enumeration spanning multiple paragraphs
- Exception: Methods sections (procedural sequences) receive 0.5x weight reduction

**S8: Repetitive Paragraph Openers (Weight: 10, Risk: HIGH)**

More than 3 paragraphs within the same section starting with the same syntactic pattern. Most common: "The [noun]..." repeated with different nouns.

- Detection: Extract first 3 words of each paragraph, normalize by removing articles, flag if >3 share the same pattern
- Severity scaling: 3 matches = base weight; 4 matches = 1.3x; 5+ matches = 1.6x

**S9: Formulaic Section Structure (Weight: 8, Risk: MEDIUM)**

Discussion section following the rigid template: restate findings -> compare to literature -> state implications -> acknowledge limitations -> suggest future research.

- Scoring: All 5 moves in canonical order = full weight; 4 of 5 = 0.7x; 3 of 5 = 0.4x
- Additional +3 penalty if each subsection internally repeats the restate-compare-imply pattern

**S10: Hypothesis Checklist Pattern (Weight: 10, Risk: HIGH)**

Sequential hypothesis confirmation statements: "H1 was supported. H2 was partially supported. H3 was not supported."

- Trigger: 3+ sequential hypothesis verdicts within the same section
- Aggravating factor (1.5x): All hypotheses in a single paragraph, identical syntactic structure, no narrative connecting outcomes

#### 4.1.3 Quantitative Metrics

Four stylometric metrics supplement pattern-based detection:

| Metric | Method | Human Baseline | AI Typical | Weight | Penalty Formula |
|--------|--------|----------------|------------|--------|-----------------|
| Burstiness (CV) | SD(sentence_lengths) / Mean(sentence_lengths) | > 0.45 | < 0.30 | 15 | `max(0, (0.45 - CV) / 0.45 * 100)` |
| MTLD | Mean factor length at TTR > 0.72 | > 80 | < 60 | 10 | `max(0, (80 - MTLD) / 80 * 100)` |
| Sentence Length Range | max(word_count) - min(word_count) | > 25 words | < 15 words | 5 | `max(0, (25 - range) / 25 * 100)` |
| Paragraph Opener Diversity | unique_first_3_words / total_paragraphs | > 0.70 | < 0.50 | 8 | `max(0, (0.70 - div) / 0.70 * 100)` |
| Fano Factor (supplementary) | Variance / Mean of sentence lengths | > 1.0 | < 1.0 | -- | Diagnostic only |

#### 4.1.4 Composite Scoring Formula

```
AI_Probability = (0.60 * pattern_score)
              + (0.20 * burstiness_penalty)
              + (0.10 * vocab_diversity_penalty)
              + (0.10 * structural_penalty)
```

| Component | Weight | Source | Range |
|-----------|--------|--------|-------|
| pattern_score | 60% | Phase 1 pattern detection, 28 categories, normalized 0-100 | 0-100 |
| burstiness_penalty | 20% | `max(0, (0.45 - CV) / 0.45 * 100)` | 0-100 |
| vocab_diversity_penalty | 10% | `max(0, (80 - MTLD) / 80 * 100)` | 0-100 |
| structural_penalty | 10% | S7+S8+S9+S10 weighted scores, normalized 0-100 | 0-100 |

**Weight rationale**: Pattern detection is the core signal (60%), validated across 28 categories. Burstiness carries the highest quantitative weight (20%) because sentence length variance is one of the most reliable discriminators between human and AI text, partially independent of vocabulary patterns. Vocabulary diversity (10%) is complementary but less discriminative in academic text. Structural penalty (10%) captures section/paragraph-level AI fingerprints missed by word-level analysis.

#### 4.1.5 Risk Classification

| Score Range | Risk Level | Label | Action |
|-------------|------------|-------|--------|
| 0-20 | Low | Likely Human | Optional review |
| 21-40 | Moderate | Mixed Signals | Recommended review |
| 41-60 | Elevated | Probably AI-Assisted | Review needed |
| 61-80 | High | Likely AI-Generated | Humanization recommended |
| 81-100 | Critical | Obviously AI | Humanization required |

#### 4.1.6 Context Modifiers

**Section-based multipliers**:

| Section | Multiplier | Rationale |
|---------|------------|-----------|
| Abstract | 1.2 | Highest scrutiny from reviewers |
| Introduction | 1.1 | Important for first impression |
| Literature Review | 1.0 | Some formality expected |
| Methods | 0.8 | Boilerplate somewhat acceptable |
| Results | 1.0 | Standard |
| Discussion | 1.1 | Claims scrutinized |
| Conclusion | 1.1 | Final impression matters |
| Response Letter | 0.9 | Some formality expected |

**Clustering detection**:

- Vocabulary clustering: 2+ tier1 words OR 4+ tier2 words -> +20 bonus
- Paragraph clustering: 3+ patterns in same paragraph -> +10 per additional pattern
- Category clustering: 3 categories co-occurring -> +20; 4+ categories -> +30

#### 4.1.7 Non-Native Speaker Calibration

Opt-in only. Reduces false positive rates for non-native English academic writers (Liang et al. 2023: >61% misclassification rate).

```yaml
non_native_calibration:
  enabled: false  # User must explicitly opt in
  adjustments:
    L1_weight: "x 0.7"         # Reduce AI vocabulary flagging by 30%
    H1_weight: "x 0.8"         # Reduce verbose phrase flagging by 20%
    burstiness_threshold: 0.35  # Lower from 0.45 for non-native writers
  scoring_impact:
    burstiness_penalty: "max(0, (0.35 - CV) / 0.35 * 100)"
    vocab_diversity_penalty: "unchanged (MTLD threshold remains 80)"
```

### 4.2 G6-AcademicStyleHumanizer v2.0

**Agent ID**: G6
**Category**: G -- Publication & Communication
**Model Tier**: HIGH (Opus)
**Tools**: Read, Glob, Grep, Edit, Write

#### 4.2.1 Transformation Layers

G6 operates through three transformation layers, applied in strict order:

```
Layer 1 (Vocabulary)        Layer 2 (Phrase)           Layer 3 (Structural)
-------------------         ----------------           --------------------
L1: AI vocabulary swap      Phrase restructuring       S7: Enumeration dissolution
M1: Chatbot artifact        Copula simplification      S8: Paragraph opener variation
    removal                 Hedge reduction            S9: Discussion architecture
C1: Inflation downgrade     Parallel construction      S10: Hypothesis narrative
C4: Promotional neutralize      variation              Burstiness CV enhancement
C5: Attribution fix                                    Paragraph length variation
```

**Layer 1 -- Vocabulary Substitution**

Direct word-for-word replacement of AI-typical vocabulary. Two tiers:

Tier 1 (always transform): `delve` -> `examine`, `tapestry` -> `range`, `intricacies` -> `details`, `multifaceted` -> `complex`, `nuanced` -> `detailed`, `myriad` -> `many`, `plethora` -> `many`, `paramount` -> `essential`, `testament to` -> `evidence of`, `embark on` -> `begin`, `realm` -> `area`, `indelible` -> `lasting`

Tier 2 (balanced + aggressive): `landscape` -> `context`, `underscore` -> `emphasize`, `pivotal` -> `key`, `leverage` -> `use`, `utilize` -> `use`, `facilitate` -> `enable`, `foster` -> `encourage`, `synergy` -> `collaboration`, `holistic` -> `comprehensive`, `robust` -> `strong` (unless statistical context)

Tier 3 (aggressive only): `comprehensive` -> `thorough`, `innovative` -> `new`, `significant` -> `large` (unless statistics), `substantial` -> `large`, `considerable` -> `large`

**Layer 2 -- Phrase Restructuring**

Transforms multi-word patterns: copula avoidance (`serves as` -> `is`), hedge stacking (`could potentially` -> `may`), verbose phrases (`in order to` -> `to`), superficial -ing constructions (`highlighting the importance of` -> `[X] is important because`).

**Layer 3 -- Structural Transformation**

Deep paragraph/section-level transformation. Applied in balanced and aggressive modes only. See Section 4.2.3 for detailed transformation strategies per structural pattern.

#### 4.2.2 Transformation Modes

| Mode | Target Patterns | Intensity | Text Change | Expected Reduction |
|------|----------------|-----------|-------------|-------------------|
| Conservative | HIGH-risk only | L1 + L2 | 5-15% | 15-25 points |
| Balanced (default) | HIGH + MEDIUM risk | L1 + L2 + L3 | 15-30% | 40-60 points |
| Aggressive | ALL patterns | L1 + L2 + L3 (max) | 30-50% | 60-80 points |

**Conservative mode** targets: C1, C4, C5, L1 (tier1 only), S5, M1, M2, A3, A4
- Excludes: All low-risk patterns, S7-S10 structural patterns
- Use case: Journal submissions, thesis chapters

**Balanced mode** targets: All conservative targets PLUS C2, C3, L1 (tier2), L2, L3, L5, S1, S3, S7, S8, S9, S10, M3, H2, H3
- Excludes: C6, L4, L6, S2, S4, S6, H1, A1, A2, A5, A6
- Use case: Conference papers, working papers, most academic writing

**Aggressive mode** targets: ALL 28 pattern categories with no exclusions
- Use case: Blog posts, informal summaries, very high AI probability (>80%)

#### 4.2.3 Structural Transformation Strategies

**S7 Enumeration Dissolution**:
- Remove ordinal markers entirely
- Replace with varied transitional devices: cause-effect links, contrast connectors, concessive transitions, or no connector at all
- Merge closely related enumerated points into compound sentences
- Weave enumerated findings into an argument arc

**S8 Paragraph Opener Variation**:
- Balanced: Fix sequences of >2 consecutive same-pattern openers
- Aggressive: Zero consecutive paragraphs with similar openers allowed
- Strategies: question opener, short declarative, dependent clause, concrete number/example, contrast/concession

**S9 Discussion Architecture**:
- Replace formulaic "The present study examined..." openers with hooks: compelling question, surprising finding, real-world scenario, tension/paradox
- Embed limitations within the argument rather than isolating them
- Weave future directions into the discussion narrative

**S10 Hypothesis Narrative**:
- Group hypotheses thematically rather than numerically
- Lead with the most interesting finding, not H1
- Use concrete effect sizes as narrative anchors
- Frame null results as discoveries rather than failures

#### 4.2.4 Burstiness Enhancement

Target CV: > 0.45 (balanced), > 0.50 (aggressive)

Strategies:
1. Insert 2-5 word declarative sentences at impact points ("That gap is real.")
2. Allow 1-2 complex sentences per section to reach 40-60 words
3. Break medium-length sentences (15-25 words) into shorter or longer forms
4. Use sentence fragments strategically for emphasis
5. Vary paragraph length: alternate 2-sentence and 6-sentence paragraphs

#### 4.2.5 Section-Aware Mode Escalation

Instead of applying a single mode to the entire document, the pipeline automatically escalates transformation intensity per section based on G5 section-level scores:

```
Section         Base Mode      Escalation Trigger     Escalated Mode
-----------     -----------    ------------------     --------------
Abstract        Conservative   section_score > 50     Balanced
Introduction    Balanced       (no escalation)        Balanced
Methods         Conservative   NEVER                  Conservative
Results         Conservative   section_score > 60     Balanced
Discussion      Balanced       section_score > 50     Aggressive
Conclusion      Balanced       section_score > 50     Aggressive
```

**Rationale**: Methods sections receive minimal transformation (boilerplate is expected; changes risk accuracy). Discussion and Conclusion sections benefit most from structural transformation. Results sections should only have framing language changed, never statistics.

Users can override with a global mode: `"Humanize (force: conservative)"` applies conservative to all sections regardless of section scores.

#### 4.2.6 Preservation Rules

Elements that must NEVER be transformed, regardless of mode:

| Category | Examples | Rule |
|----------|----------|------|
| Citations | (Author, year), [1], DOIs | Exact preservation |
| Statistics | p-values, effect sizes, CIs, N, M, SD | Exact preservation |
| Methodology | Instrument names, software versions, scale anchors | Exact preservation |
| Direct quotes | Any text in quotation marks from sources | Exact preservation |
| Technical terms | Named theories, named frameworks, named analyses | Context-dependent preservation |
| Proper nouns | Author names, institutions, journals, locations | Exact preservation |
| Acronyms | Defined abbreviations and standard forms | Preserve definitions |

**Context-sensitive exceptions**:
- `robust`: preserve in statistical context ("robust standard errors"), transform in general context
- `significant`: preserve with p-values, transform when meaning "important"
- `framework`: preserve in named framework context, transform in vague usage

### 4.3 F5-HumanizationVerifier v2.0

**Agent ID**: F5
**Category**: F -- Quality & Validation
**Model Tier**: LOW (Haiku)
**Tools**: Read, Glob, Grep

#### 4.3.1 Verification Domains (7)

```
+----------------------------------+
| 1. Citation Check                | -> Pass/Fail  (CRITICAL)
| 2. Statistics Check              | -> Pass/Fail  (CRITICAL)
| 3. Meaning Check                 | -> Pass/Fail  (MAJOR)
| 4. AI Pattern Reduction Check    | -> Pass/Fail
| 5. Burstiness Check              | -> Pass/Warn/Fail (MAJOR)
| 6. Structural Pattern Check      | -> Pass/Warn/Fail (MAJOR)
| 7. Cross-Section Coherence Check | -> Pass/Warn/Fail
+----------------------------------+
```

**Domain 1: Citation Integrity** -- All author names, years, page numbers, DOIs unchanged.

**Domain 2: Statistical Accuracy** -- All numbers, decimals, test statistics, effect sizes, p-values exact match.

**Domain 3: Meaning Preservation** -- Core argument intact, causal claims preserved, hedging appropriate, conclusions unchanged.

**Domain 4: AI Pattern Reduction** -- AI probability decreased from baseline; minimum >= 20% reduction expected per full pipeline; no new patterns introduced by G6.

**Domain 5: Burstiness Verification**:
```
IF post_cv < pre_cv:
    FLAG "Burstiness decreased after humanization" (severity: Major)
IF post_cv < 0.35:
    WARN "Burstiness still in AI-typical range"
IF post_cv >= 0.45:
    PASS "Burstiness meets human-like target"
```

**Domain 6: Structural Pattern Check**:
```
IF post_structural_count > pre_structural_count:
    FLAG "New structural patterns introduced" (severity: Major)
IF post_structural_count == pre_structural_count AND pass >= 2:
    WARN "Structural patterns unchanged after structural pass"
IF post_structural_count < pre_structural_count:
    PASS "Structural patterns reduced by {delta}"
```

**Domain 7: Cross-Section Coherence** -- Terminology consistency across sections, structural contradictions detected, section transitions validated, internal references still valid, abbreviations defined before use.

#### 4.3.2 Verification Modes

| Mode | When Applied | Checks Performed |
|------|-------------|------------------|
| Quick Verify | After Pass 1 (vocabulary) | Domains 1-2 only (citation + statistics) |
| Full Verify | After Pass 2/3 (structural/polish) | All 7 domains |

#### 4.3.3 Error Severity Classification

| Severity | Type | Examples | Pipeline Action |
|----------|------|----------|-----------------|
| Critical | Citation or statistic error | Author name changed, p-value altered | ABORT pass, revert |
| Major | Meaning distortion or burstiness decrease | Core claim changed, CV decreased | FLAG, require review |
| Minor | Style inconsistency or coherence warning | Term variation across sections | WARN, continue |

---

## 5. State Machine Design

### 5.1 State Diagram

The pipeline is governed by a finite state machine with 17 states:

```
                                    +--------+
                            +------>|  IDLE  |<---------------------------+
                            |       +---+----+                            |
                            |           |                                 |
                            |      [start]                                |
                            |           |                                 |
                            |       +---v---------+                       |
                            |       | ANALYZING   |                       |
                            |       | (G5 initial)|                       |
                            |       +---+---------+                       |
                            |           |                                 |
                            |      [report ready]                         |
                            |           |                                 |
                            |       +---v-----------+                     |
                            |       | AWAITING      |    [skip]           |
                            +-------+ DECISION      +------->-------------+
                                    | (CP_HUM_REV)  |                     |
                                    +---+-----------+                     |
                                        |                                 |
                                   [mode selected]                        |
                                        |                                 |
          +-----------------------------v-----------------------------+   |
          |                                                           |   |
          |   +-------------------+                                   |   |
          |   | PASS1             |                                   |   |
          |   | _TRANSFORMING     |                                   |   |
          |   | (G6 vocabulary)   |                                   |   |
          |   +--------+----------+                                   |   |
          |            |                                              |   |
          |   +--------v----------+                                   |   |
          |   | PASS1             |                                   |   |
          |   | _RESCANNING       |                                   |   |
          |   | (G5 delta)        |                                   |   |
          |   +--------+----------+                                   |   |
          |            |                                              |   |
          |   +--------v----------+                                   |   |
          |   | PASS1             |                                   |   |
          |   | _VERIFYING        |                                   |   |
          |   | (F5 quick)        |                                   |   |
          |   +--------+----------+                                   |   |
          |            |                                              |   |
          |   +--------v----------+          +----------+             |   |
          |   | AWAITING          |--[accept]-->|COMPLETE|----------->+   |
          |   | _PASS1_REVIEW     |          +----------+             |   |
          |   | (CP_PASS1_REV)    |                                   |   |
          |   +--------+----------+                                   |   |
          |            |                                              |   |
          |       [continue]                                          |   |
          |            |                                              |   |
          |   +--------v----------+                                   |   |
          |   | PASS2             |                                   |   |
          |   | _TRANSFORMING     |                                   |   |
          |   | (G6 structural)   |                                   |   |
          |   +--------+----------+                                   |   |
          |            |                                              |   |
          |   +--------v----------+                                   |   |
          |   | PASS2             |                                   |   |
          |   | _RESCANNING       |                                   |   |
          |   | (G5 delta)        |                                   |   |
          |   +--------+----------+                                   |   |
          |            |                                              |   |
          |   +--------v----------+                                   |   |
          |   | PASS2             |                                   |   |
          |   | _VERIFYING        |                                   |   |
          |   | (F5 full)         |                                   |   |
          |   +--------+----------+                                   |   |
          |            |                                              |   |
          |   +--------v----------+          +----------+             |   |
          |   | AWAITING          |--[accept]-->|COMPLETE|----------->+   |
          |   | _PASS2_REVIEW     |          +----------+             |   |
          |   | (CP_PASS2_REV)    |                                   |   |
          |   +--------+----------+                                   |   |
          |            |                                              |   |
          |       [one more pass]                                     |   |
          |            |                                              |   |
          |   +--------v----------+                                   |   |
          |   | PASS3             |                                   |   |
          |   | _TRANSFORMING     |                                   |   |
          |   | (G6 polish)       |                                   |   |
          |   +--------+----------+                                   |   |
          |            |                                              |   |
          |   +--------v----------+                                   |   |
          |   | PASS3             |                                   |   |
          |   | _RESCANNING       |                                   |   |
          |   | (G5 full audit)   |                                   |   |
          |   +--------+----------+                                   |   |
          |            |                                              |   |
          |   +--------v----------+                                   |   |
          |   | PASS3             |                                   |   |
          |   | _VERIFYING        |                                   |   |
          |   | (F5 full)         |                                   |   |
          |   +--------+----------+                                   |   |
          |            |                                              |   |
          |   +--------v----------+          +----------+             |   |
          |   | AWAITING          |--[approve]->|COMPLETE|----------->+   |
          |   | _FINAL_REVIEW     |          +----------+             |   |
          |   | (CP_FINAL_REV)    |                                   |   |
          |   +---+----------+----+                                   |   |
          |       |          |                                        |   |
          |  [revert to P2] [revert to orig]                          |   |
          |       |          |                                        |   |
          |       v          +------->--------------------------------+   |
          |   PASS2_TRANSFORMING (re-enter)                           |   |
          |                                                           |   |
          +-----------------------------------------------------------+   |
                                                                          |
          COMPLETE -----> [export / idle] --->-----------------------------+
```

### 5.2 State Definitions

| # | State | Description | Active Agent | Transitions |
|---|-------|-------------|-------------|-------------|
| 1 | `idle` | No humanization in progress | None | -> `analyzing` |
| 2 | `analyzing` | G5 running initial pattern detection | G5 | -> `awaiting_decision`, -> `idle` |
| 3 | `awaiting_decision` | CP_HUMANIZATION_REVIEW presented | None (human) | -> `pass1_transforming`, -> `idle` |
| 4 | `pass1_transforming` | G6 applying vocabulary transformations | G6 (L1) | -> `pass1_rescanning` |
| 5 | `pass1_rescanning` | G5 re-scanning after Pass 1 | G5 | -> `pass1_verifying` |
| 6 | `pass1_verifying` | F5 quick verify after Pass 1 | F5 | -> `awaiting_pass1_review` |
| 7 | `awaiting_pass1_review` | CP_PASS1_REVIEW presented | None (human) | -> `pass2_transforming`, -> `complete` |
| 8 | `pass2_transforming` | G6 applying structural transformations | G6 (L3) | -> `pass2_rescanning` |
| 9 | `pass2_rescanning` | G5 re-scanning after Pass 2 | G5 | -> `pass2_verifying` |
| 10 | `pass2_verifying` | F5 full verify after Pass 2 | F5 | -> `awaiting_pass2_review` |
| 11 | `awaiting_pass2_review` | CP_PASS2_REVIEW presented | None (human) | -> `pass3_transforming`, -> `complete` |
| 12 | `pass3_transforming` | G6 applying polish transformations | G6 | -> `pass3_rescanning` |
| 13 | `pass3_rescanning` | G5 final audit scan | G5 | -> `pass3_verifying` |
| 14 | `pass3_verifying` | F5 full verify after Pass 3 | F5 | -> `awaiting_final_review` |
| 15 | `awaiting_final_review` | CP_FINAL_REVIEW presented | None (human) | -> `complete`, -> `pass2_transforming`, -> `idle` |
| 16 | `complete` | Pipeline finished, ready for export | None | -> `idle` |
| 17 | `error` | Verification failure (implicit) | None | -> revert to previous state or `idle` |

### 5.3 Transition Guards

| Transition | Guard Condition |
|-----------|-----------------|
| `idle` -> `analyzing` | Input text provided, length >= 100 words |
| `awaiting_decision` -> `pass1_transforming` | User selected mode (A/B/C) |
| `awaiting_decision` -> `idle` | User selected Skip (E) |
| `pass1_verifying` -> `awaiting_pass1_review` | F5 quick verify: no CRITICAL errors |
| `awaiting_pass1_review` -> `complete` | User selected Accept (B) |
| `awaiting_pass1_review` -> `pass2_transforming` | User selected Continue (A) |
| `awaiting_pass2_review` -> `complete` | User selected Accept (A) OR target met |
| `awaiting_pass2_review` -> `pass3_transforming` | User selected One More Pass (B) AND pass_reduction >= 5 points |
| `awaiting_final_review` -> `complete` | User selected Approve (A) |
| `awaiting_final_review` -> `pass2_transforming` | User selected Revert to Pass 2 |
| `awaiting_final_review` -> `idle` | User selected Revert to Original |
| Any `*_verifying` -> `error` | F5 detects CRITICAL error (citation/stat changed) |
| `error` -> previous state | Automatic revert of current pass |

### 5.4 Termination Conditions

The pipeline terminates (transitions to `complete`) when any of these conditions is met:

1. User explicitly accepts at any checkpoint
2. Score target is met after a pass
3. Diminishing returns: pass reduced score by < 5 percentage points
4. Maximum 3 passes reached
5. CRITICAL verification failure (terminates to `idle` after revert)

---

## 6. Interface Design

### 6.1 Agent-to-Agent Contracts

#### 6.1.1 G5 Output -> G6 Input

```yaml
# G5 PatternReport (output of G5, input to G6)
pattern_report:
  composite_score: 67          # 0-100 AI probability
  pattern_score: 72            # 0-100 pattern component
  risk_level: "high"           # low/moderate/elevated/high/critical

  patterns_detected:
    total: 18
    high_risk: 5
    medium_risk: 9
    low_risk: 4
    by_category:
      C: [C1, C4, C5]
      L: [L1_tier1, L1_tier2, L2, L5]
      S: [S1, S7, S8]
      M: [M1]
      H: [H2, H3]
      A: [A3, A4]
    instances:
      - pattern_id: "C1"
        location: {section: "discussion", paragraph: 3, sentence: 1}
        matched_text: "pivotal study"
        risk: "high"
        suggestion: "this study"
      # ... more instances

  quantitative_metrics:
    burstiness_cv: 0.28
    mtld: 52
    sentence_length_range: 18
    paragraph_opener_diversity: 0.48
    fano_factor: 0.82           # diagnostic only

  section_scores:
    abstract: 55
    introduction: 48
    methods: 22
    results: 35
    discussion: 78
    conclusion: 62

  structural_patterns:
    S7: {count: 2, locations: [...]}
    S8: {count: 1, locations: [...]}
    S9: {detected: true, severity: "full_template"}
    S10: {count: 1, locations: [...]}

  recommendation:
    mode: "balanced"
    section_escalation:
      abstract: "conservative"
      introduction: "balanced"
      methods: "conservative"
      results: "conservative"
      discussion: "aggressive"   # section_score 78 > 50
      conclusion: "aggressive"   # section_score 62 > 50
```

#### 6.1.2 G6 Output -> F5 Input

```yaml
# G6 TransformationResult (output of G6, input to F5)
transformation_result:
  pass_number: 2
  mode: "balanced"
  layer: "structural"

  original_text: "..."         # Full original text
  transformed_text: "..."      # Full transformed text

  changes:
    total: 8
    by_type:
      S7_dissolution: 2
      S8_opener_variation: 3
      S10_narrative: 1
      burstiness_enhancement: 2
    details:
      - change_id: 1
        pattern_id: "S7"
        location: {section: "discussion", paragraph: 2}
        before: "First, education... Second, partisan..."
        after: "Education emerged as a reliable predictor..."
      # ... more changes

  metrics:
    burstiness_cv_before: 0.30
    burstiness_cv_after: 0.48
    short_sentences_added: 4    # sentences <= 12 words
    long_sentences_added: 2     # sentences >= 35 words

  preservation_log:
    citations_preserved: 24
    statistics_preserved: 18
    technical_terms_preserved: 12
```

#### 6.1.3 F5 Output -> Checkpoint / Pipeline Controller

```yaml
# F5 VerificationReport (output of F5)
verification_report:
  mode: "full"                  # "quick" or "full"
  pass_number: 2
  overall_result: "PASS"        # PASS / WARN / FAIL

  domains:
    citation_integrity:
      result: "PASS"
      citations_checked: 24
      issues: []

    statistical_accuracy:
      result: "PASS"
      statistics_checked: 18
      issues: []

    meaning_preservation:
      result: "PASS"
      notes: "Core claims intact"

    ai_pattern_reduction:
      result: "PASS"
      baseline_score: 67
      current_score: 28
      reduction: 39
      new_patterns_introduced: 1

    burstiness:
      result: "PASS"
      pre_cv: 0.28
      post_cv: 0.48
      target: 0.45
      met: true

    structural_patterns:
      result: "PASS"
      pre_count: 4           # S7:2 + S8:1 + S10:1
      post_count: 1          # S8:1 remaining
      delta: -3

    cross_section_coherence:
      result: "WARN"
      issues:
        - "Term 'AI concern' used in Discussion but 'AI worry' in Conclusion"
      severity: "minor"

  errors: []
  warnings:
    - "Minor terminology inconsistency between Discussion and Conclusion"
  recommendation: "APPROVE with minor edits"
```

### 6.2 Input/Output Specifications

#### 6.2.1 Pipeline Input

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | Yes | Raw academic text (minimum 100 words) |
| `sections` | map[string]string | No | Section labels mapped to text ranges |
| `mode` | enum | No | `conservative` / `balanced` / `aggressive` (default: `balanced`) |
| `target_score` | integer | No | Target AI probability (0-100); activates target mode |
| `preset` | enum | No | `journal_safe` (30) / `conference` (40) / `working_paper` (50) |
| `force_mode` | boolean | No | If true, override section-aware escalation with global mode |
| `non_native_calibration` | boolean | No | Enable non-native speaker calibration (default: false) |
| `max_passes` | integer | No | Override maximum passes (1-3, default: 3) |
| `document_type` | enum | No | `journal` / `conference` / `thesis` / `grant` / `blog` / `social` |

#### 6.2.2 Pipeline Output

| Field | Type | Description |
|-------|------|-------------|
| `humanized_text` | string | Final transformed text |
| `score_progression` | array[integer] | AI probability at each stage: [baseline, pass1, pass2, pass3] |
| `total_passes` | integer | Number of passes executed |
| `target_met` | boolean | Whether target score was achieved |
| `audit_trail` | array[Change] | Detailed log of every transformation |
| `verification_report` | VerificationReport | Final F5 report |
| `metrics_progression` | array[Metrics] | Quantitative metrics at each stage |
| `preservation_log` | PreservationLog | All preserved elements |

---

## 7. Configuration Schema

### 7.1 balanced.yaml

The default transformation configuration. Targets HIGH and MEDIUM risk patterns.

```yaml
version: "2.0.0"
mode: "balanced"
default_mode: true

target_patterns:
  include:
    # High-risk (all)
    - C1, C4, C5, L1, S5, M1, M2, A3, A4
    # Medium-risk
    - C2, C3, L2, L3, L5, S1, S3, M3, H2, H3
    # Structural (v2.0)
    - S7, S8, S9, S10

  exclude:
    - C6, L4, L6, S2, S4, S6, H1, A1, A2, A5, A6

intensity:
  vocabulary_changes: "moderate"
  phrase_restructuring: "selective"
  sentence_changes: "occasional"
  paragraph_changes: "rare"

burstiness_enhancement:
  target_cv: ">0.45"

expected_changes:
  ai_probability_reduction: "40-60%"
  pattern_reduction: "60-80%"
  text_change_percentage: "15-30%"
```

Key transformation rules in balanced mode:
- L1: Substitute both tier1 and tier2 AI vocabulary
- S7: Dissolve First/Second/Third in Discussion and Conclusion; preserve in Methods
- S8: Fix sequences of >2 consecutive same-pattern openers
- S9: Rewrite Discussion opener; allow some formulaic structure elsewhere
- S10: Convert hypothesis checklists to narrative; keep H-labels in tables

### 7.2 aggressive.yaml

Maximum transformation configuration. Targets ALL patterns.

```yaml
version: "2.0.0"
mode: "aggressive"

target_patterns:
  include: [ALL]        # C1-C6, L1-L6, S1-S10, M1-M3, H1-H3, A1-A6
  exclude: []           # Nothing excluded

intensity:
  vocabulary_changes: "extensive"
  phrase_restructuring: "frequent"
  sentence_changes: "common"
  paragraph_changes: "when_beneficial"

burstiness_enhancement:
  target_cv: ">0.50"
  sentence_length_variation:
    directive: "Minimum 3 short (<=5 word) sentences per section"

expected_changes:
  ai_probability_reduction: "60-80%"
  pattern_reduction: "80-95%"
  text_change_percentage: "30-50%"
```

Key differences from balanced:
- L1: Adds tier3 vocabulary substitutions (`comprehensive` -> `thorough`, `innovative` -> `new`)
- S7: Dissolve ALL enumeration including "N main X" framing; only Methods exempt
- S8: Zero consecutive paragraphs with similar openers allowed
- S9: Break ALL formulaic section structures across entire document
- S10: Eliminate H-labels from prose entirely (keep only in tables)
- H1: All verbose phrases transformed (maximum conciseness)

### 7.3 structural.yaml

Layer 3 structural transformation reference. Applied in balanced and aggressive modes.

```yaml
version: "2.0.0"
layer: "structural"
apply_order: "Layer 1 (vocabulary) -> Layer 2 (phrase) -> Layer 3 (structural)"

mode_application:
  conservative:
    S7: "Not applied"
    S8: "Not applied"
    S9: "Not applied"
    S10: "Not applied"

  balanced:
    S7: "Dissolve in Discussion/Conclusion; preserve in Methods"
    S8: "Fix >2 consecutive same-pattern openers"
    S9: "Rewrite Discussion opener"
    S10: "Convert checklists to narrative; keep H-labels in tables"

  aggressive:
    S7: "Dissolve ALL; Methods exempt"
    S8: "ZERO consecutive same openers"
    S9: "Break ALL formulaic structures"
    S10: "Eliminate all H-labels from prose"

post_structural_check:
  - "Verify no new L1 vocabulary introduced"
  - "Verify burstiness CV improved"
  - "Verify all citations/statistics preserved"
  - "Verify paragraph opener diversity improved"

cross_pattern_interactions:
  S7_S10: +8    # Enumerated hypotheses in prose
  S8_S9:  +5    # Repetitive openers within formulaic structure
  S7_S8:  +6    # Enumeration with repetitive paragraph starts
  ALL_FOUR: +15 # Full structural AI fingerprint
```

### 7.4 academic-exceptions.md (Key Rules)

Absolute preservation rules that override all transformation configurations:

1. **Citations and References**: All (Author, year) references, DOIs, page numbers -- exact preservation
2. **Statistical Values**: All p-values, effect sizes, CIs, sample sizes, test statistics -- exact preservation
3. **Methodology Specifics**: Instrument names, software versions, scale anchors, reliability values -- exact preservation
4. **Direct Quotations**: Any text in quotation marks from sources -- exact preservation
5. **Technical Terminology**: Named theories, frameworks, methodologies, measures -- context-dependent
6. **Proper Nouns**: Author names, institutions, journals, locations -- exact preservation

**Structural exceptions**:
- S7 fully exempt in Methods sections and response letters
- S9 does not apply to Methods (formulaic structure is expected) or Abstract (IMRAD required)
- S10 may retain some tabular structure for studies testing 8+ hypotheses

**Ethical red lines**: Never fabricate citations, alter statistics, change methodology claims, remove genuine limitations, or misrepresent findings.

---

## 8. Algorithm Specifications

### 8.1 Composite AI Probability Scoring

#### 8.1.1 Phase 1: Pattern Scanning

```
FUNCTION scan_patterns(text):
    detected_patterns = []

    FOR each category IN [C, L, S, M, H, A]:
        FOR each pattern IN category:
            indicators = SCAN(text, pattern.rules)
            FOR each indicator IN indicators:
                IF NOT in_exception_context(indicator, text):
                    detected_patterns.append({
                        pattern_id: pattern.id,
                        location: indicator.location,
                        matched_text: indicator.text,
                        risk_level: pattern.risk,
                        base_weight: pattern.weight
                    })

    RETURN detected_patterns
```

#### 8.1.2 Phase 2: Quantitative Metric Calculation

```
FUNCTION calculate_metrics(text):
    sentences = tokenize_sentences(text)
    lengths = [word_count(s) for s in sentences if word_count(s) >= 3]

    # Burstiness CV
    mean_len = mean(lengths)
    std_len = std_dev(lengths)
    cv = std_len / mean_len
    burstiness_penalty = max(0, (0.45 - cv) / 0.45 * 100)

    # MTLD (bidirectional)
    tokens = tokenize_words(text)
    mtld_fwd = calculate_mtld_pass(tokens, threshold=0.72)
    mtld_bwd = calculate_mtld_pass(reverse(tokens), threshold=0.72)
    mtld = (mtld_fwd + mtld_bwd) / 2
    vocab_diversity_penalty = max(0, (80 - mtld) / 80 * 100)

    # Sentence Length Range
    length_range = max(lengths) - min(lengths)
    range_penalty = max(0, (25 - length_range) / 25 * 100)

    # Paragraph Opener Diversity
    paragraphs = split_paragraphs(text)
    first_words = [normalize(first_n_words(p, 3)) for p in paragraphs]
    opener_diversity = len(set(first_words)) / len(first_words)
    opener_penalty = max(0, (0.70 - opener_diversity) / 0.70 * 100)

    # Fano Factor (diagnostic only)
    fano = variance(lengths) / mean_len

    RETURN {cv, burstiness_penalty, mtld, vocab_diversity_penalty,
            length_range, range_penalty, opener_diversity, opener_penalty,
            fano}
```

#### 8.1.3 Phase 3: Structural Pattern Detection

```
FUNCTION detect_structural(text):
    scores = {}

    # S7: Enumeration as Prose
    ordinals = find_sequential_ordinals(text, min_count=3)
    s7_count = len(ordinals)
    s7_weight = 12
    IF any ordinal_sequence has 4+ markers:
        s7_weight *= 1.5
    IF section == "methods":
        s7_weight *= 0.5
    scores["S7"] = s7_count * s7_weight

    # S8: Repetitive Paragraph Openers
    FOR each section IN text.sections:
        openers = extract_first_3_words(section.paragraphs)
        max_repeats = max_consecutive_matching(openers)
        IF max_repeats > 3:
            s8_base = 10
            IF max_repeats == 4: s8_base *= 1.3
            IF max_repeats >= 5: s8_base *= 1.6
            scores["S8"] += s8_base

    # S9: Formulaic Section Structure
    IF section == "discussion":
        moves = detect_rhetorical_moves(text.discussion)
        canonical_count = count_canonical_order(moves)
        IF canonical_count == 5: scores["S9"] = 8
        IF canonical_count == 4: scores["S9"] = 8 * 0.7
        IF canonical_count == 3: scores["S9"] = 8 * 0.4
        IF subsection_repeats_pattern: scores["S9"] += 3

    # S10: Hypothesis Checklist
    hypotheses = find_sequential_hypothesis_verdicts(text, min_count=3)
    s10_count = len(hypotheses)
    s10_weight = 10
    IF all_in_single_paragraph: s10_weight *= 1.5
    IF identical_syntactic_structure: s10_weight *= 1.5
    scores["S10"] = s10_count * s10_weight

    # Interaction bonuses
    IF "S7" in scores AND "S10" in scores: total += 8
    IF "S8" in scores AND "S9" in scores: total += 5
    IF "S7" in scores AND "S8" in scores: total += 6
    IF all four present: total += 15

    max_possible = 12 + 10 + 8 + 10  # = 40 (base weights)
    structural_penalty = min(100, sum(scores.values()) / max_possible * 100)

    RETURN structural_penalty, scores
```

#### 8.1.4 Phase 4: Composite Scoring

```
FUNCTION composite_score(detected_patterns, metrics, structural):
    # Pattern score
    total_weight = 0
    FOR each pattern IN detected_patterns:
        score = pattern.base_weight
        IF pattern.is_clustered: score *= 1.5
        IF pattern.context_suspicious: score *= section_multiplier
        IF pattern.instance_count > 1:
            score *= (1 + 0.2 * (pattern.instance_count - 1))
        total_weight += score
    pattern_score = min(100, total_weight / MAX_EXPECTED * 100)

    # Composite
    ai_probability = (0.60 * pattern_score)
                   + (0.20 * metrics.burstiness_penalty)
                   + (0.10 * metrics.vocab_diversity_penalty)
                   + (0.10 * structural.structural_penalty)

    RETURN round(ai_probability)
```

### 8.2 Burstiness CV Calculation

```
FUNCTION calculate_burstiness_cv(text, non_native=false):
    sentences = tokenize_sentences(text)
    # Handle abbreviations, decimal numbers, parenthetical citations
    lengths = []
    FOR each sentence IN sentences:
        wc = count_words(sentence)
        IF wc >= 3:  # Exclude fragments
            lengths.append(wc)

    IF len(lengths) < 5:
        RETURN null  # Insufficient data

    mean_len = sum(lengths) / len(lengths)
    variance = sum((L - mean_len)^2 for L in lengths) / len(lengths)
    std_dev = sqrt(variance)
    cv = std_dev / mean_len

    # Penalty calculation
    threshold = 0.35 IF non_native ELSE 0.45
    IF cv >= threshold:
        penalty = 0
    ELSE:
        penalty = (threshold - cv) / threshold * 100

    RETURN {cv, penalty, mean_len, std_dev, min(lengths), max(lengths)}
```

**Interpretation table**:

| CV Range | Label | Interpretation |
|----------|-------|----------------|
| > 0.55 | High burstiness | Strong human signal |
| 0.45-0.55 | Normal burstiness | Within human range |
| 0.35-0.45 | Low burstiness | Borderline |
| 0.25-0.35 | Very low burstiness | Strong AI signal |
| < 0.25 | Minimal burstiness | Almost certainly AI |

### 8.3 MTLD Algorithm

```
FUNCTION calculate_mtld(text, ttr_threshold=0.72):
    tokens = tokenize_words(lowercase(text))

    # Forward pass
    factors_fwd = 0
    token_count = 0
    type_set = set()

    FOR each token IN tokens:
        token_count += 1
        type_set.add(token)
        current_ttr = len(type_set) / token_count

        IF current_ttr <= ttr_threshold:
            factors_fwd += 1
            token_count = 0
            type_set = set()

    # Handle partial factor
    IF token_count > 0:
        current_ttr = len(type_set) / token_count
        partial = (1.0 - current_ttr) / (1.0 - ttr_threshold)
        factors_fwd += partial

    mtld_fwd = len(tokens) / factors_fwd

    # Backward pass (same algorithm on reversed tokens)
    mtld_bwd = calculate_mtld_single_pass(reverse(tokens), ttr_threshold)

    RETURN (mtld_fwd + mtld_bwd) / 2
```

**Interpretation table**:

| MTLD Range | Label | Interpretation |
|------------|-------|----------------|
| > 100 | Very high diversity | Strong human signal |
| 80-100 | Normal diversity | Within human range |
| 60-80 | Low diversity | Borderline |
| 40-60 | Very low diversity | Strong AI signal |
| < 40 | Minimal diversity | Very likely AI or heavily templated |

### 8.4 Section-Aware Mode Escalation

```
FUNCTION determine_section_mode(section_name, section_score, user_mode, force_override):
    IF force_override:
        RETURN user_mode

    escalation_rules = {
        "abstract":     {base: "conservative", escalate: "balanced",    trigger: 50},
        "introduction": {base: "balanced",     escalate: "balanced",    trigger: null},
        "methods":      {base: "conservative", escalate: "conservative", trigger: null},
        "results":      {base: "conservative", escalate: "balanced",    trigger: 60},
        "discussion":   {base: "balanced",     escalate: "aggressive",  trigger: 50},
        "conclusion":   {base: "balanced",     escalate: "aggressive",  trigger: 50}
    }

    rule = escalation_rules[section_name]

    IF rule.trigger IS NOT null AND section_score > rule.trigger:
        RETURN rule.escalate
    ELSE:
        RETURN rule.base
```

### 8.5 Score Target System

```
FUNCTION execute_target_pipeline(text, target_score, max_passes=3):
    baseline = g5_scan(text)

    IF baseline.score <= target_score:
        RETURN {skip: true, reason: "Already below target"}

    current_text = text
    current_score = baseline.score
    pass_history = [baseline.score]

    FOR pass_num IN 1..max_passes:
        # Determine layer for this pass
        IF pass_num == 1: layer = "vocabulary"
        IF pass_num == 2: layer = "structural"
        IF pass_num == 3: layer = "polish"

        # Transform
        result = g6_transform(current_text, layer, section_escalation)

        # Re-scan
        new_score = g5_rescan(result.text)

        # Verify
        IF pass_num == 1:
            verify = f5_quick_verify(text, result.text)
        ELSE:
            verify = f5_full_verify(text, result.text)

        # Check termination conditions
        reduction = current_score - new_score.score
        current_text = result.text
        current_score = new_score.score
        pass_history.append(current_score)

        # Present checkpoint, await human decision
        decision = present_checkpoint(pass_num, pass_history, target_score)

        IF current_score <= target_score:
            RETURN {met: true, passes: pass_num, history: pass_history}
        IF reduction < 5:
            RETURN {met: false, reason: "diminishing_returns", history: pass_history}
        IF decision == "accept":
            RETURN {met: false, reason: "user_accepted", history: pass_history}

    RETURN {met: current_score <= target_score, passes: max_passes, history: pass_history}
```

---

## 9. Checkpoint Integration

### 9.1 Checkpoint Definitions

The humanization pipeline defines 5 checkpoints within the broader Diverga checkpoint system:

| Checkpoint | Level | Icon | When Triggered | Agent |
|-----------|-------|------|----------------|-------|
| CP_HUMANIZATION_REVIEW | Recommended | Orange | After G5 analysis, before transformation | G5 |
| CP_PASS1_REVIEW | Recommended | Orange | After Pass 1 (vocabulary), before Pass 2 | G6 |
| CP_PASS2_REVIEW | Recommended | Orange | After Pass 2 (structural), before Pass 3 | G6 |
| CP_FINAL_REVIEW | Optional | Yellow | After Pass 3 (polish), before export | F5 |
| CP_HUMANIZATION_VERIFY | Optional | Yellow | On-demand verification review | F5 |

### 9.2 Checkpoint Behavior

All checkpoints follow the Diverga checkpoint enforcement protocol:

1. System STOPS immediately at checkpoint
2. Options presented via structured interface
3. System WAITS for explicit human approval
4. System does NOT proceed until approval received
5. System does NOT assume approval based on context

### 9.3 CP_HUMANIZATION_REVIEW (Recommended)

**Trigger**: After G5 initial analysis completes.

**Presents**:
- AI probability score (composite)
- Pattern summary (high/medium/low counts)
- Quantitative metrics dashboard (burstiness CV, MTLD, sentence length range, opener diversity)
- Recommended mode (based on score)
- Section-level scores (if section-aware mode enabled)

**Options**:
```
[A] Conservative  -- High-risk patterns only (Layer 1-2)
[B] Balanced      -- Recommended (Layer 1-3)
[C] Aggressive    -- Maximum naturalness (Layer 1-3, all patterns)
[D] View detailed report
[E] Skip humanization
```

**Decision flow**: Selecting A/B/C transitions to `pass1_transforming`. Selecting E transitions to `idle`.

### 9.4 CP_PASS1_REVIEW (Recommended)

**Trigger**: After Pass 1 vocabulary transformation + G5 re-scan + F5 quick verify.

**Presents**:
- Score before/after Pass 1 (e.g., 67% -> 48%)
- Patterns remaining by category
- Burstiness CV score
- Estimated improvement from structural pass

**Options**:
```
[A] Continue to structural pass
[B] Accept current state
[C] View detailed diff
```

### 9.5 CP_PASS2_REVIEW (Recommended)

**Trigger**: After Pass 2 structural transformation + G5 re-scan + F5 full verify.

**Presents**:
- Score progression: original -> Pass 1 -> Pass 2 (e.g., 67% -> 48% -> 28%)
- Structural metrics: burstiness CV before/after, MTLD before/after
- Remaining pattern count
- Whether target is met (if target mode active)

**Options**:
```
[A] Accept
[B] One more polish pass
[C] Manual review mode
```

### 9.6 CP_FINAL_REVIEW (Optional)

**Trigger**: After Pass 3 polish + G5 audit + F5 full verify.

**Presents**:
- Complete score history across all passes
- Full diff report (original vs final)
- F5 verification summary (all 7 domains)
- Target compliance status

**Options**:
```
[A] Approve and export
[B] Adjust specific changes
[C] Revert to earlier pass
[D] Revert to original
```

### 9.7 CP_HUMANIZATION_VERIFY (Optional)

**Trigger**: On-demand when user requests detailed verification review after any pass.

**Presents**:
- Before/after comparison for the specific pass
- Change summary with pattern IDs
- New AI probability score
- Full integrity verification results (7 domains)

**Options**:
```
[A] Approve and continue
[B] Adjust specific changes
[C] Try different mode
[D] Revert to original
```

### 9.8 Prerequisites

Within the Diverga agent prerequisite system:

| Agent | Prerequisites | Own Checkpoints |
|-------|--------------|-----------------|
| G5 | (none) | CP_HUMANIZATION_REVIEW |
| G6 | CP_HUMANIZATION_REVIEW | CP_HUMANIZATION_VERIFY |
| F5 | (none) | (none -- F5 is invoked by pipeline, not independently) |

G6 cannot execute without a prior CP_HUMANIZATION_REVIEW approval. This ensures users always see the G5 analysis before any transformation occurs.

---

## 10. Non-Functional Requirements

### 10.1 Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| G5 analysis time | < 30 seconds per 5000 words | Pattern scan + quantitative metrics |
| G6 transformation time | < 120 seconds per pass per 5000 words | Opus-tier model required |
| F5 verification time | < 15 seconds (quick), < 30 seconds (full) | Haiku-tier model |
| Full pipeline (2 passes) | < 10 minutes per 5000 words | Including human checkpoint wait time |
| Score accuracy | +/- 10 points for texts > 200 words | Calibrated against human judgment |
| Score accuracy (short text) | +/- 15 points for texts < 200 words | Wider margin for short texts |
| Score accuracy (long text) | +/- 5 points for texts > 2000 words | Narrower margin for long texts |

### 10.2 Score Presets

Pre-defined target scores for common use cases:

| Preset | Target Score | Use Case | Typical Passes Required |
|--------|-------------|----------|------------------------|
| `journal_safe` | 30 | Peer-reviewed journal submissions | 2-3 |
| `conference` | 40 | Conference papers | 1-2 |
| `working_paper` | 50 | Working papers, preprints | 1 |

### 10.3 Preservation Guarantees

| Element | Guarantee | Verification |
|---------|-----------|-------------|
| Citations | 100% exact preservation | F5 Domain 1 (CRITICAL) |
| Statistics | 100% exact preservation | F5 Domain 2 (CRITICAL) |
| Technical terms | Context-dependent preservation | F5 Domain 3 |
| Core meaning | Semantic equivalence | F5 Domain 3 |
| Burstiness CV | Non-decreasing after transformation | F5 Domain 5 |
| Structural patterns | Non-increasing count after transformation | F5 Domain 6 |

### 10.4 Error Recovery

| Error Type | Detection | Recovery |
|------------|-----------|----------|
| Citation modified | F5 Domain 1 | ABORT pass, automatic revert |
| Statistic modified | F5 Domain 2 | ABORT pass, automatic revert |
| Score increased | G5 re-scan | WARN, offer revert |
| New patterns introduced | G5 re-scan | FLAG with net change, user decides |
| Burstiness decreased | F5 Domain 5 | FLAG, recommend additional variation |
| Meaning distorted | F5 Domain 3 | FLAG, require manual review |

### 10.5 Pipeline Constraints

```yaml
max_passes: 3
diminishing_returns_threshold: 5    # Stop if pass reduces < 5 points
between_pass_rescan: true           # MANDATORY G5 re-scan between every pass
checkpoint_between_passes: true     # Human checkpoint between every pass
skip_if_below: 20                   # Skip pipeline if AI probability < 20%
recommend_if_above: 40              # Recommend pipeline if > 40%
require_review_if_above: 70         # Require human review if > 70%
```

### 10.6 Ethical Requirements

1. The pipeline helps express ideas naturally; it does NOT make AI use "undetectable."
2. Researchers must follow institutional and journal AI disclosure policies.
3. The pipeline must never fabricate citations, alter statistics, or misrepresent findings.
4. Non-native speaker calibration is opt-in only to avoid implicit bias assumptions.
5. An AI use disclosure reminder is shown after pipeline completion (configurable).

---

## 11. Appendices

### Appendix A: Complete Pattern Weight Table

| ID | Pattern Name | Base Weight | Risk | Category |
|----|-------------|-------------|------|----------|
| C1 | Significance Inflation | 10 | High | Content |
| C2 | Notability Claims | 7 | Medium | Content |
| C3 | Superficial -ing | 6 | Medium | Content |
| C4 | Promotional Language | 10 | High | Content |
| C5 | Vague Attributions | 12 | High | Content |
| C6 | Formulaic Sections | 3 | Low | Content |
| L1-tier1 | AI Vocabulary (high alert) | 15 | High | Language |
| L1-tier2 | AI Vocabulary (moderate) | 8 | Medium | Language |
| L1-cluster | AI Vocab Clustering Bonus | 20 | High | Language |
| L2 | Copula Avoidance | 8 | Medium | Language |
| L3 | Negative Parallelism | 6 | Medium | Language |
| L4 | Rule of Three | 4 | Low | Language |
| L5 | Elegant Variation | 7 | Medium | Language |
| L6 | False Ranges | 3 | Low | Language |
| S1 | Em Dash Overuse | 5 | Medium | Style |
| S2 | Excessive Boldface | 3 | Low | Style |
| S3 | Inline-Header Lists | 6 | Medium | Style |
| S4 | Title Case Overuse | 2 | Low | Style |
| S5 | Emoji Usage | 20 | High | Style |
| S6 | Quote Inconsistency | 2 | Low | Style |
| S7 | Enumeration as Prose | 12 | High | Style (Structural) |
| S8 | Repetitive Paragraph Openers | 10 | High | Style (Structural) |
| S9 | Formulaic Section Structure | 8 | Medium | Style (Structural) |
| S10 | Hypothesis Checklist Pattern | 10 | High | Style (Structural) |
| M1 | Chatbot Artifacts | 25 | High | Communication |
| M2 | Knowledge Disclaimers | 30 | High | Communication |
| M3 | Sycophantic Tone | 10 | Medium | Communication |
| H1 | Verbose Phrases | 2 (per instance) | Low | Filler |
| H2 | Hedge Stacking | 8 | Medium | Filler |
| H3 | Generic Conclusions | 6 | Medium | Filler |
| A1 | Abstract Template | 4 | Low | Academic |
| A2 | Methods Boilerplate | 4 | Low | Academic |
| A3 | Discussion Inflation | 12 | High | Academic |
| A4 | Citation Hedging | 15 | High | Academic |
| A5 | Contribution Enumeration | 3 | Low | Academic |
| A6 | Limitation Disclaimers | 3 | Low | Academic |

### Appendix B: Worked Scoring Example

**Given text with**:
- 34 patterns detected, normalized pattern_score = 62
- Burstiness CV = 0.31
- MTLD = 58
- Structural: S7 (1 instance, weight 12), S8 (1 instance, weight 10), S9 absent, S10 absent

**Calculation**:

```
pattern_score = 62

burstiness_penalty = max(0, (0.45 - 0.31) / 0.45 * 100)
                   = max(0, 0.14 / 0.45 * 100)
                   = 31.1

vocab_diversity_penalty = max(0, (80 - 58) / 80 * 100)
                        = max(0, 22 / 80 * 100)
                        = 27.5

structural_penalty:
  S7: 1 * 12 = 12
  S8: 1 * 10 = 10
  S9: 0
  S10: 0
  raw = 22, max_possible = 40
  structural_penalty = 22 / 40 * 100 = 55.0

AI_Probability = (0.60 * 62) + (0.20 * 31.1) + (0.10 * 27.5) + (0.10 * 55.0)
               = 37.2 + 6.22 + 2.75 + 5.50
               = 51.67
               = 52% (rounded)

Risk Level: ELEVATED (Probably AI-Assisted)
Recommendation: Balanced mode humanization
```

### Appendix C: Before/After Transformation Examples

**Example 1: S7 Enumeration Dissolution**

Before (AI-like):
```
Education significantly predicted AI concern in three ways. First,
higher education was associated with greater awareness of AI
capabilities. Second, educational attainment correlated with more
nuanced understanding of automation risks. Third, the education-concern
relationship was moderated by partisan identity.
```

After (human-like):
```
Education mattered, but not in the straightforward way we expected.
People with college degrees were more likely to know what large language
models actually do -- and that awareness amplified their concern. Yet
the relationship fractured along partisan lines. Among Democrats,
education strengthened worry about job displacement. Among Republicans,
it did the opposite.
```

Changes: Ordinal markers removed. Narrative builds through cause-effect. Short emphatic sentence added. Sentence length varies from 7 to 24 words. Burstiness enhanced.

**Example 2: S10 Hypothesis Narrative**

Before (AI-like):
```
H1 predicted that education would positively predict AI concern. This
hypothesis was supported (beta = 0.23, p < .001). H2 predicted that
partisan identity would moderate the education-concern relationship.
This hypothesis was partially supported. H3 predicted that AI awareness
would mediate the age-concern relationship. This hypothesis was not
supported (beta = 0.02, 95% CI [-0.01, 0.05]).
```

After (human-like):
```
The partisan divide we predicted materialized clearly -- Republicans
were 14 percentage points more likely to express concern (AME = 0.14,
p < .001). But the education gradient surprised us: rather than a
simple linear relationship, the effect flattened above a bachelor's
degree. Two predictions fell flat. We thought AI awareness would
explain why younger people worried more, but the mediation path was
a dead end (indirect effect: 0.02, 95% CI crossing zero).
```

Changes: Hypotheses grouped thematically. H-labels removed from prose. Effect sizes anchor the narrative. Null findings framed as discoveries. All statistics preserved verbatim.

**Example 3: S8 Paragraph Opener Variation**

Before (AI-like):
```
The results for education revealed a significant positive association...

The partisan gap emerged as the strongest predictor...

The interaction between age and awareness complicated the picture...

The Blinder-Oaxaca decomposition showed that demographic differences...
```

After (human-like):
```
Education's role proved more complicated than a simple linear gradient...

What explains the partisan gap? Not demographics alone...

Age and awareness interacted in ways that complicate any simple
generational narrative...

Decomposing the partisan gap revealed something unexpected...
```

Changes: Five different opening strategies instead of "The [X]..." monotony. Question opener, noun phrase, subject-verb, gerund phrase used.

### Appendix D: Score Progression Example (Multi-Pass)

```
+-------+----------+----------+---------+----------+
| Stage | AI Score | CV       | MTLD    | S7-S10   |
+-------+----------+----------+---------+----------+
| Base  |   67%    |   0.28   |   52    |  4 flags |
| Pass1 |   48%    |   0.30   |   58    |  4 flags |
| Pass2 |   28%    |   0.48   |   74    |  1 flag  |
| Pass3 |   24%    |   0.51   |   78    |  0 flags |
+-------+----------+----------+---------+----------+
Target: 30% (journal_safe) -- MET after Pass 2
```

### Appendix E: Pipeline Configuration Reference

```yaml
# Complete pipeline configuration
humanization:
  enabled: true
  default_mode: "balanced"
  pipeline_version: "2.0"
  auto_check: true
  show_checkpoint: true
  require_verification: false

  multi_pass:
    max_passes: 3
    inter_pass_checkpoint: true
    auto_stop_threshold: 5
    mandatory_rescan: true

  score_target:
    enabled: true
    default_target: null
    presets:
      journal_safe: 30
      conference: 40
      working_paper: 50

  section_escalation:
    enabled: true
    allow_override: true

  thresholds:
    skip_if_below: 20
    recommend_if_above: 40
    require_if_above: 70

  reports:
    include_pattern_report: false
    include_audit_trail: true
    include_score_progression: true
    save_original: true

  ethics:
    show_disclosure_reminder: true
    suggest_acknowledgment: true
```

### Appendix F: Cross-Pattern Interaction Bonuses

| Combination | Bonus Points | Condition |
|-------------|-------------|-----------|
| S7 + S10 | +8 | Enumerated hypotheses in prose |
| S8 + S9 | +5 | Repetitive openers within formulaic structure |
| S7 + S8 | +6 | Enumeration with repetitive paragraph starts |
| S7 + S8 + S9 + S10 | +15 | Full structural AI fingerprint |
| Content + Language | +10 | Multi-category clustering |
| Language + Style | +5 | Multi-category clustering |
| Content + Communication | +15 | Multi-category clustering |
| Any 3 categories | +20 | Multi-category clustering |
| 4+ categories | +30 | Multi-category clustering |

### Appendix G: Error Handling Matrix

| Error | Detection Agent | Severity | Automatic Action | User Options |
|-------|----------------|----------|------------------|-------------|
| Citation modified | F5 (Domain 1) | CRITICAL | ABORT, revert pass | -- (automatic) |
| Statistic modified | F5 (Domain 2) | CRITICAL | ABORT, revert pass | -- (automatic) |
| Meaning distorted | F5 (Domain 3) | MAJOR | FLAG | Review, accept, revert |
| Score increased | G5 re-scan | WARNING | WARN | Accept, revert |
| New patterns introduced | G5 re-scan | WARNING | FLAG with net delta | Accept, target in next pass, revert |
| Burstiness decreased | F5 (Domain 5) | MAJOR | FLAG | Add variation, accept |
| Structural count increased | F5 (Domain 6) | MAJOR | FLAG | Review, revert |
| Terminology inconsistency | F5 (Domain 7) | MINOR | WARN | Fix manually, accept |
| Mode inappropriate | G6 self-check | INFO | SUGGEST | Change mode, continue |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.0.0 | 2026-02-22 | Diverga Team | Initial SDD for Humanization Pipeline v2.0 |

---

*This document describes the Diverga Humanization Pipeline v2.0 as implemented in Diverga v8.1+. For the latest source code and documentation, see https://github.com/HosungYou/humanizer.*
