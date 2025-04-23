# 🔄 Spring `@Transactional` : 롤백 조건과 예외 처리 전략

Spring의 `@Transactional`은 예외가 발생할 경우 자동으로 트랜잭션을 **롤백**해주는 편리한 기능을 제공하지만,  
예외의 종류나 사용 방식에 따라 **롤백이 발생하지 않을 수 있다.**

---

## ✅ 기본 동작

- **`RuntimeException` 또는 그 하위 클래스**가 발생하면 자동으로 롤백된다.
- **`Checked Exception`은 기본적으로 롤백되지 않는다.**

---

## ❗ 예외 상황별 트랜잭션 롤백 여부

| 예외 타입 | 롤백 여부 | 설명 |
|----------|------------|------|
| `RuntimeException` | ✅ 롤백 | 기본 동작 |
| `BizException extends RuntimeException` | ✅ 롤백 | 커스텀 예외지만 unchecked이므로 롤백됨 |
| `Exception` (Checked) | ❌ 롤백 안 됨 | 명시적으로 설정 필요 |
| `@Transactional(rollbackFor = Exception.class)` | ✅ 롤백 | checked 예외도 롤백 지정 가능 |
| 예외를 catch 후 swallow | ❌ 롤백 안 됨 | throw 하지 않으면 롤백 트리거되지 않음 |

---

## 🧱 예시: 커스텀 예외 + 롤백

```java
public class BizException extends RuntimeException {
    public BizException(HttpStatus status, String code, String message, Throwable cause) {
        super(message, cause);
        // 상태 코드, 에러 코드, 원인 예외 등을 멤버로 구성할 수 있음
    }
}
```

```java
@Transactional
public void doSomething() {
    if (invalidAccess) {
        throw new BizException(HttpStatus.UNAUTHORIZED, "401", "UNAUTHORIZED", e);
    }
}
```

- `BizException`은 `RuntimeException`을 상속하므로 트랜잭션 자동 롤백됨
- 메시지, 상태 코드, 원인 예외 등도 함께 전달 가능하여 API 응답 처리도 유연하게 가능

---

## ⚠ 트랜잭션이 롤백되지 않는 구조적 문제들

### 1. 같은 클래스 내부 메서드 호출

```java
@Service
public class MyService {
    @Transactional
    public void outer() {
        inner(); // ❌ 트랜잭션 적용 안 됨
    }

    @Transactional
    public void inner() {
        throw new BizException(...); // 롤백되지 않음
    }
}
```

- 해결: `inner()`를 다른 Bean으로 분리하거나, 프록시 구조를 명확히 활용해야 함

---

### 2. readOnly = true 옵션 주의

```java
@Transactional(readOnly = true)
public void modifyData() {
    // ❗ 실제 데이터 수정 시 동작이 예측과 다를 수 있음
}
```

- 일부 DB에서는 update/delete가 예외를 발생하거나 적용되지 않을 수 있음

---

## ✅ 트랜잭션 100% 보장을 위한 체크리스트

1. ❓ 예외 타입이 RuntimeException인가?
2. ❓ rollbackFor 설정이 필요한 checked 예외인가?
3. ❓ 예외를 catch 후 무시하지는 않았는가?
4. ❓ 메서드 호출은 프록시 구조를 타고 있는가?
5. ❓ readOnly 트랜잭션에서 write 작업을 시도하지 않았는가?

---

이 체크리스트를 충족하면 `@Transactional`의 롤백은 완전히 보장된다.
