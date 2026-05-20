# Evaluation

## 평가 목적

이 문서는 Course Study RAG Tutor의 검색 결과와 답변 품질을 수동으로 평가하기 위해 작성되었습니다.

이 프로젝트는 v1, v2, v2.1, v3을 거치며 검색 방식과 사용성을 단계적으로 개선했습니다.

- v1: 키워드 기반 검색
- v2: sentence-transformers 기반 임베딩 검색
- v2.1: embedding score, keyword score, domain boost score를 결합한 Hybrid Retrieval
- v3: Streamlit UI

---

## 평가 기준

| 기준 | 설명 |
|---|---|
| Success | 질문 의도에 맞는 chunk가 Top-3 안에 포함되고 답변이 자연스러움 |
| Partial | 관련 chunk가 일부 포함되지만 불필요한 chunk나 표현 문제가 있음 |
| Fail | 질문 의도와 맞지 않는 chunk가 검색되거나 답변이 부정확함 |

---

## v1 Keyword Search Evaluation

v1은 질문과 chunk 사이의 단어 겹침을 기준으로 검색합니다.

| No. | Question | Result | Note |
|---|---|---|---|
| 1 | 머신러닝은 무엇인가요? | Success | machine_learning.md의 개념 설명 chunk 검색 |
| 2 | 지도학습과 비지도학습의 차이는 무엇인가요? | Success | 두 개념이 모두 포함된 chunk 검색 |
| 3 | 과적합은 무엇이고 어떻게 줄일 수 있나요? | Success | 과적합 설명 chunk 검색 |
| 4 | 데이터베이스는 무엇인가요? | Success | database.md의 개념 설명 chunk 검색 |
| 5 | 기본 키와 외래 키의 차이는 무엇인가요? | Success | 기본 키와 외래 키 chunk 검색 |
| 6 | Python에서 함수는 왜 사용하나요? | Success | 함수 설명 chunk 검색 |
| 7 | 키는 무엇인가요? | Partial | 기본 키와 외래 키가 함께 검색될 수 있으나 질문 의도가 모호함 |
| 8 | 학습은 무엇인가요? | Partial | 머신러닝, 지도학습, 비지도학습 chunk가 섞여 검색될 수 있음 |

---

## v2 Embedding Search Observation

v2에서 sentence-transformers 기반 임베딩 검색을 적용한 결과, 키워드 기반 검색보다 표현이 다른 질문을 처리할 수 있는 가능성을 확인했습니다.

그러나 다음과 같은 한계도 확인했습니다.

- 질문이 짧거나 추상적이면 의도와 다른 chunk가 상위에 노출될 수 있음
- `정답이 있는 데이터로 학습하는 방법` 질문에서 비지도학습 chunk가 상위에 노출됨
- `데이터를 구분하는 식별자` 질문에서 군집화 chunk가 함께 검색됨

---

## v2.1 Hybrid Retrieval Evaluation

v2.1에서는 임베딩 검색의 한계를 보완하기 위해 다음 세 가지 점수를 함께 사용했습니다.

- embedding similarity score
- keyword overlap score
- domain-specific boost score

| Question | Before | After |
|---|---|---|
| 데이터를 구분하는 식별자는 무엇인가요? | 군집화 chunk가 1위 또는 상위 노출 | 기본 키 chunk가 1위 |
| 기본 키와 외래 키의 차이는 무엇인가요? | 관련 chunk 검색 가능 | 기본 키와 외래 키 chunk 모두 Top-3 포함 |
| 외래 키가 뭐야? | 짧은 질문이라 관련 chunk가 제외될 수 있음 | 외래 키 chunk가 검색되도록 보정 |

---

## Chunking Evaluation

초기 버전에서는 paragraph 기반 chunking을 사용했기 때문에 Markdown heading이 본문과 분리되는 문제가 있었습니다.

예를 들어 `database_md_chunk_006`이 `## 기본 키` 제목만 포함하고, 실제 설명은 다음 chunk에 들어가는 문제가 있었습니다. 이 경우 검색 결과에는 잡히지만 답변 근거로는 정보가 부족했습니다.

이를 개선하기 위해 Markdown heading 기준 chunking으로 변경했습니다. 그 결과 제목과 본문이 하나의 chunk로 묶여 검색 근거의 품질이 개선되었습니다.

---

## Answer Formatting Evaluation

검색된 chunk를 그대로 이어 붙이면 `지도학습 지도학습은...`, `외래 키 외래 키는...`처럼 제목과 본문이 반복되어 답변 가독성이 떨어지는 문제가 있었습니다.

이를 개선하기 위해 답변 생성 단계에서 heading과 본문을 분리했습니다.

- 짧은 개념 질문은 heading을 제거하고 본문만 답변에 사용
- 비교/차이 질문은 heading을 Markdown 소제목으로 표시
- 답변에 사용한 chunk만 근거로 표시

개선 후 `기본 키와 외래 키의 차이는?` 질문은 다음과 같이 표시됩니다.

```text
### 외래 키

외래 키는 다른 테이블의 기본 키를 참조하는 값입니다.

### 기본 키

기본 키는 테이블에서 각 행을 고유하게 식별하기 위한 값입니다.
```

---

## Final Evaluation Summary

Course Study RAG Tutor는 v1, v2, v2.1, v3을 거치며 검색 방식과 사용성이 단계적으로 개선되었습니다.

### v1 Keyword Search

v1은 질문과 chunk의 단어 겹침을 기준으로 검색했습니다. 명확한 키워드가 포함된 질문에서는 잘 동작했지만, 표현이 다른 질문에서는 검색 품질이 떨어질 수 있었습니다.

### v2 Embedding Search

v2는 sentence-transformers 기반 임베딩 검색을 적용했습니다. 의미 기반 검색이 가능해졌지만, 짧거나 추상적인 질문에서는 의도와 다른 chunk가 상위에 노출되는 문제가 있었습니다.

### v2.1 Hybrid Search

v2.1은 embedding similarity, keyword overlap, domain-specific boost score를 함께 반영했습니다. 그 결과 특정 개념 질문에서 의도한 chunk가 더 안정적으로 상위에 노출되었습니다.

### v3 Streamlit UI

v3에서는 Streamlit UI를 추가하여 질문 입력, 검색 방식 선택, 답변 확인, 근거 카드 확인을 브라우저에서 수행할 수 있도록 개선했습니다.

---

## Portfolio Reflection

이 프로젝트는 단순히 RAG라는 이름을 붙인 것이 아니라, 검색 방식별 한계를 직접 확인하고 개선한 과정을 포함합니다.

이를 통해 다음 역량을 보여줄 수 있습니다.

- RAG 파이프라인 기본 구조 이해
- 문서 chunking과 source tracking 구현
- 검색 결과 평가 및 실패 사례 분석
- 키워드 검색과 임베딩 검색의 차이 이해
- hybrid retrieval 개선 설계
- 답변 가독성 개선
- Streamlit 기반 시연 UI 구성

---

## 향후 개선 방향

현재 v2.1은 샘플 데이터에 맞춘 간단한 보정 규칙을 사용합니다. 더 큰 문서나 다양한 과목으로 확장하려면 다음 개선이 필요합니다.

- BM25 기반 검색 추가
- 한국어 형태소 분석기 적용
- Cross-encoder reranker 적용
- 검색 결과 평가 자동화
- PDF 문서 지원
- 문서 업로드 기능 추가
- 로컬 LLM 기반 답변 생성
- Streamlit 배포
