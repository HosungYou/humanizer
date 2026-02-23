# Diverga Humanization Pipeline Upgrade: AI Detection Evasion Strategy Through Structural Transformation

> **Version**: 1.0
> **Date**: 2026-02-22
> **Target System**: Diverga Plugin v8.0.1 (G5/G6/F5 Pipeline)
> **Related Repository**: [HosungYou/humanizer](https://github.com/HosungYou/humanizer)

---

## Table of Contents

1. [Background and Problem Recognition](#1-background-and-problem-recognition)
2. [Current Architecture Analysis (G5→G6→F5)](#2-current-architecture-analysis-g5g6f5)
3. [AI Text Detection Research Literature Review (2024-2026)](#3-ai-text-detection-research-literature-review-2024-2026)
4. [Three-Pillar Upgrade Proposal](#4-three-pillar-upgrade-proposal)
5. [Objective Metrics and Benchmarks](#5-objective-metrics-and-benchmarks)
6. [References](#6-references)

---

## 1. Background and Problem Recognition

### 1.1 3-Round Experience: The Humanization Process of Two Academic Papers

The experience of humanizing two academic papers using the Diverga pipeline (G5→G6→F5) served as the direct impetus for this upgrade. Both papers aimed to reduce AI detection scores to journal-submission-safe levels following LLM-assisted writing (AI-assisted writing).

**Target Papers:**

| Category | Paper 1 | Paper 2 |
|----------|---------|---------|
| **Title** | "The Politicization of Workforce Futures" | "Beyond the Information Deficit" |
| **Theoretical Framework** | Occupational Identity Threat | Epistemic Cognition |
| **Target Journal** | Technological Forecasting and Social Change (TFSC) | International Journal of AI in Education (IJAIED) |
| **Impact Factor** | ~12.0 | ~4.7 |

Both papers received a HIGH RISK determination in the initial G5 analysis:

| Metric | Paper 1 (Occupational Identity) | Paper 2 (Epistemic Cognition) |
|--------|--------------------------------|-------------------------------|
| **AI probability** | **80%** | **82%** |
| **Risk level** | HIGH | HIGH |
| **Pattern count** | 34 (HIGH 21, MEDIUM 12, LOW 1) | 36 (HIGH 24, MEDIUM 12) |

### 1.2 Score Progression

**Three manual rounds** were required to reach the LOW risk level:

| Paper | Round 1 | Round 2 | Round 3 (Final) |
|-------|---------|---------|-----------------|
| Paper 1 (TFSC) | 80% HIGH, 34 patterns | 62% MEDIUM, 24 patterns | **31% LOW, 7 patterns** |
| Paper 2 (IJAIED) | 82% HIGH, 36 patterns | 61% MEDIUM-HIGH, 29 patterns | **22% LOW, 4 patterns** |

Key observation: After Rounds 1-2 (G6 automated processing), scores dropped by approximately 20 percentage points before **hitting a ceiling around 60%**. The final breakthrough was only achievable through complete manual structural dismantling in Round 3.

### 1.3 Round-by-Round Gap Analysis

| Round | Strategy | Score Change | Work Performed by G6 | Work Performed Manually |
|-------|----------|-------------|----------------------|------------------------|
| **Round 1** | Vocabulary substitution | 80→62% | L1 tier1/tier2 vocabulary substitution | No additional work needed |
| **Round 2** | Surface pattern fixes | 62→~60% | C1, H1, H2 pattern processing | Minimal improvement — ceiling reached |
| **Round 3** | Deep structural dismantling | 60→31/22% | N/A (manual work) | Dismantled all enumeration structures, rewrote Discussion openers, narrativized hypothesis checklists, added concrete scenarios, introduced dramatic sentence length variation |

### 1.4 Root Cause Analysis

**G6 operates at the word/phrase level.** After vocabulary is cleaned up, the residual 60% detection signal originates from **structural patterns** that G6 cannot address.

The reasons high scores persist even after vocabulary substitution are as follows:

1. **Structural regularity** — Predictable paragraph structure (topic sentence → evidence → synthesis → transition)
2. **Enumeration fingerprint** — Numbered lists embedded within prose
3. **Hypothesis checklist pattern** — Mechanical H1/H2/H3 confirmation sequences
4. **Formulaic section openers** — Discussion always begins with a summary restatement
5. **Sentence length uniformity** — No variation within the 25-45 word range (low burstiness)
6. **Paragraph opener repetition** — Consecutive paragraphs beginning with "The [X]..."

### 1.5 Common Issues Found Across Both Papers (In Priority Order)

**Issue 1: LLM-Specific Expressions — Immediate Removal Required**

| Original Expression | Treatment |
|---------------------|-----------|
| "worth noting/emphasizing" | Delete or state directly |
| "Several patterns stand out" | Begin with specific content |
| "unprecedented challenge" | Begin with empirical data |
| "through the lens of" | Remove |
| "theoretically grounded" | Remove |
| "landscape" | Replace with specific context |
| "illuminate," "underscore," "emerge" | Replace with plain verbs |
| "precisely the kind of" | "this kind of" |

**Issue 2: Structural Problems**

- **Tricolon overuse**: 6 instances in Paper 1; 14 instances of "X rather than Y" pattern in Paper 2
- **Mechanical repetition in hypothesis summary sections**: "H1 supported, H2 supported..."
- **Excessive numbered lists**: "four gaps," "three findings," "five directions"
- **Identical paragraph structures**: topic sentence → citation → interpretation → transition

**Issue 3: Author Voice Absence**

- No first-person usage
- No expressions of intellectual surprise or questioning
- All findings treated as equally "expected"
- Discussion is a mere restatement of Results

**Issue 4: Monotonous Sentence Rhythm**

- Uniform sentence length within the 25-45 word range
- No short declarative sentences under 12 words
- Metronomic rhythm with no variation

---

## 2. Current Architecture Analysis (G5→G6→F5)

### 2.1 G5 — Academic Style Auditor (AI Pattern Detection)

| Attribute | Value |
|-----------|-------|
| **Agent ID** | G5 |
| **Category** | G - Publication & Communication |
| **VS Level** | Light |
| **Tier** | MEDIUM (Sonnet) |
| **Tools** | Read, Glob, Grep |
| **Basis** | 24 pattern categories from the Wikipedia AI Cleanup initiative |

#### 2.1.1 Detection Categories (24)

**Content Patterns (C1-C6)**

| Pattern | Risk | Target | Example |
|---------|------|--------|---------|
| C1: Significance Inflation | HIGH | Overclaimed importance | "groundbreaking", "revolutionary", "paradigm-shifting" |
| C2: Notability Claims | MEDIUM | Vague appeals to authority | "widely recognized", "well-established" |
| C3: Superficial -ing Constructions | MEDIUM | Indirect language | "highlighting the importance of", "demonstrating the value of" |
| C4: Promotional Language | HIGH | Marketing language | "impressive", "remarkable", "exciting", "cutting-edge" |
| C5: Vague Attributions | HIGH | Missing sources | "Studies show...", "Research demonstrates..." |
| C6: Formulaic Section Openings | LOW | Template language | "In conclusion", "It is worth noting" |

**Language Patterns (L1-L6)**

| Pattern | Risk | Target | Example |
|---------|------|--------|---------|
| L1: AI Vocabulary Clustering | HIGH | AI-typical vocabulary | Tier 1: delve, tapestry, intricacies, multifaceted, myriad, paramount, testament, embark, realm; Tier 2: landscape, underscore, pivotal, leverage, utilize, facilitate, foster, synergy, holistic, robust |
| L2: Copula Avoidance | MEDIUM | Elaborate replacements for "is/has" | "serves as", "stands as", "functions as", "boasts", "possesses" |
| L3: Negative Parallelism | LOW | Repetitive structures | "not only X but also Y" |
| L4: Rule of Three | MEDIUM | Artificial tripartite structures | Forcing 3 items when 2-4 exist |
| L5: Elegant Variation | LOW | Unnecessary synonym cycling | Alternating "study/research/investigation" |
| L6: False Ranges | MEDIUM | Artificial dichotomies | "from theory to practice", "local to global" |

**Style Patterns (S1-S6)**

| Pattern | Risk | Target | Example |
|---------|------|--------|---------|
| S1: Em Dash Overuse | MEDIUM | Excessive punctuation | Multiple — dashes per paragraph |
| S2: Excessive Boldface | LOW | Over-formatting | **Excessive** **emphasis** **text** |
| S3: Inline-Header Lists | MEDIUM | Artificial enumeration | "First, ... Second, ... Third, ..." |
| S4: Title Case Overuse | LOW | Excessive capitalization | "The Importance Of This Finding" |
| S5: Emoji Usage | HIGH | Non-academic markers | Emojis within academic text |
| S6: Curly Quote Artifacts | LOW | Formatting inconsistency | Mixed quotation mark styles |

**Communication Patterns (M1-M3)**

| Pattern | Risk | Target | Example |
|---------|------|--------|---------|
| M1: Meta-Commentary | HIGH | AI self-reference | "As an AI language model...", "I hope this helps" |
| M2: Excessive Affirmation | HIGH | Chatbot residue | "Great question!", "Absolutely!", "Excellent point!" |
| M3: Apology Hedging | MEDIUM | Excessive politeness | "I apologize if...", "I hope you don't mind..." |

**Filler/Hedging Patterns (H1-H3)**

| Pattern | Risk | Target | Example |
|---------|------|--------|---------|
| H1: Verbose Phrases | MEDIUM | Wordy constructions | "in order to" → "to", "at this point in time" → "now" |
| H2: Excessive Hedging | MEDIUM | Over-hedging | "could potentially perhaps", "may possibly" |
| H3: Redundant Intensifiers | LOW | Contradictory emphasis | "very unique", "extremely essential" |

**Academic-Specific Patterns (A1-A6)**

| Pattern | Risk | Target | Example |
|---------|------|--------|---------|
| A1: Overclaiming | HIGH | Unsupported causal claims | Using causal language without evidence |
| A2: Underclaiming | LOW | Over-hedging clear findings | Excessive hedging |
| A3: Citation Clustering | LOW | Citation density | Multiple citations in a single sentence |
| A4: Methods Boilerplate | MEDIUM | Methodology templates | Generic methodology descriptions |
| A5: Discussion Formula | MEDIUM | Structural templates | Predictable structure of Limitations, Implications, Future |
| A6: Implications Inflation | HIGH | Overclaimed significance | "profound implications for society" |

#### 2.1.2 Vocabulary Tier System

**Tier 1 — High Alert (Always Flagged)**

```
delve, dive into, crucial, foster, intricate, intricacies
realm, landscape, multifaceted, comprehensive, underscore
noteworthy, meticulous, leverage, utilize, pivotal
embark, endeavor, unveil, unravel, intriguing, testimony, testament
```

Action: Transform in all modes (Conservative and above)

**Tier 2 — Moderate Alert (Flagged When Clustering)**

```
robust, streamline, facilitate, enhance, fundamental
substantial, significant, paramount, innovative
nuanced, sophisticated, compelling, profound
```

Action: Transform in Balanced mode and above

**Tier 3 — Context Check (Evaluated in Context)**

```
important, effective, relevant, appropriate
demonstrate, indicate, suggest, reveal
```

Action: Transform only in Aggressive mode

#### 2.1.3 Scoring Algorithm

```
AI_Probability = SUM(pattern_weight * frequency) / max_score * 100
```

**Pattern Weights (Base Weights):**

| Pattern ID | Base Weight | Category |
|------------|-------------|----------|
| C1 | 10 | Significance Inflation |
| C2 | 7 | Notability Claims |
| C3 | 6 | Superficial -ing |
| C4 | 10 | Promotional Language |
| C5 | 12 | Vague Attributions |
| C6 | 3 | Formulaic Sections |
| L1-tier1 | 15 | AI Vocabulary (high alert) |
| L1-tier2 | 8 | AI Vocabulary (moderate) |
| L1-cluster | 20 | AI Vocab Clustering Bonus |
| L2 | 8 | Copula Avoidance |
| L3 | 6 | Negative Parallelism |
| L4 | 4 | Rule of Three |
| L5 | 7 | Elegant Variation |
| L6 | 3 | False Ranges |
| S1 | 5 | Em Dash Overuse |
| S2 | 3 | Excessive Boldface |
| S3 | 6 | Inline-Header Lists |
| S4 | 2 | Title Case Overuse |
| S5 | 20 | Emoji Usage |
| S6 | 2 | Quote Inconsistency |
| M1 | 25 | Chatbot Artifacts |
| M2 | 30 | Knowledge Disclaimers |
| M3 | 10 | Sycophantic Tone |
| H1 | 2 | Verbose Phrases (per instance) |
| H2 | 8 | Hedge Stacking |
| H3 | 6 | Generic Conclusions |
| A1 | 4 | Abstract Template |
| A2 | 4 | Methods Boilerplate |
| A3 | 12 | Discussion Inflation |
| A4 | 15 | Citation Hedging |
| A5 | 3 | Contribution Enumeration |
| A6 | 3 | Limitation Disclaimers |

#### 2.1.4 Risk Classification

| Score Range | Risk Level | Label | Action |
|-------------|------------|-------|--------|
| 0-20 | Low | Likely Human | Optional review |
| 21-40 | Moderate | Mixed Signals | Recommended review |
| 41-60 | Elevated | Probably AI-Assisted | Review needed |
| 61-80 | High | Likely AI-Generated | Humanization recommended |
| 81-100 | Critical | Obviously AI | Humanization required |

#### 2.1.5 Section-Based Weighted Multipliers

| Section | Multiplier | Rationale |
|---------|------------|-----------|
| Abstract | 1.2 | Highest scrutiny intensity |
| Introduction | 1.1 | First impression matters |
| Literature Review | 1.0 | Some formality expected |
| Methods | 0.8 | Some template language acceptable |
| Results | 1.0 | Standard |
| Discussion | 1.1 | High scrutiny of claims |
| Conclusion | 1.1 | Final impression matters |
| Response Letter | 0.9 | Some formality expected |

#### 2.1.6 Clustering Detection

```python
# Vocabulary clustering
IF (tier1_words >= 2) OR (tier2_words >= 4):
    cluster_detected = True
    bonus_score = 20

# Within-paragraph clustering
IF (patterns_in_same_paragraph >= 3):
    paragraph_cluster = True
    bonus_score += 10 * (pattern_count - 2)
```

**Pattern Type Combination Bonuses:**

| Combination | Bonus |
|-------------|-------|
| Content + Language | +10 |
| Language + Style | +5 |
| Content + Communication | +15 |
| 3 or more categories | +20 |
| 4 or more categories | +30 |

#### 2.1.7 Density Calculations

```python
pattern_density = total_patterns / (word_count / 100)

IF pattern_density > 3:
    density_flag = "high"
    score_multiplier = 1.3
ELIF pattern_density > 2:
    density_flag = "moderate"
    score_multiplier = 1.1
ELSE:
    density_flag = "normal"
    score_multiplier = 1.0
```

#### 2.1.8 False Positive Mitigation

```python
IF text_is_from_established_academic_author:
    score *= 0.8  # Reduce suspicion

IF journal_has_strict_style_guide:
    exempt(S1, S2, S4)  # Style may be required

IF text_is_from_non_native_english_speaker:
    reduce_L1_weight_by(0.30)  # Some AI vocabulary overlaps with ESL patterns
```

#### 2.1.9 Confidence Calibration

```python
# score +/- confidence_margin
confidence_margin = 10  # Most texts
confidence_margin = 15  # Very short texts (<200 words)
confidence_margin = 5   # Long texts (>2000 words)
```

---

### 2.2 G6 — Academic Style Humanizer (Text Transformation)

| Attribute | Value |
|-----------|-------|
| **Agent ID** | G6 |
| **Category** | G - Publication & Communication |
| **VS Level** | Enhanced (3-Phase) |
| **Tier** | HIGH (Opus) |
| **Tools** | Read, Glob, Grep, Edit, Write |

#### 2.2.1 Transformation Modes

| Mode | Target | AI Probability Reduction | Text Change Rate | Suitable Use |
|------|--------|--------------------------|------------------|--------------|
| **Conservative** | HIGH-RISK only (C1,C4,C5,L1-T1,S5,M1,M2,A1,A6) | 20-35% | 5-15% | Journal submission |
| **Balanced** (default) | HIGH + MEDIUM-RISK | 35-50% | 15-30% | Most academic documents |
| **Aggressive** | All patterns | 50-70% | 30-50% | Blog/informal documents |

#### 2.2.2 HAVS 3-Phase Process (Humanization-Adapted Verbalized Sampling)

Standard VS (Verbalized Sampling) is a research decision-making tool for theory/methodology selection. Applying 5-Phase VS to text transformation causes a category error. HAVS is an adaptation of this approach:

| Aspect | Standard VS | HAVS |
|--------|------------|------|
| Purpose | Theory/methodology selection | Text transformation strategy |
| T-Score meaning | Typicality of theory | Typicality of transformation pattern |
| Number of phases | 5 phases (0-5) | 3 phases (0-2) |
| Creativity focus | Conceptual innovation | Natural expression |

**Phase 0: Transformation Context Collection**
- Collect G5 analysis results
- Identify target style (journal/conference/thesis/informal)
- Confirm user mode selection

**Phase 1: Modal Transformation Warning** (Warning when T > 0.7)

| Strategy | T-Score | Risk |
|----------|---------|------|
| Synonym substitution only | 0.9 | AI detectors have learned this |
| Sentence rearrangement only | 0.85 | Structure preserved; patterns persist |
| Passive/active voice conversion only | 0.8 | Inconsistent voice creates new patterns |

Recommendation: "Combine strategies for better camouflage"

**Phase 2: Differentiated Transformation Directions**

| Direction | T-Score | Strategy | Mode | Suitable Use |
|-----------|---------|----------|------|--------------|
| **A** | ~0.6 | Vocabulary + syntax substitution | Conservative | Journal submission |
| **B** (recommended) | ~0.4 | A + sentence recombination, flow improvement | Balanced | Most academic documents |
| **C** | ~0.2 | A+B + paragraph restructuring, style transfer | Aggressive | Informal documents |

#### 2.2.3 Detailed Transformation Rules

**Conservative Mode — word_map:**

```yaml
"delve": "examine"
"delve into": "examine"
"tapestry": "range"
"intricacies": "details"
"multifaceted": "complex"
"myriad": "many"
"plethora": "many"
"paramount": "essential"
"testament to": "evidence of"
"embark on": "begin"
"realm": "area"
```

**Balanced Mode — Additional Rules:**

```yaml
C2: "widely cited" → "cited [N] times"
    "well-established theory" → "[Author]'s [year] theory"
C3: "highlighting the importance of" → "[X] is important because"
    "demonstrating the value of" → "[Z] shows value by"
L2: "serves as" → "is"
    "stands as" → "is"
    "boasts" → "has"
    "possesses" → "has"
    "encompasses" → "includes"
S1: Em dash threshold: 2 per document; alternatives: parentheses, colons, commas, new sentences
S3: Convert inline-header lists to prose
H1: "in order to" → "to"
    "due to the fact that" → "because"
    "the majority of" → "most"
H2: "could potentially" → "may"
    "seems to suggest" → "suggests"
```

**Aggressive Mode — Additional Rules:**

```yaml
C6: Dismantle "First,...Second,...Third,..." templates into natural prose
L1: "delve" → "look at"
    "nuanced" → "subtle"
    "landscape" → "field"
    "synergy" → "teamwork"
L3: "not only... but also" → "both... and"
L5: Choose one term and use it consistently (no synonym cycling)
A1: "This paper aims to" → "We"
    "The present study investigates" → "We investigated"
A5: "This study makes three contributions. First,..." → Narrate contributions naturally
```

#### 2.2.4 Preservation Rules — Non-Negotiable, 100% Accuracy Required

Elements that must **never be modified** during transformation:

- **Citations**: (Author, year) format, DOIs, URLs, page numbers
- **Statistics**: p-values, effect sizes, confidence intervals, N values, means/standard deviations, test statistics, percentages, correlation coefficients, beta weights, odds ratios
- **Direct quotes**: Original text, block quotes, interview excerpts
- **Technical terminology**: Named theories, frameworks, methodologies
- **Proper nouns**: Author names, institutions, journals, conferences, databases
- **Acronyms**: All defined acronyms and field-standard abbreviations
- **Methodology specifics**: Tool names, software versions, scale anchors, reliability values

#### 2.2.5 Context-Dependent Preservation

```yaml
"significant":
  preserve: When used in p-value context
  transform: When used in the general sense of "important"

"robust":
  preserve: Statistical robustness (e.g., 'robust standard errors')
  transform: When used in the general sense of 'strong'

"framework":
  preserve: Named frameworks
  transform: General usage

"paradigm":
  preserve: Philosophy of science context
  transform: General sense of 'approach'
```

#### 2.2.6 Iterative Refinement

In Balanced/Aggressive modes, G6 applies an iterative loop (maximum 2 iterations):

1. Apply initial transformation strategy
2. Self-check the transformed text for new AI patterns
3. Verify: No new patterns, meaning preservation (>95% similarity), citation integrity (100%), statistical invariance (100%)
4. If issues found, remove self-generated AI patterns and refine

#### 2.2.7 Humanization Modules

**h-style-transfer**: Apply discipline-specific writing styles
- Education: Practice-oriented, accessible language
- Psychology: Human-centered, measurement-focused
- Management: Action-oriented, stakeholder-aware

**h-flow-optimizer**: Three-level prose flow optimization
- Sentence level: Length/complexity variation, opener diversity
- Paragraph level: Topic sentences, evidence flow, transitions
- Document level: Argument progression, section balance

---

### 2.3 F5 — Humanization Verifier (Quality Assurance)

| Attribute | Value |
|-----------|-------|
| **Agent ID** | F5 |
| **Category** | F - Quality Assurance |
| **Tier** | LOW (Haiku) |

#### 2.3.1 Five Verification Checks

**1. Citation Integrity Check** (CRITICAL — Automatic rejection on failure)
- Citation count matches before/after transformation
- Format preserved: (Author, year)
- Content accuracy: Citation text unchanged
- Placement logic intact

**2. Statistical Accuracy Check** (CRITICAL — Automatic rejection on failure)
- p-values: Exact match
- Effect sizes: Unchanged (d, r, eta-squared)
- Sample sizes: N unchanged
- Test statistics: t, F, chi-squared unchanged
- Percentages: All % unchanged
- Confidence intervals: All CIs unchanged

**3. Meaning Preservation Check** (MAJOR — Review flagged)
- Key findings preserved
- Conclusions unchanged
- Methodology description accurate
- No new causal language added
- Hedging appropriateness verified
- Target: >=95% semantic similarity

**4. AI Pattern Reduction Check**
- Confirm AI probability reduction
- Minimum 20% reduction expected
- Confirm target patterns resolved
- Warning if <20% reduction

**5. Academic Tone Check**
- Formality level appropriateness
- Objectivity maintained
- Technical precision maintained
- Voice consistency

#### 2.3.2 Strictness Levels

| Level | Description |
|-------|-------------|
| Low | Basic checks only |
| Medium (default) | Full verification |
| High | Deep context analysis, tone consistency, compliance checks |

---

### 2.4 Full Pipeline Flow Diagram

```
Stage 1: Content Generation (G2-AcademicCommunicator / G3-PeerReviewStrategist / Auto-Doc)
    |
    v
Stage 2: Analysis (G5-AcademicStyleAuditor)
    |-- 24 pattern category detection
    |-- AI probability calculation
    |-- Risk level classification
    |-- Recommendation generation
    |
    v
CHECKPOINT: CP_HUMANIZATION_REVIEW (Recommended)
    "AI patterns detected. Humanize?"
    [A] Conservative [B] Balanced [C] Aggressive [D] View Report [E] Skip
    |
    v
Stage 3: Transformation (G6-AcademicStyleHumanizer, using HAVS 3-Phase)
    |-- Phase 0: Context collection
    |-- Phase 1: Modal warning
    |-- Phase 2: Direction selection (CP_HAVS_DIRECTION)
    |-- Iterative refinement (B/C modes)
    |
    v
Stage 4: Verification (F5-HumanizationVerifier)
    |-- Citation integrity
    |-- Statistical accuracy
    |-- Meaning preservation
    |-- AI pattern reduction
    |-- Academic tone
    |
    v
CHECKPOINT: CP_HUMANIZATION_VERIFY (Optional)
    Review changes. [A] Approve [B] Review [C] Revert [D] Try different mode
    |
    v
Stage 5: Output (Export humanized content to Word/PDF)
    + Optional: AI Pattern Report Appendix
    + Optional: Transformation Audit Trail
```

### 2.5 Pipeline States (FSM)

```
idle → analyzing → awaiting_decision → transforming → verifying → (optional) awaiting_approval → complete
```

State transition diagram:

```
                   G5 starts       Results shown     User selects
   [idle] --------> [analyzing] --------> [awaiting_decision] --------> [transforming]
                                              |                              |
                                              | (Skip selected)             | G6 complete
                                              v                              v
                                          [complete]                    [verifying]
                                                                             |
                                                                             | F5 complete
                                                                             v
                                                                    [awaiting_approval]
                                                                             |
                                                                             | Approved
                                                                             v
                                                                        [complete]
```

### 2.6 Agent Communication Protocol

**G5 → G6**: G5 outputs a complete analysis report (24 patterns, probability, risk level). G6 receives this as the `g5_analysis` input parameter and incorporates it into its transformation strategy.

**G6 → F5**: G6 outputs the humanized text + transformation log (original/replacement pairs). F5 receives both the original and humanized versions to compare and verify integrity violations.

### 2.7 Auto-Activation Thresholds

```yaml
skip_if_below: 20%      # Skip if AI probability < 20%
recommend_if_above: 40%  # Recommend if > 40%
require_if_above: 70%    # Require review if > 70%
```

### 2.8 Ethics Note

> **"Humanization improves expression, not deception."**

**What humanization does:**
- Help express ideas naturally
- Remove robotic phrasing
- Improve readability while maintaining academic tone
- Remove obvious AI artifacts

**What humanization does not do:**
- Make AI usage "undetectable"
- Replace the need for AI disclosure
- Generate original ideas
- Replace human judgment
- Guarantee acceptance

---

## 3. AI Text Detection Research Literature Review (2024-2026)

> A detailed literature review is available in a separate document [research-literature-review.md](./research-literature-review.md). This section summarizes the key conclusions directly incorporated into the upgrade design.

### 3.1 Overview of Detection Approaches

Current AI text detection is broadly classified into three approaches:

| Approach | Principle | Representative Tools | Key Limitations |
|----------|-----------|---------------------|-----------------|
| **Perplexity-based** | Measures how much a language model is "surprised" by each token | GPTZero, DetectGPT | Model-dependent — text predictable for one model may not be for another |
| **Classifier-based** | Fine-tuned transformers trained on AI/human pairs | Originality.ai, Turnitin, Copyleaks, ZeroGPT | Training data bias, vulnerable to paraphrasing |
| **Watermarking-based** | Embeds statistical signals in token selection during generation | SynthID-Text (Google DeepMind) | Requires cooperation from the generating model, cannot detect retroactively |

### 3.2 Comparison of Major Commercial Detectors

| Tool | Claimed Accuracy | Independent Verification Results | False Positive Rate | Notes |
|------|------------------|----------------------------------|---------------------|-------|
| GPTZero | 99.3% | High on unmodified text; fails on translated content | 0.24% (claimed) | Misclassified all translated AI text as human |
| Originality.ai | 98-100% | Top performance across multiple benchmarks | Low | Optimal for long-form academic text |
| Turnitin AI | 92-100% | Misses ~15% of AI text | ~1% (claimed) | Multiple universities deactivating |
| Copyleaks | 90.7% | Best multilingual detection; ~1/20 false positives | ~5% | Strength in non-English AI text |
| ZeroGPT | Variable | Generally low accuracy | High | Free tier; low reliability |

### 3.3 Evidence-Based Key Conclusions (7)

Literature evidence directly incorporated into the upgrade design:

**1. No detector can be solely trusted for high-stakes decisions.**
Independent studies consistently report false positive rates of 10-27%, starkly contrasting vendor claims of 0.24-1%. At least 12 elite universities including Yale, Vanderbilt, Johns Hopkins, and Northwestern have deactivated AI detection.

**2. Paraphrasing is the most effective evasion method.**
DIPPER (Krishna et al., 2023) reduced DetectGPT detection from 70.3% to 4.6%. A 2025 adversarial paraphrasing study achieved an average 87.88% TPR reduction across 8 detectors.

**3. Burstiness and perplexity are the key quantitative signals.**
Burstiness (CV or Fano Factor) and per-sentence perplexity variance are the most practically measurable features. MTLD is the recommended metric for lexical diversity measurement.

**4. AI vocabulary signatures are specific and well-documented.**
A 2024 PubMed data analysis identified **454 AI-excess words**, with a sharp inflection point appearing in 2023-2024.

**5. Non-native speakers are systematically disadvantaged.**
Liang et al. (2023) found that **over 61%** of TOEFL essays were misclassified as AI by at least one detector. The most accurate detectors also show the strongest bias against non-native speakers.

**6. Structural fingerprints persist even after humanization.**
Discourse structure, paragraph architecture, and enumeration patterns survive paraphrasing more robustly than vocabulary. This is the cause of the 60% ceiling after Round 2.

**7. Watermarking is the only technically robust solution.**
However, it requires cooperation from LLM providers and cannot retroactively detect text generated without watermarking.

---

## 4. Three-Pillar Upgrade Proposal

### Overview

Synthesizing the 3-Round experience and literature review findings, simultaneous upgrades across three pillars are needed to overcome the limitations of the current pipeline:

| Pillar | Target Agent | Key Change | Problem Addressed |
|--------|-------------|------------|-------------------|
| **Pillar 1**: Detection Enhancement | G5 v2.0 | Add quantitative stylometric metrics, new pattern categories S7-S10 | Failure to detect structural patterns |
| **Pillar 2**: Structural Transformation | G6 v2.0 | Add Layer 3 structural transformation, burstiness enhancement | Operates only at word/phrase level |
| **Pillar 3**: Iterative Pipeline | Pipeline v2.0 | Multi-pass architecture, feedback loops | 60% ceiling of single-pass approach |

---

### Pillar 1: Detection Enhancement (G5 v2.0)

Extends detection accuracy and coverage by adding **quantitative stylometric metrics** to pattern-based detection.

#### 4.1.1 New Quantitative Metrics Module

**Research basis**: GPTZero uses perplexity + burstiness. MTLD is the only lexical diversity metric invariant to text length (McCarthy & Jarvis, 2010). Fano Factor >1 indicates human-like variance.

```yaml
quantitative_metrics:
  burstiness:
    method: "coefficient_of_variation"  # CV = SD(sentence_lengths) / Mean(sentence_lengths)
    human_baseline: ">0.45"
    ai_typical: "<0.30"
    weight_in_score: 15
    interpretation: |
      CV above 0.45 indicates human-like sentence length variation.
      CV below 0.30 suggests AI-typical uniform sentence length.
      AI prefers medium-length sentences (15-25 words),
      while humans mix short declarations (3-5 words) with long complex sentences (30-50 words).

  vocabulary_diversity:
    method: "MTLD"  # Measure of Textual Lexical Diversity (length-invariant)
    human_baseline: ">80"
    ai_typical: "<60"
    weight_in_score: 10
    interpretation: |
      MTLD is the mean length of sequential strings maintaining a TTR above a threshold.
      The only length-invariant lexical diversity metric validated by McCarthy & Jarvis (2010).
      AI text generally shows lower lexical diversity,
      particularly lacking contextual appropriateness in academic writing.

  sentence_length_range:
    method: "max_minus_min_word_count"
    human_baseline: ">25 word spread"
    ai_typical: "<15 word spread"
    weight_in_score: 5
    interpretation: |
      The difference in word count between the longest and shortest sentences in a document.
      Human-written text ranges widely from 2-word declarations to 60-word complex sentences.
      AI text concentrates in the 15-35 word range with a narrow spread.

  paragraph_opener_diversity:
    method: "unique_first_3_words / total_paragraphs"
    human_baseline: ">0.70"
    ai_typical: "<0.50"
    weight_in_score: 8
    interpretation: |
      The proportion of paragraphs whose first 3 words are unique.
      AI tends to generate repetitive paragraph openers such as
      "The results..." "The analysis..." "The findings..."
```

#### 4.1.2 New Detection Categories (S7-S10)

Based on patterns discovered manually in Round 3, four structural-level detection categories are added:

| New Pattern | ID | Weight | Description | Detection Criteria |
|-------------|-----|--------|-------------|-------------------|
| **Enumeration as Prose** | S7 | 12 | "First,...Second,...Third,..." within prose | 3 or more ordinal markers within paragraphs, not in explicit lists |
| **Repetitive Paragraph Openers** | S8 | 10 | 3 or more consecutive paragraphs with "The [X]..." pattern | Structural similarity of first 3 words in consecutive paragraphs |
| **Formulaic Section Structure** | S9 | 8 | Discussion template structure: restate → compare → implications → limitations → future | Predictable ordering of sub-structures within sections |
| **Hypothesis Checklist Pattern** | S10 | 10 | "H1 was supported. H2 was partially supported. H3 was not supported." | Mechanical enumeration of hypothesis confirmations |

**S7 Detection Logic Detail:**

```python
def detect_s7_enumeration(text):
    """Detect enumeration patterns within prose"""
    ordinal_markers = [
        r'\bFirst(?:ly)?,',
        r'\bSecond(?:ly)?,',
        r'\bThird(?:ly)?,',
        r'\bFourth(?:ly)?,',
        r'\bFifth(?:ly)?,',
    ]
    # Exclude explicit lists (bullet points, numbered lists)
    # Markers within same paragraph or consecutive paragraphs, not across distant paragraphs
    # Flag if 3 or more ordinal markers exist within prose
    pass
```

**S8 Detection Logic Detail:**

```python
def detect_s8_repetitive_openers(paragraphs):
    """Detect repetitive paragraph openers"""
    first_words = [get_first_n_words(p, 3) for p in paragraphs]
    # Extract "The [noun]..." patterns
    # Calculate structural similarity (POS tag-based)
    # Flag if 3 or more consecutive paragraphs share the same pattern
    # Example: "The results...", "The analysis...", "The findings..."
    pass
```

#### 4.1.3 Updated Scoring Algorithm

**Current algorithm:**

```
AI_Probability = SUM(pattern_weight * frequency) / max_score * 100
```

**Proposed composite score:**

```
AI_Probability = (0.60 * pattern_score)
              + (0.20 * burstiness_penalty)
              + (0.10 * vocab_diversity_penalty)
              + (0.10 * structural_penalty)
```

Calculation of each component:

```python
# pattern_score: Current G5 algorithm (normalized 0-100)
pattern_score = current_g5_algorithm(text)  # normalized 0-100

# burstiness_penalty: Penalty when CV falls below human baseline (0.45)
burstiness_penalty = max(0, (0.45 - CV) / 0.45 * 100)
# CV > 0.45: 0 (no penalty)
# CV = 0: 100 (maximum penalty)
# CV = 0.30: approximately 33 (moderate penalty)

# vocab_diversity_penalty: Penalty when MTLD falls below human baseline (80)
vocab_diversity_penalty = max(0, (80 - MTLD) / 80 * 100)
# MTLD > 80: 0 (no penalty)
# MTLD = 0: 100 (maximum penalty)
# MTLD = 60: 25 (moderate penalty)

# structural_penalty: S7-S10 weighted scores (normalized 0-100)
structural_penalty = normalize_0_100(
    S7_weight * S7_count +
    S8_weight * S8_count +
    S9_weight * S9_count +
    S10_weight * S10_count
)
```

**Weight Allocation Rationale:**

| Component | Weight | Rationale |
|-----------|--------|-----------|
| pattern_score | 0.60 | Preserves proven detection power of existing 24 patterns |
| burstiness_penalty | 0.20 | Strongest quantitative signal in the literature (GPTZero's core metric) |
| vocab_diversity_penalty | 0.10 | MTLD is a complementary signal but varies by discipline |
| structural_penalty | 0.10 | New category; start conservatively, adjust after validation |

#### 4.1.4 Non-Native Speaker Calibration

**Research basis**: Liang et al. (2023) found that over 61% of TOEFL essays were misclassified as AI. Non-native academic English naturally exhibits lower lexical diversity and more regular sentence patterns, which overlap with AI characteristics.

```yaml
non_native_calibration:
  enabled: false  # User opt-in (disabled by default)
  adjustments:
    L1_weight: "x 0.7"    # 30% reduction in vocabulary flags
    H1_weight: "x 0.8"    # 20% reduction in verbose phrase flags
    burstiness_threshold: "0.35"  # Lower non-native baseline (0.45 → 0.35)
  rationale: >
    Non-native academic English naturally exhibits lower lexical diversity
    and more regular sentence patterns. This calibration prevents these
    natural characteristics from being misclassified as AI usage.
  activation: >
    User sets the --non-native flag when running G5 or specifies
    non_native_mode: true in the pipeline configuration.
```

---

### Pillar 2: Structural Transformation (G6 v2.0)

Adds **deep structural transformation capabilities** beyond word/phrase substitution.

#### 4.2.1 New Transformation Layer: Layer 3 — Structural Transformation

The current G6 operates at two layers:
- **Layer 1**: Word substitution (L1 vocabulary → alternatives)
- **Layer 2**: Phrase restructuring (H1 verbose → concise, C1 inflated → neutral)

**Layer 3 to be added: Structural Transformation** — operates at the paragraph/section level:

---

**S7 Enumeration Dissolution: Converting enumeration structures into flowing prose**

Before:
```
First, education significantly predicted AI concern. Second, partisan
identity showed the strongest association. Third, age interacted with
awareness to shape attitudes.
```

After:
```
Education emerged as a reliable predictor of AI concern, but partisan
identity dwarfed its effect -- a finding that persisted even after
adjusting for demographic covariates. Age told a more complicated story,
one that depended heavily on whether respondents had heard of ChatGPT
before the survey.
```

Transformation principles:
- Complete removal of ordinal markers (First, Second, Third)
- Replace with causal/contrastive connectives ("but", "one that", "even after")
- Explicitly express semantic relationships between findings
- Introduce sentence length variation

---

**S8 Paragraph Opener Variation: Diversifying repetitive paragraph openers**

Before:
```
The results for education...
The partisan gap...
The interaction between age and awareness...
The Blinder-Oaxaca decomposition...
```

After:
```
Education's role proved more nuanced than a simple linear gradient...
What explains the partisan gap? Not demographics alone...
Age and awareness interacted in ways that complicate...
Decomposing the partisan gap revealed something unexpected...
```

Transformation principles:
- Introduce paragraphs beginning with questions
- Use possessive/adjectival constructions ("Education's role")
- Use gerund phrases ("Decomposing the partisan gap")
- Introduce foreshadowing/surprise expressions ("something unexpected")
- Mix at least 4 different grammatical structures for paragraph openers

---

**S9 Discussion Architecture: Dismantling formulaic Discussion structure**

Before:
```
The present study examined... Our findings are consistent with...
```

After:
```
Why do Democrats and Republicans -- who agree on almost nothing -- both
worry about AI at nearly identical rates?
```

Transformation principles:
- Begin with a provocative question or surprising finding instead of summary restatement
- Frame in a way that challenges the reader's intuition
- Enter immediately with specific numbers or cases
- Remove self-referential openers like "The present study..."

---

**S10 Hypothesis Narrative: Converting hypothesis confirmation checklists into narrative**

Before:
```
H1 was supported (p < .001). H2 was partially supported. H3 was not
supported.
```

After:
```
The partisan divide we predicted materialized clearly -- Republicans were
14 percentage points more likely to express concern (AME = 0.14,
p < .001). But the education gradient surprised us...
```

Transformation principles:
- Remove H1/H2/H3 labels
- Use specific numbers (effect sizes, AMEs) as narrative anchors
- Create intellectual tension with unexpected results ("surprised us")
- Group related hypotheses by theme
- Preserve statistics 100% while changing only the narrative style

#### 4.2.2 Burstiness Enhancement Instructions

```yaml
burstiness_enhancement:
  description: "Intentionally vary sentence length to increase CV"
  target_cv: ">0.45"
  strategies:
    - strategy: "Insert short declarations"
      detail: "Insert 2-5 word declarative sentences at impact points"
      example: '"That gap is real." / "The data say otherwise."'

    - strategy: "Allow long complex sentences"
      detail: "Allow 1-2 sentences of 40-60 words per section"
      example: "Extended sentences using subordinate clause chains and parentheticals"

    - strategy: "Break up medium-length sentences"
      detail: "Break 15-25 word sentences into shorter or longer forms"
      example: "Intentional restructuring to break uniform rhythm"

    - strategy: "Strategic use of sentence fragments"
      detail: "Strategically use sentence fragments for emphasis"
      example: '"Not even close." / "A pattern worth noting."'

    - strategy: "Vary paragraph length"
      detail: "Alternate between 2-sentence and 6-sentence paragraphs"
      example: "Alternating short impact paragraphs with detailed analysis paragraphs"
```

**Target sentence length distribution:**

```
Ideal distribution to achieve target CV > 0.45:
  - Very short sentences (2-8 words):   ~10-15%
  - Short sentences (9-15 words):       ~20-25%
  - Medium sentences (16-30 words):     ~35-40%
  - Long sentences (31-45 words):       ~15-20%
  - Very long sentences (46+ words):    ~5-10%
```

#### 4.2.3 Section-Aware Mode Escalation

**Current**: The user selects a single mode for the entire document.

**Proposed**: Apply automatic section-specific mode escalation based on G5 per-section scores.

```yaml
section_aware_escalation:
  abstract:
    base_mode: conservative
    escalate_to: balanced
    trigger: "section_score > 50"
    rationale: "Abstract receives highest scrutiny but structural conventions are accepted"

  introduction:
    base_mode: balanced
    escalate_to: balanced  # No escalation
    trigger: null
    rationale: "Introduction has expected formality"

  methods:
    base_mode: conservative
    escalate_to: conservative  # Never escalate
    trigger: null
    rationale: "Template language in Methods is normal; excessive transformation risks accuracy"

  results:
    base_mode: conservative
    escalate_to: balanced
    trigger: "section_score > 60"
    rationale: "Results: only transform framing language; preserve data descriptions"

  discussion:
    base_mode: balanced
    escalate_to: aggressive
    trigger: "section_score > 50"
    rationale: "Discussion benefits most from structural transformation"

  conclusion:
    base_mode: balanced
    escalate_to: aggressive
    trigger: "section_score > 50"
    rationale: "Conclusion has a similar pattern profile to Discussion"
```

**Escalation decision flow:**

```
G5 per-section analysis complete
    |
    v
For each section:
    IF section_score > escalation_trigger:
        mode = escalated_mode
    ELSE:
        mode = base_mode
    |
    v
Pass section-specific mode_map to G6:
  {
    "abstract": "balanced",
    "introduction": "balanced",
    "methods": "conservative",
    "results": "conservative",
    "discussion": "aggressive",
    "conclusion": "aggressive"
  }
```

---

### Pillar 3: Iterative Pipeline (Pipeline v2.0)

Replaces the single pass with a **multi-pass architecture with feedback loops**.

#### 4.3.1 Multi-Pass Iterative Pipeline Architecture

```
========================================================================
Pass 1: VOCABULARY PASS (Conservative)
========================================================================
  G5 Scan (full)
    → G6 Transformation (targeting L1, M1, C1 — vocabulary layer only)
      → F5 Quick Verify (citation/statistics integrity only)
        |
        v
  CP_PASS1_REVIEW:
    "Score dropped from X% to Y%. Proceed with structural pass?"
    [A] Continue to structural pass
    [B] Accept current state
    [C] View detailed diff
        |
        v (if Continue selected)

========================================================================
Pass 2: STRUCTURAL PASS (Balanced)
========================================================================
  G5 Scan (delta — residual patterns after Pass 1 only)
    → G6 Transformation (S7-S10, CV enhancement — structural layer)
      → F5 Full Verify (all 5 checks)
        |
        v
  CP_PASS2_REVIEW:
    "Score is now Z%. Target achieved?"
    [A] Accept
    [B] One more pass
    [C] Manual review
        |
        v (if One more pass selected, optional)

========================================================================
Pass 3 (Optional): POLISH PASS
========================================================================
  G5 Scan (audit — full re-scan)
    → G6 micro fixes (targeting residual patterns)
      → F5 Full Verify (all 5 checks)
        |
        v
  CP_FINAL_REVIEW:
    Final approval
    [A] Approve [B] View full diff [C] Revert to Pass 2
========================================================================
```

**Key design decisions:**

| Decision | Rationale |
|----------|-----------|
| Each pass targets a different layer | Sequential approach of vocabulary → structure → fine-tuning minimizes interference |
| G5 re-scan between passes | Measures actual progress; Round 3 experience confirmed G6 can introduce new patterns |
| Human checkpoints between passes | Provides decision opportunities with score reports |
| Maximum 3 passes | Diminishing returns; minimal improvement after 3 passes |
| Pass 3 is optional | Only when score target is not met |

#### 4.3.2 New Checkpoints

```yaml
CP_PASS1_REVIEW:
  level: recommended
  description: "Vocabulary pass complete -- review before structural pass"
  presents:
    - Pass 1 before/after scores
    - Residual pattern list
    - Burstiness CV score
    - Patterns processed / patterns remaining
  options:
    - "Continue to structural pass"
    - "Accept current state"
    - "View detailed diff"

CP_PASS2_REVIEW:
  level: recommended
  description: "Structural pass complete -- review results"
  presents:
    - Score progression (original → Pass 1 → Pass 2)
    - Structural metrics (CV, MTLD, paragraph opener diversity)
    - S7-S10 residual pattern count
  options:
    - "Accept"
    - "One more polish pass"
    - "Manual review mode"

CP_FINAL_REVIEW:
  level: optional
  description: "Final review before export"
  presents:
    - Full score history
    - Full diff report
    - F5 verification summary
    - Final quantitative metrics (CV, MTLD, opener diversity)
```

#### 4.3.3 Post-Transformation G5 Re-Scan — Mandatory

**Research basis**: Round 3 experience confirmed that G6 can **introduce new AI patterns** while fixing existing ones.

```yaml
post_transformation_audit:
  trigger: "After every G6 transformation pass"
  agent: "G5"
  checks:
    - "Were no new HIGH-RISK patterns introduced?"
    - "Were no new pattern categories activated?"
    - "Did the overall score decrease (not increase)?"

  on_new_patterns_found:
    action: "FLAG to user"
    message: "G6 removed {M} patterns but introduced {N} new patterns. Net effect: {delta}"
    options:
      - "Accept (net improvement, accept)"
      - "Revert this pass"
      - "Target new patterns in next pass"

  severity_thresholds:
    info: "0 new patterns, score decreased"
    warning: "1-2 new patterns but net score decrease"
    error: "3 or more new patterns or net score increase"
```

#### 4.3.4 Score Target System

```yaml
target_mode:
  enabled: true
  usage: '"Humanize to target: 30%"'
  behavior:
    1: "Run G5 → check baseline score"
    2: "Calculate required reduction"
    3: "Auto-select section-specific modes to achieve target"
    4: "Run iterative passes until target achieved or 3-pass limit reached"
    5: "Report final score vs target"

  presets:
    journal_safe: 30     # For peer-reviewed journals
    conference: 40       # For conference papers
    working_paper: 50    # For working papers/preprints

  custom_target:
    description: "User can specify a custom target score"
    range: "10-60"
    example: '"Humanize to target: 25%"'
```

**Automatic strategy selection logic for target achievement:**

```python
def select_strategy(baseline_score, target_score):
    gap = baseline_score - target_score

    if gap <= 20:
        # Vocabulary pass alone is sufficient
        return ["Pass 1: Vocabulary (Conservative)"]
    elif gap <= 40:
        # Vocabulary + structural pass
        return [
            "Pass 1: Vocabulary (Conservative)",
            "Pass 2: Structural (Balanced)"
        ]
    else:
        # Full 3-pass
        return [
            "Pass 1: Vocabulary (Conservative)",
            "Pass 2: Structural (Aggressive)",
            "Pass 3: Polish"
        ]
```

---

## 5. Objective Metrics and Benchmarks

### 5.1 Performance Targets

| Metric | Target | Current Status | Notes |
|--------|--------|----------------|-------|
| **Citation Preservation** | **100%** | Required | Absolutely non-negotiable |
| **Statistics Preservation** | **100%** | Required | Absolutely non-negotiable |
| **Meaning Preservation** | **>=95%** semantic similarity | Target | F5 meaning check |
| **AI Probability Reduction (Conservative)** | 20-35% | Expected | Vocabulary layer only |
| **AI Probability Reduction (Balanced)** | 35-50% | Expected | Vocabulary + structure |
| **AI Probability Reduction (Aggressive)** | 50-70% | Expected | Full transformation |
| **Pattern Reduction (Conservative)** | 50-70% | Expected | Targeting HIGH-RISK patterns |
| **Pattern Reduction (Balanced)** | 60-80% | Expected | Targeting HIGH + MEDIUM |
| **Pattern Reduction (Aggressive)** | 80-95% | Expected | Targeting all patterns |
| **G5 Analysis Time** | <30 sec per 1000 words | Target | May increase with quantitative metrics addition |
| **G6 Transformation Time** | <60 sec per 1000 words | Target | May increase with Layer 3 addition |
| **F5 Verification Time** | <15 sec per 1000 words | Target | Maintain existing level |

### 5.2 Before/After Upgrade Benchmark Comparison

| Metric | Current Pipeline | Target (Post-Upgrade) |
|--------|-----------------|----------------------|
| **Passes needed to reach <35%** | 3 (manual) | **2 (automated)** |
| **Achievable final AI score** | 31%/22% (with manual Round 3) | **<30% (automated, no manual work needed)** |
| **Burstiness CV (post-humanization)** | Not measured | **>0.45** |
| **MTLD (post-humanization)** | Not measured | **>70** |
| **Paragraph opener diversity** | Not measured | **>0.70** |
| **Residual structural patterns** | Not measured (S7-S10 did not exist) | **0 HIGH-risk** |
| **Citations preserved** | 100% | **100% (no regression)** |
| **Statistics preserved** | 100% | **100% (no regression)** |

### 5.3 Expected Score Progression Comparison

**Current pipeline (manual 3-Round):**

```
Paper 1: 80% ──[G6 R1]──> 62% ──[G6 R2]──> ~60% ──[Manual R3]──> 31%
Paper 2: 82% ──[G6 R1]──> 61% ──[G6 R2]──> ~60% ──[Manual R3]──> 22%

                    |--- G6 automated ---|    |-- Manual structural dismantling --|
                        ~20pp reduction              ~30pp reduction
```

**Target upgraded pipeline (automated 2-Pass):**

```
Paper 1: 80% ──[Pass 1: Vocab]──> ~55% ──[Pass 2: Structural]──> <30%
Paper 2: 82% ──[Pass 1: Vocab]──> ~55% ──[Pass 2: Structural]──> <30%

                |-- Vocabulary layer --|    |-- Structural layer (new) --|
                    ~25pp reduction              ~25pp reduction
```

### 5.4 Validation Protocol

A five-step protocol for validating the effectiveness of the upgraded pipeline:

| Step | Procedure | Measured Items |
|------|-----------|----------------|
| **1** | Prepare original (pre-humanization) versions of Paper 1 and Paper 2 | Confirm baseline scores |
| **2** | Process with upgraded pipeline (target: 30%) | Scores and pattern counts after each pass |
| **3** | Measure quantitative metrics | Passes needed, final score, burstiness CV, MTLD |
| **4** | Integrity verification | Citation/statistics integrity (100% required) |
| **5** | Compare with Round 3 manual results (31%/22%) | Confirm performance parity or superiority |

**Success criteria:**

```
SUCCESS = (
    final_score < 30%
    AND passes_needed <= 2
    AND citation_preservation == 100%
    AND statistics_preservation == 100%
    AND meaning_preservation >= 95%
    AND burstiness_CV > 0.45
    AND MTLD > 70
    AND paragraph_opener_diversity > 0.70
)
```

### 5.5 Fallback Strategy

When the automated 2-pass fails to meet the target:

| Situation | Response |
|-----------|----------|
| Score 30-35% after Pass 2 | Automatically run Pass 3 (Polish) |
| Still >35% after Pass 3 | Recommend manual review to user, provide detailed residual pattern report |
| Integrity violation detected | Immediately revert the affected pass, report violated items |
| New patterns introduced (net score increase) | Revert the affected pass, suggest alternative strategy |

---

## 6. References

### AI Text Detection and Bias

1. Liang, W., Yuksekgonul, M., Mao, Y., Wu, E., & Zou, J. (2023). GPT detectors are biased against non-native English writers. *arXiv:2304.02819*.

2. Popkov, A. et al. (2024). Median 27.2% false positive rate across free AI detectors on pre-ChatGPT human academic texts.

3. Stanford HAI. (2025). AI-Detectors biased against non-native English writers. *Stanford University Human-Centered Artificial Intelligence*.

4. IACIS. (2025). Critical look at reliability of AI detection tools. *Proceedings of IACIS 2025*.

### Paraphrasing and Evasion

5. Krishna, K., Song, Y., Karpinska, M., Wieting, J., & Iyyer, M. (2023). Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense. *Advances in Neural Information Processing Systems (NeurIPS)*. arXiv:2303.13408.

6. Adversarial Paraphrasing. (2025). A universal attack for humanizing AI-generated text. *arXiv:2506.07001*.

7. Contrastive Paraphrase Attacks on LLM Detectors. (2025). *arXiv:2505.15337*.

8. On the Detectability of LLM-Generated Text. (2025). *arXiv:2510.20810*.

### Detection Methodology and Characteristics

9. Mitchell, E. et al. DetectGPT: Zero-shot machine-generated text detection using probability curvature.

10. Feature-Based Detection: Stylometric and Perplexity Markers. (2024). *ResearchGate*.

11. Detecting AI-Generated Text with Pre-Trained Models. (2024). *ACL Anthology*.

12. Generative AI models and detection: tokenization and dataset size. (2024). *Frontiers in AI*.

13. Aggregated AI detector outcomes in STEM writing. (2024). *American Physiological Society*.

### AI Vocabulary and Language Patterns

14. Delving into ChatGPT usage in academic writing through excess vocabulary. (2024). *arXiv:2406.07016*. [14 million PubMed abstracts, 454 AI excess words identified]

15. Differentiating Human-Written and AI-Generated Texts: Linguistic Features. (2024). *MDPI*.

16. A Comparative Analysis of AI-Generated and Human-Written Text. (2024). *SSRN*.

17. Hedging Devices in AI vs. Human Essays. (2024). *SCIRP*.

18. AI and human writers share stylistic fingerprints. (2024). *Johns Hopkins Hub*.

### Watermarking

19. Kirchenbauer, J. et al. (2023). A watermark for large language models. *University of Maryland*.

20. Christ, M. & Gunn, S. (2024). Pseudorandom error-correcting codes as the theoretical basis for robust watermarks. *CRYPTO 2024*.

21. SynthID-Text: Scalable watermarking for LLM outputs. (2024). *Nature*.

22. AI watermarking must be watertight. (2024). *Nature News*.

23. Watermarking for AI-Generated Content: SoK. *arXiv:2411.18479*.

24. Cryptographic watermarks. (2024). *Cloudflare*.

### Lexical Diversity and Stylometrics

25. McCarthy, P. M. & Jarvis, S. (2010). MTLD, vocd-D, and HD-D: A validation study of sophisticated approaches to lexical diversity assessment. *Behavior Research Methods, 42*(2), 381-392.

26. MATTR: Pros and cons. (2024). *ResearchGate*.

27. Vocabulary Quality in NLP: Autoencoder-Based Framework. (2024). *Springer*.

### Non-Native Speakers and L2 Research

28. Lexical diversity, syntactic complexity: ChatGPT vs L2 students. (2025). *Frontiers in Education*.

29. More human than human? ChatGPT and L2 writers. (2024). *De Gruyter*.

### Academic-Specific Detection

30. Accuracy-bias trade-offs in AI text detection and scholarly publication fairness. (2024). *PMC*.

31. Characterizing AI Content Detection in Oncology Abstracts 2021-2023. (2024). *PMC*.

32. Distinguishing academic science writing with >99% accuracy. (2023). *PMC*.

### Commercial Detector Comparisons

33. Originality.AI — AI Detection Studies Meta-Analysis.

34. GPTZero vs Copyleaks vs Originality comparison.

35. AI vs AI: Turnitin, ZeroGPT, GPTZero, Writer AI. (2024). *ResearchGate*.

### Discourse and Paraphrasing Patterns

36. How AI Tools Affect Discourse Markers When Paraphrased. (2024). *ResearchGate*.

37. Netus AI — How stylometric patterns survive paraphrasing.

38. Deep Dive Into AI Text Fingerprints. *Hastewire*.

---

> **End of Document** | Related documents: [research-literature-review.md](./research-literature-review.md), [round3-strategy.md](./round3-strategy.md)
> **Implementation Roadmap**: [../roadmap/TODO.md](../roadmap/TODO.md)
