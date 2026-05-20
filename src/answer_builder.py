def is_simple_concept_question(query: str) -> bool:
    """
    짧은 개념 설명 질문인지 판단한다.
    예: '지도학습이 뭐야?', '외래 키가 뭐야?'
    """
    query = query.strip().lower()

    simple_patterns = [
        "뭐야",
        "무엇",
        "뭔가요",
        "설명",
        "정의",
    ]

    comparison_patterns = [
        "차이",
        "비교",
        "와",
        "과",
        "vs",
    ]

    has_simple_pattern = any(pattern in query for pattern in simple_patterns)
    has_comparison_pattern = any(pattern in query for pattern in comparison_patterns)

    return has_simple_pattern and not has_comparison_pattern


def clean_chunk_text(text: str, remove_heading: bool = False) -> str:
    """
    chunk text에서 Markdown heading 기호를 제거하고 답변용 텍스트로 정리한다.
    remove_heading=True이면 heading 줄 자체를 답변에서 제외한다.
    """
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            if remove_heading:
                continue
            line = line.replace("#", "").strip()

        cleaned_lines.append(line)

    return " ".join(cleaned_lines)


def filter_chunks_for_answer(query: str, retrieved_chunks: list[dict]) -> list[dict]:
    """
    답변 생성에 사용할 chunk를 선택한다.
    - 짧은 개념 질문이면 가장 관련 높은 chunk 1개만 사용
    - 비교/차이 질문이면 검색된 chunk 여러 개 사용
    """
    if not retrieved_chunks:
        return []

    if is_simple_concept_question(query):
        return retrieved_chunks[:1]

    return retrieved_chunks


def build_answer(query: str, retrieved_chunks: list[dict]) -> str:
    """
    검색된 chunk를 바탕으로 근거 기반 답변을 생성한다.
    v1/v2.1 모두에서 사용할 수 있도록 규칙 기반으로 답변한다.
    """
    if not retrieved_chunks:
        return (
            "관련 근거를 찾지 못했습니다. "
            "질문을 더 구체적으로 입력하거나, data 폴더에 관련 문서를 추가해 주세요."
        )

    answer_chunks = filter_chunks_for_answer(query, retrieved_chunks)

    evidence_texts = []

    remove_heading = is_simple_concept_question(query)

    for chunk in answer_chunks:
        evidence_texts.append(
            clean_chunk_text(
                chunk["text"],
                remove_heading=remove_heading
            )
        )

    answer_body = " ".join(evidence_texts)

    answer = f"""질문: {query}

답변:
{answer_body}

사용한 근거:
"""

    for index, chunk in enumerate(answer_chunks, start=1):
        answer += (
            f"\n{index}. {chunk['file_name']} / "
            f"{chunk['chunk_id']} / score: {chunk['score']}"
        )

    return answer