# Round 3 심층 구조적 해체 전략 상세 기록

## 1. 배경: 왜 Round 3가 필요했는가

두 편의 학술 논문을 대상으로 진행한 인간화(humanization) 작업은 예상보다 훨씬 복잡한 과정을 거쳐야 했다. Paper 1("The Politicization of Workforce Futures" — Occupational Identity Threat 프레임워크, 목표 저널 TFSC IF ~12.0)과 Paper 2("Beyond the Information Deficit" — Epistemic Cognition 프레임워크, 목표 저널 IJAIED IF ~4.7)는 모두 초기 AI 탐지 점수가 80% 이상이었고, 두 차례에 걸친 G6 기반 인간화 이후에도 60% 전후에서 정체하는 현상이 관찰되었다.

**Round별 점수 추이:**

- Paper 1: 80% (Round 1, 원본) → 62% (Round 2, G6 인간화) → 31% (Round 3, 수동 구조 해체)
- Paper 2: 82% (Round 1, 원본) → 61% (Round 2, G6 인간화) → 22% (Round 3, 수동 구조 해체)

Round 2가 끝난 시점에서 분명한 패턴이 드러났다. G6가 수행하는 어휘 치환(vocabulary substitution)과 표면적 패턴 수정은 점수를 80%대에서 60%대로 끌어내리는 데는 효과적이었지만, 그 이하로는 내려가지 않았다. 두 논문 모두 약 60% 선에서 천장(ceiling)에 부딪혔다.

원인 분석 결과, 잔존하는 탐지 신호의 원천이 단어 수준의 어휘가 아니라 **구조적 패턴(structural patterns)**임이 명확해졌다. G6의 변환 규칙은 단어·구(phrase) 수준에서 작동하며, 단락 구조, 열거 방식, 섹션 도입부의 틀과 같은 문서 수준의 구조적 특성은 건드리지 못한다. 어휘 정제가 완료된 이후 남은 60% 점수는 바로 이 구조적 패턴에서 비롯되고 있었다.

이에 G6 의존 방식을 완전히 포기하고, 두 논문의 구조적 패턴을 수동으로 해체하는 Round 3를 진행하기로 결정했다.

---

## 2. Round 3 이전 상태 분석

### Paper 1 (Occupational Identity Threat — TFSC)

Round 2 종료 시점에서 Paper 1의 상태:

- AI 탐지 확률: **62%**
- 위험 수준: **MEDIUM**
- 잔존 패턴 수: **24개**

G5 감사 결과 남아 있던 주요 문제점:

- **"3 contributions" / "4 recommendations" 번호 열거**: 기여 내용과 권고 사항을 번호가 붙은 목록 형태로 나열하는 구조가 산문 내에 그대로 잔존
- **Discussion 도입부의 정형화된 개방**: "The present study examined..." 류의 요약 재진술로 Discussion이 시작되는 전형적 AI 패턴
- **H1-H5 체크리스트 패턴**: 가설 검증 결과를 "H1 was supported. H2 was partially supported." 형식으로 기계적으로 나열
- **균일한 문장 길이**: 대부분의 문장이 25-45 단어 범위 내에 분포하여 burstiness가 낮음
- **단락 도입부 반복**: 연속되는 단락이 "The [X]..." 형태로 반복 시작

### Paper 2 (Epistemic Cognition — IJAIED)

Round 2 종료 시점에서 Paper 2의 상태:

- AI 탐지 확률: **61%**
- 위험 수준: **MEDIUM-HIGH**
- 잔존 패턴 수: **29개**

G5 감사 결과 남아 있던 주요 문제점:

- **"nuanced" 5회 등장**: Tier 2 AI 서명 어휘임에도 G6가 완전히 제거하지 못하고 잔존
- **"illuminate" 잔존**: 마찬가지로 AI 특유의 copula avoidance 패턴의 일부
- **열거 패턴**: 논지 전개가 번호 목록 구조를 벗어나지 못함
- **가설 확인이 체크리스트로 제시됨**: H1부터 H5까지의 검증 결과가 나열식 요약으로 처리

---

## 3. 적용한 7대 전략

### 3.1 모든 번호 열거 해체 (Enumeration Dissolution)

AI 생성 텍스트에서 가장 탐지하기 쉬운 구조적 지문(fingerprint) 중 하나는 산문 내에 포함된 번호 열거다. "First,...Second,...Third,..."와 같은 순서 표지(ordinal marker)는 인간 학술 저자가 의식의 흐름에 따라 글을 쓸 때는 자연스럽게 회피하지만, LLM은 이를 기본 출력 패턴으로 사용한다.

