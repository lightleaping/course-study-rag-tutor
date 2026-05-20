# Course Study RAG Tutor

> 수업자료와 개인 학습 노트를 기반으로 질문과 관련된 근거 chunk를 검색하고, 출처와 함께 답변을 제공하는 RAG 기반 학습 도우미입니다.

---

## 1. Project Overview

Course Study RAG Tutor는 Markdown/TXT 형식의 수업자료를 읽고, 사용자의 질문과 관련된 문서 조각(chunk)을 검색한 뒤, 검색된 근거를 바탕으로 답변을 생성하는 RAG 구조의 학습용 프로젝트입니다.

이 프로젝트는 처음부터 완성형 AI 챗봇을 만드는 것이 아니라, RAG 시스템의 기본 구성 요소를 단계적으로 직접 구현하고 개선하는 것을 목표로 했습니다.

구현 과정은 다음과 같이 발전했습니다.

- v1: 외부 LLM API나 딥러닝 모델 없이 키워드 기반 검색 구현
- v2: sentence-transformers 기반 임베딩 검색 추가
- v2.1: 임베딩 점수, 키워드 점수, 도메인 보정 점수를 결합한 Hybrid Retrieval 적용

---

## 2. Why I Built This

AI 서비스에서 중요한 것은 단순히 답변을 생성하는 것이 아니라, 사용자가 답변의 근거를 확인할 수 있도록 만드는 것입니다.

이 프로젝트에서는 다음 역량을 보여주는 데 집중했습니다.

- 문서를 검색 가능한 단위로 분할하는 능력
- 질문과 관련된 근거를 찾는 검색 파이프라인 구현
- 검색 결과에 file_name, chunk_id, score를 함께 표시
- 검색 방식의 한계를 분석하고 개선하는 과정
- 키워드 검색에서 임베딩 검색, 하이브리드 검색으로 발전시키는 구조 설계

---

## 3. Key Features

| Feature | Description |
|---|---|
| Document Loading | data 폴더의 Markdown/TXT 문서 로딩 |
| Chunking | 문서를 paragraph 단위 chunk로 분할 |
| Keyword Retrieval | 질문과 chunk의 단어 겹침 기반 검색 |
| Embedding Retrieval | sentence-transformers 기반 의미 유사도 검색 |
| Hybrid Retrieval | embedding score, keyword score, domain boost score 결합 |
| Source Tracking | file_name, chunk_id, score 출력 |
| Grounded Answer | 검색된 근거 chunk를 기반으로 답변 생성 |

---

## 4. RAG Pipeline

```text
User Question
     ↓
Load Course Documents
     ↓
Split Documents into Chunks
     ↓
Retrieve Relevant Chunks
     ↓
Rank Top-K Evidence
     ↓
Generate Grounded Answer
     ↓
Show Source File, Chunk ID, Score
```

---

## 5. Project Structure

```text
course-study-rag-tutor/
├─ README.md
├─ requirements.txt
├─ app.py
├─ app_embedding.py
├─ data/
│  ├─ machine_learning.md
│  ├─ database.md
│  └─ python_basic.md
├─ src/
│  ├─ loader.py
│  ├─ chunker.py
│  ├─ keyword_retriever.py
│  ├─ embedding_retriever.py
│  └─ answer_builder.py
├─ outputs/
│  ├─ sample_result_keyword.md
│  ├─ sample_result_embedding.md
│  └─ test_questions.md
└─ docs/
   ├─ evaluation.md
   └─ version_history.md
```

---

## 6. Version Comparison

| Version | Method | Description | Limitation |
|---|---|---|---|
| v1 | Keyword-based Retrieval | 질문과 chunk의 단어 겹침을 기준으로 검색 | 표현이 다르면 검색 성능 저하 |
| v2 | Embedding-based Retrieval | sentence-transformers로 문장 의미 기반 검색 | 짧거나 모호한 질문에서 부정확한 chunk 검색 가능 |
| v2.1 | Hybrid Retrieval | embedding, keyword, domain boost 점수를 결합 | 현재는 샘플 도메인 규칙 기반 |

---

## 7. Retrieval Methods

### v1. Keyword-based Retrieval

v1에서는 질문과 chunk의 단어 겹침 수를 기준으로 관련 문서를 검색했습니다.

```text
query tokens ∩ chunk tokens → relevance score
```

이 방식은 구조가 단순하고 동작 과정을 이해하기 쉽지만, 질문과 문서의 표현이 다르면 검색 품질이 낮아질 수 있습니다.

---

### v2. Embedding-based Retrieval

