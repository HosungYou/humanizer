# Round 3 Deep Structural Deconstruction Strategy

## 1. Background: Why Round 3 Was Necessary

The humanization effort applied to two academic manuscripts turned out to be far more complex than anticipated. Paper 1 ("The Politicization of Workforce Futures" — Occupational Identity Threat framework, target journal TFSC IF ~12.0) and Paper 2 ("Beyond the Information Deficit" — Epistemic Cognition framework, target journal IJAIED IF ~4.7) both opened with AI detection scores above 80%, and after two rounds of G6-based humanization, both stalled in the 60% range.

**Score progression by round:**

- Paper 1: 80% (Round 1, original) → 62% (Round 2, G6 humanization) → 31% (Round 3, manual structural deconstruction)
- Paper 2: 82% (Round 1, original) → 61% (Round 2, G6 humanization) → 22% (Round 3, manual structural deconstruction)

A clear pattern emerged by the end of Round 2. G6's vocabulary substitution and surface-level pattern modification were effective at pulling scores down from the 80s into the 60s, but could not push them any lower. Both papers hit a ceiling at roughly 60%.

Root cause analysis made it clear that the remaining detection signals originated not from word-level vocabulary but from **structural patterns**. G6's transformation rules operate at the word and phrase level; they cannot touch document-level structural characteristics such as paragraph architecture, enumeration logic, and section-opening templates. The 60% scores that persisted after vocabulary refinement were coming entirely from these structural patterns.

The decision was therefore made to abandon the G6-dependent approach entirely and proceed with Round 3: a manual structural deconstruction of both manuscripts.

---

## 2. Pre-Round 3 State Analysis

### Paper 1 (Occupational Identity Threat — TFSC)

State of Paper 1 at the close of Round 2:

- AI detection probability: **62%**
- Risk level: **MEDIUM**
- Remaining pattern count: **24**

Primary issues identified in the G5 audit:

- **Numbered enumeration of "3 contributions" and "4 recommendations"**: The structure of listing contributions and recommendations as numbered items persisted within running prose
- **Formulaic Discussion opener**: Discussion began with a summary restatement of the form "The present study examined..." — a textbook AI pattern
- **H1–H5 checklist pattern**: Hypothesis verification results were presented mechanically in the format "H1 was supported. H2 was partially supported."
- **Uniform sentence length**: Most sentences fell within the 25–45 word range, producing low burstiness
- **Repetitive paragraph openers**: Consecutive paragraphs began with "The [X]..." constructions

### Paper 2 (Epistemic Cognition — IJAIED)

State of Paper 2 at the close of Round 2:

- AI detection probability: **61%**
- Risk level: **MEDIUM-HIGH**
- Remaining pattern count: **29**

Primary issues identified in the G5 audit:

- **"nuanced" appearing 5 times**: A Tier 2 AI signature word that G6 failed to eliminate entirely
- **"illuminate" persisting**: Part of the AI-characteristic copula avoidance pattern
- **Enumeration patterns**: Argumentation remained trapped within numbered-list architecture
- **Hypothesis results presented as a checklist**: Verification outcomes for H1 through H5 were handled as a sequential list summary

---

## 3. Seven Strategies Applied

### 3.1 Enumeration Dissolution

One of the most detectable structural fingerprints in AI-generated text is numbered enumeration embedded within prose. Ordinal markers such as "First,...Second,...Third,..." are something human academic writers naturally avoid when composing in the flow of thought, whereas LLMs use them as a default output pattern.

Round 3 eliminated this pattern entirely. Specifically:

- All "First,...Second,...Third,..." patterns were dissolved into natural narrative flow
- Ordinal markers were removed completely, with logical connections replaced by concrete connectors and cause-effect links
- Briefly enumerated items were merged into compound sentences
- Transitional devices were diversified to eliminate predictability

This strategy produced the most immediate and largest impact on detection scores. Paper 1's "3 contributions" structure and "4 recommendations" structure were both dismantled by this method, and Paper 2's main argumentation was rebuilt from enumerated structure into narrative continuity.

### 3.2 Discussion Opener Rewrite (Compelling Hooks)

