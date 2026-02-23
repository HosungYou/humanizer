# AI 텍스트 탐지 및 휴머나이제이션 연구 문헌 리뷰 (2024-2026)

> 본 문헌 리뷰는 AI 생성 텍스트 탐지(AI-generated text detection) 및 탐지 회피(evasion/humanization) 분야의 2024-2026년 주요 연구를 체계적으로 정리한다. 탐지 방법론, 스타일로메트릭 특징, 패러프레이징 회피 연구, 비원어민 편향, 상용 탐지기 비교, 학술 특화 탐지, 종합 인간유사성 점수 체계를 포괄적으로 다룬다.

---

## 1. AI 텍스트 탐지 방법론

AI 생성 텍스트 탐지 기술은 크게 세 가지 접근법으로 분류된다: 퍼플렉시티 기반(perplexity-based), 분류기 기반(classifier-based), 워터마킹 기반(watermarking-based). 각 접근법은 고유한 장단점과 적용 범위를 가지며, 최신 상용 도구들은 이들을 복합적으로 활용한다.

### 1.1 퍼플렉시티 기반 탐지 (Perplexity-Based Detection)

퍼플렉시티 기반 방법은 언어 모델의 토큰 예측 확률(token-level probability)을 이용하여 텍스트의 "예측 가능성"을 평가한다. 낮은 perplexity는 모델이 해당 토큰 시퀀스를 높은 확률로 예측할 수 있음을 의미하며, 이는 AI가 생성한 텍스트의 전형적 특성이다.

**주요 연구 및 도구:**

- **DetectGPT (Mitchell et al.)**: 학술적으로 가장 많이 인용되는 perplexity 기반 탐지 방법이다. 원본 텍스트와 perturbation된 텍스트 간의 log-probability 차이를 통계적으로 비교하여 AI 생성 여부를 판별한다. 모델이 생성한 텍스트는 perturbation 후 log-probability가 크게 감소하는 경향이 있다는 관찰에 기반한다.

- **GPTZero**: perplexity와 burstiness를 결합한 하이브리드 접근법을 채택한다. 단일 신호가 아닌 이중 신호(dual-signal) 시스템으로, 토큰 수준의 예측 가능성과 문장 수준의 변동성을 동시에 측정한다.

**핵심 약점 -- 모델 특이성(model-specificity):**

퍼플렉시티는 본질적으로 모델 의존적이다. 동일한 텍스트가 하나의 모델에게는 "놀라운"(높은 perplexity) 텍스트로, 다른 모델에게는 "예측 가능한"(낮은 perplexity) 텍스트로 나타날 수 있다. 이는 다양한 LLM이 공존하는 현재 환경에서 심각한 한계로 작용한다. 특히 GPT-4 이후 세대의 모델들은 이전 세대보다 더 높은 perplexity를 보이는 텍스트를 생성할 수 있어, perplexity 단일 지표로의 탐지가 점점 어려워지고 있다.

### 1.2 분류기 기반 탐지 (Classifier-Based Detection)

분류기 기반 방법은 fine-tuned transformer 분류기를 사용하여 perplexity를 넘어서는 분포적 특징(distributional features)을 학습한다. AI 생성 텍스트와 인간 작성 텍스트 쌍(AI/human pairs)으로 훈련된 분류기는 어휘, 통사, 담화 수준의 복합적 패턴을 포착한다.

**주요 도구 및 접근:**

- **RoBERTa 기반 fine-tuned 분류기**: AI/human 텍스트 쌍으로 훈련된 RoBERTa 모델이 기본 아키텍처로 광범위하게 사용된다.
- **ZeroGPT**: 분류기 기반 접근의 상용 구현체.
- **Originality.ai**: 장문 학술 텍스트에 특화된 분류기 기반 탐지기로, 독립 벤치마크에서 상위 성능을 기록한다.
- **Copyleaks**: 다국어 탐지에 강점을 보이는 분류기 기반 도구.
- **Turnitin AI Detection**: 학술 기관에 가장 광범위하게 배포된 분류기 기반 시스템.

**2024 메타 분석 결과:**

스타일로메트릭(stylometric) 방법만으로는 GPT-4 수준 텍스트에 대해 70-80% 정밀도(precision)를 달성하지만, ML 분류기와 결합(fusion)할 경우 약 90%까지 상승한다. 이는 단일 신호 의존이 아닌 복합 특징 활용의 중요성을 시사한다.

### 1.3 워터마킹 기반 탐지 (Watermarking-Based Detection)

워터마킹은 LLM이 텍스트 생성 시 토큰 선택을 pseudo-random "green list"로 편향시켜 통계적 신호를 삽입하는 사전적(proactive) 접근법이다. 생성 후가 아닌 생성 중에 신호를 삽입한다는 점에서 근본적으로 다른 패러다임이다.

**핵심 연구 진행:**

- **Kirchenbauer et al. (University of Maryland, 2023)**: "Green list" 알고리즘으로 워터마킹의 기초 알고리즘을 수립했다. 각 토큰 생성 시 이전 토큰에 기반한 pseudo-random 함수로 어휘를 "green"과 "red" 그룹으로 분할하고, green list 토큰의 logit을 증가시켜 생성 텍스트에 통계적으로 탐지 가능한 편향을 만든다.