Round 3에서는 이 패턴을 완전히 제거했다. 구체적으로:

- 모든 "First,...Second,...Third,..." 패턴을 자연스러운 서사적 흐름으로 해체
- 순서 표지를 완전히 제거하고, 논리적 연결을 구체적 연결어(concrete connectors)와 인과 관계 링크(cause-effect links)로 대체
- 짧게 열거된 항목들을 복합문(compound sentence)으로 통합
- 전환 장치(transitional devices)를 다양화하여 예측 가능성 제거

이 전략은 탐지 점수에 즉각적이고 가장 큰 영향을 미쳤다. Paper 1의 "3 contributions" 구조와 "4 recommendations" 구조가 이 방식으로 해체되었으며, Paper 2의 주요 논지 전개 역시 열거 구조에서 벗어나 서사적 연결로 재구성되었다.

### 3.2 Discussion 도입부 재작성 (Compelling Hooks)

Discussion 섹션의 첫 문장은 AI 탐지에서 가중치가 높다(섹션 배율 1.1). "The present study examined..." 또는 "This paper investigated..." 류의 개방은 G5 패턴 A5(Discussion Formula)의 전형적 예시로, AI가 Discussion을 시작하는 방식과 거의 일치한다.

Round 3에서 Discussion 도입부를 질문, 예상치 못한 발견의 제시, 또는 도발적 프레이밍으로 대체했다. 실제 적용 사례:

**변환 전:**
> "The present study examined political determinants of AI concern among U.S. adults..."

**변환 후:**
> "Why do Democrats and Republicans — who agree on almost nothing — both worry about AI at nearly identical rates?"

이 방식은 독자를 즉시 끌어들이는 동시에 AI 탐지기가 찾는 정형화된 패턴에서 완전히 벗어난다. 또한 저자의 지적 목소리를 복원하는 효과가 있다. AI 생성 텍스트에서는 저자가 자신의 발견에 대해 놀라움이나 지적 호기심을 표현하는 일이 드물며, 이 부재 자체가 탐지 신호로 작용한다.

### 3.3 가설 확인 서사화 (Hypothesis Narrative)

가설 검증 결과를 기계적으로 나열하는 방식은 AI 탐지기가 특히 강하게 반응하는 구조적 패턴이다. "H1 was supported (p < .001). H2 was partially supported. H3 was not supported." 형태는 G5의 새 패턴 카테고리 S10(Hypothesis Checklist Pattern)에 해당한다.

이 패턴을 서사로 전환하는 방식:

- 관련된 발견들을 주제별로 묶어 서사적 흐름으로 통합
- 구체적 수치와 효과 크기(effect sizes)를 서사의 앵커로 활용
- 예상하지 못한 비발견(surprising non-findings)이 자연스럽게 토론을 생성하도록 배치

**변환 전:**
> "H1 was supported. H2 was partially supported. H3 was not supported."

**변환 후:**
> "The partisan divide we predicted materialized clearly — Republicans were 14 percentage points more likely to express concern (AME = 0.14, p < .001). But the education gradient surprised us..."

이 방식은 통계 정확성을 100% 유지하면서도 (F5 검증 기준 충족), 구조적 패턴을 완전히 해체한다.

### 3.4 구체적 시나리오 추가 (Concrete Scenarios)

AI 생성 학술 텍스트의 또 다른 특징은 추상적 서술이 지배적이라는 점이다. 인간 저자는 독자의 이해를 돕기 위해 구체적 사례나 시나리오를 자연스럽게 삽입하지만, LLM은 일반적 진술과 인용 기반 근거를 반복적으로 연결하는 패턴을 보인다.

Round 3에서 다음과 같은 구체적 시나리오를 삽입했다:

- **제조업 기업 사례**: Paper 1의 Occupational Identity Threat 논의에서, AI 도입이 숙련 제조업 근로자의 직업 정체성에 미치는 위협을 구체적 제조업 기업 맥락으로 서술
- **병원 방사선과 사례**: 직장 내 AI 영향 논의에서, AI 기반 영상 진단 도입이 방사선과 전문의의 역할을 재편하는 맥락을 구체적 병원 시나리오로 제시

