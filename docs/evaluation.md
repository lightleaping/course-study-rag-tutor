# Evaluation

## 평가 목적

이 문서는 Course Study RAG Tutor의 검색 결과를 수동으로 평가하기 위해 작성되었습니다.

이 프로젝트는 v1, v2, v2.1을 거치며 검색 방식을 단계적으로 개선했습니다.

- v1: 키워드 기반 검색
- v2: sentence-transformers 기반 임베딩 검색
- v2.1: 임베딩 점수, 키워드 점수, 도메인 보정 점수를 결합한 Hybrid Retrieval

---

## 평가 기준

| 기준 | 설명 |
|---|---|
| Success | 질문 의도에 맞는 chunk가 Top-3 안에 포함됨 |
| Partial | 관련 chunk가 일부 포함되지만 불필요한 chunk도 함께 검색됨 |
| Fail | 질문 의도와 맞지 않는 chunk가 검색됨 |

---

## v1 Keyword Search Evaluation

v1은 질문과 chunk 사이의 단어 겹침을 기준으로 검색합니다.  
따라서 정확한 키워드가 포함된 질문에서는 잘 동작하지만, 표현이 애매하거나 동의어가 사용된 질문에서는 검색 품질이 떨어질 수 있습니다.

| No. | Question | Result | Note |
|---|---|---|---|
| 1 | 머신러닝은 무엇인가요? | Success | machine_learning.md의 개념 설명 chunk 검색 |
| 2 | 지도학습과 비지도학습의 차이는 무엇인가요? | Success | 두 개념이 모두 포함된 chunk 검색 |
| 3 | 과적합은 무엇이고 어떻게 줄일 수 있나요? | Success | 과적합 설명 chunk 검색 |
| 4 | 분류와 회귀의 차이는 무엇인가요? | Success | 지도학습 문제 유형 chunk 검색 |
| 5 | 데이터베이스는 무엇인가요? | Success | database.md의 개념 설명 chunk 검색 |
| 6 | 기본 키와 외래 키의 차이는 무엇인가요? | Success | 기본 키와 외래 키 chunk 검색 |
| 7 | SQL은 무엇을 하기 위한 언어인가요? | Success | SQL 설명 chunk 검색 |
| 8 | 관계형 데이터베이스는 어떤 방식으로 데이터를 저장하나요? | Success | 관계형 데이터베이스 설명 chunk 검색 |
| 9 | Python에서 변수는 무엇인가요? | Success | 변수 설명 chunk 검색 |
| 10 | 조건문은 언제 사용하나요? | Success | 조건문 설명 chunk 검색 |
| 11 | 반복문은 어떤 경우에 사용하나요? | Success | 반복문 설명 chunk 검색 |
| 12 | 함수는 왜 사용하나요? | Success | 함수 설명 chunk 검색 |
| 13 | 키는 무엇인가요? | Partial | 기본 키와 외래 키가 함께 검색될 수 있으나 질문 의도가 모호함 |
| 14 | 학습은 무엇인가요? | Partial | 머신러닝, 지도학습, 비지도학습 chunk가 섞여 검색될 수 있음 |
| 15 | 데이터를 다루는 방법은 무엇인가요? | Partial | 데이터베이스와 Python 문서가 함께 검색될 수 있음 |

---

## v1 분석

v1은 질문에 명확한 키워드가 포함되어 있을 때 안정적으로 관련 chunk를 검색했습니다.  
예를 들어 “기본 키와 외래 키의 차이”와 같이 문서에 포함된 핵심 용어가 질문에 그대로 들어간 경우, 관련 chunk가 Top-3 안에 포함되었습니다.

하지만 “키는 무엇인가요?” 또는 “학습은 무엇인가요?”처럼 질문이 짧거나 모호한 경우에는 여러 문서의 chunk가 함께 검색될 수 있습니다.  
이는 키워드 기반 검색이 문맥적 의미보다는 단어 일치 여부에 크게 의존하기 때문입니다.

---

## v2 Embedding Search Observation

v2에서 sentence-transformers 기반 임베딩 검색을 적용한 결과, 키워드 기반 검색보다 표현이 다른 질문을 처리할 수 있는 가능성을 확인했습니다.

그러나 다음과 같은 한계도 확인했습니다.

- 질문이 짧거나 추상적이면 의도와 다른 chunk가 상위에 노출될 수 있음
- “정답이 있는 데이터로 학습하는 방법” 질문에서 비지도학습 chunk가 상위에 노출됨
- “데이터를 구분하는 식별자” 질문에서 군집화 chunk가 함께 검색됨