- **Scott Aaronson의 Gumbel-max scheme**: Kirchenbauer 방식의 암호학적 변형으로, 더 강한 보안 보장을 제공한다.

- **Christ & Gunn (2024 CRYPTO)**: "Pseudorandom error-correcting codes"를 이론적 기반으로 도입하여 수학적으로 보장된 강건한 워터마크의 이론적 틀을 제시했다. 이는 워터마킹 분야의 이론적 기반을 크게 강화한 연구로 평가된다.

- **Google DeepMind SynthID-Text (Nature, 2024)**: 최초의 대규모 상용 배포 워터마킹 시스템이다. Nature에 발표된 이 연구는 실제 프로덕션 환경에서의 워터마킹 실현 가능성을 입증했다.

**핵심 한계:**

워터마킹은 생성 모델이 이를 구현(implement)한 경우에만 작동한다. 워터마킹을 구현하지 않은 모델이 생성한 텍스트는 사후적으로(retroactively) 탐지할 수 없다. 이는 모든 LLM 제공자의 협력이 전제되어야 한다는 근본적 한계를 의미한다.

### 1.4 탐지기 의존 특징 (Features Used by Detectors)

현재 주요 탐지 도구들이 활용하는 특징(features)을 아래 표에 정리한다.

| 특징 (Feature) | 설명 (Description) | 활용 도구 (Used By) |
|---|---|---|
| **Perplexity** | 토큰 수준의 예측 가능성 점수. 낮을수록 AI 가능성 높음 | GPTZero, DetectGPT |
| **Burstiness** | 문장 길이 및 복잡성의 변동(variance). 낮을수록 AI 가능성 높음 | GPTZero, Sapling |
| **Stylometric features** | POS 빈도, 구두점 엔트로피, 어휘 다양성 등 복합 언어 특징 | 분류기 기반 탐지기, 학술 탐지기 |
| **Entropy/randomness** | 토큰 선택의 분포 패턴. 워터마킹 신호 탐지에 활용 | 워터마킹 시스템 |
| **Semantic embeddings** | 고차원 텍스트 표현(representation)을 통한 의미적 패턴 포착 | Turnitin, Copyleaks |
| **Discourse markers** | "however," "this," "because" 등 담화 표지어의 사용 패턴 | 학술 코퍼스 연구 |

---

## 2. 스타일로메트릭 특징 (Stylometric Features)

AI 생성 텍스트와 인간 작성 텍스트를 구분하는 스타일로메트릭 특징은 어휘(lexical), 통사(syntactic), 담화(discourse) 수준에서 다층적으로 나타난다. 이 절에서는 각 수준의 특징을 체계적으로 정리한다.

### 2.1 어휘 패턴 (Lexical Patterns)

AI 생성 텍스트의 가장 직관적이고 널리 관찰되는 특징은 특정 "스타일 단어(style words)"의 과도한 사용이다.

**AI 과잉 사용 어휘 목록:**

주요 AI 시그니처 단어로는 "delve," "underscore," "showcase," "encapsulate," "noteworthy," "seamless," "crucial," "findings," "potential," "navigate the landscape" 등이 있다. 이들은 LLM의 훈련 데이터에서 고빈도로 나타나는 단어들이 생성 시 편향적으로 선택되면서 발생하는 현상이다.

**2024 PubMed 대규모 연구:**

2024년에 수행된 1,400만 건의 PubMed 초록(2010-2024) 분석 연구는 AI 작성에서 유의하게 과잉 사용되는 **454개 단어**를 식별했다. 이 단어들의 사용 빈도는 2023-2024년에 급격한 변곡점(sharp inflection point)을 보인다. 이는 ChatGPT 출시 이후 AI 보조 작문이 학술 영역에 급속히 확산되었음을 시사하는 정량적 증거이다.

**핵심 통찰:**

- **스타일 단어 과잉이 AI의 시그니처**이다. 내용어(content words) 과잉이 아닌, 기능적/수사적 스타일 단어의 과잉이 AI 보조 작문의 진정한 지표이다.
- AI 텍스트는 문서 간 단어 선택의 **일관성(consistency)이 인간 텍스트보다 현저히 높다**. 인간 작성자는 동일 주제에 대해서도 다양한 어휘 선택을 보이지만, AI는 유사한 맥락에서 동일한 단어를 반복 선택하는 경향이 있다.

### 2.2 통사 패턴 (Syntactic Patterns)

어휘 수준을 넘어, AI 텍스트는 통사 구조에서도 체계적인 차이를 보인다.

**주요 통사적 특징:**

- **동등 담화 표지어(equivocal discourse markers)의 낮은 사용**: "however," "but," "although" 같은 양보/대조 표지어의 빈도가 인간 텍스트에 비해 낮다. 이는 AI가 논증의 복잡성과 다면성을 표현하는 데 한계가 있음을 반영한다.

- **"this"와 "because"의 과소 사용**: 이 두 단어는 인간의 지시적 추론(referential reasoning)과 인과 추론(causal reasoning)의 표지로 기능한다. AI 텍스트에서의 과소 사용은 AI가 맥락 참조와 인과 설명을 덜 빈번하게 수행함을 의미한다.

