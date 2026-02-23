# Humanization Pipeline v3.0 — Improvement Plan

> **Version**: 1.0
> **Date**: 2026-02-23
> **Status**: Proposal
> **Based on**: [research-literature-review.md](./research-literature-review.md) v2.0 (72 references), [humanization-pipeline-upgrade.md](./humanization-pipeline-upgrade.md), [round3-strategy.md](./round3-strategy.md)
> **Repository**: [HosungYou/humanizer](https://github.com/HosungYou/humanizer)

---

## Executive Summary

The v2.0 pipeline (Three-Pillar upgrade) addressed vocabulary-level transformation and introduced structural patterns S7-S10. However, the 2025-2026 detection landscape reveals a critical gap: **discourse-level structural detection** is now the most evasion-resistant signal, and no current humanization approach addresses it.

Pipeline v3.0 proposes four strategic upgrades:

| Upgrade | Target | Key Innovation | Priority |
|---------|--------|----------------|----------|
| **A. Discourse Transformation** | G6 v3.0 | RST motif variation, PDTB coherence diversification | CRITICAL |
| **B. Extended Metrics** | Humanizer MCP v3.0 | Surprisal dynamics, psycholinguistic features, discourse metrics | HIGH |
| **C. Detector-Guided Feedback** | Pipeline v3.0 | Real-time detector scoring as optimization signal | HIGH |
| **D. Benchmark Evaluation** | QA Framework | RAID-based validation protocol | MEDIUM |

---

## 1. Current State Assessment

### 1.1 What v2.0 Achieved

| Component | v2.0 Status | Effectiveness |
|-----------|-------------|---------------|
| G5 v2.0: S7-S10 structural patterns | Implemented | Detects enumeration, repetitive openers, formulaic structure |
| G6 v2.0: Layer 3 structural transformation | Implemented | Dissolves enumeration, varies openers, narrativizes hypotheses |
| Pipeline v2.0: Multi-pass architecture | Implemented | Vocabulary → Structure → Polish, with checkpoints |
| Humanizer MCP: 4 stylometric tools | Deployed (v2.1.0) | Burstiness CV, MTLD, Fano Factor, opener diversity, hedge density |

### 1.2 What v2.0 Does Not Address (Gap Analysis)

| Gap | Detection Signal | Research Source | Severity |
|-----|-----------------|----------------|----------|
| **Discourse motif uniformity** | RST subgraph patterns lack variability | Kim et al., ACL 2024 [Ref 48] | CRITICAL |
| **PDTB coherence formulaicity** | Discourse relations follow predictable sequences | DTransformer, arXiv:2412.12679 [Ref 49] | HIGH |
| **Surprisal dynamics** | Token-level predictability is too smooth | DivEye, NeurIPS 2025 [Ref 43] | HIGH |
| **Section-conditional profiling** | Same approach applied uniformly across IMRaD | Sci-SpanDet, 2025 [Ref 50] | HIGH |
| **Perturbation pattern detection** | Systematic edits create detectable traces | arXiv:2510.02319 [Ref 47] | MEDIUM |
| **Transition-point detection** | Authorship shift boundaries are detectable | arXiv:2509.17830 [Ref 55] | MEDIUM |
| **Psycholinguistic markers** | Contraction density, first-person pronouns, hapax rate | arXiv:2505.01800 [Ref 51] | MEDIUM |

---

## 2. Upgrade A: Discourse Transformation (G6 v3.0)

### 2.1 Problem Statement

The 2024-2025 discourse detection research (ACL 2024, DTransformer) demonstrates that AI text generates discourse that is **locally coherent but globally formulaic**. RST discourse motifs — recurring subgraph patterns in rhetorical structure trees — are significantly less variable in AI text than human text. This is the most evasion-resistant detection signal identified in 2025 research.

Current G6 v2.0 operates at the sentence and paragraph level. It does not model or manipulate the **rhetorical structure** of the document.

### 2.2 Proposed Layer 4: Discourse Transformation

Add a fourth transformation layer to G6:

| Layer | Level | Current Status | v3.0 Addition |
|-------|-------|----------------|---------------|
| Layer 1 | Word substitution | v1.0 | — |
| Layer 2 | Phrase restructuring | v1.0 | — |
| Layer 3 | Structural transformation (S7-S10) | v2.0 | — |
| **Layer 4** | **Discourse transformation** | — | **New in v3.0** |

### 2.3 Layer 4 Transformation Strategies

**Strategy D1: Rhetorical Move Reordering**

AI text follows predictable rhetorical sequences in Discussion sections:
```
AI Default:  Summary → Comparison → Implications → Limitations → Future
```

Layer 4 introduces varied rhetorical orderings:
```
Variant A:  Surprising finding → Why it matters → What we expected → What happened instead
Variant B:  Question → Data answer → Theoretical tension → Resolution
Variant C:  Limitation first → How we addressed it → What emerged → Broader meaning
Variant D:  Concrete scenario → Abstract principle → Evidence → Counterargument → Synthesis
```

**Strategy D2: Digression Injection**

Human academic writing naturally contains:
- Parenthetical observations ("—a pattern we did not anticipate—")
- Brief retrospective cross-references ("Recall that in Section 3...")
- Intellectual asides ("One might wonder whether...")
- Methodological commentary embedded in discussion ("The Blinder-Oaxaca approach, while standard, may overstate...")

G6 v3.0 should inject 1-2 digressions per Discussion section, calibrated by discipline.

**Strategy D3: Argument Structure Diversification**

AI text uses uniform argument trees. Human argumentation embeds:
- Concessions before claims ("While X is well-established, our data suggest...")
- Counter-anticipation ("A skeptic might argue that... However,")
- Hedged speculation alongside firm claims
- Non-linear evidence presentation (conclusion before evidence, or interleaved)

**Strategy D4: Connective Reduction and Variation**

Replace explicit formulaic connectives with:
- Zero-connective transitions (juxtaposition)
- Implicit relations (the reader infers the connection)
- Varied connective vocabulary beyond "furthermore/moreover/in addition"

### 2.4 Implementation Approach

```yaml
discourse_transformation:
  activation: "Pass 2 (Structural) or Pass 3 (Polish)"
  prerequisite: "Layer 3 complete (S7-S10 resolved)"
  strategies:
    D1_rhetorical_reorder:
      target_sections: ["discussion", "conclusion"]
      min_variants: 4
      selection: "random per section, avoid AI-default sequence"
    D2_digression_injection:
      target_sections: ["discussion", "results"]
      count_per_section: "1-2"
      types: ["parenthetical", "retrospective", "methodological"]
    D3_argument_diversification:
      target_sections: ["discussion", "introduction"]
      techniques: ["concession_before_claim", "counter_anticipation", "non_linear_evidence"]
    D4_connective_variation:
      target_sections: ["all"]
      max_explicit_connectives_per_paragraph: 1
      replace_with: ["zero_connective", "implicit", "varied_vocabulary"]
```

---

## 3. Upgrade B: Extended Metrics (Humanizer MCP v3.0)

### 3.1 New Metrics to Add

Based on the 2025 research, the following metrics should be added to the humanizer MCP server:

**Tier 1: High Priority (Strong discriminative power)**

| Metric | Algorithm | Human Baseline | AI Typical | Library |
|--------|-----------|---------------|------------|---------|
| Surprisal variance | Per-sentence GPT-2 surprisal, compute variance | High | Low | `lmppl` + `gpt2` |
| Surprisal 2nd-order autocorrelation | Autocorrelation of surprisal differences | High (bursty) | Low (smooth) | `numpy` + `lmppl` |
| Hapax legomenon rate | Words appearing exactly once / total words | > 0.50 | < 0.35 | Custom (Counter) |
| Contraction density | Contractions / sentence count | > 0.15 | < 0.05 | Regex |
| Paragraph length variance | CV of paragraph word counts | > 0.40 | < 0.25 | Custom |

**Tier 2: Medium Priority (Complementary signals)**

| Metric | Algorithm | Human Baseline | AI Typical | Library |
|--------|-----------|---------------|------------|---------|
| Abstract noun density | Abstract nouns / total nouns | < 0.30 | > 0.45 | spaCy + wordnet |
| Verb concreteness ratio | Concrete verbs / total verbs | > 0.60 | < 0.40 | Custom |
| Connective diversity | Unique connectives / total connectives | > 0.70 | < 0.50 | Pattern matching |
| First-person pronoun density | I/we/my/our per sentence | varies by discipline | near 0 | Regex |
| Question sentence ratio | Questions / total sentences | > 0.03 | < 0.01 | Regex |

**Tier 3: Future Research (Requires model inference)**

| Metric | Algorithm | Notes |
|--------|-----------|-------|
| Per-sentence perplexity distribution | GPT-2 perplexity per sentence | Requires model loading |
| Surprisal kurtosis | Tail heaviness of surprisal dist. | Requires model loading |
| POS entropy | Shannon entropy of POS tag distribution | spaCy POS tagger |
| Discourse marker diversity index | Unique discourse markers / total | Pattern matching |

### 3.2 Updated Composite Score

Extend the current composite score from 4 to 6 components:

```python
# v2.0 (current)
AI_Probability = (0.60 * pattern_score)
              + (0.20 * burstiness_penalty)
              + (0.10 * vocab_diversity_penalty)
              + (0.10 * structural_penalty)

# v3.0 (proposed)
AI_Probability = (0.40 * pattern_score)
              + (0.15 * burstiness_penalty)
              + (0.10 * vocab_diversity_penalty)
              + (0.10 * structural_penalty)
              + (0.15 * discourse_penalty)        # NEW
              + (0.10 * psycholinguistic_penalty)  # NEW
```

**Weight rationale:**

| Component | v2.0 | v3.0 | Change | Rationale |
|-----------|------|------|--------|-----------|
| pattern_score | 0.60 | 0.40 | -0.20 | Reduced: vocabulary patterns are increasingly easy to evade |
| burstiness_penalty | 0.20 | 0.15 | -0.05 | Slightly reduced to accommodate new dimensions |
| vocab_diversity | 0.10 | 0.10 | 0 | Stable complementary signal |
| structural_penalty | 0.10 | 0.10 | 0 | S7-S10 remain valuable |
| discourse_penalty | — | 0.15 | +0.15 | **Most evasion-resistant signal (ACL 2024)** |
| psycholinguistic_penalty | — | 0.10 | +0.10 | Cognitive authenticity markers |

### 3.3 Discipline-Specific Calibration Updates

Based on 2025 research on discipline-specific detection differences:

| Discipline | Key Calibration | Rationale |
|------------|----------------|-----------|
| **STEM** | Reduce contraction/pronoun penalties; accept lower burstiness | Formal STEM writing naturally mimics AI uniformity |
| **Humanities** | Maximize idiosyncrasy, hedging, first-person voice | AI detection is strongest here due to voice expectations |
| **Social Sciences** | Break formula-report structure; vary citation integration | Formulaic structure aids detection |
| **Education** | Lower MTLD threshold; accept simpler vocabulary | Accessible language is the norm |
| **Psychology** | Focus on hedging gradient; increase measurement language | Hedging/boosting contrast is key |

```yaml
discipline_calibration_v3:
  stem:
    contraction_penalty_weight: 0.0     # contractions are rare in STEM
    pronoun_penalty_weight: 0.3         # reduced (passive voice is normal)
    burstiness_threshold: 0.38          # lower (STEM sentences are more uniform)
    key_strategy: "first-person agency verbs, controlled precision variation"

  humanities:
    contraction_penalty_weight: 1.0     # full weight
    pronoun_penalty_weight: 1.0         # full weight
    discourse_penalty_weight: 1.5       # elevated (voice expectations are high)
    key_strategy: "maximize idiosyncrasy, non-linear argument, personal voice"

  social_sciences:
    structural_penalty_weight: 1.2      # elevated (formula-report structure is the tell)
    discourse_penalty_weight: 1.2       # elevated
    key_strategy: "break report formula, vary citation integration, embed narrative"
```

---

## 4. Upgrade C: Detector-Guided Feedback Loop

### 4.1 Research Basis

The NeurIPS 2025 adversarial paraphrasing paper [Ref 44] achieved 87.88% average TPR reduction by using **detector scores as a real-time optimization signal**. This is the most effective humanization technique documented in 2025 research.

### 4.2 Architecture

```
╔══════════════════════════════════════════════════════╗
║  DETECTOR-GUIDED FEEDBACK LOOP (Pipeline v3.0)      ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  Input text                                          ║
║    │                                                 ║
║    ▼                                                 ║
║  G5 Analysis ──────► Score + Pattern List             ║
║    │                                                 ║
║    ▼                                                 ║
║  Humanizer MCP ────► Quantitative Metrics            ║
║    │                                                 ║
║    ▼                                                 ║
║  ┌────────────────────────────────────────────┐      ║
║  │  FEEDBACK LOOP (max 3 iterations)          │      ║
║  │                                            │      ║
║  │  G6 Transform ──► G5 Re-scan ──► Score     │      ║
║  │       │                            │       │      ║
║  │       │         IF score > target ──┘      │      ║
║  │       │         IF score <= target ──► EXIT │      ║
║  │       │                                    │      ║
║  │       ▼                                    │      ║
║  │  Humanizer MCP ──► Metric Delta            │      ║
║  │       │                                    │      ║
║  │       ▼                                    │      ║
║  │  Adjust strategy based on:                 │      ║
║  │  - Which metrics regressed                 │      ║
║  │  - Which patterns were introduced          │      ║
║  │  - Section-specific score distribution     │      ║
║  └────────────────────────────────────────────┘      ║
║    │                                                 ║
║    ▼                                                 ║
║  F5 Final Verify ──► Output                          ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

### 4.3 Feedback Signal Integration

After each G6 transformation pass, the humanizer MCP provides:

```yaml
feedback_signals:
  score_delta:
    metric: "G5 composite score change"
    action_if_positive: "REVERT pass, try alternative strategy"
    action_if_negative: "CONTINUE"

  metric_regression:
    check: "Did any individual metric worsen?"
    burstiness_regressed: "Focus next pass on sentence length variation"
    mtld_regressed: "Inject more unique vocabulary"
    opener_diversity_regressed: "Apply D3 (paragraph opener variation)"
    discourse_regressed: "Apply D1 (rhetorical reordering)"

  new_patterns_introduced:
    check: "Did G6 introduce new AI patterns?"
    action: "Target new patterns specifically in next iteration"
    max_acceptable: 2  # abort if >2 new patterns introduced

  section_distribution:
    check: "Which sections still score highest?"
    action: "Escalate mode for high-scoring sections only"
```

### 4.4 Perturbation Naturalization

The 2025 research [Ref 47] shows that systematic edits create detectable perturbation traces. To counter this:

```yaml
perturbation_naturalization:
  principle: "Edits must mimic human revision patterns, not algorithmic substitution"
  strategies:
    - "Vary edit density across sections (not uniform)"
    - "Include both additions and deletions (human edits are 74% replacements, 18% deletions, 8% insertions)"
    - "Leave some low-risk patterns untouched (humans don't fix everything)"
    - "Introduce occasional stylistic inconsistencies (human texts are not perfectly consistent)"
    - "Edit in bursts rather than uniformly distributed across the document"
```

---

## 5. Upgrade D: Benchmark Evaluation Protocol

### 5.1 RAID-Based Validation

Use the RAID benchmark conditions (ACL 2024, [Ref 56]) as the evaluation framework:

| Test Condition | What It Tests | Pass Criteria |
|----------------|---------------|---------------|
| Unmodified AI text | Baseline detection | G5 score > 60% (confirms detector works) |
| After Pass 1 (Vocabulary) | Vocabulary layer effectiveness | Score drop ≥ 20pp |
| After Pass 2 (Structure) | Structural layer effectiveness | Score drop ≥ 15pp additional |
| After Pass 3 (Discourse) | Discourse layer effectiveness | Score drop ≥ 10pp additional |
| Final output | End-to-end pipeline | Score < 30% (journal_safe) |
| Citation integrity | Preservation | 100% match |
| Statistics integrity | Preservation | 100% match |
| Meaning preservation | Semantic similarity | ≥ 95% |
| Burstiness CV | Quantitative | > 0.45 |
| MTLD | Quantitative | > 70 |
| Discourse motif diversity | Structural | > human 25th percentile |

### 5.2 Multi-Detector Validation

Test against multiple detectors to ensure robustness:

| Detector | Type | Target |
|----------|------|--------|
| G5 (internal) | Pattern + metrics composite | < 30% |
| GPTZero | Perplexity + burstiness | Not flagged as AI |
| Originality.ai | Classifier-based | < 30% AI probability |
| Binoculars (open-source) | Contrastive dual-model | Below threshold |

### 5.3 Validation Corpus

Use the two existing papers (Paper 1: TFSC, Paper 2: IJAIED) plus:

| Paper | Domain | Journal | Purpose |
|-------|--------|---------|---------|
| Paper 1 | Social Science (Occupational Identity) | TFSC (IF ~12.0) | Existing baseline |
| Paper 2 | Education (Epistemic Cognition) | IJAIED (IF ~4.7) | Existing baseline |
| Paper 3 (new) | Psychology | TBD | Test discipline-specific calibration |
| Paper 4 (new) | STEM | TBD | Test STEM-specific calibration |

---

## 6. Implementation Roadmap

### Phase 1: Extended Metrics (Weeks 1-2) — HIGH PRIORITY

| Task | Deliverable | Effort |
|------|-------------|--------|
| Add Tier 1 metrics to humanizer MCP | 5 new tools/metrics | 3 days |
| Add surprisal computation (lmppl + gpt2) | Per-sentence perplexity | 2 days |
| Update composite score to v3.0 formula | 6-component score | 1 day |
| Add discipline-specific calibration v3 | 5 discipline profiles | 2 days |
| Write tests for new metrics | 100% coverage | 2 days |

### Phase 2: Discourse Transformation (Weeks 3-4) — CRITICAL

| Task | Deliverable | Effort |
|------|-------------|--------|
| Implement D1: Rhetorical move reordering | 4+ variant templates | 3 days |
| Implement D2: Digression injection | Digression library | 2 days |
| Implement D3: Argument structure diversification | Concession/counter patterns | 2 days |
| Implement D4: Connective reduction/variation | Connective replacement rules | 1 day |
| Update G6 agent prompt with Layer 4 instructions | G6 v3.0 skill file | 2 days |

### Phase 3: Feedback Loop (Weeks 5-6) — HIGH

| Task | Deliverable | Effort |
|------|-------------|--------|
| Implement detector-guided feedback architecture | Pipeline v3.0 flow | 3 days |
| Add metric regression detection | Auto-strategy adjustment | 2 days |
| Implement perturbation naturalization | Edit pattern randomization | 2 days |
| Update F5 verifier with discourse checks | F5 v2.0 | 2 days |

### Phase 4: Benchmark & Validation (Week 7) — MEDIUM

| Task | Deliverable | Effort |
|------|-------------|--------|
| Set up RAID-based validation protocol | Test suite | 2 days |
| Run validation on Papers 1-2 | Benchmark results | 1 day |
| Multi-detector validation | Cross-detector report | 1 day |
| Write v3.0 release documentation | Release notes | 1 day |

---

## 7. Success Criteria

### 7.1 Quantitative Targets

```
SUCCESS = (
    final_score < 30%                        # journal_safe
    AND passes_needed <= 2                   # automated, no manual work
    AND citation_preservation == 100%
    AND statistics_preservation == 100%
    AND meaning_preservation >= 95%
    AND burstiness_CV > 0.45
    AND MTLD > 70
    AND paragraph_opener_diversity > 0.70
    AND discourse_motif_diversity > human_25th_percentile   # NEW
    AND surprisal_variance > human_25th_percentile          # NEW
    AND no_new_HIGH_patterns_introduced                     # NEW
)
```

### 7.2 Comparison with v2.0 Targets

| Metric | v2.0 Target | v3.0 Target | Change |
|--------|-------------|-------------|--------|
| Final score | < 30% | < 30% | Same |
| Passes needed | ≤ 2 | ≤ 2 | Same |
| Discourse motif diversity | Not measured | > human 25th percentile | **New** |
| Surprisal variance | Not measured | > human 25th percentile | **New** |
| Perturbation naturalness | Not measured | Mimics human revision | **New** |
| Multi-detector robustness | G5 only | G5 + GPTZero + Originality | **New** |

---

## 8. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Discourse transformation degrades meaning | Medium | High | F5 meaning check (≥95% threshold) |
| Surprisal computation too slow for MCP | Low | Medium | Lazy-load GPT-2; cache at server level |
| Detectors adapt to discourse diversification | High (long-term) | Medium | Continuous monitoring; RAID re-evaluation |
| EU AI Act Article 50 creates legal exposure | Medium | High | Position as "writing quality improvement," not detection evasion |
| Section-conditional approach increases complexity | Low | Low | Sensible defaults; escalation only when triggered |

---

## References

See [research-literature-review.md](./research-literature-review.md) v2.0 for full reference list (72 references).

Key papers driving this plan:
- [48] Kim et al. (ACL 2024). Discourse motifs — most evasion-resistant detection signal
- [49] DTransformer (2024). PDTB coherence features for document-level detection
- [44] Adversarial Paraphrasing (NeurIPS 2025). Detector-guided feedback loop
- [43] DivEye (NeurIPS 2025). Surprisal-based diversity features
- [50] Sci-SpanDet (2025). Section-conditional academic detection
- [51] Psycholinguistic analysis (2025). Cognitive authenticity markers
- [47] Perturbation pattern detection (2025). Evasion traces as detection signal
- [56] RAID benchmark (ACL 2024). Standard evaluation framework

---

> **End of Document** | Related: [research-literature-review.md](./research-literature-review.md), [humanization-pipeline-upgrade.md](./humanization-pipeline-upgrade.md), [round3-strategy.md](./round3-strategy.md)
