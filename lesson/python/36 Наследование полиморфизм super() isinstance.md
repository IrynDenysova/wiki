# Наследование полиморфизм super() isinstance

## 1) Принципы ООП (быстрое повторение)
- **Наследование** — дочерний класс перенимает поля/методы родителя, чтобы переиспользовать логику и не дублировать код.
- **Инкапсуляция** — скрываем внутреннее устройство и даём понятный интерфейс.
- **Полиморфизм** — один и тот же метод/интерфейс ведёт себя по‑разному у разных типов.
- **Абстракция** — выделяем главное и задаём интерфейс для будущих реализаций.

---

## 2) Наследование: базовые понятия и синтаксис
- **Родительский класс**: base / parent / superclass
- **Дочерний класс**: child / derived / subclass

Синтаксис:
```py
class Parent:
    ...

class Child(Parent):
    ...
```

### Пример: наследуем поля и методы
```py
class Employee:
    def __init__(self, name):
        self.name = name

    def work(self):
        print(f"{self.name} is working...")


class Programmer(Employee):
    pass


class Manager(Employee):
    pass


programmer = Programmer("Alice")
manager = Manager("Bob")

programmer.work()
manager.work()
```
Идея:
- `Programmer` и `Manager` “получили бесплатно” и `name`, и `work()` от `Employee`.

### Что важно помнить
- Дочерний класс наследует **все** поля/методы родителя.
- Можно добавлять свои поля и методы, не меняя родителя.
- Можно **переопределять** методы, чтобы изменить поведение.

---

## 3) Полиморфизм: переопределение метода (overriding)
Полиморфизм чаще всего проявляется так:
- у разных подклассов есть метод с одинаковым именем,
- но реализация отличается,
- код вызывает метод одинаково: `obj.work()`, а поведение меняется по типу объекта.

### Пример: у каждого “work” своё
```py
class Employee:
    def __init__(self, name):
        self.name = name

    def work(self):
        print(f"{self.name} is working...")


class Programmer(Employee):
    def work(self):
        print(f"{self.name} writing code...")


class Manager(Employee):
    def work(self):
        print(f"{self.name} managing team...")


staff = [Programmer("Alice"), Manager("Bob"), Programmer("Bill")]
for person in staff:
    person.work()  # один вызов -> разное поведение
```

### Важно: “перегрузки” по аргументам в Python нет
В Python нельзя определить два метода с одним именем, рассчитывая на перегрузку по количеству аргументов.
Последнее определение просто **перезапишет** предыдущее:
```py
class Math:
    def add(self, a, b):
        return a + b

    def add(self, a, b, c):
        return a + b + c

m = Math()
print(m.add(1, 2, 3))  # ok
print(m.add(1, 2))     # TypeError
```

---

## 4) `super()` — правильный вызов методов родителя
Зачем нужен `super()`:
- не дублировать логику родителя (DRY),
- правильно работать при изменении иерархии,
- корректно вызывать цепочку методов при (потенциальном) множественном наследовании.

### 4.1 Плохой вариант: дублирование кода родителя
```py
class Employee:
    def __init__(self, name):
        self.name = name

class Programmer(Employee):
    def __init__(self, name, language):
        self.name = name          # дублирование
        self.language = language
```

### 4.2 Тоже нежелательно: явный вызов `Employee.__init__`
```py
class Programmer(Employee):
    def __init__(self, name, language):
        Employee.__init__(self, name)  # жёсткая привязка к имени родителя
        self.language = language
```

### 4.3 Правильно: `super().__init__(...)`
```py
class Programmer(Employee):
    def __init__(self, name, language):
        super().__init__(name)
        self.language = language
```

### Частая ошибка
```py
super(name).__init__()  # ❌ неверно
```
Правильно:
```py
super().__init__(name)  # ✅
```

---

## 5) `super()` в многоуровневом наследовании
```py
class Person:
    def __init__(self, name):
        self.name = name
        print(f"Init Person: {self.name}")


class Employee(Person):
    def work(self):
        print(f"{self.name} is working...")


class Manager(Employee):
    def __init__(self, name, department):
        super().__init__(name)
        self.department = department
        print(f"Init Manager: {self.name} manages {self.department}")


m = Manager("Alice", "Development")
```

---

## 6) `super()` в обычных методах (расширяем, а не заменяем)
```py
class Employee:
    def work(self):
        print("Employee is doing general tasks.")


class Programmer(Employee):
    def work(self):
        super().work()
        print("Programmer is writing code.")


class Manager(Employee):
    def work(self):
        super().work()
        print("Manager is holding a meeting.")


staff = [Programmer(), Manager()]
for person in staff:
    person.work()
    print()
```

