# Sample Result - Keyword Search v1

## 질문

기본 키와 외래 키의 차이는 무엇인가요?

## 검색된 근거

1. database.md / database_md_chunk_009  
   score: 2  
   외래 키는 다른 테이블의 기본 키를 참조하는 값입니다. 외래 키를 사용하면 여러 테이블 사이의 관계를 표현할 수 있습니다.

2. database.md / database_md_chunk_006  
   score: 1  
   기본 키

3. database.md / database_md_chunk_007  
   score: 1  
   기본 키는 테이블에서 각 행을 고유하게 식별하기 위한 값입니다. 기본 키는 중복될 수 없으며, 일반적으로 ID와 같은 값을 사용합니다.

## 답변

외래 키는 다른 테이블의 기본 키를 참조하는 값이며, 여러 테이블 사이의 관계를 표현할 때 사용됩니다. 반면 기본 키는 하나의 테이블 안에서 각 행을 고유하게 식별하기 위한 값입니다. 기본 키는 중복될 수 없고, 일반적으로 ID와 같은 값을 사용합니다.

## 사용한 근거

- database.md / database_md_chunk_009
- database.md / database_md_chunk_006
- database.md / database_md_chunk_007

## v1 분석

v1은 질문에 포함된 단어와 chunk에 포함된 단어의 겹침을 기준으로 검색합니다.  
따라서 “기본 키”, “외래 키”처럼 문서에 있는 핵심 키워드가 질문에 직접 포함된 경우에는 관련 근거를 잘 찾을 수 있습니다.

하지만 표현이 달라지거나 질문이 모호해지면 검색 품질이 낮아질 수 있습니다.
