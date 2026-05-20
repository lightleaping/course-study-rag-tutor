from src.loader import load_documents
from src.chunker import create_chunks
from src.retriever import retrieve_top_k
from src.answer_builder import build_answer


def print_retrieved_chunks(retrieved_chunks: list[dict]) -> None:
    """
    검색된 chunk 정보를 보기 좋게 출력한다.
    """
    print("\n[검색된 근거]")

    if not retrieved_chunks:
        print("검색된 근거가 없습니다.")
        return

    for index, chunk in enumerate(retrieved_chunks, start=1):
        print(f"\n{index}. {chunk['file_name']} / {chunk['chunk_id']}")
        print(f"점수: {chunk['score']}")
        print(f"내용: {chunk['text'][:200]}...")


def main() -> None:
    print("Course Study RAG Tutor")
    print("=" * 40)

    documents = load_documents("data")
    chunks = create_chunks(documents)

    print(f"로드된 문서 수: {len(documents)}")
    print(f"생성된 chunk 수: {len(chunks)}")

    query = input("\n질문을 입력하세요: ").strip()

    if not query:
        print("질문이 입력되지 않았습니다.")
        return

    retrieved_chunks = retrieve_top_k(query, chunks, k=3)

    print_retrieved_chunks(retrieved_chunks)

    answer = build_answer(query, retrieved_chunks)

    print("\n[답변]")
    print(answer)


if __name__ == "__main__":
    main()