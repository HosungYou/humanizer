# Diverga Humanization Pipeline Upgrade Roadmap

## Overview

- Total 13 files (4 new, 9 modified)
- 4-phase implementation plan
- All file locations: Under `/Users/hosung/.claude/plugins/diverga/`
- Goal: Achieve AI detection score <30%, minimize manual intervention

---

## Phase 1: G5 Detection Upgrade (4 files)

| # | File | Changes | Complexity |
|---|------|---------|-----------|
| 1 | `.claude/references/agents/g5/detection-rules.md` | Add quantitative metrics section, add new S7-S10 categories, update scoring algorithm, add non-native speaker calibration | HIGH |
| 2 | `agents/g5.md` | Update agent prompt to include quantitative metrics calculation instructions and new pattern categories | MEDIUM |
| 3 | `.claude/references/agents/g5/structural-patterns.md` | **NEW FILE**: Detailed definitions and examples for S7-S10 | MEDIUM |
| 4 | `.claude/references/agents/g5/quantitative-metrics.md` | **NEW FILE**: Calculation methods for Burstiness, MTLD, Fano Factor | MEDIUM |

---

## Phase 2: G6 Transformation Upgrade (5 files)

| # | File | Changes | Complexity |
|---|------|---------|-----------|
| 5 | `agents/g6.md` | Add Layer 3 structural transformation instructions, add burstiness enhancement directives (enumeration dissolution, paragraph opener variation, discussion architecture, hypothesis narrative) | HIGH |
| 6 | `.claude/references/agents/g6/transformations/balanced.yaml` | Add structural transformation rules (S7-S10) | MEDIUM |
| 7 | `.claude/references/agents/g6/transformations/aggressive.yaml` | Add structural transformation rules (S7-S10) + add burstiness target values | MEDIUM |
| 8 | `.claude/references/agents/g6/transformations/structural.yaml` | **NEW FILE**: Dedicated structural transformation reference | HIGH |
| 9 | `.claude/references/agents/g6/academic-exceptions.md` | Add structural transformation exceptions (preserve IMRAD structure in Methods section) | LOW |

---

## Phase 3: Pipeline and Checkpoint Upgrade (3 files)

| # | File | Changes | Complexity |
|---|------|---------|-----------|
| 10 | `.claude/references/agents/research-coordinator/core/humanization-pipeline.md` | Replace single-pass architecture with iterative 3-pass architecture, add section-aware escalation | HIGH |
| 11 | `.claude/checkpoints/checkpoint-definitions.yaml` | Add CP_PASS1_REVIEW, CP_PASS2_REVIEW, CP_FINAL_REVIEW | LOW |
| 12 | `CLAUDE.md` | Update version to v8.1.0, document new pipeline features, update commands reference | MEDIUM |

---

## Phase 4: F5 Validator Upgrade (1 file)

| # | File | Changes | Complexity |
|---|------|---------|-----------|
| 13 | `agents/f5.md` | Add burstiness validation, add structural pattern checks, add cross-section coherence checks | MEDIUM |

---

## Priority Task List

| Rank | Priority | Task |
|------|----------|------|
| 1 | HIGHEST | Add S7-S10 structural detection categories to G5 (patterns causing 60% ceiling) |
| 2 | HIGH | Add Layer 3 structural transformations to G6 (enumeration dissolution, paragraph opener variation, discussion architecture, hypothesis narrative) |
| 3 | HIGH | Implement Burstiness CV metrics and add enhancement directives |
| 4 | MEDIUM | Build multi-pass iterative pipeline with inter-pass checkpoints |
| 5 | MEDIUM | Add MTLD vocabulary diversity metrics |
| 6 | LOW | Add non-native speaker calibration option |
| 7 | LOW | Add score target system with presets |

---

## Identified Gaps (From Architecture Analysis)

| # | Gap | Description |
|---|-----|-------------|
| 1 | Iterative Refinement Feedback Loop | No "retry with modified parameters" mechanism when F5 detects >10% unresolved patterns |
| 2 | Cross-Section Coherence Check | No validation of term consistency across sections after transformation |
| 3 | Discipline-Specific Calibration | Generic 24-pattern model applied to all fields; Psychology, Management may have different baseline values |
| 4 | Custom Preservation Lists | Users cannot protect domain-specific terminology without code modification |
| 5 | Before/After Diff Visualization | No visual side-by-side highlighting of changes |
| 6 | AI Pattern Recovery Detection | G6 may introduce new AI patterns while removing existing ones; full G5 re-scan needed post-transformation |
| 7 | Hedge Appropriateness Calibration | No validation that remaining hedges match evidence strength |

---

## Expected Outcomes

- Manual intervention frequency: Reduced from 3 manual rounds to 2 automated passes
- AI detection score: Achieve <30% without manual structural editing
- Measure and optimize: Burstiness CV > 0.45, MTLD > 70
- Citation and statistics: 100% preservation (no regression)
- Provide objective, quantitative metrics for each humanization pass
- Support non-native English speakers with calibrated detection thresholds

---

## Validation Plan

| Stage | Content |
|-------|---------|
| 1 | Prepare original (pre-humanization) versions of Paper 1 and Paper 2 |
| 2 | Run upgraded pipeline (target: 30%) |
| 3 | Metrics: Required passes, final score, burstiness CV, MTLD, citation/statistics integrity |
| 4 | Compare with Round 3 manual results (Paper 1: 31%, Paper 2: 22%) |
| 5 | Success criteria: Achieve <30% with ≤2 automated passes while preserving 100% integrity |

---

## File Structure Reference

```
/Users/hosung/.claude/plugins/diverga/
├── CLAUDE.md                                                          # Update to v8.1.0 (modified)
├── agents/
│   ├── g5.md                                                          # G5 agent definition (modified)
│   ├── g6.md                                                          # G6 agent definition (modified)
│   └── f5.md                                                          # F5 validator definition (modified)
└── .claude/
    ├── checkpoints/
    │   └── checkpoint-definitions.yaml                                # Checkpoint definitions (modified)
    └── references/
        └── agents/
            ├── g5/
            │   ├── detection-rules.md                                 # Detection algorithm (modified)
            │   ├── structural-patterns.md                             # S7-S10 pattern definitions (new)
            │   └── quantitative-metrics.md                            # Quantitative metrics calculation (new)
            ├── g6/
            │   ├── academic-exceptions.md                             # Preservation rules (modified)
            │   └── transformations/
            │       ├── balanced.yaml                                  # Balanced mode rules (modified)
            │       ├── aggressive.yaml                                # Aggressive mode rules (modified)
            │       └── structural.yaml                                # Structural transformation reference (new)
            └── research-coordinator/
                └── core/
                    └── humanization-pipeline.md                       # Pipeline architecture (modified)
```

---

## Related Repositories

- **Research Project**: https://github.com/HosungYou/AI_Polarization_Pew
- **Humanizer Documentation**: https://github.com/HosungYou/humanizer
