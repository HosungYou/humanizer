# Diverga Humanization Pipeline 업그레이드: 구조적 변환을 통한 AI 탐지 우회 전략

> **버전**: 1.0
> **작성일**: 2026-02-22
> **대상 시스템**: Diverga Plugin v8.0.1 (G5/G6/F5 파이프라인)
> **관련 저장소**: [HosungYou/humanizer](https://github.com/HosungYou/humanizer)

---

## 목차

1. [배경 및 문제 인식](#1-배경-및-문제-인식)
2. [현행 아키텍처 분석 (G5→G6→F5)](#2-현행-아키텍처-분석-g5g6f5)
3. [AI 텍스트 탐지 연구 문헌 리뷰 (2024-2026)](#3-ai-텍스트-탐지-연구-문헌-리뷰-2024-2026)
4. [3대 축 업그레이드 제안](#4-3대-축-업그레이드-제안)
5. [객관적 지표 및 벤치마크](#5-객관적-지표-및-벤치마크)
6. [참고 문헌](#6-참고-문헌)

---

## 1. 배경 및 문제 인식

### 1.1 3-Round 경험: 두 학술 논문의 humanization 과정

Diverga 파이프라인(G5→G6→F5)을 활용하여 두 편의 학술 논문을 humanization한 경험이 이번 업그레이드의 직접적 계기가 되었다. 두 논문 모두 LLM 보조 작성(AI-assisted writing) 후 AI 탐지 점수를 학술지 투고 안전 수준으로 낮추는 것이 목표였다.

**대상 논문:**

| 구분 | Paper 1 | Paper 2 |
|------|---------|---------|
| **제목** | "The Politicization of Workforce Futures" | "Beyond the Information Deficit" |
| **이론 프레임워크** | Occupational Identity Threat | Epistemic Cognition |
| **목표 학술지** | Technological Forecasting and Social Change (TFSC) | International Journal of AI in Education (IJAIED) |
| **Impact Factor** | ~12.0 | ~4.7 |

두 논문 모두 초기 G5 분석에서 HIGH RISK 판정을 받았다:

| 지표 | Paper 1 (Occupational Identity) | Paper 2 (Epistemic Cognition) |
|------|--------------------------------|-------------------------------|
| **AI probability** | **80%** | **82%** |
| **Risk level** | HIGH | HIGH |
| **Pattern count** | 34 (HIGH 21, MEDIUM 12, LOW 1) | 36 (HIGH 24, MEDIUM 12) |

### 1.2 점수 추이 (Score Progression)

최종적으로 LOW risk 수준에 도달하기까지 **3회의 수동 라운드**가 필요했다:

| Paper | Round 1 | Round 2 | Round 3 (최종) |
|-------|---------|---------|----------------|
| Paper 1 (TFSC) | 80% HIGH, 34 patterns | 62% MEDIUM, 24 patterns | **31% LOW, 7 patterns** |
| Paper 2 (IJAIED) | 82% HIGH, 36 patterns | 61% MEDIUM-HIGH, 29 patterns | **22% LOW, 4 patterns** |

핵심 관찰: Round 1-2(G6 자동 처리)에서 약 20pp 하락 후 **60% 부근에서 천장(ceiling)에 도달**했다. 최종 돌파는 Round 3의 완전한 수동 구조 해체를 통해서만 가능했다.

### 1.3 라운드별 격차 분석 (Round-by-Round Gap Analysis)

| Round | 전략 | 점수 변화 | G6가 수행한 작업 | 수동으로 수행한 작업 |
|-------|------|-----------|------------------|---------------------|
| **Round 1** | Vocabulary substitution | 80→62% | L1 tier1/tier2 어휘 치환 | 추가 작업 불필요 |
| **Round 2** | Surface pattern fixes | 62→~60% | C1, H1, H2 패턴 처리 | 최소 개선 — 천장 도달 |
| **Round 3** | Deep structural dismantling | 60→31/22% | N/A (수동 작업) | 모든 열거 구조 해체, Discussion 도입부 재작성, 가설 체크리스트의 서사화, 구체 시나리오 추가, 문장 길이 극적 변화 |

### 1.4 근본 원인 분석 (Root Cause)

**G6는 단어/구문(word/phrase) 수준에서 작동한다.** 어휘가 정리된 후 잔여 60%의 탐지 신호는 G6가 처리할 수 없는 **구조적 패턴(structural patterns)**에서 비롯된다.

어휘 치환 후에도 높은 점수가 유지되는 이유는 다음과 같다:

1. **구조적 규칙성(Structural regularity)** — 예측 가능한 문단 구조 (topic sentence → evidence → synthesis → transition)
2. **열거 지문(Enumeration fingerprint)** — 산문 속에 포함된 번호 매김 목록
3. **가설 체크리스트 패턴(Hypothesis checklist pattern)** — 기계적 H1/H2/H3 확인 시퀀스
4. **정형화된 섹션 도입부(Formulaic section openers)** — Discussion이 항상 요약 재진술로 시작
5. **문장 길이 균일성(Sentence length uniformity)** — 25-45단어 범위에 변동 없음 (낮은 burstiness)
6. **문단 도입부 반복(Paragraph opener repetition)** — 연속된 문단이 "The [X]..."로 시작

### 1.5 양 논문에서 공통 발견된 문제 (우선순위순)

**문제 1: LLM 특유 표현 — 즉시 제거 필요**

| 원문 표현 | 처리 방법 |
|-----------|-----------|
| "worth noting/emphasizing" | 삭제하거나 직접 진술 |
| "Several patterns stand out" | 구체적 내용으로 시작 |
| "unprecedented challenge" | 경험적 데이터로 시작 |
| "through the lens of" | 제거 |
| "theoretically grounded" | 제거 |
| "landscape" | 구체적 맥락으로 대체 |
| "illuminate," "underscore," "emerge" | 평이한 동사로 대체 |
| "precisely the kind of" | "this kind of" |

**문제 2: 구조적 문제**

- **Tricolon 남용**: Paper 1에서 6건, Paper 2에서 "X rather than Y" 패턴 14건
- **가설 요약 섹션의 기계적 반복**: "H1 supported, H2 supported..."
- **과도한 번호 목록**: "four gaps," "three findings," "five directions"
- **동일한 문단 구조**: topic sentence → citation → interpretation → transition

**문제 3: 저자 목소리 부재(Author voice absence)**

- 1인칭 사용 전무
- 지적 놀라움이나 질문 표현 없음
- 모든 발견이 동일하게 "예상됨"으로 처리
- Discussion이 Results의 단순 재진술

**문제 4: 단조로운 문장 리듬(Monotonous sentence rhythm)**

- 25-45단어 범위의 균일한 문장 길이
- 12단어 이하의 짧은 선언문 전무
- 메트로놈 같은 리듬, 변동 없음

---

## 2. 현행 아키텍처 분석 (G5→G6→F5)

### 2.1 G5 — Academic Style Auditor (AI 패턴 탐지)

| 속성 | 값 |
|------|-----|
| **Agent ID** | G5 |
| **Category** | G - Publication & Communication |
| **VS Level** | Light |
| **Tier** | MEDIUM (Sonnet) |
| **Tools** | Read, Glob, Grep |
| **기반** | Wikipedia AI Cleanup initiative의 24개 패턴 카테고리 |

#### 2.1.1 탐지 카테고리 (24개)

**Content Patterns (C1-C6)**

| 패턴 | Risk | 대상 | 예시 |
|------|------|------|------|
| C1: Significance Inflation | HIGH | 과대 주장된 중요성 | "groundbreaking", "revolutionary", "paradigm-shifting" |
| C2: Notability Claims | MEDIUM | 모호한 권위 호소 | "widely recognized", "well-established" |
| C3: Superficial -ing Constructions | MEDIUM | 간접 언어 | "highlighting the importance of", "demonstrating the value of" |
| C4: Promotional Language | HIGH | 마케팅 언어 | "impressive", "remarkable", "exciting", "cutting-edge" |
| C5: Vague Attributions | HIGH | 출처 누락 | "Studies show...", "Research demonstrates..." |
| C6: Formulaic Section Openings | LOW | 템플릿 언어 | "In conclusion", "It is worth noting" |

**Language Patterns (L1-L6)**

| 패턴 | Risk | 대상 | 예시 |
|------|------|------|------|
| L1: AI Vocabulary Clustering | HIGH | AI 전형적 어휘 | Tier 1: delve, tapestry, intricacies, multifaceted, myriad, paramount, testament, embark, realm; Tier 2: landscape, underscore, pivotal, leverage, utilize, facilitate, foster, synergy, holistic, robust |
| L2: Copula Avoidance | MEDIUM | "is/has"의 화려한 대체 | "serves as", "stands as", "functions as", "boasts", "possesses" |
| L3: Negative Parallelism | LOW | 반복 구조 | "not only X but also Y" |
| L4: Rule of Three | MEDIUM | 인위적 3분 구조 | 2-4개 항목이 있을 때 3개로 강제 |
| L5: Elegant Variation | LOW | 불필요한 동의어 순환 | "study/research/investigation" 혼용 |
| L6: False Ranges | MEDIUM | 인위적 이분법 | "from theory to practice", "local to global" |

**Style Patterns (S1-S6)**

| 패턴 | Risk | 대상 | 예시 |
|------|------|------|------|
| S1: Em Dash Overuse | MEDIUM | 구두점 과다 | 문단당 다수의 — 대시 사용 |
| S2: Excessive Boldface | LOW | 서식 과다 | **과도한** **강조** **텍스트** |
| S3: Inline-Header Lists | MEDIUM | 인위적 열거 | "First, ... Second, ... Third, ..." |
| S4: Title Case Overuse | LOW | 대문자 과다 | "The Importance Of This Finding" |
| S5: Emoji Usage | HIGH | 비학술적 마커 | 학술 텍스트 내 이모지 |
| S6: Curly Quote Artifacts | LOW | 서식 불일치 | 혼재된 인용부호 스타일 |

**Communication Patterns (M1-M3)**

| 패턴 | Risk | 대상 | 예시 |
|------|------|------|------|
| M1: Meta-Commentary | HIGH | AI 자기 참조 | "As an AI language model...", "I hope this helps" |
| M2: Excessive Affirmation | HIGH | 챗봇 잔재 | "Great question!", "Absolutely!", "Excellent point!" |
| M3: Apology Hedging | MEDIUM | 과도한 공손 | "I apologize if...", "I hope you don't mind..." |

**Filler/Hedging Patterns (H1-H3)**

| 패턴 | Risk | 대상 | 예시 |
|------|------|------|------|
| H1: Verbose Phrases | MEDIUM | 장황한 구문 | "in order to" → "to", "at this point in time" → "now" |
| H2: Excessive Hedging | MEDIUM | 과잉 유보 언어 | "could potentially perhaps", "may possibly" |
| H3: Redundant Intensifiers | LOW | 모순적 강조 | "very unique", "extremely essential" |

**Academic-Specific Patterns (A1-A6)**

| 패턴 | Risk | 대상 | 예시 |
|------|------|------|------|
| A1: Overclaiming | HIGH | 근거 없는 인과 주장 | 증거 없이 인과 언어 사용 |
| A2: Underclaiming | LOW | 명확한 발견의 과잉 유보 | 과도한 hedging |
| A3: Citation Clustering | LOW | 인용 밀도 | 한 문장에 다수 인용 |
| A4: Methods Boilerplate | MEDIUM | 방법론 템플릿 | 일반적 방법론 서술 |
| A5: Discussion Formula | MEDIUM | 구조적 템플릿 | Limitations, Implications, Future의 예측 가능한 구조 |
| A6: Implications Inflation | HIGH | 과대 의의 주장 | "profound implications for society" |

#### 2.1.2 어휘 티어 시스템 (Vocabulary Tier System)

**Tier 1 — High Alert (항상 플래그)**

```
delve, dive into, crucial, foster, intricate, intricacies
realm, landscape, multifaceted, comprehensive, underscore
noteworthy, meticulous, leverage, utilize, pivotal
embark, endeavor, unveil, unravel, intriguing, testimony, testament
```

조치: 모든 모드에서 변환 (Conservative 이상)

**Tier 2 — Moderate Alert (클러스터링 시 플래그)**

```
robust, streamline, facilitate, enhance, fundamental
substantial, significant, paramount, innovative
nuanced, sophisticated, compelling, profound
```

조치: Balanced 이상 모드에서 변환

**Tier 3 — Context Check (문맥 내 평가)**

```
important, effective, relevant, appropriate
demonstrate, indicate, suggest, reveal
```

조치: Aggressive 모드에서만 변환

#### 2.1.3 점수 산출 알고리즘 (Scoring Algorithm)

```
AI_Probability = SUM(pattern_weight * frequency) / max_score * 100
```

**패턴 가중치 (Base Weights):**

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

#### 2.1.4 위험 분류 (Risk Classification)

| Score Range | Risk Level | Label | Action |
|-------------|------------|-------|--------|
| 0-20 | Low | Likely Human | Optional review |
| 21-40 | Moderate | Mixed Signals | Recommended review |
| 41-60 | Elevated | Probably AI-Assisted | Review needed |
| 61-80 | High | Likely AI-Generated | Humanization recommended |
| 81-100 | Critical | Obviously AI | Humanization required |

#### 2.1.5 섹션별 가중 승수 (Section-Based Multipliers)

| Section | Multiplier | 근거 |
|---------|------------|------|
| Abstract | 1.2 | 가장 높은 심사 강도 |
| Introduction | 1.1 | 첫인상 중요 |
| Literature Review | 1.0 | 일정한 격식 예상 |
| Methods | 0.8 | 일부 템플릿 수용 가능 |
| Results | 1.0 | 표준 |
| Discussion | 1.1 | 주장 심사 강도 높음 |
| Conclusion | 1.1 | 최종 인상 중요 |
| Response Letter | 0.9 | 일정한 격식 예상 |

#### 2.1.6 클러스터링 탐지 (Clustering Detection)

```python
# 어휘 클러스터링
IF (tier1_words >= 2) OR (tier2_words >= 4):
    cluster_detected = True
    bonus_score = 20

# 문단 내 클러스터링
IF (patterns_in_same_paragraph >= 3):
    paragraph_cluster = True
    bonus_score += 10 * (pattern_count - 2)
```

**패턴 유형 조합 보너스:**

| 조합 | 보너스 |
|------|--------|
| Content + Language | +10 |
| Language + Style | +5 |
| Content + Communication | +15 |
| 3개 카테고리 이상 | +20 |
| 4개 이상 카테고리 | +30 |

#### 2.1.7 밀도 계산 (Density Calculations)

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

#### 2.1.8 오탐 경감 (False Positive Mitigation)

```python
IF text_is_from_established_academic_author:
    score *= 0.8  # 의심도 감소

IF journal_has_strict_style_guide:
    exempt(S1, S2, S4)  # 스타일이 요구될 수 있음

IF text_is_from_non_native_english_speaker:
    reduce_L1_weight_by(0.30)  # AI 어휘 일부가 ESL 패턴과 겹침
```

#### 2.1.9 신뢰도 보정 (Confidence Calibration)

```python
# score +/- confidence_margin
confidence_margin = 10  # 대부분 텍스트
confidence_margin = 15  # 매우 짧은 텍스트 (<200 words)
confidence_margin = 5   # 긴 텍스트 (>2000 words)
```

---

### 2.2 G6 — Academic Style Humanizer (텍스트 변환)

| 속성 | 값 |
|------|-----|
| **Agent ID** | G6 |
| **Category** | G - Publication & Communication |
| **VS Level** | Enhanced (3-Phase) |
| **Tier** | HIGH (Opus) |
| **Tools** | Read, Glob, Grep, Edit, Write |

#### 2.2.1 변환 모드 (Transformation Modes)

| Mode | 대상 | AI Probability 감소 | 텍스트 변경률 | 적합 용도 |
|------|------|---------------------|--------------|-----------|
| **Conservative** | HIGH-RISK만 (C1,C4,C5,L1-T1,S5,M1,M2,A1,A6) | 20-35% | 5-15% | 학술지 투고 |
| **Balanced** (기본값) | HIGH + MEDIUM-RISK | 35-50% | 15-30% | 대부분의 학술 문서 |
| **Aggressive** | 모든 패턴 | 50-70% | 30-50% | 블로그/비격식 문서 |

#### 2.2.2 HAVS 3-Phase Process (Humanization-Adapted Verbalized Sampling)

표준 VS(Verbalized Sampling)는 이론/방법론 선택을 위한 연구 의사결정 도구다. 텍스트 변환에 5-Phase VS를 적용하면 카테고리 오류(category error)가 발생한다. HAVS는 이를 적응시킨 것이다:

| 측면 | Standard VS | HAVS |
|------|------------|------|
| 목적 | 이론/방법론 선택 | 텍스트 변환 전략 |
| T-Score 의미 | 이론의 전형성 | 변환 패턴의 전형성 |
| Phase 수 | 5 phases (0-5) | 3 phases (0-2) |
| 창의성 초점 | 개념적 혁신 | 자연스러운 표현 |

**Phase 0: Transformation Context Collection**
- G5 분석 결과 수집
- 목표 스타일 식별 (journal/conference/thesis/informal)
- 사용자 모드 선택 확인

**Phase 1: Modal Transformation Warning** (T > 0.7 경고)

| 전략 | T-Score | 위험 |
|------|---------|------|
| 동의어 치환만 | 0.9 | AI 탐지기가 이를 학습함 |
| 문장 재배열만 | 0.85 | 구조 보존; 패턴 잔존 |
| 수동/능동 전환만 | 0.8 | 불일치 voice가 새 패턴 생성 |

권장: "전략 조합으로 더 나은 위장을 달성하라"

**Phase 2: Differentiated Transformation Directions**

| Direction | T-Score | 전략 | Mode | 적합 용도 |
|-----------|---------|------|------|-----------|
| **A** | ~0.6 | 어휘 + 구문 치환 | Conservative | 학술지 투고 |
| **B** (권장) | ~0.4 | A + 문장 재조합, 흐름 개선 | Balanced | 대부분의 학술 문서 |
| **C** | ~0.2 | A+B + 문단 재구성, 스타일 이전 | Aggressive | 비격식 문서 |

#### 2.2.3 상세 변환 규칙 (Detailed Transformation Rules)

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

**Balanced Mode — 추가 규칙:**

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
S1: Em dash threshold: 문서당 2개; 대안: 괄호, 콜론, 쉼표, 새 문장
S3: Inline-header lists를 산문으로 변환
H1: "in order to" → "to"
    "due to the fact that" → "because"
    "the majority of" → "most"
H2: "could potentially" → "may"
    "seems to suggest" → "suggests"
```

**Aggressive Mode — 추가 규칙:**

```yaml
C6: "First,...Second,...Third,..." 템플릿을 자연스러운 산문으로 해체
L1: "delve" → "look at"
    "nuanced" → "subtle"
    "landscape" → "field"
    "synergy" → "teamwork"
L3: "not only... but also" → "both... and"
L5: 하나의 용어를 선택하여 일관 사용 (동의어 순환 없음)
A1: "This paper aims to" → "We"
    "The present study investigates" → "We investigated"
A5: "This study makes three contributions. First,..." → 기여를 자연스럽게 서술
```

#### 2.2.4 보존 규칙 (Preservation Rules) — 비협상, 100% 정확도 필수

변환 과정에서 **절대 수정 불가**한 요소:

- **인용(Citations)**: (Author, year) 형식, DOI, URL, 페이지 번호
- **통계값(Statistics)**: p-values, effect sizes, 신뢰구간, N값, 평균/표준편차, 검정 통계량, 백분율, 상관계수, beta 가중치, odds ratios
- **직접 인용(Direct quotes)**: 원문 텍스트, block quotes, 인터뷰 발췌
- **전문 용어(Technical terminology)**: 명명된 이론, 프레임워크, 방법론
- **고유 명사(Proper nouns)**: 저자명, 기관, 학술지, 학회, 데이터베이스
- **약어(Acronyms)**: 정의된 모든 약어 및 분야 표준 약어
- **방법론 세부사항(Methodology specifics)**: 도구명, 소프트웨어 버전, 척도 앵커, 신뢰도 값

#### 2.2.5 맥락 의존적 보존 (Context-Dependent Preservation)

```yaml
"significant":
  preserve: p-value 맥락에서 사용될 때
  transform: 일반적 "중요한" 의미로 사용될 때

"robust":
  preserve: 통계적 강건성 (예: 'robust standard errors')
  transform: 일반적 '강한'의 의미일 때

"framework":
  preserve: 명명된 프레임워크
  transform: 일반적 사용

"paradigm":
  preserve: 과학철학 맥락
  transform: 일반적 '접근법' 의미
```

#### 2.2.6 반복 정제 (Iterative Refinement)

Balanced/Aggressive 모드에서 G6는 반복 루프(최대 2회)를 적용한다:

1. 1차 변환 전략 적용
2. 변환된 텍스트에서 새로운 AI 패턴 자체 점검
3. 검증: 새 패턴 없음, 의미 보존 (>95% 유사도), 인용 무결성 (100%), 통계 불변 (100%)
4. 문제 발견 시 자체 생성 AI 패턴 제거 및 정제

#### 2.2.7 Humanization 모듈

**h-style-transfer**: 학문 분야별 작성 스타일 적용
- Education: 실용 지향적, 접근 가능한 언어
- Psychology: 인간 중심, 측정 초점
- Management: 행동 지향적, 이해관계자 인식

**h-flow-optimizer**: 3단계 산문 흐름 최적화
- Sentence level: 길이/복잡성 변동, 도입부 다양성
- Paragraph level: Topic sentences, 증거 흐름, 전환
- Document level: 논증 진행, 섹션 균형

---

### 2.3 F5 — Humanization Verifier (품질 보증)

| 속성 | 값 |
|------|-----|
| **Agent ID** | F5 |
| **Category** | F - Quality Assurance |
| **Tier** | LOW (Haiku) |

#### 2.3.1 5가지 검증 점검 (Five Verification Checks)

**1. Citation Integrity Check** (CRITICAL — 실패 시 자동 거부)
- 변환 전/후 인용 수 일치
- 형식 보존: (Author, year)
- 내용 정확: 인용 텍스트 미변경
- 배치 논리성

**2. Statistical Accuracy Check** (CRITICAL — 실패 시 자동 거부)
- p-values: 정확 일치
- Effect sizes: 불변 (d, r, eta-squared)
- Sample sizes: N 불변
- Test statistics: t, F, chi-squared 불변
- Percentages: 모든 % 불변
- Confidence intervals: 모든 CI 불변

**3. Meaning Preservation Check** (MAJOR — 검토 플래그)
- 주요 발견 보존
- 결론 불변
- 방법론 서술 정확
- 새로운 인과 언어 미추가
- Hedging 적절성 검증
- 목표: >=95% semantic similarity

**4. AI Pattern Reduction Check**
- AI probability 감소 확인
- 최소 20% 감소 예상
- 목표 패턴 해결 확인
- <20% 감소 시 경고

**5. Academic Tone Check**
- 격식 수준 적절성
- 객관성 유지
- 기술적 정밀도 유지
- Voice 일관성

#### 2.3.2 엄격도 수준 (Strictness Levels)

| 수준 | 설명 |
|------|------|
| Low | 기본 검사만 |
| Medium (기본값) | 전체 검증 |
| High | 심층 문맥 분석, 톤 일관성, 준수 점검 |

---

### 2.4 전체 파이프라인 흐름도

```
Stage 1: Content Generation (G2-AcademicCommunicator / G3-PeerReviewStrategist / Auto-Doc)
    |
    v
Stage 2: Analysis (G5-AcademicStyleAuditor)
    |-- 24개 패턴 카테고리 탐지
    |-- AI probability 계산
    |-- Risk level 분류
    |-- 권장 사항 생성
    |
    v
CHECKPOINT: CP_HUMANIZATION_REVIEW (권장)
    "AI 패턴 탐지됨. Humanize?"
    [A] Conservative [B] Balanced [C] Aggressive [D] View Report [E] Skip
    |
    v
Stage 3: Transformation (G6-AcademicStyleHumanizer, HAVS 3-Phase 사용)
    |-- Phase 0: Context collection
    |-- Phase 1: Modal warning
    |-- Phase 2: Direction selection (CP_HAVS_DIRECTION)
    |-- Iterative refinement (B/C 모드)
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
CHECKPOINT: CP_HUMANIZATION_VERIFY (선택)
    변경 사항 검토. [A] Approve [B] Review [C] Revert [D] Try different mode
    |
    v
Stage 5: Output (Word/PDF로 humanized content 내보내기)
    + 선택: AI Pattern Report Appendix
    + 선택: Transformation Audit Trail
```

### 2.5 파이프라인 상태 (Pipeline States FSM)

```
idle → analyzing → awaiting_decision → transforming → verifying → (선택) awaiting_approval → complete
```

상태 전이 다이어그램:

```
                   G5 시작        결과 표시       사용자 선택
   [idle] --------> [analyzing] --------> [awaiting_decision] --------> [transforming]
                                              |                              |
                                              | (Skip 선택)                  | G6 완료
                                              v                              v
                                          [complete]                    [verifying]
                                                                             |
                                                                             | F5 완료
                                                                             v
                                                                    [awaiting_approval]
                                                                             |
                                                                             | 승인
                                                                             v
                                                                        [complete]
```

### 2.6 에이전트 통신 프로토콜

**G5 → G6**: G5는 완전한 분석 보고서 (24개 패턴, 확률, 위험 수준)를 출력한다. G6는 이를 `g5_analysis` 입력 파라미터로 수신하여 변환 전략에 반영한다.

**G6 → F5**: G6는 humanized 텍스트 + 변환 로그 (원문/대체 쌍)를 출력한다. F5는 원문과 humanized 버전을 모두 수신하여 무결성 위반을 비교 검증한다.

### 2.7 자동 활성화 임계값 (Auto-Activation Thresholds)

```yaml
skip_if_below: 20%      # AI probability < 20%이면 건너뜀
recommend_if_above: 40%  # > 40%이면 권장
require_if_above: 70%    # > 70%이면 검토 필수
```

### 2.8 윤리 원칙 (Ethics Note)

> **"Humanization improves expression, not deception."**
> (Humanization은 표현을 개선하는 것이지 기만이 아니다.)

**Humanization이 하는 것:**
- 아이디어를 자연스럽게 표현하도록 돕기
- 로봇적 어구 제거
- 가독성을 개선하면서 학술적 톤 유지
- 명백한 AI 잔재 제거

**Humanization이 하지 않는 것:**
- AI 사용을 "탐지 불가능"하게 만들기
- AI 공개(disclosure) 필요성 대체
- 독창적 아이디어 생성
- 인간 판단 대체
- 수락 보장

---

## 3. AI 텍스트 탐지 연구 문헌 리뷰 (2024-2026)

> 상세한 문헌 리뷰는 별도 문서 [research-literature-review.md](./research-literature-review.md)에 수록되어 있다. 본 절에서는 업그레이드 설계에 직접 반영된 핵심 결론을 요약한다.

### 3.1 탐지 접근법 개관

현재 AI 텍스트 탐지는 크게 세 가지 접근법으로 분류된다:

| 접근법 | 원리 | 대표 도구 | 주요 한계 |
|--------|------|-----------|-----------|
| **Perplexity 기반** | 언어 모델이 각 토큰에 얼마나 "놀라는지" 측정 | GPTZero, DetectGPT | 모델 의존적 — 한 모델에서 예측 가능한 텍스트가 다른 모델에서는 아닐 수 있음 |
| **Classifier 기반** | AI/인간 쌍으로 학습된 fine-tuned transformer | Originality.ai, Turnitin, Copyleaks, ZeroGPT | 학습 데이터 편향, paraphrasing에 취약 |
| **Watermarking 기반** | 생성 시 토큰 선택에 통계적 신호 삽입 | SynthID-Text (Google DeepMind) | 생성 모델의 협조 필요, 소급 탐지 불가 |

### 3.2 주요 상업 탐지기 비교

| Tool | 주장 정확도 | 독립 검증 결과 | 오탐률 | 비고 |
|------|------------|---------------|--------|------|
| GPTZero | 99.3% | 미수정 텍스트에서는 높음; 번역 콘텐츠에서 실패 | 0.24% (주장) | 번역된 AI 텍스트를 모두 인간으로 오분류 |
| Originality.ai | 98-100% | 여러 벤치마크에서 최고 성능 | Low | 장문 학술 텍스트에서 최적 |
| Turnitin AI | 92-100% | AI 텍스트의 ~15% 누락 | ~1% (주장) | 다수 대학이 비활성화 중 |
| Copyleaks | 90.7% | 다국어 탐지 최고; ~1/20 오탐 | ~5% | 비영어 AI 텍스트에서 강점 |
| ZeroGPT | Variable | 전반적으로 낮은 정확도 | High | 무료 tier; 신뢰도 낮음 |

### 3.3 근거 기반 핵심 결론 (7개)

업그레이드 설계에 직접적으로 반영된 문헌 근거:

**1. 어떤 탐지기도 고위험 결정에 단독으로 신뢰할 수 없다.**
독립 연구는 오탐률 10-27%를 일관되게 보고하며, 이는 벤더 주장(0.24-1%)과 극명히 대조된다. Yale, Vanderbilt, Johns Hopkins, Northwestern 등 최소 12개 엘리트 대학이 AI 탐지를 비활성화했다.

**2. Paraphrasing은 가장 효과적인 우회 수단이다.**
DIPPER(Krishna et al., 2023)는 DetectGPT 탐지를 70.3%에서 4.6%로 낮추었다. 2025년 adversarial paraphrasing 연구는 8개 탐지기에 걸쳐 평균 87.88% TPR 감소를 달성했다.

**3. Burstiness와 perplexity가 핵심 정량적 신호다.**
Burstiness(CV 또는 Fano Factor)와 문장별 perplexity 분산이 가장 실용적으로 측정 가능한 특성이다. MTLD가 어휘 다양성 측정에 권장되는 지표다.

**4. AI 어휘 서명은 구체적이며 문서화되어 있다.**
2024년 PubMed 데이터 분석에서 **454개의 AI 과잉 사용 단어**가 식별되었으며, 2023-2024년에 급격한 변곡점이 나타났다.

**5. 비원어민 화자가 체계적으로 불이익을 받는다.**
Liang et al.(2023)은 TOEFL 에세이의 **61% 이상**이 최소 하나의 탐지기에서 AI로 오분류됨을 발견했다. 가장 정확한 탐지기가 비원어민에 대한 편향도 가장 강하다.

**6. 구조적 지문은 humanization 후에도 지속된다.**
담화 구조, 문단 아키텍처, 열거 패턴은 어휘보다 paraphrasing에 더 강하게 생존한다. 이것이 Round 2 후 60% 천장의 원인이다.

**7. Watermarking이 유일하게 기술적으로 강건한 해결책이다.**
그러나 LLM 제공자의 협조가 필요하며 워터마킹 없이 생성된 텍스트를 소급 탐지할 수 없다.

---

## 4. 3대 축 업그레이드 제안

### 개요

3-Round 경험과 문헌 리뷰 결과를 종합하면, 현행 파이프라인의 한계를 극복하기 위해 세 축의 동시 업그레이드가 필요하다:

| 축 (Pillar) | 대상 에이전트 | 핵심 변경 | 해결하는 문제 |
|-------------|-------------|-----------|-------------|
| **Pillar 1**: 탐지 강화 | G5 v2.0 | 정량적 stylometric 지표 추가, 새 패턴 카테고리 S7-S10 | 구조적 패턴을 탐지하지 못함 |
| **Pillar 2**: 구조적 변환 | G6 v2.0 | Layer 3 구조적 변환 추가, burstiness 강화 | 단어/구문 수준에서만 작동 |
| **Pillar 3**: 반복 파이프라인 | Pipeline v2.0 | Multi-pass 아키텍처, 피드백 루프 | 단일 패스의 60% 천장 |

---

### Pillar 1: 탐지 강화 (G5 v2.0)

패턴 기반 탐지에 **정량적 stylometric 지표**를 추가하여 탐지 정확도와 범위를 확장한다.

#### 4.1.1 새로운 정량적 지표 모듈 (New Quantitative Metrics Module)

**연구 근거**: GPTZero는 perplexity + burstiness를 사용한다. MTLD는 유일하게 텍스트 길이에 불변인 어휘 다양성 지표다(McCarthy & Jarvis, 2010). Fano Factor >1은 인간적 분산을 나타낸다.

```yaml
quantitative_metrics:
  burstiness:
    method: "coefficient_of_variation"  # CV = SD(sentence_lengths) / Mean(sentence_lengths)
    human_baseline: ">0.45"
    ai_typical: "<0.30"
    weight_in_score: 15
    해석: |
      CV가 0.45 이상이면 인간적 문장 길이 변동을 나타냄.
      CV가 0.30 미만이면 AI의 전형적인 균일한 문장 길이를 시사함.
      AI는 중간 길이 문장(15-25단어)을 선호하는 반면,
      인간은 짧은 선언문(3-5단어)과 긴 복합문(30-50단어)을 혼합함.

  vocabulary_diversity:
    method: "MTLD"  # Measure of Textual Lexical Diversity (길이 불변)
    human_baseline: ">80"
    ai_typical: "<60"
    weight_in_score: 10
    해석: |
      MTLD는 TTR 임계값 이상을 유지하는 순차 문자열의 평균 길이.
      McCarthy & Jarvis(2010)가 검증한 유일한 길이 불변 어휘 다양성 지표.
      AI 텍스트는 일반적으로 낮은 어휘 다양성을 보이며,
      특히 학술 글쓰기에서 맥락적 적절성이 떨어짐.

  sentence_length_range:
    method: "max_minus_min_word_count"
    human_baseline: ">25 word spread"
    ai_typical: "<15 word spread"
    weight_in_score: 5
    해석: |
      문서 내 가장 긴 문장과 가장 짧은 문장의 단어 수 차이.
      인간 작성 텍스트는 2단어 선언문부터 60단어 복합문까지 광범위.
      AI 텍스트는 15-35단어 범위에 집중되어 범위가 좁음.

  paragraph_opener_diversity:
    method: "unique_first_3_words / total_paragraphs"
    human_baseline: ">0.70"
    ai_typical: "<0.50"
    weight_in_score: 8
    해석: |
      각 문단의 첫 3단어가 고유한 비율.
      AI는 "The results..." "The analysis..." "The findings..."와 같이
      반복적 문단 도입부를 생성하는 경향이 있음.
```

#### 4.1.2 새로운 탐지 카테고리 (S7-S10)

Round 3에서 수동으로 발견된 패턴을 기반으로, 구조적 수준의 탐지 카테고리 4개를 추가한다:

| 새 패턴 | ID | Weight | 설명 | 탐지 기준 |
|---------|-----|--------|------|-----------|
| **Enumeration as Prose** | S7 | 12 | 산문 내 "First,...Second,...Third,..." | 명시적 목록이 아닌 문단 내 순서 마커 3개 이상 |
| **Repetitive Paragraph Openers** | S8 | 10 | "The [X]..." 패턴의 3개 이상 연속 문단 | 연속 문단 첫 3단어의 구조적 유사도 |
| **Formulaic Section Structure** | S9 | 8 | Discussion의 템플릿 구조: restate → compare → implications → limitations → future | 섹션 내 하위 구조의 예측 가능한 순서 |
| **Hypothesis Checklist Pattern** | S10 | 10 | "H1 was supported. H2 was partially supported. H3 was not supported." | 가설 확인의 기계적 나열 |

**S7 탐지 로직 상세:**

```python
def detect_s7_enumeration(text):
    """산문 내 열거 패턴 탐지"""
    ordinal_markers = [
        r'\bFirst(?:ly)?,',
        r'\bSecond(?:ly)?,',
        r'\bThird(?:ly)?,',
        r'\bFourth(?:ly)?,',
        r'\bFifth(?:ly)?,',
    ]
    # 명시적 목록(bullet points, numbered lists) 제외
    # 연속된 문단이 아닌 동일 문단 또는 연속 문단 내 마커
    # 3개 이상의 순서 마커가 산문 내에 존재하면 플래그
    pass
```

**S8 탐지 로직 상세:**

```python
def detect_s8_repetitive_openers(paragraphs):
    """반복적 문단 도입부 탐지"""
    first_words = [get_first_n_words(p, 3) for p in paragraphs]
    # "The [명사]..." 패턴 추출
    # 구조적 유사도 계산 (POS 태그 기반)
    # 연속 3개 이상 동일 패턴이면 플래그
    # 예: "The results...", "The analysis...", "The findings..."
    pass
```

#### 4.1.3 업데이트된 점수 산출 알고리즘

**현행 알고리즘:**

```
AI_Probability = SUM(pattern_weight * frequency) / max_score * 100
```

**제안 복합 점수:**

```
AI_Probability = (0.60 * pattern_score)
              + (0.20 * burstiness_penalty)
              + (0.10 * vocab_diversity_penalty)
              + (0.10 * structural_penalty)
```

각 구성요소의 계산:

```python
# pattern_score: 현행 G5 알고리즘 (0-100 정규화)
pattern_score = current_g5_algorithm(text)  # normalized 0-100

# burstiness_penalty: CV가 인간 기준(0.45) 미달 시 페널티
burstiness_penalty = max(0, (0.45 - CV) / 0.45 * 100)
# CV > 0.45이면 0 (페널티 없음)
# CV = 0이면 100 (최대 페널티)
# CV = 0.30이면 약 33 (중간 페널티)

# vocab_diversity_penalty: MTLD가 인간 기준(80) 미달 시 페널티
vocab_diversity_penalty = max(0, (80 - MTLD) / 80 * 100)
# MTLD > 80이면 0 (페널티 없음)
# MTLD = 0이면 100 (최대 페널티)
# MTLD = 60이면 25 (중간 페널티)

# structural_penalty: S7-S10 가중 점수 (0-100 정규화)
structural_penalty = normalize_0_100(
    S7_weight * S7_count +
    S8_weight * S8_count +
    S9_weight * S9_count +
    S10_weight * S10_count
)
```

**가중치 배분 근거:**

| 구성요소 | 가중치 | 근거 |
|----------|--------|------|
| pattern_score | 0.60 | 기존 24개 패턴의 검증된 탐지력 보존 |
| burstiness_penalty | 0.20 | 문헌에서 가장 강력한 정량적 신호 (GPTZero의 핵심 지표) |
| vocab_diversity_penalty | 0.10 | MTLD는 보완적 신호이나 분야별 변동 있음 |
| structural_penalty | 0.10 | 새 카테고리이므로 보수적 시작, 검증 후 조정 |

#### 4.1.4 비원어민 화자 보정 (Non-Native Speaker Calibration)

**연구 근거**: Liang et al.(2023)은 TOEFL 에세이의 61% 이상이 AI로 오분류됨을 발견했다. 비원어민 학술 영어는 자연적으로 낮은 어휘 다양성과 더 규칙적인 문장 패턴을 보이며, 이것이 AI 특성과 겹친다.

```yaml
non_native_calibration:
  enabled: false  # 사용자 opt-in (기본 비활성)
  adjustments:
    L1_weight: "x 0.7"    # 어휘 플래그 30% 감소
    H1_weight: "x 0.8"    # 장황한 구문 플래그 20% 감소
    burstiness_threshold: "0.35"  # 비원어민 기준선 하향 (0.45 → 0.35)
  rationale: >
    비원어민 학술 영어는 자연적으로 낮은 어휘 다양성과
    더 규칙적인 문장 패턴을 보인다. 이 보정은 이러한
    자연적 특성이 AI 사용으로 오분류되는 것을 방지한다.
  activation: >
    사용자가 G5 실행 시 --non-native 플래그를 설정하거나
    파이프라인 설정에서 non_native_mode: true를 지정한다.
```

---

### Pillar 2: 구조적 변환 (G6 v2.0)

단어/구문 치환을 넘어 **심층 구조적 변환 역량**을 추가한다.

#### 4.2.1 새로운 변환 레이어: Layer 3 — Structural Transformation

현행 G6는 두 레이어에서 작동한다:
- **Layer 1**: Word substitution (L1 어휘 → 대안)
- **Layer 2**: Phrase restructuring (H1 장황 → 간결, C1 과장 → 중립)

**추가할 Layer 3: Structural Transformation** — 문단/섹션 수준에서 작동:

---

**S7 Enumeration Dissolution: 열거 구조를 흐르는 산문으로 전환**

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

변환 원칙:
- 순서 마커(First, Second, Third) 완전 제거
- 인과적/대조적 연결어로 대체 ("but", "one that", "even after")
- 발견 간의 의미적 관계를 명시적으로 표현
- 문장 길이 변동 도입

---

**S8 Paragraph Opener Variation: 반복적 문단 도입부 다양화**

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

변환 원칙:
- 질문으로 시작하는 문단 도입
- 소유격/형용사 구문 활용 ("Education's role")
- 동명사구 활용 ("Decomposing the partisan gap")
- 예고/놀라움 표현 도입 ("something unexpected")
- 문단 도입부의 문법적 구조를 최소 4가지 이상 혼합

---

**S9 Discussion Architecture: 정형화된 Discussion 구조 해체**

Before:
```
The present study examined... Our findings are consistent with...
```

After:
```
Why do Democrats and Republicans -- who agree on almost nothing -- both
worry about AI at nearly identical rates?
```

변환 원칙:
- 요약 재진술 대신 도발적 질문이나 놀라운 발견으로 시작
- 독자의 직관에 도전하는 프레이밍
- 구체적 수치나 사례로 즉시 진입
- "The present study..."와 같은 자기 참조적 도입부 제거

---

**S10 Hypothesis Narrative: 가설 확인 체크리스트를 서사로 전환**

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

변환 원칙:
- H1/H2/H3 라벨 제거
- 구체적 수치(effect sizes, AMEs)를 서사적 앵커로 활용
- 예상과 다른 결과("surprised us")로 지적 긴장감 생성
- 관련 가설을 주제별로 그룹화
- 통계값은 100% 보존하되 서술 방식만 변경

#### 4.2.2 Burstiness 강화 지침 (Burstiness Enhancement Instructions)

```yaml
burstiness_enhancement:
  description: "의도적으로 문장 길이를 변동시켜 CV를 증가시킴"
  target_cv: ">0.45"
  strategies:
    - strategy: "짧은 선언문 삽입"
      detail: "임팩트 포인트에 2-5단어 선언문 삽입"
      example: '"That gap is real." / "The data say otherwise."'

    - strategy: "긴 복합문 허용"
      detail: "섹션당 1-2개의 40-60단어 복합문 허용"
      example: "종속절 체인과 삽입구를 활용한 확장 문장"

    - strategy: "중간 길이 문장 분해"
      detail: "15-25단어 문장을 더 짧거나 더 긴 형태로 분해"
      example: "균일한 리듬을 깨기 위한 의도적 재구성"

    - strategy: "전략적 문장 단편 사용"
      detail: "강조를 위해 문장 단편(fragment)을 전략적으로 사용"
      example: '"Not even close." / "A pattern worth noting."'

    - strategy: "문단 길이 변동"
      detail: "2문장 문단과 6문장 문단을 교대"
      example: "짧은 임팩트 문단과 상세 분석 문단의 교대"
```

**목표 문장 길이 분포:**

```
목표 CV > 0.45 달성을 위한 이상적 분포:
  - 매우 짧은 문장 (2-8 words):   ~10-15%
  - 짧은 문장 (9-15 words):       ~20-25%
  - 중간 문장 (16-30 words):      ~35-40%
  - 긴 문장 (31-45 words):        ~15-20%
  - 매우 긴 문장 (46+ words):     ~5-10%
```

#### 4.2.3 섹션 인식 모드 에스컬레이션 (Section-Aware Mode Escalation)

**현행**: 사용자가 전체 문서에 대해 하나의 모드를 선택한다.

**제안**: G5 섹션별 점수를 기반으로 자동 섹션별 모드 에스컬레이션을 적용한다.

```yaml
section_aware_escalation:
  abstract:
    base_mode: conservative
    escalate_to: balanced
    trigger: "section_score > 50"
    rationale: "Abstract은 가장 높은 심사를 받지만 구조적 규칙은 수용됨"

  introduction:
    base_mode: balanced
    escalate_to: balanced  # 에스컬레이션 없음
    trigger: null
    rationale: "Introduction은 일정한 격식이 예상됨"

  methods:
    base_mode: conservative
    escalate_to: conservative  # 에스컬레이션 절대 불가
    trigger: null
    rationale: "Methods의 템플릿 언어는 정상; 과도한 변환은 정확도 위험"

  results:
    base_mode: conservative
    escalate_to: balanced
    trigger: "section_score > 60"
    rationale: "Results는 프레이밍 언어만 변환; 데이터 서술은 보존"

  discussion:
    base_mode: balanced
    escalate_to: aggressive
    trigger: "section_score > 50"
    rationale: "Discussion이 구조적 변환에서 가장 큰 혜택을 받음"

  conclusion:
    base_mode: balanced
    escalate_to: aggressive
    trigger: "section_score > 50"
    rationale: "Conclusion은 Discussion과 유사한 패턴 프로필"
```

**에스컬레이션 결정 흐름:**

```
G5 섹션별 분석 완료
    |
    v
각 섹션에 대해:
    IF section_score > escalation_trigger:
        mode = escalated_mode
    ELSE:
        mode = base_mode
    |
    v
G6에 섹션별 mode_map 전달:
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

### Pillar 3: 반복 파이프라인 (Pipeline v2.0)

단일 패스를 **피드백 루프가 있는 multi-pass 아키텍처**로 교체한다.

#### 4.3.1 Multi-Pass 반복 파이프라인 아키텍처

```
========================================================================
Pass 1: VOCABULARY PASS (Conservative)
========================================================================
  G5 Scan (전체)
    → G6 변환 (L1, M1, C1 대상 — 어휘 레이어만)
      → F5 Quick Verify (인용/통계 무결성만)
        |
        v
  CP_PASS1_REVIEW:
    "점수가 X%에서 Y%로 하락했습니다. 구조적 패스를 진행하시겠습니까?"
    [A] Continue to structural pass
    [B] Accept current state
    [C] View detailed diff
        |
        v (Continue 선택 시)

========================================================================
Pass 2: STRUCTURAL PASS (Balanced)
========================================================================
  G5 Scan (delta — Pass 1 이후 잔여 패턴만)
    → G6 변환 (S7-S10, CV 강화 — 구조 레이어)
      → F5 Full Verify (전체 5개 검증)
        |
        v
  CP_PASS2_REVIEW:
    "점수가 현재 Z%입니다. 목표 달성 여부?"
    [A] Accept
    [B] One more pass
    [C] Manual review
        |
        v (One more pass 선택 시, 선택적)

========================================================================
Pass 3 (선택): POLISH PASS
========================================================================
  G5 Scan (audit — 전체 재검사)
    → G6 micro fixes (잔여 패턴 대상)
      → F5 Full Verify (전체 5개 검증)
        |
        v
  CP_FINAL_REVIEW:
    최종 승인
    [A] Approve [B] View full diff [C] Revert to Pass 2
========================================================================
```

**핵심 설계 결정:**

| 결정 | 근거 |
|------|------|
| 각 패스가 다른 레이어 대상 | 어휘 → 구조 → 미세조정의 순차적 접근이 간섭을 최소화 |
| 패스 간 G5 재스캔 | 실제 진행 상황 측정; Round 3 경험에서 G6가 새 패턴을 도입할 수 있음을 확인 |
| 패스 간 인간 체크포인트 | 점수 보고와 함께 의사결정 기회 제공 |
| 최대 3회 패스 | 수확 체감(diminishing returns); 3회 이후 추가 개선 미미 |
| Pass 3은 선택적 | 점수 목표 미달 시에만 |

#### 4.3.2 새로운 체크포인트 (New Checkpoints)

```yaml
CP_PASS1_REVIEW:
  level: recommended
  description: "어휘 패스 완료 -- 구조적 패스 전 검토"
  presents:
    - Pass 1 전/후 점수
    - 잔여 패턴 목록
    - Burstiness CV 점수
    - 처리된 패턴 수 / 잔여 패턴 수
  options:
    - "Continue to structural pass"
    - "Accept current state"
    - "View detailed diff"

CP_PASS2_REVIEW:
  level: recommended
  description: "구조적 패스 완료 -- 결과 검토"
  presents:
    - 점수 추이 (original → Pass 1 → Pass 2)
    - 구조적 지표 (CV, MTLD, paragraph opener diversity)
    - S7-S10 잔여 패턴 수
  options:
    - "Accept"
    - "One more polish pass"
    - "Manual review mode"

CP_FINAL_REVIEW:
  level: optional
  description: "최종 검토 후 내보내기"
  presents:
    - 전체 점수 이력
    - Full diff report
    - F5 verification summary
    - 정량적 지표 최종값 (CV, MTLD, opener diversity)
```

#### 4.3.3 변환 후 G5 재스캔 (Post-Transformation G5 Re-Scan) — 필수

**연구 근거**: Round 3 경험에서 G6가 기존 패턴을 수정하면서 **새로운 AI 패턴을 도입**할 수 있음을 확인했다.

```yaml
post_transformation_audit:
  trigger: "모든 G6 변환 패스 후"
  agent: "G5"
  checks:
    - "새로운 HIGH-RISK 패턴이 도입되지 않았는가"
    - "새로운 패턴 카테고리가 활성화되지 않았는가"
    - "전체 점수가 감소했는가 (증가하지 않았는가)"

  on_new_patterns_found:
    action: "사용자에게 FLAG"
    message: "G6가 {M}개 패턴을 제거하면서 {N}개의 새 패턴을 도입했습니다. 순효과: {delta}"
    options:
      - "Accept (순 개선이므로 수락)"
      - "Revert this pass (이 패스 되돌리기)"
      - "Target new patterns in next pass (다음 패스에서 새 패턴 대상 설정)"

  severity_thresholds:
    info: "새 패턴 0개, 점수 감소"
    warning: "새 패턴 1-2개이나 순 점수 감소"
    error: "새 패턴 3개 이상 또는 순 점수 증가"
```

#### 4.3.4 점수 목표 시스템 (Score Target System)

```yaml
target_mode:
  enabled: true
  usage: '"Humanize to target: 30%"'
  behavior:
    1: "G5 실행 → 기준 점수 확인"
    2: "필요한 감소량 계산"
    3: "목표 달성을 위해 섹션별 모드 자동 선택"
    4: "목표 달성 또는 3-pass 한도까지 반복 패스 실행"
    5: "최종 점수 vs 목표 보고"

  presets:
    journal_safe: 30     # 동료 심사 학술지 대상
    conference: 40       # 학회 논문 대상
    working_paper: 50    # 워킹 페이퍼/프리프린트 대상

  custom_target:
    description: "사용자가 직접 목표 점수를 지정할 수 있음"
    range: "10-60"
    example: '"Humanize to target: 25%"'
```

**목표 달성 전략 자동 선택 로직:**

```python
def select_strategy(baseline_score, target_score):
    gap = baseline_score - target_score

    if gap <= 20:
        # 어휘 패스만으로 충분
        return ["Pass 1: Vocabulary (Conservative)"]
    elif gap <= 40:
        # 어휘 + 구조 패스
        return [
            "Pass 1: Vocabulary (Conservative)",
            "Pass 2: Structural (Balanced)"
        ]
    else:
        # 전체 3-pass
        return [
            "Pass 1: Vocabulary (Conservative)",
            "Pass 2: Structural (Aggressive)",
            "Pass 3: Polish"
        ]
```

---

## 5. 객관적 지표 및 벤치마크

### 5.1 성능 목표 (Performance Targets)

| 지표 | 목표 | 현재 상태 | 비고 |
|------|------|-----------|------|
| **Citation Preservation** | **100%** | Required | 절대 타협 불가 |
| **Statistics Preservation** | **100%** | Required | 절대 타협 불가 |
| **Meaning Preservation** | **>=95%** semantic similarity | Target | F5 meaning check |
| **AI Probability Reduction (Conservative)** | 20-35% | Expected | 어휘 레이어만 |
| **AI Probability Reduction (Balanced)** | 35-50% | Expected | 어휘 + 구조 |
| **AI Probability Reduction (Aggressive)** | 50-70% | Expected | 전체 변환 |
| **Pattern Reduction (Conservative)** | 50-70% | Expected | HIGH-RISK 패턴 대상 |
| **Pattern Reduction (Balanced)** | 60-80% | Expected | HIGH + MEDIUM 대상 |
| **Pattern Reduction (Aggressive)** | 80-95% | Expected | 모든 패턴 대상 |
| **G5 Analysis Time** | <30 sec per 1000 words | Target | 정량적 지표 추가로 소요 시간 증가 가능 |
| **G6 Transformation Time** | <60 sec per 1000 words | Target | Layer 3 추가로 소요 시간 증가 가능 |
| **F5 Verification Time** | <15 sec per 1000 words | Target | 기존 수준 유지 |

### 5.2 업그레이드 전후 벤치마크 비교 (Before/After Upgrade Benchmark)

| 지표 | 현행 파이프라인 | 목표 (업그레이드 후) |
|------|---------------|---------------------|
| **<35% 도달 필요 패스 수** | 3 (수동) | **2 (자동화)** |
| **도달 가능 최종 AI 점수** | 31%/22% (수동 Round 3 포함) | **<30% (자동, 수동 불필요)** |
| **Burstiness CV (humanization 후)** | 측정하지 않음 | **>0.45** |
| **MTLD (humanization 후)** | 측정하지 않음 | **>70** |
| **Paragraph opener diversity** | 측정하지 않음 | **>0.70** |
| **잔여 구조적 패턴** | 측정하지 않음 (S7-S10 미존재) | **HIGH-risk 0개** |
| **Citations preserved** | 100% | **100% (퇴행 없음)** |
| **Statistics preserved** | 100% | **100% (퇴행 없음)** |

### 5.3 예상 점수 추이 비교

**현행 파이프라인 (수동 3-Round):**

```
Paper 1: 80% ──[G6 R1]──> 62% ──[G6 R2]──> ~60% ──[Manual R3]──> 31%
Paper 2: 82% ──[G6 R1]──> 61% ──[G6 R2]──> ~60% ──[Manual R3]──> 22%

                    |--- G6 자동 처리 ---|    |-- 수동 구조 해체 --|
                        ~20pp 감소              ~30pp 감소
```

**목표 업그레이드 파이프라인 (자동 2-Pass):**

```
Paper 1: 80% ──[Pass 1: Vocab]──> ~55% ──[Pass 2: Structural]──> <30%
Paper 2: 82% ──[Pass 1: Vocab]──> ~55% ──[Pass 2: Structural]──> <30%

                |-- 어휘 레이어 --|    |-- 구조 레이어 (신규) --|
                    ~25pp 감소              ~25pp 감소
```

### 5.4 검증 프로토콜 (Validation Protocol)

업그레이드 파이프라인의 효과를 검증하기 위한 5단계 프로토콜:

| 단계 | 절차 | 측정 항목 |
|------|------|-----------|
| **1** | Paper 1, Paper 2의 원본(humanization 전) 버전 준비 | 기준 점수 확인 |
| **2** | 업그레이드 파이프라인으로 처리 (target: 30%) | 각 패스 후 점수, 패턴 수 |
| **3** | 정량적 지표 측정 | 필요 패스 수, 최종 점수, burstiness CV, MTLD |
| **4** | 무결성 검증 | Citation/statistics 무결성 (100% 필수) |
| **5** | Round 3 수동 결과(31%/22%)와 비교 | 성능 동등성 또는 초과 확인 |

**성공 기준:**

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

### 5.5 실패 시 대응 (Fallback Strategy)

자동화된 2-pass로 목표 미달 시:

| 상황 | 대응 |
|------|------|
| Pass 2 후 점수 30-35% | Pass 3 (Polish) 자동 실행 |
| Pass 3 후에도 >35% | 사용자에게 수동 검토 권장, 잔여 패턴 상세 보고 |
| 무결성 위반 감지 | 해당 패스 즉시 revert, 위반 항목 보고 |
| 새 패턴 도입 (순 점수 증가) | 해당 패스 revert, 대안 전략 제안 |

---

## 6. 참고 문헌

### AI 텍스트 탐지 및 편향

1. Liang, W., Yuksekgonul, M., Mao, Y., Wu, E., & Zou, J. (2023). GPT detectors are biased against non-native English writers. *arXiv:2304.02819*.

2. Popkov, A. et al. (2024). Median 27.2% false positive rate across free AI detectors on pre-ChatGPT human academic texts.

3. Stanford HAI. (2025). AI-Detectors biased against non-native English writers. *Stanford University Human-Centered Artificial Intelligence*.

4. IACIS. (2025). Critical look at reliability of AI detection tools. *Proceedings of IACIS 2025*.

### Paraphrasing 및 우회

5. Krishna, K., Song, Y., Karpinska, M., Wieting, J., & Iyyer, M. (2023). Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense. *Advances in Neural Information Processing Systems (NeurIPS)*. arXiv:2303.13408.

6. Adversarial Paraphrasing. (2025). A universal attack for humanizing AI-generated text. *arXiv:2506.07001*.

7. Contrastive Paraphrase Attacks on LLM Detectors. (2025). *arXiv:2505.15337*.

8. On the Detectability of LLM-Generated Text. (2025). *arXiv:2510.20810*.

### 탐지 방법론 및 특성

9. Mitchell, E. et al. DetectGPT: Zero-shot machine-generated text detection using probability curvature.

10. Feature-Based Detection: Stylometric and Perplexity Markers. (2024). *ResearchGate*.

11. Detecting AI-Generated Text with Pre-Trained Models. (2024). *ACL Anthology*.

12. Generative AI models and detection: tokenization and dataset size. (2024). *Frontiers in AI*.

13. Aggregated AI detector outcomes in STEM writing. (2024). *American Physiological Society*.

### AI 어휘 및 언어 패턴

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

### 어휘 다양성 및 Stylometrics

25. McCarthy, P. M. & Jarvis, S. (2010). MTLD, vocd-D, and HD-D: A validation study of sophisticated approaches to lexical diversity assessment. *Behavior Research Methods, 42*(2), 381-392.

26. MATTR: Pros and cons. (2024). *ResearchGate*.

27. Vocabulary Quality in NLP: Autoencoder-Based Framework. (2024). *Springer*.

### 비원어민 화자 및 L2 연구

28. Lexical diversity, syntactic complexity: ChatGPT vs L2 students. (2025). *Frontiers in Education*.

29. More human than human? ChatGPT and L2 writers. (2024). *De Gruyter*.

### 학술 특화 탐지

30. Accuracy-bias trade-offs in AI text detection and scholarly publication fairness. (2024). *PMC*.

31. Characterizing AI Content Detection in Oncology Abstracts 2021-2023. (2024). *PMC*.

32. Distinguishing academic science writing with >99% accuracy. (2023). *PMC*.

### 상업 탐지기 비교

33. Originality.AI — AI Detection Studies Meta-Analysis.

34. GPTZero vs Copyleaks vs Originality comparison.

35. AI vs AI: Turnitin, ZeroGPT, GPTZero, Writer AI. (2024). *ResearchGate*.

### Discourse 및 Paraphrasing 패턴

36. How AI Tools Affect Discourse Markers When Paraphrased. (2024). *ResearchGate*.

37. Netus AI — How stylometric patterns survive paraphrasing.

38. Deep Dive Into AI Text Fingerprints. *Hastewire*.

---

> **문서 끝** | 관련 문서: [research-literature-review.md](./research-literature-review.md), [round3-strategy.md](./round3-strategy.md)
> **구현 로드맵**: [../roadmap/TODO.md](../roadmap/TODO.md)
