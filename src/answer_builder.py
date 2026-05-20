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
        " vs ",
        "와 ",
        "과 ",
    ]

    has_simple_pattern = any(pattern in query for pattern in simple_patterns)
    has_comparison_pattern = any(pattern in query for pattern in comparison_patterns)

    return has_simple_pattern and not has_comparison_pattern


def split_heading_and_body(text: str) -> tuple[str | None, str]:
    """
    chunk에서 Markdown heading과 본문을 분리한다.
    """
    lines = text.splitlines()
    heading = None
    body_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("#") and heading is None:
            heading = line.replace("#", "").strip()
            continue

        body_lines.append(line)

    body = " ".join(body_lines).strip()
    return heading, body


def format_answer_section(chunk: dict, show_heading: bool = True) -> str:
    """
    chunk 하나를 답변용 단락으로 변환한다.
    비교 질문에서는 heading을 Markdown 소제목으로 분리해서 보여준다.
    """
    heading, body = split_heading_and_body(chunk["text"])

    if show_heading and heading:
        if body:
            return f"### {heading}\n\n{body}"
        return f"### {heading}"

    if body:
        return body

    if heading:
        return heading

    return chunk["text"].strip()


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
    짧은 개념 질문은 하나의 chunk만 사용하고,
    비교 질문은 chunk별로 소제목과 단락을 나누어 답변한다.
    """
    if not retrieved_chunks:
        return (
            "관련 근거를 찾지 못했습니다. "
            "질문을 더 구체적으로 입력하거나, data 폴더에 관련 문서를 추가해 주세요."
        )

    answer_chunks = filter_chunks_for_answer(query, retrieved_chunks)
    simple_question = is_simple_concept_question(query)

    answer_sections = []

    for chunk in answer_chunks:
        section = format_answer_section(
            chunk,
            show_heading=not simple_question
        )

        if section:
            answer_sections.append(section)

    answer_body = "\n\n".join(answer_sections)

    evidence_lines = []

    for index, chunk in enumerate(answer_chunks, start=1):
        evidence_lines.append(
            f"{index}. {chunk['file_name']} / "
            f"{chunk['chunk_id']} / score: {chunk['score']}"
        )

    evidence_text = "\n".join(evidence_lines)

    answer = f"""질문: {query}

답변:

{answer_body}

사용한 근거:

{evidence_text}
"""

    return answer