- **문장 구조의 균일성**: AI 텍스트는 문장 구조가 더 균일하며, 문서 전체에 걸쳐 통사적 다양성(syntactic variety)이 낮다. 인간 작성자는 종속절(subordination)과 등위절(coordination)을 예측 불가능하게 혼합하는 반면, AI는 일관된 구문 패턴을 유지하는 경향이 있다.

### 2.3 헤징 및 부스팅 (Hedging and Boosting)

헤징(hedging)은 주장의 확실성을 완화하는 언어 전략이고, 부스팅(boosting)은 강화하는 전략이다. AI 텍스트는 이 두 차원에서 인간 텍스트와 체계적으로 다른 패턴을 보인다.

**주요 발견:**

- AI 텍스트는 **강도를 체계적으로 완화(moderate)**한다. 예를 들어, 인간이 "undoubtedly confirms"로 강하게 주장할 문맥에서 AI는 "clearly affirms"로 완화된 표현을 사용한다.

- 인간 학술 텍스트는 **강한 헤징/부스팅 대비(contrast)**를 보인다. 즉, 확신이 있는 부분에서는 강력한 부스팅을, 불확실한 부분에서는 깊은 헤징을 사용하여 뚜렷한 그라디언트를 형성한다. 반면 AI는 이 그라디언트를 **평탄화(flatten)**하여 전반적으로 중간 수준의 확신도를 유지한다.

- 2024년 SCIRP에서 발표된 코퍼스 연구는 AI 에세이와 인간 에세이 간의 헤징 및 참여 표지어(engagement markers)를 직접 비교하여, 빈도와 분포 모두에서 측정 가능한 차이를 확인했다.

### 2.4 버스티니스 -- 문장 길이 변동 (Burstiness)

Burstiness는 텍스트 내 문장 길이와 구조적 복잡성의 변동(variance)을 측정하는 지표로, AI 탐지에서 perplexity와 함께 가장 핵심적인 정량적 신호이다.

**정의 및 계산 방법:**

Burstiness 측정의 기본 절차:
1. 텍스트를 문장 단위로 토큰화(tokenize)
2. 각 문장의 길이를 단어 수(word count)로 계산
3. 문장 길이의 분산/변동 지표를 산출

**4가지 계산 방법:**

| 방법 | 수식 | 특성 |
|---|---|---|
| **Method 1: 표준편차 (Standard Deviation)** | `burstiness_score = std_deviation(sentence_lengths)` | 가장 단순하고 직관적. 문서 길이에 의존적 |
| **Method 2: Fano Factor** | `Fano Factor = Variance(lengths) / Mean(lengths)` | Fano Factor > 1: super-Poissonian (bursty, 인간적); = 1: Poisson; < 1: sub-Poissonian (regular, AI적) |
| **Method 3: Coefficient of Variation (CV)** | `CV = Std_deviation(lengths) / Mean(lengths)` | 정규화된 지표로 문서 간 비교 가능 |
| **Method 4: Perplexity Variance** | 각 문장의 perplexity를 참조 LM으로 계산 후, 문서 내 문장별 perplexity 점수의 variance | perplexity와 burstiness를 통합한 가장 정보량이 풍부한 지표 |

**인간 vs AI 패턴:**

- 인간 작문은 **짧은 문장(3-5 단어)과 긴 복합 구문(30-50 단어)을 자연스럽게 혼합**하여 높은 burstiness를 생성한다. 이는 사고 흐름의 자연스러운 리듬을 반영한다.

- LLM은 **중간 길이의 문장을 일관된 통사적 복잡성으로 생성**하는 경향이 있어, 체계적으로 낮은 burstiness를 보인다. 이는 토큰 단위 생성 메커니즘의 구조적 특성에서 기인한다.

- 높은 perplexity를 보이는 AI 생성 텍스트조차 낮은 burstiness를 나타낸다. 이는 burstiness가 perplexity와 **부분적으로 독립적인 보완 신호(complementary, partially independent signal)**임을 의미한다.

- GPTZero의 탐지 시스템은 perplexity와 burstiness를 명시적으로 **두 가지 주요 신호(two primary signals)**로 결합하여 사용한다.

### 2.5 어휘 다양성 지표 (Vocabulary Diversity Metrics)

어휘 다양성(lexical diversity)은 텍스트 내 사용된 어휘의 풍부함과 변화를 측정하는 지표군이다. 다양한 측정 방법이 제안되었으며, 각각 고유한 장단점을 갖는다.

**주요 지표 비교:**

| 지표 (Metric) | 설명 (Description) | 강점 (Strengths) | 한계 (Limitations) |
|---|---|---|---|
| **TTR** (Type-Token Ratio) | 고유 단어 수 / 총 단어 수 | 단순하고 직관적 | 텍스트 길이에 심하게 의존적 |
| **MATTR** (Moving Average TTR) | 롤링 윈도우 TTR 평균 | 길이 편향 감소 | 윈도우 크기가 자유 매개변수 |
| **MTLD** (Measure of Textual Lexical Diversity) | TTR이 임계값 이상을 유지하는 연속 단어 문자열의 평균 길이 | **길이 불변(length-invariant)**; 4가지 타당도 차원에서 검증됨 | 계산 비용이 높음 |
| **vocd-D / HD-D** | 초기하 분포(hypergeometric distribution)에 대한 곡선 적합(curve-fitting) | 통계적으로 엄밀 | 구현이 복잡 |
| **Maas** | TTR의 로그 기반 변환 | 길이 민감도 낮음 | 직관성 부족 |

