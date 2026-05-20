def build_answer(query: str, retrieved_chunks: list[dict]) -> str:
    """
    검색된 chunk를 바탕으로 간단한 근거 기반 답변을 생성한다.
    v1에서는 LLM 없이 규칙 기반으로 답변한다.
    """
    if not retrieved_chunks:
        return (
            "관련 근거를 찾지 못했습니다. "
            "질문을 더 구체적으로 입력하거나, data 폴더에 관련 문서를 추가해 주세요."
        )

    evidence_texts = [chunk["text"] for chunk in retrieved_chunks]

    cleaned_evidence = []

    for text in evidence_texts:
        lines = text.splitlines()

        for line in lines:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            cleaned_evidence.append(line)

    if not cleaned_evidence:
        cleaned_evidence = evidence_texts

    answer_body = " ".join(cleaned_evidence)

    answer = f"""질문: {query}

답변:
{answer_body}

사용한 근거:
"""

    for index, chunk in enumerate(retrieved_chunks, start=1):
        answer += (
            f"\n{index}. {chunk['file_name']} / "
            f"{chunk['chunk_id']} / score: {chunk['score']}"
        )

    return answer