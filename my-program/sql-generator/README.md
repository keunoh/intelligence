# SQL Generator

SQL Generator는 테이블명과 컬럼명을 입력하면 MyBatis 형식으로
`INSERT`, `SELECT`, `UPDATE`, `DELETE` 문을 자동으로 생성해주는 작은 유틸리티입니다.

---

## 📥 다운로드

- [sql_generator.zip 다운로드](https://github.com/keunoh/intelligence/releases/download/v2.0.0/sql_generator.zip)

압축을 풀면 `sql_generator.exe` 파일이 생성됩니다.

---

## 🚀 실행 방법

### 1. exe 파일 실행 방법

1. [다운로드 링크](https://github.com/keunoh/intelligence/releases/download/v2.0.0/sql_generator.zip)에서 zip 파일을 다운로드합니다.
2. 압축을 해제합니다.
3. `sql_generator.exe` 파일을 더블 클릭하거나, `cmd` 창에서 실행합니다.

```bash
# cmd에서 실행 예시
cd 압축해제한_폴더
sql_generator.exe
```

### 2. exe 파일 직접 빌드 방법

`pyinstaller`를 사용해 직접 `.exe` 파일로 빌드할 수 있습니다.

#### 준비

```bash
pip install pyinstaller
```

#### 빌드

```bash
pyinstaller --onefile sql_generator.py
```

빌드가 완료되면 `dist/` 폴더 안에 `sql_generator.exe` 파일이 생성됩니다.

### 3. Python 스크립트로 실행 방법

Python이 설치되어 있으면, `.py` 파일만으로 실행할 수 있습니다.

```bash
python sql_generator.py
```

---

## 📚 사용 방법 (입력 흐름)

프로그램 실행 후 아래와 같이 입력합니다.

1. 테이블명을 입력합니다.
2. DML 타입을 선택합니다.
   - `C`: Create (INSERT)
   - `R`: Read (SELECT)
   - `U`: Update (UPDATE)
   - `D`: Delete (DELETE)
3. (C, R, U인 경우) 컬럼명을 쉼표로 구분하여 입력합니다.

---

## 🛠️ 입력 & 출력 예시

### [1] INSERT (Create)

**입력**

```
Enter table name: SY_USER
Enter DML type (C=Create, R=Read, U=Update, D=Delete): C
Enter column names (comma-separated): USER_ID, USER_NAME, EMAIL
```

**출력**

```sql
INSERT INTO /* com.myApp.homepage.business.mapper.FileMapper.createFile */
    SY_USER /* tableName */
        (
              USER_ID
            , USER_NAME
            , EMAIL
        ) VALUES (
              #{userId}
            , #{userName}
            , #{email}
        );
```

### [2] SELECT (Read)

**입력**

```
Enter table name: SY_USER
Enter DML type (C=Create, R=Read, U=Update, D=Delete): R
Enter column names (comma-separated): USER_ID, USER_NAME, EMAIL
```

**출력**

```sql
SELECT /* com.myApp.homepage.business.mapper.FileMapper.selectFile */
       USER_ID
     , USER_NAME
     , EMAIL
  FROM SY_USER /* tableName */
 WHERE /* condition */;
```

### [3] UPDATE (Update)

**입력**

```
Enter table name: SY_USER
Enter DML type (C=Create, R=Read, U=Update, D=Delete): U
Enter column names (comma-separated): USER_ID, USER_NAME, EMAIL
```

**출력**

```sql
UPDATE /* com.myApp.homepage.business.mapper.FileMapper.updateFile */
    SY_USER /* tableName */
      SET
              USER_ID   = #{userId}
            , USER_NAME = #{userName}
            , EMAIL     = #{email}
      WHERE /* condition */;
```

### [4] DELETE (Delete)

**입력**

```
Enter table name: SY_USER
Enter DML type (C=Create, R=Read, U=Update, D=Delete): D
```

**출력**

```sql
DELETE /* com.myApp.homepage.business.mapper.FileMapper.deleteFile */
  FROM SY_USER /* tableName */
 WHERE /* condition */;
```

---

## ✨ 특징

- 테이블명 주석 자동 추가
- 컬럼명을 camelCase로 자동 변환
- UPDATE 문은 = 기호 수직 정렬
- SELECT, DELETE 문은 6칸 들여쓰기 포맷 유지
- INSERT 문은 첫 번째 컬럼만 2칸 추가 들여쓰기 적용
- DELETE는 컬럼 입력 없이 바로 생성 가능

---

# ✅ 마무리

간단한 SQL 자동화가 필요할 때  
**가볍게 실행하고 빠르게 SQL을 생성하세요!**