v2에서는 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` 모델을 사용하여 질문과 chunk를 임베딩 벡터로 변환했습니다.

```text
query embedding
chunk embedding
cosine similarity
```

이를 통해 단어가 정확히 일치하지 않아도 의미적으로 가까운 chunk를 검색할 수 있도록 개선했습니다.

---

### v2.1 Hybrid Retrieval

v2 임베딩 검색만 사용할 경우 일부 짧거나 추상적인 질문에서 의도와 다른 chunk가 상위에 노출되는 문제가 있었습니다.

예를 들어, 다음 질문에서 초기 v2는 군집화 관련 chunk를 상위에 노출했습니다.

```text
데이터를 구분하는 식별자는 무엇인가요?
```

이를 개선하기 위해 v2.1에서는 다음 세 가지 점수를 함께 사용했습니다.

```text
final_score =
embedding_score * 0.75
+ keyword_score * 0.15
+ domain_boost_score
```

이 방식은 임베딩 검색의 의미 기반 검색 장점을 유지하면서, 명확한 개념 질문에서는 핵심 chunk가 상위에 오도록 보정합니다.

---

## 8. Tech Stack

| Category | Stack |
|---|---|
| Language | Python |
| Document Format | Markdown, TXT |
| Retrieval v1 | Keyword-based Search |
| Retrieval v2 | sentence-transformers |
| Similarity | Cosine Similarity |
| Output | CLI, Markdown |
| Documentation | README, evaluation.md, version_history.md |

---

## 9. Installation

```bash
pip install -r requirements.txt
```

`requirements.txt`

```txt
python-dotenv
sentence-transformers
numpy
```

---

## 10. How to Run

### Run v1 - Keyword Search

```bash
python app.py
```

### Run v2.1 - Hybrid Embedding Search

```bash
python app_embedding.py
```

---

## 11. Sample Result

### Question

```text
데이터를 구분하는 식별자는 무엇인가요?
```

### Retrieved Evidence

```text
1. database.md / database_md_chunk_007
최종 점수: 0.8463
임베딩 점수: 0.3284
키워드 점수: 0.0
보정 점수: 0.6
내용: 기본 키는 테이블에서 각 행을 고유하게 식별하기 위한 값입니다.

2. database.md / database_md_chunk_006
최종 점수: 0.687
임베딩 점수: 0.116
키워드 점수: 0.0
보정 점수: 0.6
내용: ## 기본 키
```

### Answer

```text
기본 키는 테이블에서 각 행을 고유하게 식별하기 위한 값입니다. 기본 키는 중복될 수 없으며, 일반적으로 ID와 같은 값을 사용합니다.
```

---

## 12. Evaluation Summary

v1 키워드 검색은 질문에 문서의 핵심 단어가 직접 포함되어 있을 때 안정적으로 동작했습니다.  
하지만 표현이 다르거나 질문이 짧은 경우 관련 chunk를 놓치거나 불필요한 chunk가 함께 검색될 수 있었습니다.

v2에서는 sentence-transformers 기반 임베딩 검색을 적용하여 의미 기반 검색을 시도했습니다.  
그러나 “데이터를 구분하는 식별자”와 같은 질문에서 군집화 chunk가 상위에 노출되는 문제가 있었습니다.

v2.1에서는 embedding similarity, keyword overlap, domain-specific boost score를 결합하여 검색 결과를 보정했습니다.

| Question | Before | After |
|---|---|---|
| 데이터를 구분하는 식별자는 무엇인가요? | 군집화 chunk가 상위 노출 | 기본 키 chunk가 1위 |
| 기본 키와 외래 키의 차이는 무엇인가요? | 관련 chunk 검색 가능 | 기본 키와 외래 키 chunk 모두 Top-3 포함 |

---

## 13. What I Learned

이 프로젝트를 통해 RAG 시스템이 단순히 LLM을 호출하는 구조가 아니라, 문서 전처리, chunk 설계, 검색 방식, 점수 계산, 근거 추적이 함께 설계되어야 한다는 점을 학습했습니다.

특히 키워드 검색과 임베딩 검색 모두 장단점이 있으며, 실제 서비스에서는 검색 결과를 평가하고 개선하는 과정이 중요하다는 것을 확인했습니다.

---

## 14. Future Improvements

- BM25 기반 검색 추가
- 형태소 분석기 적용
- Cross-encoder reranker 적용
- Streamlit UI 구현
- PDF 문서 지원
- 과목별 필터 기능 추가
- 검색 결과 평가 자동화
- 로컬 LLM 기반 답변 생성 추가

---

## 15. Status

```text
v1.0 Keyword-based Retrieval 완료
v2.0 Embedding-based Retrieval 완료
v2.1 Hybrid Retrieval 완료
```
