# HttpServletResponse - wait() 메서드
- 응답시간을 제어할 수 있습니다.
```java
synchronized (response) {
    try {
        response.wait(3000);
    } catch (InterruptedException e) {
        throw new RuntimeException(e);
    }
}
```
- 단 호출하려면 해당 객체에 대해 동기화가 필요합니다.
- 따라서 해당 객체를 동기화 시키기 위해 synchronized를 이용합니다.