---

## 7) Наследование от `object`
В Python все классы **неявно** наследуются от `object`, даже если это не указано:
```py
class Book:
    pass
```
Эквивалентно:
```py
class Book(object):
    pass
```
Это даёт базовые методы “по умолчанию” (например, `__str__`, `__init__` и др.).

---

## 8) `isinstance()` и `issubclass()`
### 8.1 `isinstance(obj, class_or_tuple)`
Проверяет: объект — экземпляр класса **или его наследников**.
```py
isinstance(obj, SomeClass)
isinstance(obj, (A, B, C))
```

Пример:
```py
class Employee: ...
class Programmer(Employee): ...
p = Programmer()

print(isinstance(p, Programmer))  # True
print(isinstance(p, Employee))    # True (наследник)
print(isinstance(p, object))      # True (все от object)
```

Практичный кейс: вызывать метод, который есть не у всех
```py
class Employee:
    def work(self):
        print("Выполняет общие задачи")

class Programmer(Employee):
    def write_code(self):
        print("Пишет код")

class Manager(Employee):
    def work(self):
        print("Проводит собрание")

staff = [Programmer(), Manager(), Employee()]

for person in staff:
    if isinstance(person, Programmer):
        person.write_code()
    else:
        person.work()
```

### 8.2 `issubclass(class_a, class_b)`
Проверяет: класс `class_a` является подклассом `class_b` (прямо или через цепочку).
```py
issubclass(A, B)
issubclass(A, (B, C))
```

Пример:
```py
class Employee: ...
class Programmer(Employee): ...
class BackendDeveloper(Programmer): ...

print(issubclass(Programmer, Employee))         # True
print(issubclass(BackendDeveloper, Programmer)) # True
print(issubclass(BackendDeveloper, Employee))   # True (через цепочку)
```

✅ Важно: `issubclass` принимает **классы**, не объекты:
```py
class Book: ...
b = Book()
print(issubclass(b, object))  # TypeError
```

---

# 9) Задания для закрепления — ответы
1) `Manager` наследует `work()` от `Employee`, поэтому будет напечатано: **Employee is working**.  
2) Преимущества наследования: **b, d** (меньше кода, переиспользование логики).  
3) Ошибка в `super(name).__init__()` → нужно **`super().__init__(name)`**.  
4) `issubclass(b, object)` → **TypeError**, потому что `b` — объект, а нужен класс.  
5) `isinstance()` используется для проверки, что объект является экземпляром класса или его наследника.

---

# 10) Практическая работа — решения

## 10.1 Класс `Employee`
```py
class Employee:
    def __init__(self, name):
        self.name = name

    def work(self):
        print(f"{self.name} is working...")

e = Employee("Alice")
e.work()
```

## 10.2 Класс `Developer` (наследник) + переопределение `work()` + `super()`
```py
class Developer(Employee):
    def __init__(self, name, language):
        super().__init__(name)
        self.language = language

    def work(self):
        super().work()
        print(f"{self.name} writes {self.language} code.")

d = Developer("Bob", "Python")
d.work()
```

---

# 11) Домашнее задание — решения

## 11.1 Класс `Person`
```py
class Person:
    def __init__(self, name):
        self.name = name

    def introduce(self):
        print(f"Hello, my name is {self.name}.")
```

## 11.2 Класс `Student(Person)` + `course` + расширенный `introduce()`
Требование: сначала базовое приветствие, затем строка про курс.
```py
class Student(Person):
    def __init__(self, name, course):
        super().__init__(name)
        self.course = course

    def introduce(self):
        super().introduce()
        print(f"I'm on course {self.course}.")
```

## 11.3 Класс `Teacher(Person)` + `subject` + свой `introduce()`
```py
class Teacher(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject

    def introduce(self):
        print(f"Hello, I am professor {self.name}.")
        print(f"My subject is {self.subject}.")
```

## 11.4 Список людей (Student + Teacher) и полиморфизм
```py
people = [
    Student("Alice", 2),
    Teacher("Bob", "Mathematics"),
]

for p in people:
    p.introduce()
```
Идея: **один вызов `introduce()`**, но разные реализации у разных классов.

---

## Мини-шпаргалка урока
```text
Наследование:
class Child(Parent): ...

Переопределение (полиморфизм):
class Child(Parent):
    def method(self): ...

super():
- в __init__: super().__init__(...)
- в обычных методах: super().method()

object:
все классы наследуют от object (неявно)

isinstance(obj, Class)  -> проверяет объект (экземпляр/наследник)
issubclass(A, B)        -> проверяет класс (подкласс)
```