The first sentence of a Discussion section carries elevated weight in AI detection (section multiplier: 1.1). An opener of the form "The present study examined..." or "This paper investigated..." is a textbook instance of G5 Pattern A5 (Discussion Formula) and closely mirrors how AI systems begin a Discussion section.

In Round 3, Discussion openers were replaced with questions, presentations of unexpected findings, or provocative framing. An actual example from the manuscripts:

**Before:**
> "The present study examined political determinants of AI concern among U.S. adults..."

**After:**
> "Why do Democrats and Republicans — who agree on almost nothing — both worry about AI at nearly identical rates?"

This approach draws readers in immediately while stepping entirely outside the formulaic patterns that detectors look for. It also restores the author's intellectual voice. AI-generated text rarely expresses surprise or intellectual curiosity about its own findings, and that absence itself functions as a detection signal.

### 3.3 Hypothesis Narrative

The mechanical listing of hypothesis test results is a structural pattern that triggers particularly strong responses from AI detectors. The form "H1 was supported (p < .001). H2 was partially supported. H3 was not supported." corresponds to G5's newly added pattern category S10 (Hypothesis Checklist Pattern).

The transformation approach:

- Group related findings thematically and integrate them into a narrative arc
- Use specific numbers and effect sizes as anchors within the narrative
- Position surprising non-findings so they naturally generate discussion

**Before:**
> "H1 was supported. H2 was partially supported. H3 was not supported."

**After:**
> "The partisan divide we predicted materialized clearly — Republicans were 14 percentage points more likely to express concern (AME = 0.14, p < .001). But the education gradient surprised us..."

This approach preserves 100% statistical accuracy (meeting F5 verification criteria) while fully dismantling the structural pattern.

### 3.4 Concrete Scenarios

Another characteristic of AI-generated academic text is the dominance of abstract description. Human authors naturally insert concrete examples or scenarios to aid reader comprehension, whereas LLMs tend to repeatedly chain general statements to citation-based evidence.

In Round 3, the following concrete scenarios were introduced:

- **Manufacturing firm scenario**: In Paper 1's Occupational Identity Threat discussion, the threat AI adoption poses to the occupational identity of skilled manufacturing workers was grounded in a specific manufacturing context
- **Hospital radiology scenario**: In the discussion of workplace AI impacts, the restructuring of radiologists' roles through AI-based imaging diagnosis was presented through a concrete hospital scenario

These scenarios make abstract findings tangible and allow readers to understand research results within a real-world context. A secondary effect is that concrete scenarios break the homogeneous abstraction that AI detectors use as a signal.

### 3.5 Dramatic Sentence Length Variation

One of the core signals used by GPTZero and other major AI detectors is burstiness. Burstiness is measured by the Coefficient of Variation of sentence length (CV = standard deviation of sentence lengths / mean); human-written text typically shows CV > 0.45, while AI-written text typically shows CV < 0.30.

Text through Round 2 had most sentences distributed in the 25–45 word range, resulting in low CV. Round 3 addressed this as follows:

- Two-word declarative sentences ("That gap is real.") were deliberately inserted at moments of impact
- One or two complex sentences per section were expanded to reach 40–60 words
- Mid-length sentences in the 15–25 word range were split toward shorter or longer forms
- Sentence fragments were used strategically for emphasis
- Paragraph length was alternated between 2-sentence and 6-sentence paragraphs to increase variability

The goal was to push burstiness CV above 0.45. This change directly affects AI detectors while simultaneously improving readability and rhetorical impact.

### 3.6 Removal of Residual LLM Signature Expressions

Several LLM signature expressions survived Round 2 without being eliminated by G6. Round 3 involved manually identifying and removing each one:

| Expression Removed | Frequency | Treatment |
|---|---|---|
| "This study is among the first" | 1 occurrence (Paper 1) | Deleted entirely |
| "nuanced" | 6 occurrences (Paper 2) | All removed or replaced with specific expressions |
| "emerging" | 4 occurrences (Paper 1) | All removed or replaced with specific expressions |
| "it seems" | 1 occurrence (Paper 2) | Deleted entirely |
| "The analysis presented here" | 3 occurrences (Paper 2) | Replaced with "We" constructions |

