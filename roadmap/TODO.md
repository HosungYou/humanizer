# Diverga 휴머나이제이션 파이프라인 업그레이드 로드맵

## 개요

- 총 13개 파일 (신규 4개, 수정 9개)
- 4단계 구현 계획
- 모든 파일 위치: `/Users/hosung/.claude/plugins/diverga/` 하위
- 목표: AI 탐지 점수 <30% 달성, 수동 개입 최소화

---

## Phase 1: G5 탐지 업그레이드 (4 files)

| # | 파일 | 변경 사항 | 복잡도 |
|---|------|-----------|--------|
| 1 | `.claude/references/agents/g5/detection-rules.md` | 정량적 지표 섹션 추가, 신규 S7-S10 카테고리 추가, 스코어링 알고리즘 업데이트, non-native speaker 보정 추가 | HIGH |
| 2 | `agents/g5.md` | 정량적 지표 계산 지시사항 및 신규 패턴 카테고리 포함하도록 에이전트 프롬프트 업데이트 | MEDIUM |
| 3 | `.claude/references/agents/g5/structural-patterns.md` | **NEW FILE**: S7-S10 상세 정의 및 예시 | MEDIUM |
| 4 | `.claude/references/agents/g5/quantitative-metrics.md` | **NEW FILE**: Burstiness, MTLD, Fano Factor 계산 방법 | MEDIUM |

---

## Phase 2: G6 변환 업그레이드 (5 files)

| # | 파일 | 변경 사항 | 복잡도 |
|---|------|-----------|--------|
| 5 | `agents/g6.md` | Layer 3 구조적 변환 지시사항 추가, burstiness 강화 directives 추가 (enumeration dissolution, paragraph opener variation, discussion architecture, hypothesis narrative) | HIGH |
| 6 | `.claude/references/agents/g6/transformations/balanced.yaml` | 구조적 변환 규칙 추가 (S7-S10) | MEDIUM |
| 7 | `.claude/references/agents/g6/transformations/aggressive.yaml` | 구조적 변환 규칙 추가 (S7-S10) + burstiness 목표값 추가 | MEDIUM |
| 8 | `.claude/references/agents/g6/transformations/structural.yaml` | **NEW FILE**: 전용 구조적 변환 레퍼런스 | HIGH |
| 9 | `.claude/references/agents/g6/academic-exceptions.md` | 구조적 변환 예외 추가 (Methods 섹션에서 IMRAD 구조 보존) | LOW |

---

## Phase 3: 파이프라인 및 체크포인트 업그레이드 (3 files)

| # | 파일 | 변경 사항 | 복잡도 |
|---|------|-----------|--------|
| 10 | `.claude/references/agents/research-coordinator/core/humanization-pipeline.md` | Single-pass 아키텍처를 반복적 3-pass 아키텍처로 교체, section-aware 에스컬레이션 추가 | HIGH |
| 11 | `.claude/checkpoints/checkpoint-definitions.yaml` | CP_PASS1_REVIEW, CP_PASS2_REVIEW, CP_FINAL_REVIEW 추가 | LOW |
| 12 | `CLAUDE.md` | 버전 v8.1.0으로 업데이트, 신규 파이프라인 기능 문서화, commands 레퍼런스 업데이트 | MEDIUM |

---

## Phase 4: F5 검증기 업그레이드 (1 file)

| # | 파일 | 변경 사항 | 복잡도 |
|---|------|-----------|--------|
| 13 | `agents/f5.md` | Burstiness 검증 추가, 구조적 패턴 체크 추가, cross-section coherence 체크 추가 | MEDIUM |

---

## 우선순위별 작업 목록

| 순위 | 우선순위 | 작업 |
|------|----------|------|
| 1 | HIGHEST | G5에 S7-S10 구조적 탐지 카테고리 추가 (60% ceiling을 유발한 패턴들) |
| 2 | HIGH | G6에 Layer 3 구조적 변환 추가 (enumeration dissolution, paragraph opener variation, discussion architecture, hypothesis narrative) |
| 3 | HIGH | Burstiness CV 지표 구현 및 강화 directives 추가 |
| 4 | MEDIUM | 패스 간 체크포인트를 포함한 multi-pass 반복 파이프라인 구축 |
| 5 | MEDIUM | MTLD vocabulary diversity 지표 추가 |
| 6 | LOW | Non-native speaker 보정 옵션 추가 |
| 7 | LOW | 프리셋 포함 score target 시스템 추가 |

