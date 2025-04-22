# DBeaver + Notepad++를 이용한 MyBatis INSERT 준비 매뉴얼


## 1. DBeaver에서 테이블 컬럼명 추출하기

1. SQL Editor에서 다음처럼 입력한다:
   ```sql
   SELECT * FROM 테이블명
   ```

2. `*` 바로 뒤에 **커서를 놓는다**

3. **Ctrl + Space** (자동완성 단축키)를 누른다.

4. 테이블의 **모든 컬럼 목록이 자동으로 펼쳐진다.**

5. **모든 컬럼을 드래그하여 복사**한다. (Ctrl+C)


## 2. Notepad++로 컬럼명 변환 준비하기

1. Notepad++를 열고, 복사한 컬럼명을 붙여넣는다. (Ctrl+V)

2. 컬럼명이 다음처럼 보인다:
   ```
   AFFI_SEQ, COLUMN_NAME, USER_ID
   ```


## 3. 컬럼명 camelCase 변환하기 (정규식 변환)

**[1단계] 전체를 소문자로 변환**

- 전체 선택 (Ctrl+A)
- 상단 메뉴: `Edit` → `Convert Case to` → `lower case`
- 또는 단축키: **Ctrl + U**

변환 결과:
```text
affi_seq, column_name, user_id
```


**[2단계] 언더스코어(_) 뒤 글자를 대문자로 변환**

- Ctrl+H (찾기 및 바꾸기 열기)
- **찾을 내용:**
  ```regex
  _(\w)
  ```
- **바꿀 내용:**
  ```regex
  \u\1
  ```
- **찾기 모드:** 정규 표현식 (Regex) 활성화
- "모두 바꾸기" 클릭

변환 결과:
```text
affiSeq, columnName, userId
```


## 4. 컬럼명 MyBatis #{ } 포맷으로 감싸기

- 다시 Ctrl+H (찾기 및 바꾸기)
- **찾을 내용:**
  ```regex
  ([^,\s]+)
  ```
- **바꿀 내용:**
  ```regex
  #{$1}
  ```
- **찾기 모드:** 정규 표현식 (Regex)
- "모두 바꾸기" 클릭

다음과 같은 화면에서 설정한다:

![Notepad++ 정규식 바꾸기 설정](attachment://file-UPhBBu9SydfU3czg5ZzuXL)

변환 결과:
```text
#{affiSeq}, #{columnName}, #{userId}
```


## 5. 최종 결과 예시

```text
#{affiSeq}, #{columnName}, #{userId}
```


## 6. 추가 팁: INSERT 문 만들기

이제 최종 결과를 아래처럼 사용할 수 있다.

```sql
INSERT INTO 테이블명
(AFFI_SEQ, COLUMN_NAME, USER_ID)
VALUES (#{affiSeq}, #{columnName}, #{userId});
```


---

# ✨ 요약 흐름

1. DBeaver: SELECT * FROM 테이블명 && Ctrl + Space
2. Notepad++: 붙여넣기
3. Ctrl+U: 소문자 변환
4. Ctrl+H: `_(\w)` → `\u\1` (camelCase 변환)
5. Ctrl+H: `([^,\s]+)` → `#{$1}` (MyBatis 포맷 감싸기)
6. 완성!

