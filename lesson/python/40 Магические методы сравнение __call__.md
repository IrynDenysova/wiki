# Магические методы сравнение __call__

## 📖 Быстрая навигация по операторам и функциям

- [[#1) Методы сравнения (comparison dunder methods)]](#1-методы-сравнения-comparison-dunder-methods)
- [[#2) `functools.total_ordering`]](#2-functoolstotalordering)
- [[#3) Индексация и доступ к элементам (объект как коллекция)]](#3-индексация-и-доступ-к-элементам-объект-как-коллекция)
- [[#4) Арифметические методы]](#4-арифметические-методы)
- [[#5) `__bool__`: поведение в `if/while`]](#5-bool-поведение-в-ifwhile)
- [[#6) `__call__`: делаем объект вызываемым как функцию]](#6-call-делаем-объект-вызываемым-как-функцию)
- [[#1) Про `@total_ordering`]](#1-про-totalordering)
- [[#2) Найдите ошибку в коде]](#2-найдите-ошибку-в-коде)
- [[#3) Про `__call__`]](#3-про-call)
- [[#ДЗ 1) Класс `Email`]](#дз-1-класс-email)
- [[#ДЗ 2) Класс `Money`]](#дз-2-класс-money)
- [[#Мини-шпаргалка урока]](#мини-шпаргалка-урока)
- [[#Дополнительная информация]](#дополнительная-информация)


---

## 2) `functools.total_ordering`
Чтобы не писать все 6 методов сравнения вручную, можно использовать `@total_ordering`:
- вы реализуете `__eq__` и **один** из: `__lt__`, `__le__`, `__gt__`, `__ge__`
- остальное Python создаст автоматически

```py
from functools import total_ordering

@total_ordering
class Book:
    def __init__(self, title: str):
        self.title = title

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return self.title == other.title

    def __lt__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return self.title < other.title
```

---

## 3) Индексация и доступ к элементам (объект как коллекция)
Если объект должен вести себя как список/словарь — переопределяем:

| Метод | Что делает | Вызывается |
|---|---|---|
| `__getitem__` | получить элемент по ключу/индексу | `obj[key]` |
| `__setitem__` | установить значение | `obj[key] = value` |
| `__contains__` | проверить наличие | `key in obj` |
| `__len__` | вернуть размер | `len(obj)` |

### Пример: коллекция заметок `Notes`
Требования из урока:
- ключи приводятся к lower-case,
- пустые строки запрещены,
- поддержка `[]`, `in`, `len()`, строкового вывода.

```py
class Notes:
    def __init__(self):
        self._data = {}

    def __getitem__(self, key):
        return self._data[key.lower()]

    def __setitem__(self, key, value):
        if value.strip():
            self._data[key.lower()] = value
        else:
            raise ValueError("Empty notes are not allowed")

    def __contains__(self, key):
        return key.lower() in self._data

    def __len__(self):
        return len(self._data)

    def __str__(self):
        result = "Notes:\n"
        for key, value in self._data.items():
            result += f"- {key}: {value}\n"
        return result.strip()


notes = Notes()
notes["Idea"] = "Build a game"
notes["TODO"] = "Finish the project"

print(notes["idea"])
print("todo" in notes)
print(len(notes))
print(notes)
```

---

## 4) Арифметические методы
Позволяют переопределить поведение операторов `+ - * / // % **` и т.д.

| Метод | Оператор |
|---|---|
| `__add__` | `+` |
| `__sub__` | `-` |
| `__mul__` | `*` |
| `__truediv__` | `/` |
| `__floordiv__` | `//` |
| `__mod__` | `%` |
| `__pow__` | `**` |

### Пример: 2D-вектор
```py
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"({self.x}, {self.y})"


a = Vector(2, 3)
b = Vector(1, 4)
c = a + b
print(c)  # (3, 7)
```

### Инкрементные операции (изменение “на месте”)
Для `+=` и подобных:
- `__iadd__`, `__isub__`, `__imul__`, `__itruediv__`, `__ifloordiv__`, `__imod__`, `__ipow__`
- метод должен изменять объект и **возвращать self**

```py
class Counter:
    def __init__(self, value=0):
        self.value = value

    def __iadd__(self, other):
        self.value += other
        return self

    def __str__(self):
        return f"Counter({self.value})"


c = Counter(5)
old_id = id(c)
c += 3
new_id = id(c)
print(old_id == new_id)  # True (тот же объект)
print(c)                 # Counter(8)
```

---

## 5) `__bool__`: поведение в `if/while`
`__bool__` определяет “истинность” объекта в логических выражениях.

```py
class Counter:
    def __init__(self, value):
        self.value = value

    def __bool__(self):
        return self.value > 0


c1 = Counter(-5)
c2 = Counter(3)

print(bool(c1))  # False
print(bool(c2))  # True

if c1:
    print("Есть элементы")
else:
    print("Пусто")
```

---

## 6) `__call__`: делаем объект вызываемым как функцию
Если реализован `__call__`, объект можно вызывать: `obj(...)`.

```py
class CurrencyConverter:
    def __init__(self, rate):
        self.rate = rate  # сколько единиц валюты за 1 доллар

    def __call__(self, dollars):
        return dollars * self.rate


euro_converter = CurrencyConverter(0.88)
print(euro_converter(10))   # 8.8
print(euro_converter(5.5))  # 4.84
```

---

# Задания для закрепления — ответы

## 1) Про `@total_ordering`
Верно: **b, c**  
- b) достаточно `__eq__` и одного из `__lt__/__le__/__gt__/__ge__`  
- c) недостающие методы сравнения создаются автоматически

## 2) Найдите ошибку в коде
Было:
```py
class Box:
    def __init__(self, weight):
        self.weight = weight
    def __add__(self):
        return Box(self.weight + 1)
```
Ошибка: у `__add__` **должно быть два аргумента**: `(self, other)`.

## 3) Про `__call__`
Верно: **a, c**  
- a) делает объект вызываемым как функцию  
- c) может принимать аргументы

---

# Домашнее задание — решения

## ДЗ 1) Класс `Email`
Требования:
- поля: `sender`, `recipient`, `subject`, `body`, `date` (`datetime`)
- сравнение писем по дате
- строковое представление
- `len(email)` → длина текста письма (body)
- `bool(email)` → есть ли текст (не пустой и не из пробелов)

```py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from functools import total_ordering


@total_ordering
@dataclass(frozen=True)
class Email:
    sender: str
    recipient: str
    subject: str
    body: str
    date: datetime

    def __str__(self) -> str:
        body_line = f"- {self.body} -" if self.body.strip() else "- -"
        return (
            f"From: {self.sender}\n"
            f"To: {self.recipient}\n"
            f"Subject: {self.subject}\n"
            f"{body_line}"
        )

    def __len__(self) -> int:
        return len(self.body)

    def __bool__(self) -> bool:
        return bool(self.body.strip())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Email):
            return NotImplemented
        return self.date == other.date

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Email):
            return NotImplemented
        return self.date < other.date


# Пример использования (как в задании)
e1 = Email("alice@example.com", "bob@example.com",
           "Meeting", "Let's meet at 10am", datetime(2024, 6, 10))
e2 = Email("bob@example.com", "alice@example.com",
           "Report", "", datetime(2024, 6, 11))

print(e1)
print(e2)
print("Length:", len(e1))
print("Has text:", bool(e1))
print("Is newer:", e2 > e1)
```

## ДЗ 2) Класс `Money`
Требования:
- `+` и `-` между объектами `Money`
- вывод как строка: `"$<amount>"`
- при операциях возвращается **новый** объект
- если вычитание даёт отрицательное — вернуть `$0`

```py
from __future__ import annotations

class Money:
    def __init__(self, amount: int):
        self.amount = max(int(amount), 0)

    def __add__(self, other: object) -> "Money":
        if not isinstance(other, Money):
            return NotImplemented
        return Money(self.amount + other.amount)

    def __sub__(self, other: object) -> "Money":
        if not isinstance(other, Money):
            return NotImplemented
        return Money(max(self.amount - other.amount, 0))

    def __str__(self) -> str:
        return f"${self.amount}"

    def __repr__(self) -> str:
        return f"Money(amount={self.amount})"


money1 = Money(100)
money2 = Money(50)

print(money1 + money2)  # $150
print(money1 - money2)  # $50
print(money2 - money1)  # $0
```

---

## Мини-шпаргалка урока
```text
Сравнение: __eq__ __ne__ __lt__ __le__ __gt__ __ge__
- возвращай NotImplemented для чужих типов
- isinstance(other, Class)

@total_ordering:
- реализуй __eq__ + один из (__lt__/__le__/__gt__/__ge__)

Коллекция:
__getitem__  obj[key]
__setitem__  obj[key] = value
__contains__ key in obj
__len__      len(obj)

Арифметика:
__add__ __sub__ __mul__ __truediv__ __floordiv__ __mod__ __pow__
Инкрементные: __iadd__ ... (меняют self и возвращают self)

__bool__:
bool(obj) и поведение в if/while

__call__:
obj(...) — объект как функция
```


---

## Дополнительная информация

_Этот раздел будет дополнен практическими примерами и дополнительной информацией._
