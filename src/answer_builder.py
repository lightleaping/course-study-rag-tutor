def build_answer(query: str, retrieved_chunks: list[dict]) -> str:
    """
    검색된 chunk를 바탕으로 간단한 근거 기반 답변을 생성한다.
    v1에서는 LLM 없이 템플릿 방식으로 답변한다.
    """
    if not retrieved_chunks:
        return (
            "관련 근거를 찾지 못했습니다. "
            "질문을 더 구체적으로 입력하거나, data 폴더에 관련 문서를 추가해 주세요."
        )

    evidence_texts = []

    for chunk in retrieved_chunks:
        evidence_texts.append(chunk["text"])

    combined_evidence = "\n".join(evidence_texts)

    answer = f"""질문: {query}

아래 검색된 근거를 바탕으로 답변합니다.

{combined_evidence}

요약 답변:
위 근거에 따르면, 질문과 관련된 핵심 내용은 검색된 문서 조각에서 확인할 수 있습니다. 자세한 내용은 함께 표시된 출처 파일명과 chunk_id를 참고해 주세요.
"""

    return answer