**McCarthy & Jarvis (2010)의 타당도 검증:**

McCarthy & Jarvis (2010)는 MTLD, vocd-D, HD-D를 원시 TTR보다 우수한 지표로 검증했다. 특히 **MTLD는 텍스트 길이의 함수로 변하지 않는 유일한 지표**로 확인되었으며, 이는 서로 다른 길이의 텍스트를 비교할 때 가장 적합한 지표임을 의미한다.

**AI vs 인간 텍스트 비교 결과:**

- LLM은 **전반적으로 더 낮은 어휘 다양성**을 보이며, 일반적인 통사 구조를 선호하는 경향이 있다. 다만 이는 장르에 의존적이다.

- **장르별 역전 현상**: 미스터리, 모험, 로맨스 등 일부 장르에서 GPT-4 텍스트가 인간 저작 텍스트보다 더 높은 어휘 다양성을 보인다. 이는 단순히 "AI = 낮은 다양성"이라는 일반화가 위험함을 시사한다.

- **학술 작문 특수성**: 학술 작문 영역에서 ChatGPT는 표면적으로 어휘가 풍부해 보임에도 불구하고, **연어 사용(collocational usage)의 미묘함과 맥락 적절성(contextual appropriateness)에서 인간 작성자보다 열등**한 것으로 나타났다.

- 전통적 지표(TTR, MTLD, vocd-D)는 점차 신경망 방법으로 보완되고 있다. 2024년 한 연구는 **오토인코더 기반 프레임워크(autoencoder-based framework)**를 제안하여 표면 지표가 놓치는 맥락적 관계(contextual relationships)를 포착할 수 있음을 보였다.

### 2.6 구조적 및 담화 수준 패턴 (Structural and Discourse-Level Patterns)

어휘와 통사를 넘어, 담화 수준(discourse-level)의 구조적 패턴은 AI 텍스트의 가장 깊은 수준의 시그니처를 형성한다.

#### 2.6.1 단락 구조 (Paragraph Architecture)

AI 생성 학술 텍스트는 공식적인(formulaic) 단락 구조를 보인다: **주제문(topic sentence) -> 뒷받침 근거(supporting evidence) -> 전환적 종합(transitional synthesis)**. 이러한 규칙성은 구조적 지문(structural fingerprint)으로 탐지 가능하다.

서로 다른 LLM은 담화 수준에서도 구별 가능한 스타일 지문을 갖는다. ChatGPT, Gemini, LLaMA는 서로, 그리고 인간 저자와도 구별 가능한 것으로 밝혀졌다.

#### 2.6.2 열거 지문 (Enumeration Fingerprint)

AI 텍스트는 산문(prose) 내에 번호 매긴 목록(numbered lists)과 병렬 불릿 구조(parallel bullet structures)를 과도하게 사용한다. 이는 학술 작문 분석에서 플래그된 패턴이다.

이 "열거 지문"은 **구조적으로 지속적(structurally persistent)**이며, 표면 어휘보다 패러프레이징으로 제거하기 훨씬 어렵다. 패러프레이저가 문장/구 수준에서 작동하기 때문에, 목록 구조 자체는 변환 후에도 상당 부분 보존된다.

#### 2.6.3 전환 및 담화 표지어 (Transition and Discourse Markers)

AI 텍스트는 예측 가능한 간격으로 명시적 논리 연결어(explicit logical connectors)에 과도하게 의존한다:
- "Furthermore," "Moreover," "In conclusion," "It is worth noting that" 등

인간 학술 텍스트는 더 다양하고 종종 암시적(implicit)인 논리적 연결을 사용한다. 2024년 패러프레이징 시 담화 표지어에 관한 연구는 이러한 패턴이 패러프레이징 도구를 거친 후에도 **부분적으로 생존(partially survive)**함을 확인했다.

---

## 3. 휴머나이제이션/패러프레이징 회피 연구

AI 탐지를 회피하기 위한 패러프레이징(paraphrasing) 및 휴머나이제이션(humanization) 기법의 효과와 한계에 대한 연구는 탐지 연구와 함께 활발히 진행되고 있다.

### 3.1 패러프레이징 효과 (Paraphrasing Effectiveness)

#### DIPPER 연구 (Krishna et al., 2023 -- NeurIPS)

패러프레이징 공격 분야에서 가장 많이 인용되는 논문이다. DIPPER는 110억 매개변수(11B parameter) 패러프레이즈 모델로, 어휘 다양성(lexical diversity)과 내용 재배열(content reordering) 제어 기능을 갖춘다.

주요 결과:
- DetectGPT 탐지율을 1% false positive rate 기준 **70.3%에서 4.6%로** 급락시켰다
- GPTZero, 워터마킹 시스템, OpenAI의 분류기를 모두 회피했다
- 원본 텍스트 대비 의미적 수정(semantic modification)이 최소한이었다
- 방어 측 발견: 검색 기반 탐지(retrieval-based detection, 데이터베이스 조회 방식)는 패러프레이징에 대해 강건(robust)하다