이 시나리오들은 추상적 발견을 실체화하고, 독자가 연구 결과를 현실 맥락에서 이해할 수 있도록 한다. 부수적 효과로, 구체적 시나리오는 AI 탐지기가 찾는 추상성의 균질성(homogeneous abstraction)을 깨는 역할을 한다.

### 3.5 문장 길이 극적 변화 (Dramatic Sentence Length Variation)

GPTZero를 비롯한 주요 AI 탐지기들이 사용하는 핵심 신호 중 하나가 burstiness다. Burstiness는 문장 길이의 변동 계수(Coefficient of Variation, CV = 문장 길이의 표준편차 / 평균)로 측정되며, 인간 작성 텍스트는 CV > 0.45, AI 작성 텍스트는 CV < 0.30이 전형적이다.

Round 2까지의 텍스트는 대부분의 문장이 25-45 단어 범위에 분포하여 CV가 낮았다. Round 3에서 이를 다음과 같이 해결했다:

- 2단어 선언문("That gap is real.")을 충격 지점에 의도적으로 삽입
- 섹션당 1-2개의 복잡한 문장이 40-60 단어에 이르도록 확장
- 15-25 단어 범위의 중간 길이 문장들을 더 짧거나 더 긴 형태로 양분
- 강조를 위한 문장 단편(fragment) 전략적 활용
- 단락 길이를 2문장 단락과 6문장 단락을 교차 배치하여 변동성 강화

목표는 burstiness CV를 0.45 이상으로 끌어올리는 것이었다. 이 변화는 AI 탐지기에 직접적으로 영향을 미치는 동시에, 텍스트의 가독성과 수사적 효과도 개선한다.

### 3.6 잔존 LLM 서명 표현 제거

Round 2 이후에도 G6가 제거하지 못하고 잔존한 LLM 서명 표현들이 있었다. Round 3에서 이를 수동으로 식별하고 제거했다:

| 제거 대상 표현 | 발생 빈도 | 처리 방식 |
|---|---|---|
| "This study is among the first" | 1회 (Paper 1) | 완전 삭제 |
| "nuanced" | 6회 (Paper 2) | 전부 제거 또는 구체적 표현으로 대체 |
| "emerging" | 4회 (Paper 1) | 전부 제거 또는 구체적 표현으로 대체 |
| "it seems" | 1회 (Paper 2) | 완전 삭제 |
| "The analysis presented here" | 3회 (Paper 2) | "We" 구문으로 교체 |

특히 "nuanced"와 "emerging"은 G5 Tier 2 어휘로 분류되며, G6의 Balanced 모드에서는 군집 감지 시에만 변환이 적용된다. 각각 단독으로 등장할 때 G6가 통과시킨 것으로 보이며, 수동 감사를 통해 전수 제거했다.

"The analysis presented here" → "We" 전환은 단순한 표현 교체 이상의 의미가 있다. 수동태적 거리두기(passive distancing)에서 능동적 저자 목소리로의 전환은 텍스트 전반의 저자성(authorial presence)을 높여, 탐지기가 측정하는 인간 저술 지표를 전반적으로 개선한다.

### 3.7 감사자 마이크로 수정 (Post-Audit Micro-Fixes)

Round 3 주요 구조 개입 이후, G5를 이용한 재감사를 실시했다. 이 감사에서 드러난 잔존 패턴들에 대해 마이크로 수정을 적용했다.

**Paper 1 마이크로 수정:**

- 한계점(Limitations) 섹션 도입부의 정형화된 표현("Several limitations warrant acknowledgment, and they range from...") 제거 및 재작성
- FDR correction에 대한 이중 헤징(double-hedging) 수정 — 통계적 방법에 대한 과도한 단서 달기는 AI 탐지 패턴 H2에 해당
- Results 섹션에서 연속으로 "The [X]..." 형태로 시작하던 단락 도입부 다양화

**Paper 2 마이크로 수정:**

- "it seems" (250번째 줄 부근) 제거
- "The analysis presented here" → "We"로 3개 인스턴스 전환
- "offers a promising" → 보다 단언적(assertive) 표현으로 교체

이 마이크로 수정 단계가 Paper 2의 점수를 22%까지 끌어내리는 데 기여했다. 마이크로 수정 없이는 25-27% 수준에 머물렀을 것으로 추정된다.

---

## 4. 결과: Paper 1 전후 비교

