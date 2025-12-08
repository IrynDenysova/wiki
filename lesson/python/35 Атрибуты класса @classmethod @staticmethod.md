# Атрибуты класса @classmethod @staticmethod

## 📖 Быстрая навигация по операторам и функциям

- [[#План занятия]](#план-занятия)
- [[#1) Поля класса (атрибуты класса)]](#1-поля-класса-атрибуты-класса)
- [[#2) Доступ к полям класса и изменение]](#2-доступ-к-полям-класса-и-изменение)
- [[#3) Магическое поле `__dict__`]](#3-магическое-поле-dict)
- [[#4) Поля объекта по умолчанию]](#4-поля-объекта-по-умолчанию)
- [[#5) Классовые методы: `@classmethod`]](#5-классовые-методы-classmethod)
- [[#6) Статические методы: `@staticmethod`]](#6-статические-методы-staticmethod)
- [[#7) `__str__` и `__repr__`]](#7-str-и-repr)
- [[#9.1 Класс `City` + `distance()` (static) + `__str__`]](#91-класс-city-distance-static-str)
- [[#9.2 `from_string()` (classmethod) — создание из строки]](#92-fromstring-classmethod-—-создание-из-строки)
- [[#ДЗ 1) Счётчик экземпляров (`total_users`)]](#дз-1-счётчик-экземпляров-totalusers)
- [[#ДЗ 2) Валидация + `__str__` + `ValueError`]](#дз-2-валидация-str-valueerror)
- [[#Мини-шпаргалка (самое важное)]](#мини-шпаргалка-самое-важное)
- [[#📚 Дополнительная информация]](#📚-дополнительная-информация)

**[[#📚 Дополнительная информация]](#дополнительная-информация)**

---

## 1) Поля класса (атрибуты класса)
**Поле класса** — переменная, которая принадлежит **самому классу**, а не конкретному объекту.  
Все экземпляры класса могут читать это поле, а значение хранится “в одном месте” — в классе.

Синтаксис:
```py
class ClassName:
    class_attribute = value  # поле класса
```

Пример (поле класса + поля объекта):
```py
class Book:
    library_name = "Central Library"  # поле класса

    def __init__(self, title, author):
        self.title = title            # поле объекта
        self.author = author          # поле объекта
```

Когда использовать поля класса:
- для **общих настроек** (язык/формат по умолчанию),
- для **счётчиков** (сколько создано объектов),
- когда значение **одинаково** для всех объектов.

---

## 2) Доступ к полям класса и изменение

### 2.1 Чтение поля класса
Можно читать:
- через класс: `ClassName.attribute`
- через объект: `obj.attribute`
- внутри методов: `self.attribute` или `ClassName.attribute`

```py
class Book:
    library_name = "Central Library"

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def show_library(self):
        print(self.library_name)   # через self (если у объекта нет такого поля — возьмёт из класса)
        print(Book.library_name)   # через имя класса

print(Book.library_name)

book = Book("1984", "George Orwell")
print(book.library_name)
book.show_library()
```

### 2.2 Изменение поля через класс (меняется для всех объектов)
Если нужно изменить значение для **всех** экземпляров — меняем через **класс**:
```py
book1 = Book("1984", "George Orwell")
book2 = Book("Brave New World", "Aldous Huxley")

Book.library_name = "City Library"
print(Book.library_name)
print(book1.library_name)  # тоже "City Library"
print(book2.library_name)  # тоже "City Library"
```

### 2.3 “Изменение” через объект: на деле создаётся новое поле объекта
Если присваивать `obj.library_name = ...`, Python **создаёт атрибут в объекте**, не меняя поле класса.
```py
book1 = Book("1984", "George Orwell")
book2 = Book("Brave New World", "Aldous Huxley")

book1.library_name = "Private Shelf"  # тень (override) только у book1

print(book1.library_name)  # "Private Shelf" (атрибут объекта)
print(Book.library_name)   # поле класса не поменялось
print(book2.library_name)  # читает поле класса
```

### 2.4 Механизм поиска атрибутов
При `obj.attr` Python ищет:
1) сначала в **самом объекте**
2) если не нашёл — в **классе**

---

## 3) Магическое поле `__dict__`
`__dict__` — словарь явно заданных атрибутов.

- `obj.__dict__` — атрибуты **конкретного объекта**
- `ClassName.__dict__` — атрибуты **класса** (включая методы и поля класса)

```py
book1 = Book("1984", "George Orwell")
book2 = Book("Brave New World", "Aldous Huxley")

book1.library_name = "Private Shelf"  # появится только у book1

print(book1.__dict__)  # {'title': ..., 'author': ..., 'library_name': 'Private Shelf'}
print(book2.__dict__)  # {'title': ..., 'author': ...}
print(Book.__dict__)   # много всего: методы + поля класса
```

### Добавление новых полей “снаружи” (не рекомендуется)
Python позволяет добавить поле к объекту/классу в любой момент, но это ухудшает читаемость и поддержку:
```py
book1.book_color = "black"       # поле объекта извне
Book.default_language = "eng"    # поле класса извне
```

---

## 4) Поля объекта по умолчанию
Чтобы задать базовое значение поля, используем значение по умолчанию в `__init__`:
```py
class Book:
    def __init__(self, title, author, language="English"):
        self.title = title
        self.author = author
        self.language = language

book1 = Book("1984", "George Orwell")                 # язык по умолчанию
book2 = Book("Cien años de soledad", "G. G. Márquez", "Spanish")
print(book1.language)
print(book2.language)
```

---

## 5) Классовые методы: `@classmethod`
**Классовый метод** работает с **классом**, а не с объектом:
- получает первым аргументом **`cls`** (ссылка на класс),
- удобен для работы с полями класса,
- часто используется как **альтернативный конструктор**.

Синтаксис:
```py
class ClassName:
    @classmethod
    def method_name(cls, ...):
        ...
```

### 5.1 Счётчик созданных объектов (поле класса + classmethod)
```py
class Book:
    total_books = 0

    def __init__(self, title, author):
        self.title = title
        self.author = author
        Book.total_books += 1

    @classmethod
    def show_total(cls):
        print(f"Total books: {cls.total_books}")

Book.show_total()
b1 = Book("1984", "George Orwell")
b2 = Book("Brave New World", "Aldous Huxley")
Book.show_total()
b1.show_total()  # можно вызывать и через объект (cls всё равно будет Book)
```

### 5.2 Альтернативный конструктор: `from_string`
```py
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    @classmethod
    def from_string(cls, data):
        title, author = data.split(" - ")
        return cls(title, author)  # создаёт и возвращает объект

book = Book.from_string("1984 - George Orwell")
print(book.title, book.author)
```

---

## 6) Статические методы: `@staticmethod`
**Статический метод** не зависит ни от объекта, ни от класса:
- не получает автоматически `self` или `cls`,
- логически “принадлежит” классу (удобно группировать связанную логику).

Синтаксис:
```py
class ClassName:
    @staticmethod
    def method_name(...):
        ...
```

Пример: валидация значения:
```py
class Book:
    def __init__(self, title):
        self.title = title

    @staticmethod
    def is_title_valid(title):
        return isinstance(title, str) and len(title) > 0

print(Book.is_title_valid("1984"))  # True
print(Book.is_title_valid(""))      # False
print(Book.is_title_valid(123))     # False
```

Пример: “логически связанные”, но независимые операции:
```py
class MathHelper:
    @staticmethod
    def square(x):
        return x * x

    @staticmethod
    def cube(x):
        return x * x * x
```

### 6.1 Сравнение типов методов (главное)
```text
Обычный метод:        def m(self, ...)        -> работает с объектом
Классовый метод:      @classmethod def m(cls, ...) -> работает с классом / альтернативный конструктор
Статический метод:    @staticmethod def m(...)     -> логическая функция внутри класса (без self/cls)
```

---

## 7) `__str__` и `__repr__`
### 7.1 `__str__`: “человеческое” представление (для print)
`print(obj)` вызывает `obj.__str__()` (если определён).

```py
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"{self.title} by {self.author}"

book = Book("1984", "George Orwell")
print(book)       # использует __str__
print(str(book))  # тоже __str__
```

Правила:
- `__str__` **не печатает**, а **возвращает** строку.

### 7.2 `__repr__`: техническое/отладочное представление
Чаще видно:
- при `repr(obj)`
- при выводе объектов в списках/коллекциях
- в дебаге/интерактивной оболочке

```py
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __repr__(self):
        return f"Book(title={self.title!r}, author={self.author!r})"

b1 = Book("1984", "George Orwell")
b2 = Book("Brave New World", "Aldous Huxley")
print(repr(b1))
print([b1, b2])  # внутри списка будет __repr__
```

Если `__str__` не определён, Python часто использует `__repr__` как запасной вариант для `print(obj)`.

---

# 8) Задания для закрепления — ответы
### 8.1 Поля класса: правильные варианты
a) поле класса общее для всех объектов ✅  
d) поле класса можно прочитать через объект ✅  
Ответ: **a, d**

### 8.2 `@classmethod`: правильные варианты
b) может создавать объект класса ✅  
e) имеет доступ к классу ✅  
Ответ: **b, e**

### 8.3 Ошибка в коде со `@staticmethod`
```py
class Person:
    @staticmethod
    def greet(self):
        print("Hello!")
```
Ошибка: у статического метода **не должно** быть параметра `self`.

Правильно:
```py
class Person:
    @staticmethod
    def greet():
        print("Hello!")
```

---

# 9) Практическая работа — решения

## 9.1 Класс `City` + `distance()` (static) + `__str__`
Задание: город с `name`, `latitude`, `longitude`, вывод объекта и вычисление “расстояния” как разницы координат.

```py
class City:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"City: {self.name} ({self.latitude}, {self.longitude})"

    @staticmethod
    def distance(city1, city2):
        lat_diff = round(city1.latitude - city2.latitude, 2)
        lon_diff = round(city1.longitude - city2.longitude, 2)
        return lat_diff, lon_diff


berlin = City("Berlin", 52.52, 13.40)
paris = City("Paris", 48.85, 2.35)

print(berlin)
print(paris)
print("Distance:", City.distance(berlin, paris))
```

## 9.2 `from_string()` (classmethod) — создание из строки
Формат: `"Rome:41.89,12.51"`

```py
class City:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"City: {self.name} ({self.latitude}, {self.longitude})"

    @classmethod
    def from_string(cls, data):
        name_part, coords_part = data.split(":")
        lat, lon = map(float, coords_part.split(","))
        return cls(name_part, lat, lon)

    @staticmethod
    def distance(city1, city2):
        lat_diff = round(city1.latitude - city2.latitude, 2)
        lon_diff = round(city1.longitude - city2.longitude, 2)
        return lat_diff, lon_diff


rome = City.from_string("Rome:41.89,12.51")
print(rome)
```

---

# 10) Домашнее задание — решения

## ДЗ 1) Счётчик экземпляров (`total_users`)
Требования:
- `User(username, password)`
- класс-атрибут `total_users`
- при создании нового пользователя увеличиваем счётчик
- метод `get_total()`

```py
class User:
    total_users = 0  # поле класса

    def __init__(self, username, password):
        self.username = username
        self.password = password
        User.total_users += 1

    @classmethod
    def get_total(cls):
        return cls.total_users


u1 = User("alice", "secret")
u2 = User("bob", "qwerty")
print("Total users:", User.get_total())
```

## ДЗ 2) Валидация + `__str__` + `ValueError`
Требования:
- username: непустая строка
- password: строка длиной минимум 5
- при ошибке: `ValueError`
- строковое представление пользователя

```py
class User:
    total_users = 0

    def __init__(self, username, password):
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Invalid username")
        if not isinstance(password, str) or len(password) < 5:
            raise ValueError(f"Invalid password: {password!r}")

        self.username = username
        self.password = password
        User.total_users += 1

    def __str__(self):
        return f"User: {self.username}"

    @classmethod
    def get_total(cls):
        return cls.total_users


user1 = User("alice", "secret")
print(user1)

try:
    user2 = User("bob", "qwe")
except ValueError as e:
    print("ValueError:", e)
```

---

## Мини-шпаргалка (самое важное)
```text
Поле класса: ClassName.attr = value
Поле объекта: self.attr = value  (обычно в __init__)

Чтение: obj.attr -> сначала ищет в obj.__dict__, потом в ClassName.__dict__

Изменение через класс: ClassName.attr = ... -> меняется для всех
Присваивание через объект: obj.attr = ... -> создаёт/переопределяет атрибут только у obj

@classmethod -> первый аргумент cls, работает с классом / альт. конструкторы
@staticmethod -> без self/cls, логическая функция внутри класса

__str__ -> для пользователя (print)
__repr__ -> для разработчика (debug/коллекции)
__dict__ -> словарь атрибутов
```


---

## 📚 Дополнительная информация

_Этот раздел будет дополнен практическими примерами и дополнительной информацией._
