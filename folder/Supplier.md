# Supplier<T> 
- 다른 함수형 인터페이스들의 추상메서드는 모두 매개변수를 받았는데,
Supplier<T>는 특이하게 매개변수를 받지 않고 단순히 무엇인가를 반환하는
추상메서드가 존재합니다.

```java
import java.util.function.Supplier;

public class SupplierExample {
    public static void main(String[] args) {
        Supplier<String> helloSupplier = () -> "Hello ";

        System.out.println(helloSupplier.get() + "World");
    }
}
```
- Lazy Evaluation
    - 직역은 "게으른 연산"으로, 불필요한 연산을 피하기 위해 연산을 지연시키는 것을 말합니다.
    - 즉 불필요한 연산을 피한다는 의미입니다.

```java
import java.util.concurrent.TimeUnit;
import java.util.function.Supplier;

public class SupplierExample {
    public static void main(String[] args) {
        long start = System.currentTimeMillis();
        
        printIfValidIndex(0, getVeryExpensiveValue());
        printIfValidIndex(-1, getVeryExpensiveValue());
        printIfValidIndex(-2, getVeryExpensiveValue());
        System.out.println("It took " + ((System.currentTimeMillis() - start) / 1000) + " Second");
    }

    public static String getVeryExpensiveValue() {
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        //Let's just say it has very expensive calculation here!
        return "Kaltz";
    }
    
    public static void printIfValidIndex(int number, String value) {
        if (number >= 0) {
            System.out.println("The value is " + value + ".");
        } else {
            System.out.println("Invalid");
        }
    }
}
```
```dtd
The value is Kaltz.
Invalid
Invalid
It took 3 Second
```
- 위 코드의 결과를 보면 실제적으로 불필요한 연산을 제거하고, 결과가 3초로 나오는 것을 확인할 수 있습니다