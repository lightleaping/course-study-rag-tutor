from pathlib import Path # 파일 경로나 디렉터리를 객체로 다룰 수 있게 함


def load_documents(data_dir: str = "data") -> list[dict]:
    # 매개변수 data_dir는 기본값 "data"를 가지며, 읽을 폴더 경로 지정
    # 반환 타입은 list[dict], 즉 딕셔너리들을 요소로 가지는 리스트
    """
    data 폴더 안의 .md, .txt 파일을 읽어서 문서 리스트로 반환한다.
    """
    documents = []
    data_path = Path(data_dir) # data_dir 문자열을 Path 객체로 변환. 파일 시스템 경로를 객체로 다루기 위함

    if not data_path.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")
    # 지정된 경로가 존재하지 않으면 FileNotFoundError 예외를 발생시킴
    # 잘못된 경로나 없는 폴더를 지정했을 때 에러를 알려줌

    for file_path in data_path.glob("*"):
    # data_path 안의 모든 파일을 순회
    # glob("*")는 해당 디렉터리의 모든 항목을 가져옴

        if file_path.suffix.lower() not in [".md", ".txt"]:
            continue
        # 파일 확장자를 확인. .md 또는 .txt 가 아니면 건너뜀

        text = file_path.read_text(encoding="utf-8")
        # 파일 내용을 UTF-8 인코딩으로 읽어 문자열로 저장

        documents.append({
            "file_name": file_path.name,
            "text": text
        })
        # 읽은 파일을 딕셔너리로 만들어 리스트에 추가
        # 딕셔너리에는 파일 이름(file_name)과 파일 내용(text)이 들어감

    return documents
    # 모든 파일을 처리한 후, 문서 리스트를 반환