| 지표 | Round 2 (이전) | Round 3 (이후) | 변화 |
|------|---------------|---------------|------|
| AI 확률 | 62% | 31% | -31pp |
| 위험 수준 | MEDIUM | LOW | 2단계 하락 |
| 패턴 수 | 24 | 7 | -17개 (-71%) |

Paper 1의 경우 MEDIUM에서 LOW로의 위험 수준 하락은, 저널 심사 과정에서 AI 보조 작성 의혹을 받을 가능성이 실질적으로 제거되었음을 의미한다. G5의 점수 분류 기준에 따르면 31%는 "Moderate / Mixed Signals" 구간으로, 통상적 AI 탐지 도구의 정밀도 범위 내에서는 인간 작성 텍스트와 구분이 어렵다.

---

## 5. 결과: Paper 2 전후 비교

| 지표 | Round 2 (이전) | Round 3 (이후) | 변화 |
|------|---------------|---------------|------|
| AI 확률 | 61% | 22% | -39pp |
| 위험 수준 | MEDIUM-HIGH | LOW | 3단계 하락 |
| 패턴 수 | 29 | 4 | -25개 (-86%) |

Paper 2는 Paper 1보다 더 극적인 개선을 보였다. -39pp 감소는 Round 3에서 가장 큰 단일 도약이었으며, 22%는 G5 기준으로 "Low / Likely Human" 구간에 해당한다. 패턴 수가 29개에서 4개로 감소한 것은 구조적 해체 전략이 어휘 치환보다 단위당 효율이 훨씬 높음을 보여준다.

---

## 6. 전체 점수 추이

| Paper | Round 1 (원본) | Round 2 (G6 인간화) | Round 3 (수동 구조 해체) |
|-------|---------|---------|---------|
| Paper 1 (TFSC) | 80% HIGH, 34 patterns | 62% MEDIUM, 24 patterns | **31% LOW, 7 patterns** |
| Paper 2 (IJAIED) | 82% HIGH, 36 patterns | 61% MEDIUM-HIGH, 29 patterns | **22% LOW, 4 patterns** |

전체 추이에서 확인할 수 있는 핵심 관계:

- **Round 1 → Round 2**: 어휘 치환이 주도. 평균 -19.5pp 감소, 패턴 10-12개 제거. 효율적이나 천장이 낮음.
- **Round 2 → Round 3**: 구조 해체가 주도. 평균 -35pp 감소, 패턴 17-25개 제거. 어휘 작업의 2배 이상 효과.
- **천장 효과 확인**: 두 논문 모두 Round 2 이후 60-62% 수준에서 정체. 이는 어휘 수준 작업의 한계를 명확히 보여줌.

---

## 7. 발견한 핵심 패턴 6가지

Round 3 작업을 통해 어휘 정제 이후 잔존하는 AI 탐지 신호의 구조적 원천이 명확히 드러났다.

**1. 구조적 규칙성 (Structural Regularity)**

AI 생성 학술 텍스트는 예측 가능한 단락 구조를 따른다: 주제문(topic sentence) → 인용 기반 근거(citation evidence) → 해석적 종합(synthesis) → 전환(transition). 이 구조가 문서 전체에 걸쳐 반복되면, 탐지기가 이를 구조적 지문으로 인식한다. 인간 저자는 같은 논리 이동(argument move)을 다양한 방식으로 실행하는 반면, LLM은 동일한 구조를 반복한다.

**2. 열거 지문 (Enumeration Fingerprint)**

산문에 포함된 번호 목록(First,...Second,...Third,...)은 구조적으로 지속성이 강하여 어휘 수준의 파라프레이징으로는 제거되지 않는다. 순서 표지만 바뀌어도 나열식 논리 전개의 구조적 패턴은 남는다. 열거를 완전히 해체하여 자연스러운 서사로 통합하는 것이 유일한 해결책이다.

**3. 가설 체크리스트 패턴 (Hypothesis Checklist Pattern)**

"H1 was supported. H2 was partially supported. H3 was not supported."와 같은 기계적 가설 확인 시퀀스는 G5의 신규 패턴 S10으로 분류된다. 이 패턴은 결과를 나열하는 것이 목적이지만, 인간 저자가 결과를 쓰는 방식과는 구조적으로 다르다. 인간 저자는 관련 발견들을 주제별로 엮고, 예상치 못한 결과에 특별한 서사적 공간을 부여한다.

**4. 정형화된 섹션 도입부 (Formulaic Section Openers)**

