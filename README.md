# Diverga 휴머나이제이션 파이프라인 업그레이드 연구

## 개요

이 저장소는 Diverga 휴머나이제이션 파이프라인 업그레이드를 위한 연구 및 개선 논의를 보존하는 별도의 문서화 저장소입니다. 글로벌 Diverga 배포에는 포함되지 않으며, 파이프라인의 구조적 한계를 분석하고 차세대 아키텍처를 설계하는 과정에서 도출된 인사이트와 제안 사항을 기록합니다.

---

## 연구 배경

두 편의 학술 논문 휴머나이제이션 작업 과정에서 현행 G5→G6→F5 파이프라인의 구조적 한계가 발견되었습니다.

### 대상 논문

| 논문 | 주제 | 목표 저널 | 영향력 지수 (IF) |
|------|------|-----------|----------------|
| Paper 1 | Occupational Identity Threat | TFSC (Technological Forecasting and Social Change) | ~12.0 |
| Paper 2 | Epistemic Cognition | IJAIED (International Journal of AI in Education) | ~4.7 |

### 점수 진행 과정

두 논문 모두 허용 가능한 AI 탐지 점수에 도달하기 위해 3라운드의 수동 개입이 필요했습니다.

**Paper 1 (TFSC):**

| 라운드 | AI 탐지 점수 |
|--------|-------------|
| Round 1 | 80% |
| Round 2 | 62% |
| Round 3 | 31% |

**Paper 2 (IJAIED):**

| 라운드 | AI 탐지 점수 |
|--------|-------------|
| Round 1 | 82% |
| Round 2 | 61% |
| Round 3 | 22% |

### 핵심 발견

Round 3에서의 돌파구는 심층 구조 해체(deep structural deconstruction)를 통해 달성되었습니다. 이 과정에서 어휘 정리(vocabulary cleanup) 이후에는 **단어가 아닌 구조적 패턴**이 주요 AI 탐지 신호임이 밝혀졌습니다.

---

## 저장소 구조

```
humanizer/
├── README.md                      # 이 문서. 연구 배경 및 주요 발견 요약.
├── article/                       # 연구 논의 및 분석 문서
│   └── (논문별 분석, 라운드별 개선 기록 등)
└── roadmap/                       # 파이프라인 업그레이드 로드맵 문서
    └── (G5 v2.0, G6 v2.0, 반복 파이프라인 설계안 등)
```

---

## 주요 발견

### 1. G6의 어휘 수준 변환의 한계

현행 G6 에이전트의 단어 및 구절 수준(word/phrase-level) 변환은 어휘 정리 이후 AI 탐지율 약 60% 선에서 천장에 도달합니다. 추가적인 어휘 교체만으로는 탐지율을 유의미하게 낮추기 어렵습니다.

### 2. 구조적 패턴이 주요 탐지 신호

어휘 정리 이후 AI 탐지기가 포착하는 주요 신호는 다음과 같은 구조적 지문(structural fingerprints)입니다.

- **열거 지문 (Enumeration Fingerprints)**: 첫째/둘째/셋째 구조, 병렬 나열 패턴
- **정형화된 단락 아키텍처 (Formulaic Paragraph Architecture)**: 주제문-전개-결론의 균일한 단락 구조
- **가설 체크리스트 (Hypothesis Checklists)**: AI 특유의 가설 제시 및 검증 순서
- **균일한 문장 길이 (Uniform Sentence Length)**: 문장 길이 분포의 인공적 균일성

### 3. 3축 업그레이드 제안

발견된 한계를 극복하기 위해 다음의 3축 업그레이드를 제안합니다.

| 축 | 구성 요소 | 설명 |
|----|----------|------|
| 1축 | Enhanced Detection (G5 v2.0) | 어휘 정리와 함께 구조적 지문을 정량적으로 측정하는 메트릭 도입 |
| 2축 | Structural Transformation (G6 v2.0) | 어휘 변환에 Layer 3(구조 해체 레이어)를 추가하여 단락 구조 자체를 재편 |
| 3축 | Iterative Pipeline | 단일 패스 파이프라인을 피드백 루프를 포함한 다중 패스(multi-pass) 구조로 전환 |

---

## 관련 링크

- **Diverga 플러그인**: 비공개 저장소 (Private)
- **AI_Polarization_Pew**: [https://github.com/HosungYou/AI_Polarization_Pew](https://github.com/HosungYou/AI_Polarization_Pew)

---

## 저작권 및 저자 정보

본 저장소의 모든 내용은 연구 기록 보존을 목적으로 작성되었습니다. 무단 복제 및 배포를 금지합니다.

저자: Hosung You
작성 시작일: 2026년 2월
