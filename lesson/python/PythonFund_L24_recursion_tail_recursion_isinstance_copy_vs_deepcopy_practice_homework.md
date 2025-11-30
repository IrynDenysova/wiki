# Python Fundamentals — Урок 24: рекурсия (base case/recursive case), хвостовая рекурсия, `isinstance()`, `copy()` vs `deepcopy()`

## 0) План урока
- Примеры рекурсивных функций (факториал, бинарный поиск)
- Хвостовая рекурсия
- Рекурсия или итерация? (плюсы/минусы, когда что выбирать)
- `isinstance()` — проверка типа
- Поверхностная и глубокая копия: `copy()` vs `deepcopy()`
- Практика + домашние задания (решения)

---

## 1) Что такое рекурсия
**Рекурсия** — функция вызывает саму себя, решая задачу через более простую подзадачу.

У рекурсивной функции всегда есть:
- **базовый случай (base case)** — условие остановки.
- **рекурсивный случай (recursive case)** — шаг, который приближает к базовому.

### 1.1 Важно про стек вызовов (RecursionError)
Каждый рекурсивный вызов создаёт новый “кадр” в стеке. Если базового случая нет / он недостижим — стек переполнится.

**Пример “бесконечной рекурсии”:**
```py
def infinite():
    return infinite()

infinite()  # RecursionError
```

✅ Ответ на вопрос из урока: будет **ошибка `RecursionError`**.

---

## 2) Примеры рекурсивных функций

### 2.1 Факториал
`n!` — произведение всех чисел от 1 до `n`.

Рекурсивная реализация:
```py
def factorial(n: int) -> int:
    if n == 0 or n == 1:     # base case
        return 1
    return n * factorial(n - 1)  # recursive case

print(factorial(5))  # 120
```

---

### 2.2 Бинарный поиск (в отсортированном списке)
Ищет элемент в **отсортированном** массиве за `O(log n)`.

Рекурсивная реализация:
```py
def binary_search(arr: list[int], target: int, left: int, right: int) -> int:
    if left > right:  # base case: не найден
        return -1

    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, right)
    else:
        return binary_search(arr, target, left, mid - 1)

array = [1, 3, 5, 7, 9, 11, 13]
print(binary_search(array, 5, 0, len(array) - 1))   # 2
print(binary_search(array, 13, 0, len(array) - 1))  # 6
print(binary_search(array, 8, 0, len(array) - 1))   # -1
```

---

## 3) Хвостовая рекурсия (tail recursion)
**Хвостовая рекурсия** — рекурсивный вызов является **последней операцией** перед `return`.

Пример факториала с аккумулятором:
```py
def factorial_tail(n: int, accumulator: int = 1) -> int:
    if n == 0 or n == 1:
        return accumulator
    return factorial_tail(n - 1, n * accumulator)

print(factorial_tail(5))  # 120
```

### 3.1 Важно: Python НЕ оптимизирует хвостовую рекурсию
В Python **нет tail-call optimization** (оптимизации хвостовой рекурсии), поэтому при больших `n` хвостовая рекурсия всё равно может привести к `RecursionError`.

Итеративный вариант факториала обычно предпочтительнее:
```py
def factorial_iterative(n: int) -> int:
    accumulator = 1
    while n > 1:
        accumulator *= n
        n -= 1
    return accumulator

print(factorial_iterative(5))  # 120
```

---

## 4) Разный порядок выполнения (до/после рекурсивного вызова)
Две функции печатают числа в разном порядке:

```py
def print_numbers(n):
    if n == 0:
        return
    print(n)
    print_numbers(n - 1)

def print_nums(n):
    if n == 0:
        return
    print_nums(n - 1)
    print(n)
```

Что происходит:
- `print_numbers(5)` → **5 4 3 2 1** (печатаем **до** рекурсивного вызова)
- `print_nums(5)` → **1 2 3 4 5** (печатаем **после** возврата из рекурсии)

---

## 5) Рекурсия или итерация?
### 5.1 Плюсы рекурсии
- помогает разбивать сложную задачу на подзадачи
- удобно для деревьев/графов/вложенных структур
- иногда код получается **выразительнее и короче**

### 5.2 Минусы рекурсии
- риск `RecursionError` (переполнение стека)
- часто медленнее итерации из‑за накладных расходов вызовов функций
- дополнительная память на каждый вызов (кадры стека)

### 5.3 Когда выбирать
Рекурсию — когда естественно “делить на подзадачи” и/или работать с деревьями/графами/вложенными структурами.  
Итерацию — когда важнее скорость + память или глубина может быть большой.

---

## 6) Где рекурсия особенно полезна (примеры задач)
- обход деревьев (DFS — поиск в глубину)
- обход графов (DFS, рекурсивный поиск путей)
- разбор вложенных выражений (syntax parsing)
- Ханойские башни
- комбинаторика: комбинации/перестановки/подмножества

---

## 7) `copy()` vs `deepcopy()` (и почему это связано с рекурсией)

### 7.1 `copy()` — поверхностная копия (shallow)
Копирует верхний уровень, а вложенные изменяемые объекты остаются **ссылками** на оригинал.

