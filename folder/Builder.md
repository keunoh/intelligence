# 빌더 패턴 구조
```java
class Student {
    private int id;
    private String name = "아무개";
    private String grade = "freshman";
    private String phoneNumber = "010-0000-0000";

    public Student(int id, String name, String grade, String phoneNumber) {
        this.id = id;
        this.name = name;
        this.grade = grade;
        this.phoneNumber = phoneNumber;
    }
    
    @Override
    public String toString() {
        return "Student { " +
                "id='" + id + '\'' +
                ", name=" + name +
                ", grade=" + grade +
                ", phoneNumber=" + phoneNumber +
                " }";
    }
}
```
- 빌더 클래스 구현하기
먼저 Builder 클래스를 만들고 필드 멤버 구성을 만들고자 하는 Student 클래스 멤버 구성과 똑같이 구성한다.
```java
class StudentBuilder {
    private int id;
    private String name;
    private String grade;
    private String phoneNumber;

    public StudentBuilder id(int id) {
        this.id = id;
        return this;
    }

    public StudentBuilder name(String name) {
        this.name = name;
        return this;
    }

    public StudentBuilder grade(String grade) {
        this.grade = grade;
        return this;
    }

    public StudentBuilder phoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
        return this;
    }
}
```
여기서 주목할 부분은 각 Setter 함수 마지막 반환 구문인 return this 부분이다.
여기서 this란 StudentBuilder 객체 자신을 말한다. 즉 빌더 객체 자신을 리턴함으로써
메서드 호출 후 연속적으로 빌더 메서드들을 체이닝(Chaining) 하여 호출할 수 있게 된다.
마지막으로 빌더의 목표였던 최종 Student 객체를 만들어주는 build 메서드를 구성해준다.
빌더 클래스의 필드들을 Student 생성자의 인자에 넣어줌으로써 멤버 구성이 완료된
Student 인스턴스를 얻게 되는 것이다.
```java
class StudentBuilder {
    private int id;
    private String name;
    private String grade;
    private String phoneNumber;

    public StudentBuilder id(int id) { ... }

    public StudentBuilder name(String name) { ... }

    public StudentBuilder grade(String grade) { ... }

    public StudentBuilder phoneNumber(String phoneNumber) { ... }

    public Student build() {
        return new Student(id, name, grade, phoneNumber); // Student 생성자 호출
    }
}
```