# dto_generator 사용 가이드

Java VO(예: PVO/RVO) 클래스를 자동 생성하는 간단한 CLI 도구 사용법을 안내합니다.

---

## 📥 다운로드

- [dto_generator.zip 다운로드](https://github.com/keunoh/intelligence/releases/download/v2.1.1/dto_generator.zip)
- 압축을 풀면 `sql_generator.exe` 파일이 생성됩니다.
---

## 1. 사전 작업: MSSQL에서 컬럼 정보 조회

먼저 아래 SQL 쿼리를 실행하여 테이블의 컬럼명, 데이터 타입, 설명(Description)을 조회합니다.

```sql
SELECT
  C.TABLE_SCHEMA + '.' + C.TABLE_NAME       AS [Table],
  C.COLUMN_NAME                             AS [Column],
  C.DATA_TYPE
    + COALESCE(
        '(' +
        CASE
          WHEN C.CHARACTER_MAXIMUM_LENGTH = -1 THEN 'MAX'
          ELSE CAST(C.CHARACTER_MAXIMUM_LENGTH AS VARCHAR(10))
        END
        + ')',
        ''
      )                                      AS [DataType],
  EP.[value]                                AS [Description]
FROM INFORMATION_SCHEMA.COLUMNS C
LEFT JOIN sys.extended_properties EP
  ON EP.major_id   = OBJECT_ID(
        QUOTENAME(C.TABLE_SCHEMA) + '.' + QUOTENAME(C.TABLE_NAME)
      )
 AND EP.minor_id   = C.ORDINAL_POSITION
 AND EP.name       = 'MS_Description'
WHERE C.TABLE_SCHEMA = 'dbo'              -- 스키마 이름
  AND C.TABLE_NAME   = 'YourTableName';    -- 조회할 테이블명
```

- `YourTableName`을 실제 테이블명으로 변경하세요.
- 조회 결과에서 `Column`, `DataType`, `Description` 값 세 개를 복사합니다.

## 2. 도구 실행

스크립트를 파이썬으로 실행하거나, PyInstaller로 만든 실행 파일을 사용합니다.

```bash
# 파이썬 스크립트 실행
python dto_generator.py

# 또는 exe 실행 (Windows)
dto_generator.exe
```

## 3. 복사한 결과 붙여넣기

1. 도구가 요청할 때, 복사해 둔 조회 결과를 **한 줄씩** 붙여넣거나 전체 붙여넣기합니다.
   ```text
   AFFI_SEQint계열사순번
   AFFI_NMvarchar(200)계열사명
   ...
   ```
2. 마지막 줄에서 Enter를 두 번 누르면 VO 클래스 파일이 생성됩니다.

## 4. 생성된 파일 확인

- 생성된 Java 파일은 현재 작업 디렉터리 하위의 `vo/ExamplePVO.java` 경로에 저장됩니다.
- 콘솔에 아래와 같은 형식으로 출력됩니다:
  ```text
  ========================================
  Generated VO at: /path/to/current/dir/vo/ExamplePVO.java
  ========================================
  ```

## 5. 반복 및 종료

- 생성 후 `Generate another? (y/n):` 메시지가 표시됩니다.
  - `y`를 입력하면 다시 1번 단계부터 진행
  - 그 외 입력 시 종료

---

## 옵션 및 커스터마이징

스크립트 상단의 기본 값을 수정해보세요:

```python
DEFAULT_PACKAGE     = "vo"
DEFAULT_CLASS_NAME  = "ExamplePVO"
DEFAULT_AUTHOR      = "작성자명"
DEFAULT_DESCRIPTION = "테이블 설명PVO"
```

추가 SQL 타입 매핑이 필요하면 `map_sql_type()` 함수를 업데이트하세요.

---

*이 문서는 dto_generator 도구 사용을 돕기 위해 자동 생성되었습니다.*