---

## 식별된 갭 (Architecture Analysis에서 발견)

| # | 갭 | 설명 |
|---|----|------|
| 1 | Iterative Refinement Feedback Loop | F5가 미해결 패턴 >10% 탐지 시 "수정된 파라미터로 재시도" 메커니즘 없음 |
| 2 | Cross-Section Coherence Check | 변환 후 섹션 간 용어 일관성 검증 없음 |
| 3 | Discipline-Specific Calibration | 24-패턴 범용 모델이 모든 분야에 적용됨; Psychology, Management는 다른 기준값을 가질 수 있음 |
| 4 | Custom Preservation Lists | 사용자가 코드 수정 없이 도메인 특화 전문 용어를 보호할 수 없음 |
| 5 | Before/After Diff Visualization | 변경 사항의 시각적 side-by-side 하이라이팅 없음 |
| 6 | AI Pattern Recovery Detection | G6가 기존 AI 패턴 제거 중 새로운 AI 패턴을 도입할 수 있음; 변환 후 G5 전체 재스캔 필요 |
| 7 | Hedge Appropriateness Calibration | 남아있는 hedges가 근거 강도와 일치하는지 검증 없음 |

---

## 기대 효과

- 수동 개입 횟수: 3회 수동 라운드 → 2회 자동화 패스로 감소
- AI 탐지 점수: 수동 구조 편집 없이 <30% 달성
- Burstiness CV > 0.45, MTLD > 70 측정 및 최적화
- 인용 및 통계 100% 보존 (regression 없음)
- 각 휴머나이제이션 패스별 객관적, 정량적 지표 제공
- 보정된 탐지 임계값으로 non-native English speaker 지원

---

## 검증 계획

| 단계 | 내용 |
|------|------|
| 1 | Paper 1, Paper 2의 원본 (휴머나이제이션 이전) 버전 준비 |
| 2 | 업그레이드된 파이프라인으로 실행 (목표: 30%) |
| 3 | 측정 항목: 필요한 패스 수, 최종 점수, burstiness CV, MTLD, 인용/통계 무결성 |
| 4 | Round 3 수동 결과와 비교 (Paper 1: 31%, Paper 2: 22%) |
| 5 | 성공 기준: 100% 무결성 보존 상태에서 2회 이하 자동화 패스로 <30% 달성 |

---

## 파일 구조 참조

```
/Users/hosung/.claude/plugins/diverga/
├── CLAUDE.md                                                          # v8.1.0으로 업데이트 (수정)
├── agents/
│   ├── g5.md                                                          # G5 에이전트 정의 (수정)
│   ├── g6.md                                                          # G6 에이전트 정의 (수정)
│   └── f5.md                                                          # F5 검증기 정의 (수정)
└── .claude/
    ├── checkpoints/
    │   └── checkpoint-definitions.yaml                                # 체크포인트 정의 (수정)
    └── references/
        └── agents/
            ├── g5/
            │   ├── detection-rules.md                                 # 탐지 알고리즘 (수정)
            │   ├── structural-patterns.md                             # S7-S10 패턴 정의 (신규)
            │   └── quantitative-metrics.md                            # 정량적 지표 계산 (신규)
            ├── g6/
            │   ├── academic-exceptions.md                             # 보존 규칙 (수정)
            │   └── transformations/
            │       ├── balanced.yaml                                  # Balanced 모드 규칙 (수정)
            │       ├── aggressive.yaml                                # Aggressive 모드 규칙 (수정)
            │       └── structural.yaml                                # 구조적 변환 레퍼런스 (신규)
            └── research-coordinator/
                └── core/
                    └── humanization-pipeline.md                       # 파이프라인 아키텍처 (수정)
```

---

## 관련 리포지토리

- **연구 프로젝트**: https://github.com/HosungYou/AI_Polarization_Pew
- **휴머나이저 문서**: https://github.com/HosungYou/humanizer
