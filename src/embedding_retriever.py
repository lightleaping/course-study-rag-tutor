from sentence_transformers import SentenceTransformer
# SentenceTransformer : 문장을 벡터로 변환하는 모델을 불러옴
import numpy as np # 벡터 연산(내적, norm 계산 등)에 사용
import re
from collections import Counter


def load_embedding_model(model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
    """
    한국어와 영어를 모두 처리할 수 있는 다국어 sentence-transformers 모델을 로드한다.
    """
    model = SentenceTransformer(model_name)
    return model


def cosine_similarity(vector_a: np.ndarray, vector_b: np.ndarray) -> float:
    """
    두 벡터 사이의 cosine similarity를 계산한다.
    """
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    # 각 벡터의 크기(norm)를 계산

    if norm_a == 0 or norm_b == 0:
        return 0.0
    # 벡터가 영벡터(모든 값이 0)라면 유사도를 0으로 반환

    return float(np.dot(vector_a, vector_b) / (norm_a * norm_b))
    # 내적을 두 벡터의 크기로 나누어 코사인 유사도를 계산
    # 값은 -1 ~ 1 사이이며, 1에 가까울수록 유사도가 높음

def tokenize(text: str) -> list[str]:
    """
    한글, 영어, 숫자 기준으로 간단히 토큰화한다.
    """
    text = text.lower()
    return re.findall(r"[가-힣a-zA-Z0-9]+", text)
    # re.findall(pattern, text) → 정규표현식 pattern에 맞는 모든 문자열을 찾아 리스트로 반환
    # + → 위 조건에 맞는 문자가 1개 이상 연속된 부분을 하나의 토큰으로 인식

def keyword_overlap_score(query: str, chunk_text: str) -> float:
    """
    질문과 chunk 사이의 키워드 겹침 점수를 계산한다.
    """
    query_tokens = tokenize(query)
    chunk_tokens = tokenize(chunk_text)

    if not query_tokens or not chunk_tokens:
        return 0.0

    query_counter = Counter(query_tokens)
    chunk_counter = Counter(chunk_tokens)

    overlap = 0

    for token, count in query_counter.items():
        if token in chunk_counter:
            overlap += min(count, chunk_counter[token])

    return overlap / len(query_tokens)


def domain_boost_score(query: str, chunk_text: str) -> float:
    """
    간단한 도메인 규칙 기반 보정 점수.
    짧은 개념 질문에서도 핵심 개념 chunk가 검색되도록 보정한다.
    """
    score = 0.0

    query = query.lower()
    chunk_text = chunk_text.lower()

    is_primary_key_chunk = "기본 키는" in chunk_text or "## 기본 키" in chunk_text
    is_foreign_key_chunk = "외래 키는" in chunk_text or "## 외래 키" in chunk_text
    is_supervised_chunk = "지도학습은" in chunk_text or "## 지도학습" in chunk_text
    is_unsupervised_chunk = "비지도학습은" in chunk_text or "## 비지도학습" in chunk_text

    # 직접 개념 질문 보정
    if "외래 키" in query and is_foreign_key_chunk:
        score += 0.7

    if "기본 키" in query and is_primary_key_chunk:
        score += 0.7

    if "지도학습" in query and is_supervised_chunk:
        score += 0.7

    if "비지도학습" in query and is_unsupervised_chunk:
        score += 0.7

    # 의미 기반 우회 질문 보정
    if "식별자" in query and is_primary_key_chunk:
        score += 0.45

    if "구분" in query and is_primary_key_chunk:
        score += 0.35

    if "참조" in query and is_foreign_key_chunk:
        score += 0.35

    if "정답" in query and is_supervised_chunk:
        score += 0.4

    if "정답" in query and is_unsupervised_chunk:
        score -= 0.25

    # 차이 질문 보정
    if "차이" in query and is_primary_key_chunk:
        score += 0.25

    if "차이" in query and is_foreign_key_chunk:
        score += 0.25

    return score


def create_chunk_embeddings(chunks: list[dict], model) -> list[dict]:
    """
    각 chunk text를 embedding vector로 변환하여 chunk에 추가한다.
    """
    chunk_texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        chunk_texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )
    # 모델을 이용해 각 텍스트를 벡터로 변환
    # numpy 배열로 반환, 진행 상황 표시

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
    # zip() 함수 : 여러 반복 가능한 객체를 인자로 받아, 각 객체의 같은 인덱스에 있는 요소들을 묶어 튜플로 만들어 순회할 수 있는 이터레이터를 반환
        embedded_chunk = {
            **chunk,
            "embedding": embedding
        }
        # 각 chunk에 "embedding" 키를 추가해 새로운 딕셔너리로 저장
        # 원래 chunk 정보(chunk_id, file_name, text) + 임베딩 벡터가 함께 들어감
        embedded_chunks.append(embedded_chunk)

    return embedded_chunks


def retrieve_top_k_by_embedding(
    query: str,
    embedded_chunks: list[dict],
    model,
    k: int = 3,
    min_score: float = 0.45
) -> list[dict]:
    """
    embedding similarity + keyword overlap + domain boost를 함께 사용하여 Top-K chunk를 반환한다.
    min_score보다 낮은 chunk는 제외하되, 결과가 없으면 fallback으로 상위 chunk를 반환한다.
    """
    query_embedding = model.encode(
        query,
        convert_to_numpy=True
    )

    all_scored_chunks = []

    for chunk in embedded_chunks:
        embedding_score = cosine_similarity(query_embedding, chunk["embedding"])
        keyword_score = keyword_overlap_score(query, chunk["text"])
        boost_score = domain_boost_score(query, chunk["text"])

        final_score = (
            embedding_score * 0.75
            + keyword_score * 0.15
            + boost_score
        )

        scored_chunk = {
            "chunk_id": chunk["chunk_id"],
            "file_name": chunk["file_name"],
            "text": chunk["text"],
            "score": round(final_score, 4),
            "embedding_score": round(embedding_score, 4),
            "keyword_score": round(keyword_score, 4),
            "boost_score": round(boost_score, 4)
        }

        all_scored_chunks.append(scored_chunk)

    all_scored_chunks.sort(key=lambda x: x["score"], reverse=True)

    filtered_chunks = [
        chunk for chunk in all_scored_chunks
        if chunk["score"] >= min_score
    ]

    if filtered_chunks:
        return filtered_chunks[:k]

    return all_scored_chunks[:1]