```py
original_list = [[1, 2], [3, 4]]
copy_lst = original_list.copy()

copy_lst.append(99)         # не влияет на оригинал (верхний уровень)
copy_lst[0][0] = "X"        # влияет на оригинал (вложенный список общий!)

print("Оригинал:", original_list)
print("Копия:", copy_lst)
```

### 7.2 `deepcopy()` — глубокая копия (deep)
Создаёт независимую копию всех вложенных объектов (делает это **рекурсивно**).

```py
from copy import deepcopy

original_list = [[1, 2], [3, 4]]
copy_lst = deepcopy(original_list)

copy_lst.append(99)
copy_lst[0][0] = "X"        # НЕ влияет на оригинал

print("Оригинал:", original_list)
print("Копия:", copy_lst)
```

### 7.3 Когда `deepcopy()` не нужен
- объект не содержит вложенных изменяемых структур
- критична производительность (deepcopy медленнее), а полная независимость не требуется

---

## 8) `isinstance()` — проверка типа
`isinstance(obj, classinfo)` возвращает `True/False`.

Примеры:
```py
x = 10
y = "Hello"

print(isinstance(x, int))   # True
print(isinstance(y, str))   # True
print(isinstance(y, int))   # False
```

Проверка нескольких типов:
```py
value = 3.14
if isinstance(value, (int, float)):
    print("Число")
else:
    print("Не число")
```

Фильтрация по типу:
```py
data = [1, "hello", 2.5, True, "world", 42]
numbers = [x for x in data if isinstance(x, (int, float))]
print(numbers)  # [1, 2.5, 42]
```

---

# Практика (решения)

## Практика 1) Реализовать аналог `deepcopy()` рекурсивно
Данные:
```py
original_data = [
    [1, 2, 3],
    (4, [5, 6], {7, 8}),
    {"a": 9, "b": [10, 11]},
    "Hello",
    [12, (13, 14)],
    15.5,
    5
]
```

Решение (из урока, с `isinstance`):
```py
def deep_copy(data):
    if isinstance(data, list):
        return [deep_copy(item) for item in data]
    elif isinstance(data, dict):
        return {key: deep_copy(value) for key, value in data.items()}
    elif isinstance(data, set):
        return {deep_copy(item) for item in data}
    elif isinstance(data, tuple):
        return tuple(deep_copy(item) for item in data)
    else:
        return data

original_data = [
    [1, 2, 3],
    (4, [5, 6], {7, 8}),
    {"a": 9, "b": [10, 11]},
    "Hello",
    [12, (13, 14)],
    15.5,
    5
]

copied_data = deep_copy(original_data)

# Проверяем независимость копии:
original_data[1][1][0] = 0

print("Исходный:", original_data)
print("Копия:", copied_data)
```

---

# Домашнее задание (решения)

## ДЗ 1) Сумма цифр числа (рекурсивно)
Дано:
```py
num = 43197
```

Решение:
```py
def sum_digits(n: int) -> int:
    n = abs(n)
    if n < 10:         # base case
        return n
    return (n % 10) + sum_digits(n // 10)

print(sum_digits(43197))  # 24
```

---

## ДЗ 2) Сумма всех чисел во вложенных списках (рекурсивно)
Дано:
```py
nested_numbers = [1, [2, 3], [4, [5, 6]], 7]
```

Решение:
```py
def sum_nested(data) -> int:
    total = 0
    for item in data:
        if isinstance(item, list):
            total += sum_nested(item)
        else:
            total += item
    return total

nested_numbers = [1, [2, 3], [4, [5, 6]], 7]
print(sum_nested(nested_numbers))  # 28
```

---

## (Доп.) Обратный вывод строки (рекурсивно)
```py
def reverse_string(s: str) -> str:
    if not s:
        return ""
    return s[-1] + reverse_string(s[:-1])

print(reverse_string("hello"))  # olleh
```

## (Доп.) Подсчёт слова во вложенной структуре (списки/строки)
```py
def count_word(nested_sentences, word: str) -> int:
    if isinstance(nested_sentences, str):
        return nested_sentences.split().count(word)
    if isinstance(nested_sentences, list):
        return sum(count_word(sub, word) for sub in nested_sentences)
    return 0

nested_sentences = [
    ["Python is great", "I love Python"],
    ["Python is powerful", ["Python is everywhere", "Learn Python"]],
    "Coding in Python is fun"
]
print("Количество вхождений:", count_word(nested_sentences, "Python"))  # 6
```

---

## Мини-шпаргалка
```text
Рекурсия:
- обязательно: base case + recursive case
- риск: RecursionError (переполнение стека)

Хвостовая рекурсия:
- рекурсивный вызов — последняя операция
- Python не делает оптимизацию хвостовых вызовов → чаще выбирают итерацию

copy() vs deepcopy():
- copy()    -> поверхностная копия, вложенные объекты общие
- deepcopy() -> глубокая копия, всё независимое (делается рекурсивно)

isinstance(obj, (type1, type2, ...)):
- проверка типа (полезно для рекурсивной обработки вложенных структур)
```
