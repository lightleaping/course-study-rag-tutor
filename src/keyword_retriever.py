import re
from collections import Counter
# 정규표현식 모듈(re)와 Counter 클래스 import
# re는 문자열에서 원하는 패턴을 찾을 때 사용, Counter는 리스트 안의 요소 개수를 셈
# 예: ["apple", "apple", "banana"] → {"apple": 2, "banana": 1}

def tokenize(text: str) -> list[str]:
    """
    간단한 키워드 기반 검색을 위한 토큰화 함수.
    한글, 영어, 숫자를 기준으로 단어를 추출한다.
    """
    text = text.lower()
    tokens = re.findall(r"[가-힣a-zA-Z0-9]+", text)
    # 정규표현식을 이용해 한글, 영어, 숫자로 이루어진 단어들을 추출. 특수문자나 공백은 제외됨
    return tokens


def calculate_score(query: str, chunk_text: str) -> int:
    """
    질문과 chunk 사이의 단어 겹침 수를 점수로 계산한다.
    """
    query_tokens = tokenize(query)
    chunk_tokens = tokenize(chunk_text)

    if not query_tokens or not chunk_tokens:
        return 0

    query_counter = Counter(query_tokens)
    chunk_counter = Counter(chunk_tokens)

    score = 0

    for token, query_count in query_counter.items():
        if token in chunk_counter:
            score += min(query_count, chunk_counter[token])

    return score


def retrieve_top_k(query: str, chunks: list[dict], k: int = 3) -> list[dict]:
    """
    질문과 관련도 높은 chunk 상위 k개를 반환한다.
    """
    scored_chunks = []

    for chunk in chunks:
        score = calculate_score(query, chunk["text"])

        if score > 0:
            scored_chunk = {
                **chunk,
                "score": score
            }
            # 점수가 0보다 크면, 원래 chunk 딕셔너리에 "score" 값을 추가해 scored_chunk 리스트에 넣음
            # **chunk는 기존 딕셔너리 내용을 그대로 복사하는 문법

            scored_chunks.append(scored_chunk)

    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    # 점수를 기준으로 내림차순 정렬. 즉, 점수가 높은 문서 조각이 앞에 오도록 함

    return scored_chunks[:k]
    # 상위 k 개의 문서 조각만 반환