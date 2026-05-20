def split_markdown_by_heading(text: str) -> list[str]:
    """
    Markdown 문서를 heading 기준으로 나누되,
    heading과 그 아래 본문을 하나의 chunk로 묶는다.
    """
    lines = text.splitlines()
    chunks = []

    current_chunk = []

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("#") and current_chunk:
            chunks.append("\n".join(current_chunk).strip())
            current_chunk = [stripped]
        else:
            current_chunk.append(stripped)

    if current_chunk:
        chunks.append("\n".join(current_chunk).strip())

    return chunks


def create_chunks(documents: list[dict]) -> list[dict]:
    """
    문서 리스트를 chunk 리스트로 변환한다.
    각 chunk에는 chunk_id, file_name, text를 포함한다.
    """
    chunks = []

    for document in documents:
        file_name = document["file_name"]
        sections = split_markdown_by_heading(document["text"])

        for index, section in enumerate(sections, start=1):
        # sections 라는 리스트를 순회.
        # enumerate는 각 요소와 함께 인덱스를 반환. start=1 을 지정했기 때문에 인덱스는 1부터 시작
        # 즉, index는 1, 2, 3 ... 순서 번호가 되고, section는 각 문단의 내용이 됨
            chunk_id = f"{file_name.replace('.', '_')}_chunk_{index:03d}"
            # 각 문단에 고유한 chunk ID를 만들어줌
            # 파일 이름에 있는 . 을 _ 로 바꿈, 인덱스를 3자리 숫자로 포맷. 이때 앞에 0을 채움.
            chunks.append({
                "chunk_id": chunk_id,
                "file_name": file_name,
                "text": section
            })

    return chunks