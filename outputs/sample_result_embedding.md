# Sample Result - Hybrid Embedding Search v2.1

## 질문 1

데이터를 구분하는 식별자는 무엇인가요?

## 검색된 근거

1. database.md / database_md_chunk_007  
   final score: 0.8463  
   embedding score: 0.3284  
   keyword score: 0.0  
   boost score: 0.6  
   기본 키는 테이블에서 각 행을 고유하게 식별하기 위한 값입니다. 기본 키는 중복될 수 없으며, 일반적으로 ID와 같은 값을 사용합니다.

2. database.md / database_md_chunk_006  
   final score: 0.687  
   embedding score: 0.116  
   keyword score: 0.0  
   boost score: 0.6  
   기본 키

## 답변

기본 키는 테이블에서 각 행을 고유하게 식별하기 위한 값입니다. 기본 키는 중복될 수 없으며, 일반적으로 ID와 같은 값을 사용합니다.

---

## 질문 2

기본 키와 외래 키의 차이는 무엇인가요?

## 검색된 근거

1. database.md / database_md_chunk_009  
   final score: 0.975  
   embedding score: 0.6333  
   keyword score: 0.3333  
   boost score: 0.45  
   외래 키는 다른 테이블의 기본 키를 참조하는 값입니다. 외래 키를 사용하면 여러 테이블 사이의 관계를 표현할 수 있습니다.

2. database.md / database_md_chunk_007  
   final score: 0.9638  
   embedding score: 0.6518  
   keyword score: 0.1667  
   boost score: 0.45  
   기본 키는 테이블에서 각 행을 고유하게 식별하기 위한 값입니다. 기본 키는 중복될 수 없으며, 일반적으로 ID와 같은 값을 사용합니다.

3. database.md / database_md_chunk_006  
   final score: 0.9227  
   embedding score: 0.597  
   keyword score: 0.1667  
   boost score: 0.45  
   기본 키

## 답변

외래 키는 다른 테이블의 기본 키를 참조하는 값이며, 여러 테이블 사이의 관계를 표현할 때 사용됩니다. 반면 기본 키는 테이블에서 각 행을 고유하게 식별하기 위한 값입니다.

## v2.1 분석

v2.1에서는 embedding similarity, keyword overlap, domain boost score를 함께 반영했습니다.  
그 결과 “데이터를 구분하는 식별자”처럼 직접적으로 “기본 키”라는 단어가 들어가지 않은 질문에서도 기본 키 관련 chunk를 상위에 노출할 수 있었습니다.