#### 적대적 패러프레이징 연구 (Adversarial Paraphrasing, 2025)

2025년에 발표된 탐지기 피드백(detector feedback)에 의해 유도되는(guided) 적대적 패러프레이징 연구:
- 1% false positive rate 기준, 8개 탐지기에 대해 평균 **87.88% true positive rate 감소**를 달성했다
- **범용적 전이성(universal transferability)**: 하나의 탐지기에 대한 적대적 패러프레이징이 다른 모든 탐지기의 탐지율도 감소시킨다
- 텍스트 품질 저하(text quality degradation)가 최소한이었다

#### 실용적 회피 결과 (Practical Evasion Results)

- Spinbot만 사용한 패러프레이징: Copyleaks에서 약 85% AI 탐지 (회피 효과 제한적)
- 다중 도구 + 수동 편집 결합: 일관되게 **10% 미만**의 탐지율 달성
- **다중 도구 + 수동 편집이 가장 효과적인 회피 전략**으로 확인됨

### 3.2 단일 패스 vs 다중 패스 (Single-Pass vs Multi-Pass)

| 전략 | 설명 | 일반적 결과 |
|---|---|---|
| **단일 패스 (Single-pass)** | 하나의 도구를 한 번 적용, 수동 편집 없음 | 탐지율 감소하나 상위 탐지기에서 20% 미만 달성이 어려움 |
| **다중 패스 (Multi-pass)** | 서로 다른 도구의 반복 적용 | 텍스트 엔트로피를 증가시키고 AI 지문을 더 실질적으로 감소 |
| **다중 패스 + 수동 편집** | 다중 도구 적용 후 인간의 수동 편집 | 가장 낮은 탐지율 달성 (10% 미만); **인간 개입이 핵심 차별 요인** |

다중 패스 접근이 효과적인 이유는 각 패스가 서로 다른 유형의 AI 지문을 대상으로 하며, 반복 적용이 텍스트의 전반적 엔트로피를 증가시키기 때문이다. 그러나 궁극적으로 인간의 수동 편집이 결합되어야만 구조적 패턴까지 효과적으로 처리할 수 있다.

### 3.3 휴머나이제이션이 어려운 특징 (Hard-to-Humanize Features)

패러프레이징 및 휴머나이제이션 후에도 지속되는 특징과 쉽게 제거되는 특징 사이에는 명확한 구분이 존재한다.

**구조적 특징 -- 지속성 높음 (Persistent after paraphrasing):**

| 특징 | 지속 이유 |
|---|---|
| 담화 구조 (Discourse structure) | 단락 구조, 주제문 패턴은 패러프레이저가 문장/구 수준에서 작동하기 때문에 보존됨 |
| 열거 패턴 (Enumeration patterns) | 산문에 내장된 목록 구조는 패러프레이즈에 저항적 |
| 전환 논리 (Transition logic) | 논증 이동(argument moves)의 순서는 표면 단어가 변해도 부분적으로 보존됨 |
| 스타일로메트릭 규칙성 (Stylometric regularities) | 균일한 문장 길이, 낮은 burstiness는 단일 패스 패러프레이징 후에도 부분적으로 생존 |

**어휘적 특징 -- 쉽게 대체됨 (Easily replaced):**

| 특징 | 대체 용이성 이유 |
|---|---|
| AI 시그니처 어휘 (AI-signature vocabulary) | "delve," "underscore" 등은 패러프레이저에 의해 쉽게 동의어로 교체됨 |
| 표면 수준 헤징 패턴 (Surface-level hedging) | 휴머나이저에 의해 수정 가능 |

이 구분은 효과적인 휴머나이제이션이 어휘 교체(lexical replacement)를 넘어 **구조적 변환(structural transformation)**을 포함해야 함을 시사한다.

---

## 4. 비원어민 편향 문제

AI 텍스트 탐지의 가장 심각한 타당도(validity) 문제는 비원어민(non-native) 영어 작성자에 대한 체계적 편향이다. 이는 단순한 기술적 한계를 넘어 교육적, 윤리적 함의를 갖는 문제로, 다수의 엘리트 대학이 이를 이유로 AI 탐지를 중단하는 결과를 낳았다.

### 4.1 주요 연구 결과

| 연구 결과 (Finding) | 출처 (Source) | 비율 (Rate) |
|---|---|---|
| TOEFL 에세이가 AI로 오분류됨 | Liang et al. (2023) | 최소 1개 탐지기에서 **>61%** 플래그 |
| 91개 TOEFL 에세이 중 18개 만장일치 플래그 | Liang et al. (2023) | **19.8%** 만장일치 false positive |
| UC Davis 2024 수동 검토 | 사례 연구 | 17건 플래그 중 **15건이 false positive** |
| Stanford 2025 10,000+ 샘플 분석 | Stanford 연구 | 비원어민에 대해 **>20%** false positive |
| 무료 탐지기 false positive (pre-ChatGPT 인간 학술 텍스트) | Popkov et al. (2024) | 중앙값 **27.2%** |

### 4.2 편향 메커니즘

비원어민 영어 작문은 AI 텍스트와 **표면적 특징을 공유**한다:
- 더 단순한 어휘 (simpler vocabulary)
- 더 규칙적인 문장 구조 (more regular sentence structures)
- 덜 관용적인 표현 사용 (less idiomatic usage)

