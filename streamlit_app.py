import streamlit as st
# Streamlit 라이브러리를 불러옴. 웹 앱 UI를 만들 때 사용.

from src.loader import load_documents
from src.chunker import create_chunks
from src.keyword_retriever import retrieve_top_k
from src.embedding_retriever import (
    load_embedding_model,
    create_chunk_embeddings,
    retrieve_top_k_by_embedding
)
from src.answer_builder import build_answer
# 프로젝트 내부 모듈(src 폴더)에서 필요한 함수들을 가져옴
# 문서 로딩, 청킹, 키워드 검색, 임베딩 검색, 답변 생성 기능 담당


st.set_page_config(
    page_title="Course Study RAG Tutor",
    page_icon="📚",
    layout="wide"
)
# Streamlit 앱의 기본 설정 지정
# 페이지 제목, 아이콘, 레이아웃(넓은 화면)을 설정


@st.cache_data
def load_and_chunk_documents():
    documents = load_documents("data")
    chunks = create_chunks(documents)
    return documents, chunks
# 문서를 불러오고 청킹한 결과를 캐싱(임시 저장)
# 같은 작업을 반복하지 않도록 성능 최적화

@st.cache_resource
def get_embedding_model():
    return load_embedding_model()
# 임베딩 모델을 로드하고 캐싱.
# 모델은 무겁기 때문에 한 번만 불러오도록 한다

@st.cache_data
def get_embedded_chunks(_model, chunks):
    return create_chunk_embeddings(chunks, _model)
# 청킹된 문서들을 임베딩 벡터롤 변환하고 캐싱

def render_chunk_card(chunk: dict, index: int):
    with st.container(border=True):
    # 검색된 chunk를 카드 형태로 화면에 표시
        st.markdown(f"### 근거 {index}")
        st.markdown(f"**파일명:** `{chunk['file_name']}`")
        st.markdown(f"**chunk_id:** `{chunk['chunk_id']}`")

        if "score" in chunk:
            st.markdown(f"**최종 점수:** `{chunk['score']}`")
        # score에 점수가 있으면 표시

        if "embedding_score" in chunk:
            st.markdown(f"**임베딩 점수:** `{chunk['embedding_score']}`")

        if "keyword_score" in chunk:
            st.markdown(f"**키워드 점수:** `{chunk['keyword_score']}`")

        if "boost_score" in chunk:
            st.markdown(f"**보정 점수:** `{chunk['boost_score']}`")

        st.markdown("**내용:**")
        st.write(chunk["text"])
        # chunk의 실제 텍스트 내용을 출력


