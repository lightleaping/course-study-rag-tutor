# Course Study RAG Tutor

수업자료와 개인 학습 노트를 검색하여 근거 기반 답변을 제공하는 RAG 학습 도우미

A simple RAG-based study assistant that retrieves relevant course notes and generates grounded answers with source chunks.


## 1. 프로젝트 소개

Course Study RAG Tutor는 수업자료와 개인 학습 노트를 기반으로 사용자의 질문에 관련 근거를 검색하고, 검색된 문서 조각(chunk)을 바탕으로 답변을 생성하는 RAG 기반 학습 도우미입니다.

이 프로젝트는 단순히 질문에 답하는 챗봇이 아니라, 답변에 사용된 근거 문서와 chunk_id를 함께 제공하여 사용자가 답변의 출처를 확인할 수 있도록 설계되었습니다.

## 2. 개발 목적

AI 서비스에서 중요한 것은 단순한 답변 생성이 아니라, 사용자가 결과를 신뢰할 수 있도록 근거를 함께 제공하는 것입니다.

본 프로젝트는 다음 과정을 직접 구현하는 것을 목표로 합니다.

- 문서 로딩
- 문서 chunk 분할
- 질문 기반 관련 문서 검색
- Top-K 근거 반환
- 근거 기반 답변 생성
- 출처 파일명 및 chunk_id 표시

## 3. 주요 기능

| 기능 | 설명 |
|---|---|
| 문서 입력 | Markdown/TXT 형식의 수업자료 입력 |
| Chunk 분할 | 긴 문서를 검색 가능한 단위로 분할 |
| 키워드 기반 검색 | 사용자 질문과 관련 있는 chunk 검색 |
| Top-K 반환 | 관련도 높은 chunk 상위 3개 반환 |
| 출처 표시 | 파일명, chunk_id, 점수 표시 |
| 답변 생성 | 검색된 근거를 바탕으로 답변 템플릿 생성 |

## 4. 사용 기술

- Python
- Markdown
- Keyword-based Retrieval
- Simple RAG Pipeline

## 5. 프로젝트 구조

```text
course-study-rag-tutor/
├─ README.md
├─ requirements.txt
├─ app.py
├─ data/
│  ├─ machine_learning.md
│  ├─ database.md
│  └─ python_basic.md
├─ src/
│  ├─ loader.py
│  ├─ chunker.py
│  ├─ retriever.py
│  └─ answer_builder.py
└─ outputs/
   └─ sample_result.md
```
6. 실행 방법

pip install -r requirements.txt

python app.py

7. 실행 예시

질문:
머신러닝에서 지도학습은 무엇인가요?

검색된 근거:
1. machine_learning.md / chunk_001
2. machine_learning.md / chunk_002
3. python_basic.md / chunk_001

답변:
지도학습은 입력 데이터와 정답 레이블을 함께 사용하여 모델을 학습시키는 머신러닝 방식입니다. 대표적인 예로 분류와 회귀 문제가 있습니다.

8. 향후 개선 계획
sentence-transformers 기반 임베딩 검색 추가
FAISS 또는 Chroma 벡터 DB 적용
Streamlit UI 구현
과목별 필터 기능 추가
복습 문제 자동 생성 기능 추가
검색 점수 시각화

---
