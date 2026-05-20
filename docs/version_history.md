# Version History

## v1.0 - Keyword-based RAG Prototype

### 구현 내용

- Markdown/TXT 문서 로딩
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

- 질문과 문서의 단어가 정확히 겹치지 않으면 검색 성능이 낮아질 수 있음
- 의미는 비슷하지만 표현이 다른 문장을 잘 찾지 못함
- 형태소 분석이나 동의어 처리가 없어 한국어 검색에 한계가 있음
- 답변 생성이 LLM 기반이 아니라 규칙 기반 템플릿에 가까움

---

## v2.0 - Embedding-based Retrieval

### 구현 내용

- sentence-transformers 모델 적용
- chunk text를 embedding vector로 변환
- 사용자 질문을 embedding vector로 변환
- cosine similarity 기반 Top-K 검색
- 키워드가 직접 일치하지 않아도 의미적으로 가까운 chunk 검색 가능

### 사용 모델

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

### 확인된 한계

임베딩 검색만 사용할 경우, 짧거나 추상적인 질문에서는 의도와 다른 chunk가 상위에 노출될 수 있었습니다.

예를 들어 `데이터를 구분하는 식별자는 무엇인가요?`라는 질문에서 초기 v2는 군집화 관련 chunk를 상위에 노출했습니다.

---

## v2.1 - Hybrid Retrieval

### 구현 내용

v2.1에서는 검색 품질 개선을 위해 세 가지 점수를 결합했습니다.

```text
final_score =
embedding_score * 0.75
+ keyword_score * 0.15
+ domain_boost_score
```

### 점수 구성

| Score | Description |
|---|---|
| embedding_score | 질문과 chunk embedding 사이의 cosine similarity |
| keyword_score | 질문과 chunk 사이의 키워드 겹침 비율 |
| domain_boost_score | 도메인 핵심 개념에 대한 보정 점수 |

### 개선 결과

| Question | v2 Result | v2.1 Result |
|---|---|---|
| 데이터를 구분하는 식별자는 무엇인가요? | 군집화 chunk가 상위 노출 | 기본 키 chunk가 1위 |
| 외래 키가 뭐야? | 짧은 질문이라 관련 chunk가 제외될 수 있음 | 외래 키 chunk가 검색되도록 보정 |

---

## Chunking Improvement

### 문제

초기 chunking 방식은 빈 줄 기준으로 문서를 나누었습니다. 이로 인해 Markdown 제목과 본문이 서로 다른 chunk로 분리되는 문제가 있었습니다.

예를 들어 `## 기본 키` 제목이 단독 chunk로 생성되어, 검색 결과에 `기본 키`라는 제목만 표시되는 경우가 있었습니다.

### 개선

chunking 방식을 Markdown heading 기준으로 변경했습니다. 현재는 heading과 그 아래 본문을 하나의 chunk로 묶습니다.

### 개선 효과

- 제목만 있는 chunk 감소
- 검색 근거의 정보량 증가
- 답변 생성에 사용할 수 있는 근거 품질 개선
- Streamlit UI에서 근거 카드가 더 자연스럽게 표시됨

---

## Answer Formatting Improvement

### 문제

heading과 본문을 하나의 chunk로 묶은 뒤에는 답변 생성 단계에서 `외래 키 외래 키는...`, `지도학습 지도학습은...`처럼 제목과 본문이 어색하게 반복되는 문제가 있었습니다.

### 개선

답변 생성 단계에서 Markdown heading과 본문을 분리했습니다.

- 짧은 개념 질문은 heading을 제거하고 본문만 사용
- 비교/차이 질문은 heading을 Markdown 소제목으로 표시
- 답변에 실제 사용한 chunk만 사용한 근거로 표시

### 개선 효과

- 짧은 개념 질문 답변이 자연스러워짐
- 비교 질문에서 개념별 단락 구분이 쉬워짐
- 검색 결과와 답변 내용의 가독성 향상

---

## v3.0 - Streamlit UI

### 구현 내용

- Streamlit 기반 웹 UI 구현
- 질문 입력 화면 제공
- v1 Keyword Retrieval / v2.1 Hybrid Retrieval 선택 기능
- 검색된 근거 chunk 카드 형태로 표시
- file_name, chunk_id, score 출력
- 답변과 근거를 한 화면에서 확인 가능

### 의의

기존 CLI 기반 실행 방식은 결과 확인이 가능하지만, 포트폴리오나 시연 상황에서는 직관성이 낮았습니다.

v3에서는 Streamlit UI를 추가하여 사용자가 브라우저에서 질문을 입력하고, 검색된 근거와 답변을 바로 확인할 수 있도록 개선했습니다.

### 남은 한계

- 현재는 로컬 실행 기반 UI
- 배포 환경은 아직 구성하지 않음
- 대용량 문서 업로드 기능은 아직 없음
