# Version History

## v1.0 - Keyword-based RAG Prototype

### 구현 내용

- Markdown/TXT 문서 로딩
- 문서 paragraph 기반 chunk 분할
- 질문과 chunk의 단어 겹침 기반 검색
- Top-K 관련 chunk 반환
- file_name, chunk_id, score 출력
- 검색된 근거 기반 답변 생성

### 특징

v1에서는 외부 LLM API나 딥러닝 모델을 사용하지 않고, RAG 시스템의 기본 흐름을 직접 구현했습니다.

구현한 흐름은 다음과 같습니다.

```text
document loading
→ chunking
→ keyword-based retrieval
→ top-k evidence selection
→ grounded answer generation
→ source tracking