이는 임베딩 검색이 문장 전체의 의미적 유사성을 계산하기 때문에, 질문에 포함된 일부 표현이 다른 개념과도 강하게 연결될 수 있기 때문입니다.

---

## v2.1 Hybrid Retrieval Evaluation

v2.1에서는 임베딩 검색의 한계를 보완하기 위해 다음 세 가지 점수를 함께 사용했습니다.

- embedding similarity score
- keyword overlap score
- domain-specific boost score

## 개선 결과

| Question | v2 Result | v2.1 Result |
|---|---|---|
| 데이터를 구분하는 식별자는 무엇인가요? | 군집화 chunk가 1위 또는 상위 노출 | 기본 키 chunk가 1위 |
| 기본 키와 외래 키의 차이는 무엇인가요? | 관련 chunk 검색 가능 | 기본 키와 외래 키 chunk 모두 Top-3 포함 |
| 정답이 있는 데이터로 학습하는 방법은 무엇인가요? | 비지도학습 chunk가 상위 노출 | 지도학습 chunk가 상위로 올라오도록 보정 가능 |

---

## v2.1 분석

v2.1에서는 임베딩 검색의 의미 기반 검색 장점을 유지하면서, 특정 개념 질문에 대해서는 도메인 보정 점수를 적용해 더 적절한 chunk가 상위에 오도록 개선했습니다.

예를 들어 “데이터를 구분하는 식별자는 무엇인가요?”라는 질문은 “기본 키”라는 단어를 직접 포함하지 않지만, 데이터베이스 문맥에서는 기본 키를 묻는 질문으로 볼 수 있습니다.  
v2.1에서는 이 경우 기본 키 관련 chunk에 보정 점수를 부여하여 검색 결과를 개선했습니다.

---

## Final Evaluation Summary

Course Study RAG Tutor는 v1, v2, v2.1을 거치며 검색 방식이 단계적으로 개선되었습니다.

### v1 Keyword Search

v1은 질문과 chunk의 단어 겹침을 기준으로 검색했습니다.  
명확한 키워드가 포함된 질문에서는 잘 동작했지만, 표현이 다른 질문에서는 검색 품질이 떨어질 수 있었습니다.

### v2 Embedding Search

v2는 sentence-transformers 기반 임베딩 검색을 적용했습니다.  
의미 기반 검색이 가능해졌지만, 짧거나 추상적인 질문에서는 의도와 다른 chunk가 상위에 노출되는 문제가 있었습니다.

### v2.1 Hybrid Search

v2.1은 embedding similarity, keyword overlap, domain-specific boost score를 함께 반영했습니다.  
그 결과 특정 개념 질문에서 의도한 chunk가 더 안정적으로 상위에 노출되었습니다.

---

## Portfolio Reflection

이 프로젝트는 단순히 RAG라는 이름을 붙인 것이 아니라, 검색 방식별 한계를 직접 확인하고 개선한 과정을 포함합니다.

이를 통해 다음 역량을 보여줄 수 있습니다.

- RAG 파이프라인 기본 구조 이해
- 문서 chunking과 source tracking 구현
- 검색 결과 평가 및 실패 사례 분석
- 키워드 검색과 임베딩 검색의 차이 이해
- hybrid retrieval 개선 설계

---

## 향후 개선 방향

현재 v2.1은 샘플 데이터에 맞춘 간단한 보정 규칙을 사용합니다.  
더 큰 문서나 다양한 과목으로 확장하려면 다음 개선이 필요합니다.

- BM25 기반 검색 추가
- 한국어 형태소 분석기 적용
- Cross-encoder reranker 적용
- 검색 결과 평가 자동화
- PDF 문서 지원
- Streamlit 기반 UI 구현
- 로컬 LLM 기반 답변 생성

## Chunking Evaluation

초기 버전에서는 paragraph 기반 chunking을 사용했기 때문에 Markdown heading이 본문과 분리되는 문제가 있었습니다.

예를 들어 `database_md_chunk_006`이 `## 기본 키` 제목만 포함하고, 실제 설명은 다음 chunk에 들어가는 문제가 있었습니다.  
이 경우 검색 결과에는 잡히지만 답변 근거로는 정보가 부족했습니다.

이를 개선하기 위해 Markdown heading 기준 chunking으로 변경했습니다.  
그 결과 제목과 본문이 하나의 chunk로 묶여 검색 근거의 품질이 개선되었습니다.