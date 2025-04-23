# 💡 MyBatis 동적 SQL 조립 예시 모음

MyBatis는 SQL을 XML 기반으로 동적으로 조립할 수 있는 강력한 기능을 제공한다. 다양한 조건에 따라 SQL 문장을 유연하게 조합하는 데 자주 사용하는 실전 예제들을 정리한다.

---

## 1. 조건부 WHERE 절 (`<if>`)

```xml
WHERE 1=1
<if test="name != null and name != ''">
  AND NAME = #{name}
</if>
<if test="status != null">
  AND STATUS = #{status}
</if>
```

👉 필요한 조건만 WHERE 절에 동적으로 붙음  
✅ 필터 기능이 있는 리스트 조회에서 매우 자주 쓰임

---

## 2. 조건부 SET 절 (UPDATE 쿼리)

```xml
<update id="updateUser">
  UPDATE USER
  <set>
    <if test="name != null">NAME = #{name},</if>
    <if test="email != null">EMAIL = #{email},</if>
    <if test="phone != null">PHONE = #{phone}</if>
  </set>
  WHERE ID = #{id}
</update>
```

👉 null이 아닌 필드만 업데이트됨  
✅ 유저 정보 수정 시 자주 등장

---

## 3. 조건부 정렬 (`<choose>` 사용)

```xml
<choose>
  <when test="sort == 'date'">
    ORDER BY CREATED_AT DESC
  </when>
  <when test="sort == 'name'">
    ORDER BY NAME ASC
  </when>
  <otherwise>
    ORDER BY ID DESC
  </otherwise>
</choose>
```

👉 어떤 필드로 정렬할지 동적으로 결정 가능

---

## 4. IN 절 조건 (리스트 기반)

```xml
<if test="idList != null and idList.size() > 0">
  AND ID IN
  <foreach collection="idList" item="id" open="(" separator="," close=")">
    #{id}
  </foreach>
</if>
```

👉 다중 선택 필터, 체크박스 선택 등에서 자주 사용됨  
✅ SQL Injection 방지도 가능한 안전한 방식

---

## 5. 동적 JOIN

```xml
SELECT t.*, u.name
FROM TASK t
<if test="includeUser">
  LEFT JOIN USER u ON t.user_id = u.id
</if>
```

👉 조건에 따라 필요한 테이블만 JOIN하여 성능 최적화 가능

---

## 6. WHERE 절의 시작을 자동 제어 (`<trim>`)

```xml
<trim prefix="WHERE" prefixOverrides="AND |OR ">
  <if test="title != null">AND TITLE = #{title}</if>
  <if test="category != null">AND CATEGORY = #{category}</if>
</trim>
```

👉 첫 번째 조건 앞에 붙는 `AND` 또는 `OR`를 자동으로 제거해줌  
✅ WHERE 절을 더 깔끔하고 유연하게 구성 가능

---

## 7. 조건별로 서로 다른 SQL 선택 (전체 조회 vs 페이징 조회)

```xml
<choose>
  <when test="searchAll">
    SELECT * FROM PRODUCT
  </when>
  <otherwise>
    SELECT * FROM PRODUCT LIMIT #{limit} OFFSET #{offset}
  </otherwise>
</choose>
```

👉 조회 범위 조절이 필요한 상황에서 유용하게 사용됨

---

이러한 동적 SQL 조립 방식은 MyBatis에서 **조건부 쿼리, 업데이트, 정렬, 페이징, 다중 선택, 동적 조인**을 유연하게 처리할 수 있게 해준다.