이러한 공유 특징으로 인해, 원어민 영어의 인간/AI 대비(native English human/AI contrasts)로 훈련된 탐지기가 비원어민 텍스트를 AI로 오분류(misclassify)한다.

### 4.3 정확도-편향 상충 (Accuracy-Bias Trade-off)

가장 심각한 구조적 문제는, 벤치마크 테스트에서 **가장 정확한 탐지기가 비원어민에 대해 가장 강한 편향**을 보인다는 점이다. 즉, 탐지 정확도를 높이면 편향이 증가하고, 편향을 줄이면 정확도가 감소하는 상충(trade-off)이 존재한다.

단순한 프롬프팅 전략(예: GPT에게 "인간처럼 작성하라" 또는 어휘를 풍부하게 하라고 지시)이 편향을 완화하면서 동시에 탐지를 우회할 수 있다는 발견은, 현재 탐지기들이 "AI 특성"이 아닌 "비원어민 특성"을 학습하고 있을 가능성을 시사한다.

### 4.4 기관 대응 (Institutional Response)

최소 **12개 엘리트 대학**이 AI 탐지를 비활성화(deactivate)했다:

| 대학 | 시기 |
|---|---|
| Yale University | 2024-2025 |
| Vanderbilt University | 2024-2025 |
| Johns Hopkins University | 2024-2025 |
| Northwestern University | 2024-2025 |
| UCLA | 2024-2025 |
| UC San Diego | 2024-2025 |
| Cal State LA | 2024-2025 |
| UT Austin | 2024-2025 |

이들 대학은 false positive의 불균형한 영향과 편향 문제를 AI 탐지 중단의 주요 근거로 제시했다.

---

## 5. 상용 탐지기 비교

현재 시장의 주요 상용 AI 텍스트 탐지기에 대한 상세 비교를 아래에 정리한다. 특히 벤더의 주장과 독립 연구 결과 간의 괴리에 주목할 필요가 있다.

| 도구 (Tool) | 주장 정확도 (Claimed Accuracy) | 독립 연구 결과 (Independent Findings) | False Positive Rate | 비고 (Notes) |
|---|---|---|---|---|
| **GPTZero** | 99.3% | 수정되지 않은 텍스트에서 높은 성능; 번역된 콘텐츠에서 실패 | 0.24% (주장) | 번역된 AI 텍스트를 모두 인간 텍스트로 오분류 |
| **Originality.ai** | 98-100% | 여러 벤치마크에서 최상위 성능; ChatGPT/Grok/Gemini에서 100% | 낮음 | 장문 학술 텍스트에서 최고 성능 |
| **Turnitin AI** | 92-100% | AI 텍스트의 약 15%를 놓침; 학계에 가장 광범위하게 배포 | ~1% (주장) | 다수 대학이 비활성화 중 |
| **Copyleaks** | 90.7% (한 벤치마크) | 다국어 탐지에서 최고 성능; 약 1/20 false positive | ~5% | 비영어 AI 텍스트에 강점 |
| **ZeroGPT** | 가변적 | 일반적으로 낮은 정확도; 높은 false positive 보고 | 높음 | 무료 티어; 신뢰도 낮음 |
| **Sapling** | 97% | 클린 텍스트에서 경쟁력 있는 성능 | -- | 기업 맥락에서 사용 |

**핵심 관찰:**

- 벤더 주장(GPTZero: 0.24%; Turnitin: ~1%)과 독립 연구 결과는 극적으로 괴리된다. Popkov et al. (2024)은 무료 AI 탐지기들이 2016-2018년의 pre-ChatGPT 인간 학술 텍스트를 분석했을 때 **중앙값 27.2%의 false positive rate**를 보고했다.

- 2024년 IACIS 논문은 false positive rate를 0.5% 미만으로 제한할 경우, 대부분의 탐지기가 거의 0%의 true positive rate를 달성한다고 밝혔다. 이는 **엄격한 임계값에서 탐지기가 사실상 무용**함을 의미한다.

- 패러프레이징에 대한 취약성: 모든 테스트된 도구에서 패러프레이징 후 탐지 정확도가 "급락(plummet)"하며, 도구와 조작 유형에 따라 sensitivity가 0%에서 100%까지 범위를 보인다.

---

## 6. 학술 특화 탐지 연구

학술 텍스트, 특히 과학 논문은 일반 텍스트와 구별되는 탐지 특성을 보인다. 학술 텍스트의 형식적 레지스터(formal register)가 AI의 균일성을 모방할 수 있어, 고유한 도전과 기회를 동시에 제공한다.

### 6.1 과학 초록 탐지

- **인간 주석자(human annotators)의 성능**: 인간 주석자는 AI 초록과 인간 초록을 구별하는 데 거의 우연 수준(near-chance)의 성능을 보인다. 이는 AI가 학술 초록의 형식적 규약을 매우 효과적으로 모방함을 의미한다.

- **모델 세대별 차이**: 이전 LLM 버전의 텍스트는 더 탐지가 용이하다. GPT-4 이후 모델은 탐지가 유의하게 어렵다.

