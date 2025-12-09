# Lambda map filter reduce any all sorted

## 📖 Быстрая навигация по операторам и функциям

- [[#План занятия]](#план-занятия)
- [[#1) Передача функций в качестве аргументов]](#1-передача-функций-в-качестве-аргументов)
- [[#2) Lambda-функции]](#2-lambda-функции)
- [[#3) Парадигмы программирования (кратко)]](#3-парадигмы-программирования-кратко)
- [[#4) Функциональное программирование — ключевые идеи]](#4-функциональное-программирование-—-ключевые-идеи)
- [[#5) Функции высшего порядка (Higher-Order Functions)]](#5-функции-высшего-порядка-higher-order-functions)
- [[#6) `map`, `filter`, `reduce`]](#6-map-filter-reduce)
- [[#7) `any()` и `all()`]](#7-any-и-all)
- [[#8) Функция как `key` в `sorted()`, `min()`, `max()`]](#8-функция-как-key-в-sorted-min-max)
- [[#1) Исправьте ошибку]](#1-исправьте-ошибку)
- [[#2) Произойдёт ли ошибка?]](#2-произойдёт-ли-ошибка)
- [[#3) map(len, words)]](#3-maplen-words)
- [[#4) filter(odd)]](#4-filterodd)
- [[#5) reduce(sum)]](#5-reducesum)
- [[#6) any([]) и all([...])]](#6-any-и-all)
- [[#1) Список квадратов без циклов и comprehension]](#1-список-квадратов-без-циклов-и-comprehension)
- [[#2) Сортировка (имя, возраст) по возрасту]](#2-сортировка-имя-возраст-по-возрасту)
- [[#3) Сортировка по убыванию возраста, а при равном возрасте — по имени]](#3-сортировка-по-убыванию-возраста-а-при-равном-возрасте-—-по-имени)
- [[#4) Сотрудники: age > 30, зарплату +20%]](#4-сотрудники-age-30-зарплату-20)
- [[#ДЗ 1) Выбор заказов: дороже 500 → имена по алфавиту]](#дз-1-выбор-заказов-дороже-500-→-имена-по-алфавиту)
- [[#ДЗ 2) Статистика продаж: выручка по товару, сортировка по убыванию]](#дз-2-статистика-продаж-выручка-по-товару-сортировка-по-убыванию)
- [[#Мини-шпаргалка]](#мини-шпаргалка)
- [[#Дополнительная информация]](#дополнительная-информация)


---

## 1) Передача функций в качестве аргументов
В Python **функции — это объекты**: их можно присваивать переменным, хранить в коллекциях и передавать в другие функции.

### 1.1 Главное правило
При передаче функции **не ставим** `()` — иначе передадим **результат вызова**, а не саму функцию.

✅ Правильно (передаём ссылку на функцию):
```py
def square(x):
    return x * x

def apply_function(func, value):
    return func(value)

print(apply_function(square, 5))  # 25
```

❌ Неправильно (передали результат `square(5)`):
```py
result = apply_function(square(5), 5)  # TypeError
```

### 1.2 Хранение функций в коллекциях
```py
def add(x, y):
    return x + y

def multiply(x, y):
    return x * y

operations = {
    "+": add,
    "*": multiply,
}

choice = "+"
print(operations[choice](10, 5))  # 15
```

### 1.3 Можно передавать и встроенные функции
```py
def process_data(func, data):
    return func(data)

print(process_data(abs, -10))  # 10
```

---

## 2) Lambda-функции
**Lambda** — маленькая “анонимная” функция для коротких выражений.

### 2.1 Синтаксис
```py
lambda arguments: expression
```
- `return` не пишется: результат выражения возвращается автоматически
- lambda содержит **одно выражение** (не многострочный блок)

### 2.2 Примеры
Один аргумент:
```py
square = lambda x: x ** 2
print(square(4))  # 16
```

Несколько аргументов:
```py
add = lambda x, y: x + y
print(add(3, 5))  # 8
```

Lambda как аргумент:
```py
def apply_func(func, numbers):
    return [func(n) for n in numbers]

print(apply_func(lambda x: x + 10, [5, 8, 3]))  # [15, 18, 13]
```

---

## 3) Парадигмы программирования (кратко)
- **Императивная**: “делай шаги 1→2→3”, меняем состояние программы.
- **Процедурная** (подтип императивной): организуем код через функции/процедуры.
- **ООП**: данные + методы в объектах/классах.
- **Функциональная**: функции, неизменяемость, чистые функции, минимум побочных эффектов.
- **Декларативная**: описываем “что нужно получить” (пример: SQL).

---

## 4) Функциональное программирование — ключевые идеи
- **Чистые функции**: одинаковый ввод → одинаковый вывод, нет побочных эффектов
- **Неизменяемость данных**
- **Функции как объекты**
- **Функции высшего порядка**
- Часто: рекурсия вместо циклов (в Python обычно всё равно используют циклы, но идеи важны)

---

## 5) Функции высшего порядка (Higher-Order Functions)
Это функции, которые:
- принимают функцию как аргумент, и/или
- возвращают функцию как результат

Часто используемые: `map()`, `filter()`, `reduce()`, а также `sorted(..., key=...)`.

---

## 6) `map`, `filter`, `reduce`

### 6.1 `map(function, iterable)`
Применяет функцию к каждому элементу и возвращает **итератор**.

```py
numbers = [1, 2, 3, 4]
squared = map(lambda x: x ** 2, numbers)
print(list(squared))  # [1, 4, 9, 16]
```

С несколькими iterable:
```py
a = [1, 2, 3]
b = [4, 5, 6]
result = map(lambda x, y: x + y, a, b)
print(list(result))  # [5, 7, 9]
```

С встроенной функцией:
```py
group_numbers = [(1, 2, 3), (4, 5, 6)]
print(list(map(sum, group_numbers)))  # [6, 15]
```

---

### 6.2 `filter(function, iterable)`
Отбирает элементы, для которых `function(elem)` возвращает `True` (возвращает итератор).

```py
numbers = [1, 2, 4, 5, 7, 9, 10, 11]
even_numbers = filter(lambda x: x % 2 == 0, numbers)
print(list(even_numbers))  # [2, 4, 10]
```

Если функцию поставить `None`, останутся только “truthy” элементы:
```py
data = [0, 1, False, True, "", "Python", [], [1, 2, 3]]
print(list(filter(None, data)))  # [1, True, 'Python', [1, 2, 3]]
```

---

### 6.3 `reduce(function, iterable[, initializer])`
Сворачивает последовательность в одно значение (в `functools`).

```py
from functools import reduce

numbers = [1, 2, 3, 4]
print(reduce(lambda x, y: x * y, numbers))       # 24
print(reduce(lambda x, y: x * y, numbers, 10))   # 240
```

---

## 7) `any()` и `all()`
Ложные значения: `0`, `None`, `False`, пустые коллекции (`[]`, `{}`, `()`, `set()`).

### 7.1 `any(iterable)`
`True`, если есть хотя бы один “истинный” элемент. Пустой iterable → `False`.
```py
print(any([0, None, False, 1]))  # True
print(any([]))                   # False
```

### 7.2 `all(iterable)`
`True`, если все элементы “истинные”. Пустой iterable → `True`.
```py
print(all([1, 2, 3, "None"]))  # True
print(all([1, 0, 3]))          # False
print(all([]))                 # True
```

---

## 8) Функция как `key` в `sorted()`, `min()`, `max()`
Параметр `key` задаёт критерий сортировки/поиска.

### 8.1 `sorted(iterable, key=..., reverse=False)`
```py
words = ["mango", "grape", "apple", "strawberry", "banana", "pineapple", "kiwi"]
print(sorted(words, key=len))  # по длине
```

Пользовательская функция:
```py
def last_char_len(s):
    return s[-1], len(s)

print(sorted(words, key=last_char_len))
```

Lambda-ключ:
```py
words = ["mango", "grape", "apple", "Strawberry", "Banana", "pineapple", "kiwi"]
print(sorted(words, key=lambda x: (x[0].lower(), x[-1])))
```

Список кортежей:
```py
students = [("Alice", 25), ("Bob", 20), ("Charlie", 23)]
print(sorted(students, key=lambda x: x[1]))  # сортировка по возрасту
```

### 8.2 `min()` / `max()` с `key`
```py
words = ["apple", "banana", "kiwi", "grapefruit"]
print(max(words, key=len))  # grapefruit

cities = [("New York", 8419600), ("Los Angeles", 3980400), ("Chicago", 2716000)]
print(min(cities, key=lambda x: x[1]))  # ('Chicago', 2716000)
```

---

# Задания для закрепления (ответы)

## 1) Исправьте ошибку
❌ Было:
```py
print(operations("sum")(2, 3))
```
✅ Нужно:
```py
print(operations["sum"](2, 3))
print(operations["mul"](2, 3))
```

## 2) Произойдёт ли ошибка?
```py
def add(x, y):
    return x + y

print((lambda f, a, b: f(a, b))(add, 3, 4))
```
Ошибки **нет**, вывод будет `7`.

## 3) map(len, words)
```py
words = ["apple", "banana", "cherry"]
print(list(map(len, words)))
```
Ответ: **`[5, 6, 6]`**

## 4) filter(odd)
```py
numbers = [5, 3, 4, 1, 5, 2]
print(list(filter(lambda x: x % 2 == 1, numbers)))
```
Ответ: **`[5, 3, 1, 5]`**

## 5) reduce(sum)
```py
from functools import reduce
numbers = [1, 2, 3, 4]
print(reduce(lambda x, y: x + y, numbers))
```
Ответ: **`10`**

## 6) any([]) и all([...])
`any([])` → **False**  
`all([1, 2, 3, "None"])` → **True**

---

# Практическая работа (решения)

## 1) Список квадратов без циклов и comprehension
```py
def square_numbers(numbers):
    return list(map(lambda x: x ** 2, numbers))

numbers = [1, 2, 3, 4, 5]
print(square_numbers(numbers))  # [1, 4, 9, 16, 25]
```

## 2) Сортировка (имя, возраст) по возрасту
```py
def sort_by_age(people):
    return sorted(people, key=lambda person: person[1])
```

## 3) Сортировка по убыванию возраста, а при равном возрасте — по имени
```py
def sort_by_age_and_name(people):
    return sorted(people, key=lambda person: (-person[1], person[0]))
```

## 4) Сотрудники: age > 30, зарплату +20%
```py
def process_employees(employees):
    filtered = filter(lambda emp: emp["age"] > 30, employees)
    updated = map(lambda emp: {**emp, "salary": emp["salary"] * 1.2}, filtered)
    return list(updated)
```

---

# Домашнее задание (решения)

## ДЗ 1) Выбор заказов: дороже 500 → имена по алфавиту
Дано:
```py
orders = [
    {"product": "Laptop", "price": 1200},
    {"product": "Mouse", "price": 50},
    {"product": "Keyboard", "price": 100},
    {"product": "Monitor", "price": 300},
    {"product": "Chair", "price": 800},
    {"product": "Desk", "price": 400}
]
```

Решение:
```py
def select_expensive_orders(orders, min_price=500):
    filtered = filter(lambda o: o["price"] > min_price, orders)
    products = map(lambda o: o["product"], filtered)
    return sorted(products)

print(select_expensive_orders(orders))  # ['Chair', 'Laptop']
```

---

## ДЗ 2) Статистика продаж: выручка по товару, сортировка по убыванию
Дано:
```py
sales = [
    ("Laptop", 5, 1200),
    ("Mouse", 50, 20),
    ("Keyboard", 30, 50),
    ("Monitor", 10, 300),
    ("Chair", 20, 800)
]
```

Решение:
```py
def sales_stats(sales):
    revenue = {}
    for product, qty, price in sales:
        revenue[product] = revenue.get(product, 0) + qty * price

    # сортировка по убыванию выручки
    return dict(sorted(revenue.items(), key=lambda item: item[1], reverse=True))

print(sales_stats(sales))
# {'Chair': 16000, 'Laptop': 6000, 'Monitor': 3000, 'Keyboard': 1500, 'Mouse': 1000}
```

---

## Мини-шпаргалка
```text
Передача функций:
- func без () -> передаём функцию
- func() -> передаём результат вызова

lambda:
lambda args: expr   (одно выражение)

map:
map(f, it) -> итератор преобразований

filter:
filter(pred, it) -> итератор элементов, где pred(elem) == True
filter(None, it) -> оставляет truthy

reduce:
reduce(f, it[, init]) -> одно значение (из functools)

any / all:
any(it) -> True если есть хотя бы один truthy, пустой -> False
all(it) -> True если все truthy, пустой -> True

sorted/min/max key=:
sorted(it, key=f)
min(it, key=f) / max(it, key=f)
```


---

## Дополнительная информация

### Важные концепции для изучения

#### 1. Детальный разбор lambda-функций
```python
# Lambda с одним аргументом
square = lambda x: x ** 2
print(square(5))  # 25

# Lambda с несколькими аргументами
add = lambda x, y, z: x + y + z
print(add(1, 2, 3))  # 6

# Lambda с условным выражением
max_of_two = lambda a, b: a if a > b else b
print(max_of_two(10, 20))  # 20

# Lambda в списке
operations = [
    lambda x: x + 1,
    lambda x: x * 2,
    lambda x: x ** 2
]
result = [op(5) for op in operations]
print(result)  # [6, 10, 25]
```

#### 2. Комбинирование map, filter, reduce
```python
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Цепочка операций:
# 1. Отфильтровать четные числа
# 2. Возвести их в квадрат
# 3. Найти сумму
result = reduce(
    lambda x, y: x + y,
    map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers))
)
print(result)  # 220 (4 + 16 + 36 + 64 + 100)

# Более читаемый вариант с промежуточными переменными
evens = filter(lambda x: x % 2 == 0, numbers)
squared = map(lambda x: x ** 2, evens)
total = reduce(lambda x, y: x + y, squared)
print(total)  # 220
```

#### 3. Продвинутое использование sorted с key
```python
# Сортировка словарей по нескольким критериям
students = [
    {"name": "Alice", "age": 25, "grade": 85},
    {"name": "Bob", "age": 23, "grade": 90},
    {"name": "Charlie", "age": 25, "grade": 80},
    {"name": "David", "age": 23, "grade": 95}
]

# Сортировка по возрасту (убывание), затем по оценке (убывание)
sorted_students = sorted(students, key=lambda s: (-s["age"], -s["grade"]))
for s in sorted_students:
    print(f"{s['name']}: возраст {s['age']}, оценка {s['grade']}")

# Сортировка строк без учета регистра
words = ["apple", "Banana", "cherry", "Date"]
sorted_words = sorted(words, key=str.lower)
print(sorted_words)  # ['apple', 'Banana', 'cherry', 'Date']
```

#### 4. Использование функций высшего порядка
```python
# Создание функции, возвращающей функцию
def create_multiplier(n):
    return lambda x: x * n

double = create_multiplier(2)
triple = create_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15

# Декоратор как функция высшего порядка
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")  # Выведет 3 раза
```

### 💡 Практические примеры

#### Пример 1: Обработка данных с помощью map и filter
```python
# Данные о продажах
sales = [
    {"product": "Laptop", "price": 1200, "quantity": 5},
    {"product": "Mouse", "price": 25, "quantity": 50},
    {"product": "Keyboard", "price": 75, "quantity": 30},
    {"product": "Monitor", "price": 300, "quantity": 10}
]

# Получить общую стоимость для каждого товара
total_values = list(map(lambda s: s["price"] * s["quantity"], sales))
print("Общие стоимости:", total_values)  # [6000, 1250, 2250, 3000]

# Найти дорогие товары (стоимость > 2000)
expensive = list(filter(
    lambda s: s["price"] * s["quantity"] > 2000,
    sales
))
for item in expensive:
    print(f"{item['product']}: {item['price'] * item['quantity']}")
```

#### Пример 2: Работа с текстом
```python
text = "Hello World From Python Programming"
words = text.split()

# Получить длины всех слов
lengths = list(map(len, words))
print(lengths)  # [5, 5, 4, 6, 11]

# Оставить только длинные слова (больше 5 букв)
long_words = list(filter(lambda w: len(w) > 5, words))
print(long_words)  # ['Python', 'Programming']

# Все слова в нижнем регистре
lowercase = list(map(str.lower, words))
print(lowercase)  # ['hello', 'world', 'from', 'python', 'programming']
```

#### Пример 3: Анализ данных с any и all
```python
# Проверка условий в списке чисел
numbers = [2, 4, 6, 8, 10]

# Все ли числа четные?
all_even = all(map(lambda x: x % 2 == 0, numbers))
print("Все четные:", all_even)  # True

# Есть ли хотя бы одно число > 5?
any_greater_5 = any(map(lambda x: x > 5, numbers))
print("Есть больше 5:", any_greater_5)  # True

# Проверка данных о пользователях
users = [
    {"name": "Alice", "age": 25, "verified": True},
    {"name": "Bob", "age": 17, "verified": False},
    {"name": "Charlie", "age": 30, "verified": True}
]

# Все ли пользователи совершеннолетние?
all_adults = all(map(lambda u: u["age"] >= 18, users))
print("Все совершеннолетние:", all_adults)  # False

# Есть ли хотя бы один верифицированный?
any_verified = any(map(lambda u: u["verified"], users))
print("Есть верифицированные:", any_verified)  # True
```

### 🚨 Частые ошибки

**Ошибка 1: Забыли преобразовать результат map/filter в список**
```python
# ❌ НЕПРАВИЛЬНО - map возвращает итератор
numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x ** 2, numbers)
print(squared)  # <map object at 0x...>

# ✅ ПРАВИЛЬНО
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]
```

**Ошибка 2: Слишком сложная lambda**
```python
# ❌ НЕПРАВИЛЬНО - lambda слишком сложная, лучше обычная функция
process = lambda x: x * 2 if x > 0 else x / 2 if x < 0 else 0

# ✅ ПРАВИЛЬНО
def process(x):
    if x > 0:
        return x * 2
    elif x < 0:
        return x / 2
    else:
        return 0
```

**Ошибка 3: Неправильное использование reduce без начального значения**
```python
from functools import reduce

# ❌ ОПАСНО - для пустого списка будет ошибка
# result = reduce(lambda x, y: x + y, [])  # TypeError!

# ✅ ПРАВИЛЬНО - указываем начальное значение
result = reduce(lambda x, y: x + y, [], 0)
print(result)  # 0
```

**Ошибка 4: Передача функции с круглыми скобками**
```python
def square(x):
    return x ** 2

numbers = [1, 2, 3, 4, 5]

# ❌ НЕПРАВИЛЬНО - вызываем функцию вместо передачи
# result = map(square(), numbers)  # TypeError!

# ✅ ПРАВИЛЬНО - передаем ссылку на функцию
result = map(square, numbers)
print(list(result))  # [1, 4, 9, 16, 25]
```

### 📌 Полезные ресурсы
- [Документация: Lambda expressions](https://docs.python.org/3/reference/expressions.html#lambda)
- [Документация: map()](https://docs.python.org/3/library/functions.html#map)
- [Документация: filter()](https://docs.python.org/3/library/functions.html#filter)
- [Документация: functools.reduce()](https://docs.python.org/3/library/functools.html#functools.reduce)
- [Документация: sorted()](https://docs.python.org/3/library/functions.html#sorted)
- [PEP 3113: Removal of Tuple Parameter Unpacking](https://www.python.org/dev/peps/pep-3113/)
- [Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html)