"nuanced" and "emerging" in particular are classified as G5 Tier 2 vocabulary; in G6's Balanced mode, transformations are applied only when clustering is detected. Each appears to have been passed through when occurring in isolation, and a manual audit achieved complete removal.

The "The analysis presented here" → "We" conversion carries significance beyond a simple expression swap. The shift from passive distancing to an active authorial voice raises authorial presence throughout the text, improving the human-authorship indicators that detectors measure.

### 3.7 Post-Audit Micro-Fixes

Following the major structural interventions of Round 3, a re-audit using G5 was conducted. Micro-fixes were then applied to residual patterns surfaced by that audit.

**Paper 1 micro-fixes:**

- The formulaic Limitations section opener ("Several limitations warrant acknowledgment, and they range from...") was removed and rewritten
- Double-hedging on FDR correction was corrected — excessive qualification of statistical methods corresponds to AI detection Pattern H2
- Consecutive "The [X]..." paragraph openers in the Results section were diversified

**Paper 2 micro-fixes:**

- "it seems" (near line 250) was removed
- Three instances of "The analysis presented here" were converted to "We" constructions
- "offers a promising" was replaced with a more assertive expression

This micro-fix stage contributed to driving Paper 2's score down to 22%. Without these micro-fixes, the score would likely have remained at the 25–27% level.

---

## 4. Results: Paper 1 Before and After

| Metric | Round 2 (Before) | Round 3 (After) | Change |
|--------|-----------------|-----------------|--------|
| AI probability | 62% | 31% | -31pp |
| Risk level | MEDIUM | LOW | 2-level drop |
| Pattern count | 24 | 7 | -17 (-71%) |

For Paper 1, the drop in risk level from MEDIUM to LOW means that the realistic possibility of AI-assisted writing suspicion arising during journal review has been effectively eliminated. Under G5's scoring classification, 31% falls within the "Moderate / Mixed Signals" band, where AI detection tools operating within typical precision ranges cannot reliably distinguish the text from human writing.

---

## 5. Results: Paper 2 Before and After

| Metric | Round 2 (Before) | Round 3 (After) | Change |
|--------|-----------------|-----------------|--------|
| AI probability | 61% | 22% | -39pp |
| Risk level | MEDIUM-HIGH | LOW | 3-level drop |
| Pattern count | 29 | 4 | -25 (-86%) |

Paper 2 showed more dramatic improvement than Paper 1. The -39pp reduction was the largest single-round gain in Round 3, and 22% falls within G5's "Low / Likely Human" band. The reduction of pattern count from 29 to 4 demonstrates that structural deconstruction delivers far higher efficiency per unit than vocabulary substitution.

---

## 6. Overall Score Trajectory

| Paper | Round 1 (Original) | Round 2 (G6 Humanization) | Round 3 (Manual Structural Deconstruction) |
|-------|-------------------|--------------------------|-------------------------------------------|
| Paper 1 (TFSC) | 80% HIGH, 34 patterns | 62% MEDIUM, 24 patterns | **31% LOW, 7 patterns** |
| Paper 2 (IJAIED) | 82% HIGH, 36 patterns | 61% MEDIUM-HIGH, 29 patterns | **22% LOW, 4 patterns** |

Key relationships evident in the full trajectory:

- **Round 1 → Round 2**: Driven by vocabulary substitution. Average reduction of -19.5pp, 10–12 patterns removed. Efficient but with a low ceiling.
- **Round 2 → Round 3**: Driven by structural deconstruction. Average reduction of -35pp, 17–25 patterns removed. More than twice the impact of vocabulary work.
- **Ceiling effect confirmed**: Both manuscripts stalled at 60–62% after Round 2. This clearly demonstrates the limits of word-level intervention.

---

## 7. Six Core Patterns Identified

Round 3 work made the structural sources of AI detection signals that persist after vocabulary refinement clearly visible.

**1. Structural Regularity**

AI-generated academic text follows a predictable paragraph structure: topic sentence → citation evidence → interpretive synthesis → transition. When this structure repeats across an entire document, detectors recognize it as a structural fingerprint. Human authors execute the same argument move in varied ways, whereas LLMs repeat the same structure.

