# Diverga Humanization Pipeline Upgrade Research

## Overview

This repository is a separate documentation repository that preserves research discussions and improvement proposals for the Diverga humanization pipeline upgrade. It is not included in the global Diverga deployment, and documents insights and recommendations derived from analyzing structural limitations of the pipeline and designing next-generation architecture.

---

## Research Background

During the humanization of two academic papers, structural limitations were identified in the current G5→G6→F5 pipeline.

### Target Papers

| Paper | Topic | Target Journal | Impact Factor (IF) |
|-------|-------|-----------------|-------------------|
| Paper 1 | Occupational Identity Threat | TFSC (Technological Forecasting and Social Change) | ~12.0 |
| Paper 2 | Epistemic Cognition | IJAIED (International Journal of AI in Education) | ~4.7 |

### Score Progression

Both papers required three rounds of manual intervention to reach acceptable AI detection scores.

**Paper 1 (TFSC):**

| Round | AI Detection Score |
|-------|-------------------|
| Round 1 | 80% |
| Round 2 | 62% |
| Round 3 | 31% |

**Paper 2 (IJAIED):**

| Round | AI Detection Score |
|-------|-------------------|
| Round 1 | 82% |
| Round 2 | 61% |
| Round 3 | 22% |

### Key Findings

The breakthrough in Round 3 was achieved through deep structural deconstruction. In this process, it became clear that after vocabulary cleanup, **structural patterns rather than words** are the primary AI detection signals.

---

## Repository Structure

```
humanizer/
├── README.md                      # This document. Summary of research background and key findings.
├── article/                       # Research discussions and analysis documents
│   └── (paper-by-paper analysis, round-by-round improvement records, etc.)
└── roadmap/                       # Pipeline upgrade roadmap documents
    └── (G5 v2.0, G6 v2.0, iterative pipeline design proposals, etc.)
```

---

## Key Findings

### 1. Limitations of G6's Vocabulary-Level Transformation

The current G6 agent's word/phrase-level transformation reaches a ceiling at approximately 60% AI detection rate after vocabulary cleanup. Meaningful reduction in detection rates cannot be achieved through vocabulary replacement alone.

### 2. Structural Patterns as Primary Detection Signals

After vocabulary cleanup, the primary signals detected by AI detectors are structural fingerprints:

- **Enumeration Fingerprints**: First/second/third structures, parallel listing patterns
- **Formulaic Paragraph Architecture**: Uniform paragraph structure with topic sentence, development, and conclusion
- **Hypothesis Checklists**: AI-specific hypothesis presentation and verification order
- **Uniform Sentence Length**: Artificial uniformity in sentence length distribution

### 3. Three-Axis Upgrade Proposal

To overcome the identified limitations, we propose the following three-axis upgrade:

| Axis | Component | Description |
|------|-----------|-------------|
| Axis 1 | Enhanced Detection (G5 v2.0) | Introduction of metrics that quantitatively measure structural fingerprints alongside vocabulary cleanup |
| Axis 2 | Structural Transformation (G6 v2.0) | Addition of Layer 3 (structural deconstruction layer) to vocabulary transformation to restructure paragraph architecture itself |
| Axis 3 | Iterative Pipeline | Transition from single-pass pipeline to multi-pass structure with feedback loops |

---

## Related Links

- **Diverga Plugin**: https://github.com/HosungYou/Diverga
- **AI_Polarization_Pew**: [https://github.com/HosungYou/AI_Polarization_Pew](https://github.com/HosungYou/AI_Polarization_Pew)

---

## Copyright and Author Information

All content in this repository is created for the purpose of preserving research records. Unauthorized reproduction and distribution are prohibited.

Author: Hosung You
Start Date: February 2026
