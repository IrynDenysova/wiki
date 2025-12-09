# Рекурсия base case isinstance copy deepcopy

## 📖 Быстрая навигация по операторам и функциям

- [[#0) План урока]](#0-план-урока)
- [[#1) Что такое рекурсия]](#1-что-такое-рекурсия)
- [[#2) Примеры рекурсивных функций]](#2-примеры-рекурсивных-функций)
- [[#3) Хвостовая рекурсия (tail recursion)]](#3-хвостовая-рекурсия-tail-recursion)
- [[#4) Разный порядок выполнения (до/после рекурсивного вызова)]](#4-разный-порядок-выполнения-допосле-рекурсивного-вызова)
- [[#5) Рекурсия или итерация?]](#5-рекурсия-или-итерация)
- [[#6) Где рекурсия особенно полезна (примеры задач)]](#6-где-рекурсия-особенно-полезна-примеры-задач)
- [[#7) `copy()` vs `deepcopy()` (и почему это связано с рекурсией)]](#7-copy-vs-deepcopy-и-почему-это-связано-с-рекурсией)
- [[#8) `isinstance()` — проверка типа]](#8-isinstance-—-проверка-типа)
- [[#Практика 1) Реализовать аналог `deepcopy()` рекурсивно]](#практика-1-реализовать-аналог-deepcopy-рекурсивно)
- [[#ДЗ 1) Сумма цифр числа (рекурсивно)]](#дз-1-сумма-цифр-числа-рекурсивно)
- [[#ДЗ 2) Сумма всех чисел во вложенных списках (рекурсивно)]](#дз-2-сумма-всех-чисел-во-вложенных-списках-рекурсивно)
- [[#(Доп.) Обратный вывод строки (рекурсивно)]](#доп-обратный-вывод-строки-рекурсивно)
- [[#(Доп.) Подсчёт слова во вложенной структуре (списки/строки)]](#доп-подсчёт-слова-во-вложенной-структуре-спискистроки)
- [[#Мини-шпаргалка]](#мини-шпаргалка)
- [[#Дополнительная информация]](#дополнительная-информация)


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


---

## Дополнительная информация

### Важные концепции для изучения

#### 1. Углубленное изучение рекурсии и base case
```python
# Фибоначчи - классический пример рекурсии
def fibonacci_naive(n: int) -> int:
    """Вычисляет n-ое число Фибоначчи (неэффективно)"""
    # BASE CASES - критичны для останова рекурсии
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    # RECURSIVE CASE
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)

print(fibonacci_naive(5))  # 5

# Проблема: экспоненциальная сложность O(2^n)
# fibonacci_naive(35) займет много времени!

# Решение: мемоизация
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci_cached(n: int) -> int:
    """Вычисляет Фибоначчи эффективно - O(n)"""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)

print(fibonacci_cached(35))  # Моментально!

# Правильная структура рекурсии:
# 1. BASE CASE - условие остановки
# 2. RECURSIVE CASE - вызов с более простым аргументом
# 3. Гарантировать что базовый случай будет достигнут

def countdown(n: int) -> None:
    """Отсчет от n до 0 (демонстрация базового случая)"""
    # BASE CASE - обязателен!
    if n < 0:
        return
    
    print(n)
    # RECURSIVE CASE - переход к более простому аргументу
    countdown(n - 1)

countdown(3)
# Вывод: 3, 2, 1, 0
```

#### 2. Функция isinstance() - проверка типа
```python
# isinstance(object, classinfo) - проверяет тип объекта

value = 42
print(isinstance(value, int))  # True
print(isinstance(value, str))  # False
print(isinstance(value, (int, float)))  # True - проверка нескольких типов

# Практическое применение
def process_value(value):
    """Обрабатывает значение в зависимости от типа"""
    if isinstance(value, int):
        return value * 2
    elif isinstance(value, str):
        return value.upper()
    elif isinstance(value, list):
        return sum(value) if all(isinstance(x, (int, float)) for x in value) else None
    else:
        return None

print(process_value(5))  # 10
print(process_value("hello"))  # HELLO
print(process_value([1, 2, 3]))  # 6

# isinstance с наследованием
class Animal:
    pass

class Dog(Animal):
    pass

dog = Dog()
print(isinstance(dog, Dog))  # True
print(isinstance(dog, Animal))  # True - проверяет наследование!
print(isinstance(dog, str))  # False

# type() vs isinstance()
print(type(dog) == Dog)  # True
print(type(dog) == Animal)  # False - type не учитывает наследование

# isinstance предпочтительнее, т.к. работает с наследованием
```

#### 3. copy vs deepcopy - глубокое и поверхностное копирование
```python
import copy

# ПОВЕРХНОСТНОЕ КОПИРОВАНИЕ (shallow copy)
original_list = [[1, 2], [3, 4]]
shallow = original_list.copy()  # или list(original_list)

print("До изменения:")
print(f"original: {original_list}")
print(f"shallow: {shallow}")

# Изменяем вложенный список
original_list[0][0] = 999

print("\nПосле изменения original_list[0][0] = 999:")
print(f"original: {original_list}")  # [[999, 2], [3, 4]]
print(f"shallow: {shallow}")  # [[999, 2], [3, 4]] - ТОЖе изменился!

# Проблема: shallow copy копирует только ссылки!
print(f"\nСсылаются ли на один список? {original_list[0] is shallow[0]}")  # True

# ГЛУБОКОЕ КОПИРОВАНИЕ (deep copy)
original_list = [[1, 2], [3, 4]]
deep = copy.deepcopy(original_list)

original_list[0][0] = 999

print("\nДосле deepcopy:")
print(f"original: {original_list}")  # [[999, 2], [3, 4]]
print(f"deep: {deep}")  # [[1, 2], [3, 4]] - не изменился!
print(f"Разные объекты? {original_list[0] is not deep[0]}")  # True

# Сравнение методов копирования
original = {'a': [1, 2, 3], 'b': {'x': 10}}

# Поверхностное
shallow = original.copy()
original['a'].append(4)
print(f"Shallow: {shallow}")  # {'a': [1, 2, 3, 4], ...} - изменился!

# Глубокое
original = {'a': [1, 2, 3], 'b': {'x': 10}}
deep = copy.deepcopy(original)
original['a'].append(4)
print(f"Deep: {deep}")  # {'a': [1, 2, 3], ...} - не изменился
```

#### 4. Рекурсия с копированием состояния
```python
from typing import List

def permutations(arr: List[int], current: List[int] = None, result: List[List[int]] = None) -> List[List[int]]:
    """Генерирует все перестановки массива"""
    if current is None:
        current = []
    if result is None:
        result = []
    
    # BASE CASE
    if len(arr) == 0:
        # ВАЖНО: сохраняем копию, а не ссылку!
        result.append(current.copy())
        return result
    
    # RECURSIVE CASE
    for i in range(len(arr)):
        # Берем элемент
        num = arr[i]
        # Рекурсивно генерируем перестановки оставшихся элементов
        permutations(
            arr[:i] + arr[i+1:],  # Все кроме текущего
            current + [num],  # Добавляем текущий
            result
        )
    
    return result

print(permutations([1, 2, 3]))
# [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

# ВАЖНО: current.copy() это критично!
# Если просто append(current), все результаты будут ссылаться на одну список
```

### 💡 Практические примеры

#### Пример 1: Обход дерева структуры
```python
from typing import List, Optional

class Node:
    def __init__(self, value: int):
        self.value = value
        self.children: List['Node'] = []
    
    def add_child(self, child: 'Node') -> None:
        self.children.append(child)

def sum_tree(node: Optional[Node]) -> int:
    """Суммирует все значения в дереве"""
    # BASE CASE
    if node is None:
        return 0
    
    # RECURSIVE CASE
    total = node.value
    for child in node.children:
        total += sum_tree(child)
    
    return total

def print_tree(node: Optional[Node], depth: int = 0) -> None:
    """Выводит дерево с отступом"""
    # BASE CASE
    if node is None:
        return
    
    # RECURSIVE CASE
    print("  " * depth + str(node.value))
    for child in node.children:
        print_tree(child, depth + 1)

# Использование
root = Node(1)
root.add_child(Node(2))
root.add_child(Node(3))
root.children[0].add_child(Node(4))
root.children[0].add_child(Node(5))

print(f"Сумма: {sum_tree(root)}")  # 15
print_tree(root)
# 1
#   2
#     4
#     5
#   3
```

#### Пример 2: Поиск в лабиринте (DFS)
```python
from typing import Tuple, Set, List

def find_path(maze: List[List[int]], start: Tuple[int, int], 
              end: Tuple[int, int], visited: Set = None) -> bool:
    """Находит путь в лабиринте (0 - проход, 1 - стена)"""
    if visited is None:
        visited = set()
    
    # BASE CASES
    if start == end:
        return True
    
    if start in visited:
        return False
    
    row, col = start
    if (row < 0 or row >= len(maze) or col < 0 or col >= len(maze[0]) or
        maze[row][col] == 1):
        return False
    
    # Отмечаем как посещенную
    visited.add(start)
    
    # RECURSIVE CASE - пробуем все направления
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # вправо, вниз, влево, вверх
    for dr, dc in directions:
        new_pos = (row + dr, col + dc)
        if find_path(maze, new_pos, end, visited):
            return True
    
    return False

# Использование
maze = [
    [0, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 0, 0, 0],
    [1, 1, 1, 0]
]

start = (0, 0)
end = (3, 3)
print(find_path(maze, start, end))  # True
```

#### Пример 3: Сортировка с проверкой типов
```python
from typing import List, Union

def sort_mixed_list(items: List) -> List:
    """Сортирует список, разделяя элементы по типам"""
    result = []
    
    # Разделяем по типам
    ints = []
    strs = []
    others = []
    
    for item in items:
        if isinstance(item, int) and not isinstance(item, bool):
            ints.append(item)
        elif isinstance(item, str):
            strs.append(item)
        elif isinstance(item, float):
            ints.append(item)  # Рассматриваем вместе с int
        else:
            others.append(item)
    
    # Сортируем каждую группу
    result.extend(sorted(ints))
    result.extend(sorted(strs))
    result.extend(others)
    
    return result

print(sort_mixed_list([3, "hello", 1, "apple", 2.5]))
# [1, 2.5, 3, 'apple', 'hello']
```

#### Пример 4: Глубокое слияние словарей
```python
from typing import Dict, Any
import copy

def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
    """Глубоко слияет два словаря рекурсивно"""
    # Используем deepcopy чтобы не изменять исходные
    result = copy.deepcopy(dict1)
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # RECURSIVE CASE - оба значения это словари
            result[key] = deep_merge(result[key], value)
        else:
            # BASE CASE - простое значение
            result[key] = copy.deepcopy(value)
    
    return result

# Использование
dict1 = {'a': 1, 'b': {'x': 10, 'y': 20}}
dict2 = {'b': {'y': 30, 'z': 40}, 'c': 3}

merged = deep_merge(dict1, dict2)
print(merged)
# {'a': 1, 'b': {'x': 10, 'y': 30, 'z': 40}, 'c': 3}

print(dict1)  # Исходный не изменился
```

### 🚨 Частые ошибки

**Ошибка 1: Бесконечная рекурсия из-за отсутствия базового случая**
```python
# ❌ ОШИБКА - нет base case!
# def infinite():
#     return infinite()  # RecursionError: maximum recursion depth exceeded

# ✅ ПРАВИЛЬНО
def countdown(n: int) -> None:
    if n < 0:  # BASE CASE!
        return
    print(n)
    countdown(n - 1)

countdown(3)
```

**Ошибка 2: Shallow copy вместо deepcopy при сложных структурах**
```python
# ❌ НЕПРАВИЛЬНО
original = {'nested': [1, 2, 3]}
copy_shallow = original.copy()
original['nested'].append(4)
print(copy_shallow)  # {'nested': [1, 2, 3, 4]} - изменился!

# ✅ ПРАВИЛЬНО
import copy
original = {'nested': [1, 2, 3]}
copy_deep = copy.deepcopy(original)
original['nested'].append(4)
print(copy_deep)  # {'nested': [1, 2, 3]} - не изменился
```

**Ошибка 3: type() вместо isinstance() при наследовании**
```python
class Animal:
    pass

class Dog(Animal):
    pass

dog = Dog()

# ❌ НЕПРАВИЛЬНО - не работает с наследованием
if type(dog) == Animal:  # False!
    pass

# ✅ ПРАВИЛЬНО
if isinstance(dog, Animal):  # True!
    pass
```

**Ошибка 4: Забыли скопировать значение в рекурсии**
```python
# ❌ НЕПРАВИЛЬНО - all result элементы указывают на one list
def generate_combinations(arr, current=[]):
    if len(arr) == 0:
        result.append(current)  # Ошибка!
        return
    # ...

# ✅ ПРАВИЛЬНО
def generate_combinations(arr, current=[]):
    if len(arr) == 0:
        result.append(current.copy())  # Копируем!
        return
    # ...
```

### 📌 Полезные ресурсы
- [Документация: isinstance()](https://docs.python.org/3/library/functions.html#isinstance)
- [Документация: copy](https://docs.python.org/3/library/copy.html)
- [Рекурсия в Python](https://docs.python.org/3/faq/programming.html#what-is-tail-recursion)
- [Big O сложность рекурсии](https://en.wikipedia.org/wiki/Time_complexity)
- [Динамическое программирование](https://en.wikipedia.org/wiki/Dynamic_programming)