- **PMC 연구**: 2023년 PubMed의 AI 포함 초록이 2021-2022년 대비 **약 2배**로 증가했음을 확인했다.

- **도메인 특화 훈련**: University of Chicago 생물과학 연구에 따르면, 해당 도메인에 특화 훈련된 ML 도구는 기계 작성 과학 초록을 **>99% 정확도**로 탐지할 수 있다. 단, 이는 해당 도메인에 특화 훈련된 경우에만 해당한다.

- Turnitin과 GPTZero는 과학 텍스트와 일반 텍스트에서 다른 성능을 보인다. 학술 텍스트의 형식적 레지스터가 AI의 균일성을 모방하여 false positive를 증가시킬 수 있다.

### 6.2 섹션별 탐지 패턴 (Section-Specific Detection Patterns)

학술 논문의 섹션에 따라 탐지 특성이 달라진다.

| 섹션 | 탐지 특성 | 이유 |
|---|---|---|
| **Abstract (초록)** | 가장 높은 AI 탐지율 (highest detection rates) | 인간 작문에서도 구조적으로 공식적(formulaic)이어서 높은 true positive와 높은 false positive 모두 발생 |
| **Methods (방법)** | 과소 플래그 가능성 (may under-flag) | 인간 작문에서도 매우 공식적이어서, 실제 AI 사용이 탐지되지 않을 수 있음 |
| **Discussion/Conclusion (논의/결론)** | AI가 가장 탐지 가능 (most AI-detectable) | 더 많은 개인적 목소리(individual voice)와 헤징 변동성을 요구하는 섹션으로, AI의 평탄화된 헤징이 인간 패턴과 크게 괴리됨 |

이 섹션별 차이는 AI 탐지 및 휴머나이제이션 전략이 논문의 구조적 위치에 따라 차별화되어야 함을 시사한다.

---

## 7. 종합 인간유사성 점수 체계 (Composite Human-Likeness Scoring)

AI 생성 텍스트와 인간 작성 텍스트를 구별하기 위한 종합적 인간유사성 점수 체계의 구성 요소를 아래 표에 정리한다.

| 지표 (Metric) | 인간유사 방향 (Human-like Direction) | 계산 원천 (Computable From) |
|---|---|---|
| **Burstiness** (문장 길이 CV) | 높을수록 인간적 | 원시 텍스트 (raw text) |
| **MTLD** | 높을수록 인간적 (더 다양한 어휘) | 원시 텍스트 (raw text) |
| **POS entropy** | 높을수록 인간적 (더 다양한 POS 혼합) | NLP 태깅 (NLP tagging) |
| **Per-sentence perplexity variance** | 높을수록 인간적 | LM 추론 (LM inference) |
| **Discourse marker diversity** | 높을수록 인간적 | 패턴 매칭 (pattern matching) |
| **AI-signature word frequency** | 낮을수록 인간적 ("delve," "underscore" 등) | 단어 빈도 (word frequency) |
| **Fano Factor** | >1이면 인간적 (super-Poissonian) | 원시 텍스트 (raw text) |

**표준화된 프레임워크의 부재:**

현재까지 발표된 표준(published standard)으로서의 표준화된 점수 체계는 존재하지 않는다. 가장 엄밀한 학술적 접근은 **MTLD + per-sentence perplexity variance + Fano Factor를 다차원 특징 벡터(multi-dimensional feature vector)로 결합한 후, 이에 대해 분류기(classifier)를 훈련**하는 방식이다.

이 접근의 강점은 각 개별 지표의 한계를 보완하고, 단일 지표가 포착하지 못하는 복합적 패턴을 학습할 수 있다는 점이다. 그러나 분류기 훈련을 위한 대규모 주석 데이터셋의 필요성, 도메인 의존성, 시간에 따른 LLM 발전에 대한 적응 필요성 등이 과제로 남는다.

---

## 8. 근거 기반 핵심 결론

본 문헌 리뷰의 핵심 결론 7가지를 근거와 함께 정리한다.

### 결론 1: 어떤 탐지기도 단독으로 고위험 결정(high-stakes decisions)에 신뢰할 수 없다

독립 연구는 일관되게 10-27%의 false positive rate를 보고하는 반면, 벤더 주장은 0.24-1%이다. 이 극적 괴리는 벤더 주장의 신뢰성에 심각한 의문을 제기한다. 다수의 대학이 AI 탐지를 철회한 사실이 이를 뒷받침한다.

### 결론 2: 패러프레이징은 주요 회피 방법이며 매우 효과적이다

DIPPER는 DetectGPT 정확도를 70%에서 4.6%로 감소시켰다. 적대적 패러프레이징은 8개 탐지기에 걸쳐 87.88%의 TPR 감소를 달성했다. 이는 현재 탐지 시스템의 근본적 취약성을 드러낸다.

### 결론 3: Burstiness와 perplexity가 핵심 정량적 신호이다

Burstiness (CV 또는 Fano Factor)와 per-sentence perplexity variance는 가장 실용적으로 측정 가능한 특징이다. MTLD가 어휘 다양성 지표로 권장된다. 이들은 서로 부분적으로 독립적인 보완 신호로 기능한다.

### 결론 4: AI 어휘 시그니처는 구체적이며 문서화되어 있다

