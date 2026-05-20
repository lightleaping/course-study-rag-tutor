# Version History

## v1.0 - Keyword-based RAG Prototype

### 구현 내용

- Markdown/TXT 문서 로딩
- paragraph 기반 chunk 분할
- 질문과 chunk의 단어 겹침 기반 검색
- Top-K 관련 chunk 반환
- file_name, chunk_id, score 출력
- 검색된 근거 기반 답변 생성

### 의의

v1에서는 외부 LLM API나 딥러닝 모델을 사용하지 않고, RAG 시스템의 기본 흐름을 직접 구현했습니다.

```text
document loading
→ chunking
→ keyword-based retrieval
→ top-k evidence selection
→ grounded answer generation
→ source tracking
```

### 한계

질문과 문서의 단어가 정확히 겹치지 않으면 검색 성능이 낮아질 수 있음
의미는 비슷하지만 표현이 다른 문장을 잘 찾지 못함
형태소 분석이나 동의어 처리가 없어 한국어 검색에 한계가 있음
답변 생성이 LLM 기반이 아니라 규칙 기반 템플릿에 가까움


## v2.0 - Embedding-based Retrieval

### 구현 내용
sentence-transformers 모델 적용
chunk text를 embedding vector로 변환
사용자 질문을 embedding vector로 변환
cosine similarity 기반 Top-K 검색
키워드가 직접 일치하지 않아도 의미적으로 가까운 chunk 검색 가능

### 사용 모델
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

### 개선 효과
v1에서는 질문에 문서의 핵심 키워드가 직접 포함되어야 검색 성능이 높았습니다.
v2에서는 문장을 벡터로 변환하여 의미 유사도를 계산하므로, 질문과 문서의 표현이 달라도 관련 chunk를 찾을 수 있습니다.

### 확인된 한계

임베딩 검색만 사용할 경우, 짧거나 추상적인 질문에서는 의도와 다른 chunk가 상위에 노출될 수 있었습니다.

예를 들어 다음 질문에서 초기 v2는 군집화 관련 chunk를 상위에 노출했습니다.

데이터를 구분하는 식별자는 무엇인가요?

또한 다음 질문에서는 지도학습을 기대했지만, 비지도학습 chunk가 더 높은 순위로 검색되는 문제가 있었습니다.

정답이 있는 데이터로 학습하는 방법은 무엇인가요?

## v2.1 - Hybrid Retrieval
### 구현 내용

v2.1에서는 검색 품질 개선을 위해 세 가지 점수를 결합했습니다.

final_score =
embedding_score * 0.75
+ keyword_score * 0.15
+ domain_boost_score

### 점수 구성
Score	Description
embedding_score	질문과 chunk embedding 사이의 cosine similarity
keyword_score	질문과 chunk 사이의 키워드 겹침 비율
domain_boost_score	도메인 핵심 개념에 대한 보정 점수

### 개선 결과
Question	v2 Result	v2.1 Result
데이터를 구분하는 식별자는 무엇인가요?	군집화 chunk가 상위 노출	기본 키 chunk가 1위
기본 키와 외래 키의 차이는 무엇인가요?	관련 chunk 검색 가능	기본 키와 외래 키 chunk 모두 Top-3 포함

### 남은 한계
현재 domain boost는 샘플 데이터에 맞춘 규칙 기반 보정임
문서가 많아지면 BM25, 형태소 분석기, reranker 등이 필요함
답변 생성은 아직 LLM 기반이 아니라 검색 근거를 정리하는 방식임

---