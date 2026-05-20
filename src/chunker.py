def split_text_by_paragraph(text: str) -> list[str]:
    """
    문서를 빈 줄 기준으로 나누어 paragraph 단위 chunk 후보를 만든다.
    """
    paragraphs = []

    for paragraph in text.split("\n\n"):
        clean_paragraph = paragraph.strip()

        if clean_paragraph:
            paragraphs.append(clean_paragraph)

    return paragraphs


def create_chunks(documents: list[dict]) -> list[dict]:
    """
    문서 리스트를 chunk 리스트로 변환한다.
    각 chunk에는 chunk_id, file_name, text를 포함한다.
    """
    chunks = []

    for document in documents:
        file_name = document["file_name"]
        paragraphs = split_text_by_paragraph(document["text"])

        for index, paragraph in enumerate(paragraphs, start=1):
        # paragraphs 라는 리스트를 순회.
        # enumerate는 각 요소와 함께 인덱스를 반환. start=1 을 지정했기 때문에 인덱스는 1부터 시작
        # 즉, index는 1, 2, 3 ... 순서 번호가 되고, paragraph는 각 문단의 내용이 됨
            chunk_id = f"{file_name.replace('.', '_')}_chunk_{index:03d}"
            # 각 문단에 고유한 chunk ID를 만들어줌
            # 파일 이름에 있는 . 을 _ 로 바꿈, 인덱스를 3자리 숫자로 포맷. 이때 앞에 0을 채움.

            chunks.append({
                "chunk_id": chunk_id,
                "file_name": file_name,
                "text": paragraph
            })

    return chunks