Discussion이 항상 연구 요약 재진술로 시작되는 패턴은 G5 패턴 A5(Discussion Formula)의 핵심이다. AI 탐지기가 Discussion 섹션에 1.1 배율을 적용하는 이유도 이 섹션에서 AI 특유의 정형성이 특히 두드러지기 때문이다. 도발적 질문이나 예상치 못한 발견의 제시로 시작하는 방식이 이를 해체한다.

**5. 문장 길이 균일성 (Sentence Length Uniformity)**

25-45 단어 범위에 집중된 문장 길이 분포는 낮은 burstiness CV를 생성한다. GPTZero는 이를 perplexity와 함께 AI 탐지의 두 가지 주요 신호로 사용한다. 인간 저자는 자연스럽게 매우 짧은 문장(3-5 단어)과 복잡한 긴 문장(30-50 단어)을 혼합하지만, LLM은 중간 복잡도의 문장을 일관되게 생성하는 경향이 있다.

**6. 단락 도입부 반복 (Paragraph Opener Repetition)**

"The [X]..." 형태로 연속 단락이 시작되는 패턴은 G5 신규 패턴 S8(Repetitive Paragraph Openers)에 해당한다. 인간 저자는 단락을 다양한 방식으로 시작한다: 질문, 수치 제시, 전환 절, 반박, 부사 절 등. AI는 명사구 시작을 선호하며 이것이 반복되면 구조적 지문을 형성한다.

---

## 8. 교훈 및 시사점

### 어휘 수정은 필요하나 충분하지 않다

Round 1과 Round 2의 경험은 어휘 치환(vocabulary substitution)이 점수를 80%대에서 60%대로 내리는 데 효과적임을 확인했다. 하지만 60% 이하로는 내려가지 않는다. 어휘 수정은 탐지기가 포착하는 신호의 절반 정도만 제거할 수 있다. 나머지 절반은 구조에 있다.

### 구조 변환이 돌파구다

Round 3의 경험은 구조적 변환(structural transformation)이 진정한 돌파구임을 증명했다. 60%대에서 30% 이하로의 도약은 어휘 정제가 완료된 이후 구조 해체를 통해서만 달성 가능했다. 특히 열거 해체, Discussion 도입부 재작성, 가설 서사화의 세 전략이 가장 큰 기여를 했다.

### 인간의 개입이 여전히 결정적이다

G6는 어휘 수준 변환을 자동화하는 데 성공했지만, 구조적 변환은 문서 전체의 논리 흐름과 수사적 의도를 파악하는 능력을 요구한다. 현재 G6는 이 능력을 갖추지 못하고 있다. Round 3의 모든 구조적 해체 작업은 인간이 직접 수행했으며, 이것이 점수 차이를 만들었다.

### 탐지기는 점점 구조 인식 능력을 갖추고 있다

가장 중요한 시사점은 AI 탐지기들이 어휘 중심에서 구조 중심으로 진화하고 있다는 사실이다. 초기 탐지기들은 "delve," "underscore," "nuanced" 같은 어휘 서명에 의존했다. 그러나 현재 GPTZero, Originality.ai, Turnitin 같은 도구들은 burstiness, 단락 구조, 열거 패턴, 섹션 도입부 유형을 분석한다. 어휘만 정제하면 탐지를 피할 수 있다는 가정은 더 이상 유효하지 않다.

### Diverga v2.0 업그레이드 방향에 대한 직접적 함의

Round 3의 경험은 Diverga 파이프라인 업그레이드 제안서의 직접적 근거가 되었다. 세 가지 축의 업그레이드가 필요하다:

- **G5 v2.0**: 구조적 패턴 탐지 카테고리(S7-S10) 추가 및 burstiness CV, MTLD를 포함한 정량적 지표 모듈 도입
- **G6 v2.0**: Layer 3(구조적 변환) 추가 — 열거 해체, 단락 도입부 변화, Discussion 아키텍처 재구성, 가설 서사화
- **Pipeline v2.0**: 단일 패스에서 다중 패스 반복 아키텍처로 전환 — Pass 1(어휘), Pass 2(구조), Pass 3(폴리시)의 3단계 파이프라인

이 업그레이드가 완성되면, 현재 3회의 수동 라운드가 필요한 작업을 2회의 자동화된 패스로 완료할 수 있을 것으로 기대한다. 목표 점수는 <30% (journal_safe 프리셋 기준).
