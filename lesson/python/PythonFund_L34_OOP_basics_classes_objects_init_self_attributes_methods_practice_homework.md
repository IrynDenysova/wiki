# Python Fundamentals — Урок 34: Основы ООП (классы, объекты, `__init__`, `self`, поля/методы/атрибуты)

## 1) Что такое ООП
**ООП (объектно-ориентированное программирование)** — подход, где программа строится как взаимодействие **объектов**.  
Объект объединяет:
- **поля** (данные/состояние)
- **методы** (поведение)

Ключевые термины:
- **Класс** — шаблон (чертёж), по которому создаются объекты.
- **Объект** — конкретный экземпляр класса со своим состоянием.

---

## 2) ООП vs функциональный подход (коротко)
**ООП**
- код организован вокруг классов/объектов
- объект хранит состояние и имеет методы
- удобно моделировать “сущности” реального мира
- хорошо для больших, расширяемых систем

**Функциональный подход**
- код организован вокруг функций
- данные и операции разделены
- часто “чистые функции” (один ввод → один вывод)
- хорош для расчётов, анализа данных, обработки потоков

В Python обычно используют **микс** двух подходов.

---

## 3) Создание класса
Синтаксис пустого класса:
```py
class ClassName:
    pass
```

**Правила именования:**
- Имя класса с заглавной буквы
- Если несколько слов → **CamelCase** (`UserProfile`, `ShoppingCart`)
- Не использовать имена встроенных типов (`list`, `str`, `object`, ...)

---

## 4) Магический метод `__init__()`
`__init__()` — **инициализатор**, который автоматически вызывается при создании объекта и задаёт начальное состояние (поля).

Важно:
- “Конструктор” в строгом смысле — `__new__()` (создаёт объект)
- `__init__()` — инициализирует уже созданный объект

Шаблон:
```py
class ClassName:
    def __init__(self, arg1, arg2):
        self.attr1 = arg1
        self.attr2 = arg2
```

Пример:
```py
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
```

Особенности `__init__`:
- вызывается автоматически при `Book(...)`
- первым параметром всегда принимает `self`
- может отсутствовать, если класс не хранит состояние

---

## 5) Поля, методы и атрибуты
- **Поля** — переменные, хранящие состояние объекта (обычно задаются в `__init__`).
- **Методы** — функции внутри класса; описывают действия объекта.
- **Атрибут** — общее слово для всего, что доступно через точку: `obj.something`  
  (и поля, и методы — атрибуты).

---

## 6) `self` — зачем нужен
`self` — ссылка на текущий объект внутри методов класса.

Зачем:
- хранить данные **внутри объекта**
- обращаться к полям и другим методам объекта
- отличать “поле объекта” от локальной переменной функции

Пример:
```py
class Book:
    def __init__(self, book_title, book_author):
        self.title = book_title
        self.author = book_author
```

Без `self` переменные были бы локальными и “исчезли” после выхода из `__init__`.

---

## 7) Создание объекта
Синтаксис:
```py
obj = ClassName(arg1, arg2)
```

Что происходит:
1) Python вызывает `__new__()` → создаёт пустой объект
2) затем `__init__()` → инициализирует поля через `self`
3) возвращает готовый объект

Пример:
```py
book1 = Book("1984", "George Orwell")
book2 = Book("Brave New World", "Aldous Huxley")
```

---

## 8) Доступ к полям объекта и изменение
Доступ:
```py
obj.attribute
```

Пример:
```py
book = Book("1984", "George Orwell")
print(book.title)
print(book.author)

book.title = "Animal Farm"   # изменили поле
print(book.title)
```

Важно: поля принадлежат **конкретному объекту** — изменения в одном объекте не меняют другой.

---

## 9) Методы класса
Синтаксис:
```py
class ClassName:
    def method_name(self, ...):
        ...
```

Пример:
```py
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def get_description(self):
        return f"{self.title} — {self.author}"

    def show_info(self):
        print(self.get_description())

    def make_author_upper(self):
        self.author = self.author.upper()

book = Book("1984", "George Orwell")
book.show_info()
book.make_author_upper()
book.show_info()
```

Важно:
- методы вызываются как `obj.method()`
- при вызове Python автоматически передаёт `obj` в параметр `self`

---

# 10) Задания для закрепления — ответы
## 10.1 Верные утверждения об ООП
Верно: **a, b, d**
- a) объект создаётся по шаблону (классу) ✅
- b) метод использует `self` для доступа к данным объекта ✅
- c) метод — это поле ❌
- d) ООП объединяет данные и поведение ✅

## 10.2 Что делает `__init__`?
Ответ: **d — создаёт/инициализирует поля объекта**

## 10.3 Сопоставление понятий
1) класс → **d** (шаблон)  
2) self → **a** (ссылка на объект)  
3) атрибут → **b** (всё через точку)  
4) метод → **c** (функция внутри класса)

## 10.4 Сопоставление элементов кода
1) `self.title = title` → **d** (инициализация поля)  
2) `def show_info(self):` → **a** (метод класса)  
3) `book = Book("1984", "Orwell")` → **b** (создание объекта)  
4) `book.title` → **c** (доступ к полю)

---

# 11) Практическая работа — решения

## 11.1 Класс `User`
Требования:
- поля: `username`, `email`, `login_count`
- методы: `show_info()`, `login()`, `get_logins()`

```py
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.login_count = 0

    def show_info(self):
        print("-" * 30)
        print("Пользователь:", self.username)
        print("Почта:", self.email)
        print("-" * 30)

    def login(self):
        self.login_count += 1
        print(f"{self.username} вошёл в систему")

    def get_logins(self):
        return self.login_count


user = User("alice", "alice@example.com")
user.show_info()
user.login()
user.login()
print("Количество входов:", user.get_logins())
```

## 11.2 Класс `Product`
Требования:
- поля: `name`, `price`
- методы: `apply_discount(percent)`, `info()`

```py
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def apply_discount(self, percent):
        print(f"Применяем скидку {percent}%")
        self.price -= self.price * percent / 100

    def info(self):
        print(f"Название: {self.name}")
        print(f"Цена: {self.price}")


p = Product("Молоко", 120)
p.info()
p.apply_discount(25)
p.info()
```

---

# 12) Домашнее задание — решения

## 12.1 Класс `Rectangle`
Требования:
- поля: `width`, `height`
- метод: `get_area()` возвращает площадь

```py
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_area(self):
        return self.width * self.height


r = Rectangle(4, 5)
print("Площадь:", r.get_area())

r.width = 5
r.height = 7
print("Новая площадь:", r.get_area())
```

## 12.2 Класс `Counter`
Требования:
- старт с 0
- методы: `inc()`, `dec()` (печатают новое значение)
- метод `get()` возвращает текущее значение

```py
class Counter:
    def __init__(self):
        self.value = 0

    def inc(self):
        self.value += 1
        print("Значение увеличено, текущее:", self.value)

    def dec(self):
        self.value -= 1
        print("Значение уменьшено, текущее:", self.value)

    def get(self):
        return self.value


c = Counter()
c.inc()
c.inc()
c.inc()
c.dec()
print("Текущее значение:", c.get())
```

---

## Мини-шпаргалка урока
```text
class X: ...               # класс
obj = X(...)               # объект
__new__() -> создаёт объект
__init__(self, ...) -> задаёт поля

self.attr = value          # поле (состояние)
def method(self): ...      # метод (поведение)

obj.attr                   # доступ к полю
obj.method()               # вызов метода (self передаётся автоматически)
```