2024년 PubMed 데이터에서 454개의 과잉 사용 단어가 식별되었다. 이 단어들은 2023-2024년에 급격한 사용 빈도 증가를 보이며, AI 보조 학술 작문의 확산에 대한 정량적 증거를 제공한다.

### 결론 5: 비원어민은 체계적으로 불이익을 받는다

일부 연구에서 false positive rate가 61%를 초과한다. 이는 탐지기가 "AI 특성"이 아닌 "비원어민 특성"을 포착하고 있을 가능성을 시사하며, 교육적 평가에서의 AI 탐지 사용에 심각한 윤리적 문제를 제기한다.

### 결론 6: 구조적 지문은 휴머나이제이션 후에도 지속된다

담화 구조, 단락 구조, 열거 패턴은 패러프레이징 후에도 어휘보다 훨씬 잘 보존된다. 이는 효과적인 휴머나이제이션이 어휘 수준을 넘어 구조적 변환을 포함해야 함을 의미한다.

### 결론 7: 워터마킹이 유일하게 기술적으로 강건한 해결책이다

워터마킹은 수학적으로 보장된 탐지를 제공하지만, LLM 제공자의 협력이 필수적이며 워터마킹을 구현하지 않은 모델의 텍스트를 사후적으로 탐지할 수 없다. 이 한계에도 불구하고, 현재 기술적으로 가장 강건한 접근법이다.

---

## 참고 문헌

1. Liang, W., Yuksekgonul, M., Mao, Y., Wu, E., & Zou, J. (2023). GPT detectors are biased against non-native English writers. *arXiv:2304.02819*.

2. Krishna, K., Song, Y., Karpinska, M., Wieting, J., & Iyyer, M. (2023). Paraphrasing evades detectors of AI-generated text. *NeurIPS*. *arXiv:2303.13408*.

3. Adversarial Paraphrasing (2025). A Universal Attack for Humanizing AI-Generated Text. *arXiv:2506.07001*.

4. Contrastive Paraphrase Attacks on LLM Detectors (2025). *arXiv:2505.15337*.

5. On the Detectability of LLM-Generated Text (2025). *arXiv:2510.20810*.

6. Feature-Based Detection: Stylometric and Perplexity Markers (2024). *ResearchGate*.

7. Detecting AI-Generated Text with Pre-Trained Models (2024). *ACL Anthology*.

8. Delving into ChatGPT usage in academic writing through excess vocabulary (2024). *arXiv:2406.07016*.

9. SynthID-Text: Scalable watermarking for LLM outputs (2024). *Nature*.

10. AI watermarking must be watertight (2024). *Nature News*.

11. Watermarking for AI-Generated Content: SoK (2024). *arXiv:2411.18479*.

12. Cryptographic watermarks (2024). *Cloudflare*.

13. Lexical diversity, syntactic complexity: ChatGPT vs L2 students (2025). *Frontiers in Education*.

14. More human than human? ChatGPT and L2 writers (2024). *De Gruyter*.

15. McCarthy, P. M., & Jarvis, S. (2010). MTLD, vocd-D, and HD-D: A validation study of sophisticated approaches to lexical diversity assessment. *Behavior Research Methods*, 42(2), 381-392.

16. MATTR: Pros and cons (2024). *ResearchGate*.

17. Vocabulary Quality in NLP: Autoencoder-Based Framework (2024). *Springer*.

18. Hedging Devices in AI vs. Human Essays (2024). *SCIRP*.

19. AI and human writers share stylistic fingerprints (2024). *Johns Hopkins Hub*.

20. Accuracy-bias trade-offs in AI text detection and scholarly publication fairness (2024). *PMC*.

21. Characterizing AI Content Detection in Oncology Abstracts 2021-2023 (2024). *PMC*.

22. Distinguishing academic science writing with >99% accuracy (2023). *PMC*.

23. Originality.AI -- AI Detection Studies Meta-Analysis.

24. GPTZero vs Copyleaks vs Originality comparison.

25. AI vs AI: Turnitin, ZeroGPT, GPTZero, Writer AI (2024). *ResearchGate*.

26. Generative AI models and detection: tokenization and dataset size (2024). *Frontiers in AI*.

27. Aggregated AI detector outcomes in STEM writing (2024). *American Physiological Society*.

28. IACIS (2025). Critical look at reliability of AI detection tools.

29. Stanford HAI -- AI-Detectors Biased Against Non-Native English Writers.

30. AI-generated text detection: comprehensive review (2025). *ScienceDirect*.

31. Differentiating Human-Written and AI-Generated Texts: Linguistic Features (2024). *MDPI*.

32. How AI Tools Affect Discourse Markers When Paraphrased (2024). *ResearchGate*.

33. A Comparative Analysis of AI-Generated and Human-Written Text (2024). *SSRN*.

34. Popkov, A. et al. (2024). Median 27.2% false positive rate across free AI detectors.

35. Netus AI -- How stylometric patterns survive paraphrasing.

36. Deep Dive Into AI Text Fingerprints. *Hastewire*.

---

> 본 문헌 리뷰는 2024-2026년 사이 발표된 주요 연구를 기반으로 작성되었으며, AI 텍스트 탐지 기술의 급속한 발전에 따라 지속적 갱신이 필요하다.