def main():
    st.title("📚 Course Study RAG Tutor")
    st.caption("수업자료 기반 RAG 학습 도우미 | Keyword Retrieval → Embedding Retrieval → Hybrid Retrieval")
    # 앱의 제목과 설명을 화면에 표시

    st.markdown(
        """
        이 프로젝트는 Markdown/TXT 수업자료를 chunk 단위로 나누고, 사용자의 질문과 관련된 근거를 검색한 뒤  
        file_name, chunk_id, score와 함께 답변을 제공하는 RAG 기반 학습 도우미입니다.
        """
    )

    documents, chunks = load_and_chunk_documents()
    # 문서를 로드하고 청킹한 결과를 가져옴

    with st.sidebar:
        st.header("설정")
    # 사이드바에 설정 UI를 만듦

        retrieval_method = st.radio(
            "검색 방식 선택",
            [
                "v1 Keyword Retrieval",
                "v2.1 Hybrid Embedding Retrieval"
            ]
        )
        # 검색 방식을 선택할 수 있는 라디오 버튼 만듦

        top_k = st.slider(
            "검색할 근거 개수",
            min_value=1,
            max_value=5,
            value=3
        )
        # 검색할 chunk 개수를 슬라이더로 선택

        st.divider() # 구분선을 추가

        st.subheader("문서 정보")
        st.write(f"로드된 문서 수: **{len(documents)}**")
        st.write(f"생성된 chunk 수: **{len(chunks)}**")

        with st.expander("문서 목록 보기"):
            for doc in documents:
                st.write(f"- {doc['file_name']}")

        # 문서 목록을 펼쳐서 확인 가능

    st.subheader("질문 입력")
    # 질문 입력 영역 표시

    example_questions = [
        "기본 키와 외래 키의 차이는 무엇인가요?",
        "데이터를 구분하는 식별자는 무엇인가요?",
        "정답이 있는 데이터로 학습하는 방법은 무엇인가요?",
        "과적합은 무엇이고 어떻게 줄일 수 있나요?",
        "Python에서 함수는 왜 사용하나요?"
    ]
    # 예시 질문들을 미리 정의

    selected_example = st.selectbox(
        "예시 질문 선택",
        ["직접 입력"] + example_questions
    )
    # 예시 질문을 선택할 수 있는 드롭다운을 만듦

    if selected_example == "직접 입력":
        query = st.text_input("질문을 입력하세요")
    else:
        query = st.text_input("질문을 입력하세요", value=selected_example)
    # 직접 질문을 입력하거나 예시 질문을 선택할 수 있음

    search_button = st.button("검색하기", type="primary")
    # 검색 버튼을 만듦

    if search_button:
        if not query.strip():
            st.warning("질문을 입력해 주세요.")
            return
    # 버튼을 눌렀을 때, 질문이 비어 있으면 경고 메시지를 표시

        with st.spinner("관련 근거를 검색하는 중입니다..."):
            if retrieval_method == "v1 Keyword Retrieval":
                retrieved_chunks = retrieve_top_k(query, chunks, k=top_k)
            else:
                model = get_embedding_model()
                embedded_chunks = get_embedded_chunks(model, chunks)
                retrieved_chunks = retrieve_top_k_by_embedding(
                    query=query,
                    embedded_chunks=embedded_chunks,
                    model=model,
                    k=top_k
                )
            # 검색 방식에 따라 키워드 검색 또는 임베딩 검색을 실행

            answer = build_answer(query, retrieved_chunks)
            # 검색된 근거를 바탕으로 답변을 생성

        st.divider()

        st.subheader("답변")
        st.write(answer)
        # 답변을 화면에 표시

        st.subheader("검색된 근거")

        if not retrieved_chunks:
            st.info("검색된 근거가 없습니다.")
        else:
            for index, chunk in enumerate(retrieved_chunks, start=1):
                render_chunk_card(chunk, index)
        # 근거가 없으면 안내 메시지를 표시하고, 있으면 카드 형태로 출력

        st.divider()

        st.subheader("검색 방식 설명")

        if retrieval_method == "v1 Keyword Retrieval":
            st.markdown(
                """
                **v1 Keyword Retrieval**은 질문과 chunk 사이의 단어 겹침을 기준으로 관련 문서를 검색합니다.

                장점:
                - 구조가 단순함
                - 동작 과정을 이해하기 쉬움
                - 명확한 키워드가 포함된 질문에서 잘 동작함

                한계:
                - 표현이 다르면 검색 성능이 낮아질 수 있음
                - 동의어나 유사 표현을 잘 처리하지 못함
                """
            )
        else:
            st.markdown(
                """
                **v2.1 Hybrid Embedding Retrieval**은 다음 세 가지 점수를 함께 사용합니다.

                - embedding similarity score
                - keyword overlap score
                - domain-specific boost score

                이 방식은 임베딩 검색의 의미 기반 검색 장점을 유지하면서,  
                명확한 개념 질문에서는 핵심 chunk가 상위에 오도록 보정합니다.
                """
            )
        # 선택된 검색 방식에 따라 설명을 보여줌


if __name__ == "__main__":
    main()
# 프로그램 실행 시 main() 함수 호출