**2. Enumeration Fingerprint**

Numbered lists embedded in prose (First,...Second,...Third,...) are structurally persistent and cannot be removed through word-level paraphrasing. Even if ordinal markers are changed, the structural pattern of list-logic argumentation remains. The only solution is to fully dissolve enumeration and integrate it into natural narrative.

**3. Hypothesis Checklist Pattern**

The mechanical hypothesis confirmation sequence — "H1 was supported. H2 was partially supported. H3 was not supported." — is classified as G5's new Pattern S10. This pattern serves to list results, but its structure is fundamentally different from how human authors write results. Human authors weave related findings together thematically and give unexpected outcomes dedicated narrative space.

**4. Formulaic Section Openers**

The pattern of Discussion sections consistently beginning with a restatement of the study summary is the core of G5 Pattern A5 (Discussion Formula). The reason AI detectors apply a 1.1 multiplier to Discussion sections is precisely that AI-characteristic formulaic structure is especially pronounced in this section. Opening with a provocative question or the presentation of an unexpected finding dismantles this pattern.

**5. Sentence Length Uniformity**

A sentence length distribution concentrated in the 25–45 word range generates low burstiness CV. GPTZero uses this alongside perplexity as two of the primary signals for AI detection. Human authors naturally mix very short sentences (3–5 words) with complex long sentences (30–50 words), whereas LLMs tend to consistently produce sentences of intermediate complexity.

**6. Paragraph Opener Repetition**

The pattern of consecutive paragraphs beginning with "The [X]..." constructions corresponds to G5's new Pattern S8 (Repetitive Paragraph Openers). Human authors begin paragraphs in varied ways: questions, numerical presentation, transitional clauses, counterarguments, adverbial clauses, and more. AI favors noun-phrase openings, and their repetition forms a structural fingerprint.

---

## 8. Lessons Learned and Implications

### Vocabulary modification is necessary but not sufficient

The Round 1 and Round 2 experience confirmed that vocabulary substitution is effective at bringing scores down from the 80s to the 60s. But it cannot push them below 60%. Vocabulary modification can eliminate roughly half of the signals that detectors capture. The other half resides in structure.

### Structural transformation is the breakthrough

Round 3 proved that structural transformation is the true breakthrough. The leap from the 60s to below 30% was achievable only through structural deconstruction after vocabulary refinement was complete. Of the seven strategies, enumeration dissolution, Discussion opener rewriting, and hypothesis narrativization contributed the most.

### Human intervention remains decisive

G6 succeeded in automating vocabulary-level transformation, but structural transformation requires the ability to understand the logical flow and rhetorical intent of an entire document. G6 currently lacks this capability. All structural deconstruction work in Round 3 was performed by a human, and that is what made the difference in scores.

### Detectors are increasingly capable of structural recognition

The most important implication is that AI detectors are evolving from vocabulary-centered to structure-centered analysis. Early detectors relied on lexical signatures such as "delve," "underscore," and "nuanced." However, tools like GPTZero, Originality.ai, and Turnitin now analyze burstiness, paragraph structure, enumeration patterns, and section-opener types. The assumption that vocabulary refinement alone is sufficient to evade detection is no longer valid.

### Direct implications for Diverga v2.0 upgrade direction

The Round 3 experience provided direct justification for the Diverga pipeline upgrade proposal. Upgrades are needed along three axes:

- **G5 v2.0**: Addition of structural pattern detection categories (S7–S10) and introduction of a quantitative metrics module including burstiness CV and MTLD
- **G6 v2.0**: Addition of Layer 3 (structural transformation) — enumeration dissolution, paragraph opener variation, Discussion architecture reconstruction, and hypothesis narrativization
- **Pipeline v2.0**: Transition from single-pass to multi-pass iterative architecture — a three-stage pipeline of Pass 1 (vocabulary), Pass 2 (structure), Pass 3 (polish)

Once this upgrade is complete, it is expected that work currently requiring three manual rounds can be completed in two automated passes. The target score is <30% (journal_safe preset).
