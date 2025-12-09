# List Comprehension zip() стек очередь

## 📖 Быстрая навигация по операторам и функциям

- [[#0) План урока]](#0-план-урока)
- [[#1) List comprehension (списковое включение)]](#1-list-comprehension-списковое-включение)
- [[#2) List comprehension с условием `if` (фильтрация)]](#2-list-comprehension-с-условием-if-фильтрация)
- [[#3) List comprehension с `if ... else` (преобразование каждого элемента)]](#3-list-comprehension-с-if-else-преобразование-каждого-элемента)
- [[#4) Вложенное `if ... else` (несколько уровней условий)]](#4-вложенное-if-else-несколько-уровней-условий)
- [[#5) List comprehension с вложенным циклом (nested loops)]](#5-list-comprehension-с-вложенным-циклом-nested-loops)
- [[#6) Задания для закрепления (ответы)]](#6-задания-для-закрепления-ответы)
- [[#7) Функция `zip()`]](#7-функция-zip)
- [[#8) Стек и очередь]](#8-стек-и-очередь)
- [[#9) Устойчивость сортировки (stable sort)]](#9-устойчивость-сортировки-stable-sort)
- [[#10) Практические задания (решения)]](#10-практические-задания-решения)
- [[#11) Домашнее задание (решения)]](#11-домашнее-задание-решения)
- [[#12) Мини-шпаргалка]](#12-мини-шпаргалка)
- [[#Дополнительная информация]](#дополнительная-информация)


---

## 1) List comprehension (списковое включение)

### 1.1 Что это такое
**List comprehension** — удобный способ создать новый список, применяя выражение к каждому элементу итерируемого объекта и/или отфильтровав элементы по условию.

### 1.2 Базовый синтаксис
```py
new_list = [expression for item in iterable]
```
- `expression` — что добавить в новый список (элемент/операция/вызов функции)
- `item` — переменная, принимающая элементы
- `iterable` — источник (list/tuple/str/range и т.д.)

Пример: квадраты чисел
```py
numbers = [1, 4, 6, 7, 9]
squares = [n ** 2 for n in numbers]
print(squares)
```

### 1.3 List comprehension vs `for`
List comprehension:
- короче и часто читаемее для простых операций
- удобно передавать в функции (одна строка)

`for`:
- лучше для сложной логики, много шагов, когда важна отладка

Эквивалент:
```py
# list comprehension
squares = [x ** 2 for x in range(5)]

# for
squares = []
for x in range(5):
    squares.append(x ** 2)
```

---

## 2) List comprehension с условием `if` (фильтрация)

### 2.1 Синтаксис
```py
new_list = [expression for item in iterable if condition]
```

Пример: только чётные
```py
even_numbers = [x for x in range(10) if x % 2 == 0]
print(even_numbers)  # [0, 2, 4, 6, 8]
```

Пример: слова с буквой `a`
```py
words = ["apple", "banana", "cherry", "date"]
words_with_a = [word for word in words if "a" in word]
print(words_with_a)  # ['apple', 'banana', 'date']
```

---

## 3) List comprehension с `if ... else` (преобразование каждого элемента)

### 3.1 Синтаксис
⚠️ Здесь условие находится **внутри выражения**, а не в конце:
```py
new_list = [expr_if_true if condition else expr_if_false for item in iterable]
```

Пример: заменить нечётные на `-1`
```py
numbers = [2, 7, 5, 4, 1, 1, 7, 8]
modified = [x if x % 2 == 0 else -1 for x in numbers]
print(modified)  # [2, -1, -1, 4, -1, -1, -1, 8]
```

Пример: короткие слова — с заглавной буквы
```py
words = ["cat", "elephant", "dog", "bird"]
result = [w if len(w) > 3 else w.capitalize() for w in words]
print(result)
```

---

## 4) Вложенное `if ... else` (несколько уровней условий)
Пример логики:
- если длина > 5 → оставить слово
- если длина от 3 до 5 → заменить на `"medium"`
- если длина < 3 → заменить на `"short"`

```py
words = ["hi", "apple", "banana", "cat", "blueberry", "on"]

modified = [
    w if len(w) > 5 else ("medium" if len(w) >= 3 else "short")
    for w in words
]
print(modified)
```

⚠️ Чем больше логики, тем хуже читаемость. Если становится тяжело читать — лучше `for`.

---

## 5) List comprehension с вложенным циклом (nested loops)

### 5.1 Синтаксис
```py
new_list = [expression for item1 in iterable1 for item2 in iterable2]
```

Пример: пары чисел
```py
pairs = [(x, y) for x in range(3) for y in range(2)]
print(pairs)
# [(0,0), (0,1), (1,0), (1,1), (2,0), (2,1)]
```

### 5.2 Матрица и “расплющивание” (flatten)
**Матрица** — это список списков одинаковой длины (двумерная структура).

```py
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(flat)  # [1,2,3,4,5,6,7,8,9]
```

---

## 6) Задания для закрепления (ответы)

### 6.1
```py
ages = [12, 17, 24, 18, 30]
adults = [age for age in ages if age >= 18]
print(adults)
```
Ответ: **`[24, 18, 30]`**

### 6.2
```py
names = ["John", "Anna", "Zoe", "Mark"]
formatted = [name.lower() if len(name) > 3 else name.upper() for name in names]
print(formatted)
```
Ответ: **`['john', 'anna', 'ZOE', 'mark']`**

### 6.3
```py
matrix = [[7, 8], [9, 10], [11, 12]]
flattened = [value * 2 for row in matrix for value in row]
print(flattened)
```
Ответ: **`[14, 16, 18, 20, 22, 24]`**

---

## 7) Функция `zip()`

### 7.1 Что делает
`zip()` объединяет несколько итерируемых объектов в один, создавая кортежи из элементов на одинаковых позициях.

```py
zip(*iterables)
```

✅ Важно:
- `zip()` **останавливается на самом коротком** источнике
- объект `zip` — это **итератор** (если превратить в `list` один раз, второй раз он будет пустым)

### 7.2 Примеры
```py
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
cities = ["Hamburg", "Berlin", "Munich"]

z = zip(names, ages, cities)
print(list(z))
# [('Alice', 25, 'Hamburg'), ('Bob', 30, 'Berlin'), ('Charlie', 35, 'Munich')]
```

Разная длина:
```py
list1 = [1, 2, 3]
list2 = ["a", "b"]
print(list(zip(list1, list2)))
# [(1, 'a'), (2, 'b')]
```

В цикле:
```py
for name, age in zip(names, ages):
    print(f"{name} is {age} years old.")
```

---

## 8) Стек и очередь

### 8.1 Стек (Stack): LIFO
**LIFO** = Last In, First Out → “последним пришёл — первым ушёл”.

Реализация на `list`:
```py
stack = []
stack.append(1)
stack.append(2)
stack.append(3)

print(stack.pop())  # 3
print(stack.pop())  # 2
print(stack)        # [1]
```

### 8.2 Очередь (Queue): FIFO
**FIFO** = First In, First Out → “первым пришёл — первым ушёл”.

Для очереди лучше использовать `collections.deque` (быстрее для операций с началом очереди):
```py
from collections import deque

queue = deque()
queue.append(1)
queue.append(2)
queue.append(3)

print(queue.popleft())  # 1
print(queue)            # deque([2, 3])
```

---

## 9) Устойчивость сортировки (stable sort)

### 9.1 Определение
**Устойчивая сортировка** сохраняет относительный порядок элементов с одинаковым ключом.

В Python:
- `sorted()` и `.sort()` — **устойчивые**.

### 9.2 Пример
```py
words = ["orange", "mango", "apple", "banana", "kiwi", "cherry"]
sorted_words = sorted(words, key=len)
for w in sorted_words:
    print(len(w), w)
```
У слов одинаковой длины порядок будет как в исходном списке.

### 9.3 Практический смысл
Устойчивость помогает при “многошаговой сортировке”:
1) сначала сортируешь по вторичному ключу,
2) потом по первичному — и вторичный порядок сохранится.

---

## 10) Практические задания (решения)

### 10.1 “Зеркальные строки больше трёх”
Дано:
```py
words = ["cat", "elephant", "dog", "bird", "lion", "ant"]
```

Решение:
```py
words = ["cat", "elephant", "dog", "bird", "lion", "ant"]
result = [word[::-1] for word in words if len(word) > 3]
print("Перевёрнутые слова длиной больше 3 символов:", result)
# ['tnahpele', 'drib', 'noil']
```

### 10.2 “Суммы строк матрицы”
Дано:
```py
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

Решение:
```py
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
row_sums = [sum(row) for row in matrix]
print("Суммы строк:", row_sums)  # [6, 15, 24]
```

---

## 11) Домашнее задание (решения)

### 11.1 “Оценки текстом”
Дано:
```py
grades = [5, 3, 4, 2, 1, 5, 3]
```

Требование:
- 5 → "отлично"
- 3–4 → "хорошо"
- 2 и ниже → "неудовлетворительно"

Решение (сохраняем два списка):
```py
grades = [5, 3, 4, 2, 1, 5, 3]

labels = [
    "отлично" if g == 5 else ("хорошо" if g >= 3 else "неудовлетворительно")
    for g in grades
]

print(grades)
print(labels)
```

---

### 11.2 “Правильные скобки” (stack)
Дано:
```py
string = "({[}])"
```

Идея:
- открывающие скобки кладём в стек
- на закрывающей проверяем, совпадает ли с вершиной стека
- в конце стек должен быть пуст

Решение:
```py
def is_balanced(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    opening = set(pairs.values())
    stack = []

    for ch in s:
        if ch in opening:
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
        # остальные символы (если будут) игнорируем

    return len(stack) == 0


print(is_balanced("({[]})"))  # True
print(is_balanced("({[}])"))  # False
```

---

## 12) Мини-шпаргалка
```text
List comprehension:
[x for x in it]
[x for x in it if cond]
[x_if if cond else x_else for x in it]
[x for a in A for b in B]  (вложенные циклы)

zip():
zip(a,b,c) -> итератор кортежей
останавливается на самом коротком
list(zip(...)) расходует итератор

Stack (LIFO):
append + pop

Queue (FIFO):
deque().append + deque().popleft

Stable sort:
sorted / .sort устойчивые (равные key сохраняют порядок)
```


---

## Дополнительная информация

### Важные концепции для изучения

#### 1. Вложенные list comprehensions
```python
# Создание матрицы
matrix = [[i*j for j in range(5)] for i in range(5)]
print(matrix)
# [[0, 0, 0, 0, 0],
#  [0, 1, 2, 3, 4],
#  [0, 2, 4, 6, 8],
#  [0, 3, 6, 9, 12],
#  [0, 4, 8, 12, 16]]

# Flatten (развертывание вложенного списка)
nested = [[1, 2], [3, 4], [5, 6]]
flat = [item for sublist in nested for item in sublist]
print(flat)  # [1, 2, 3, 4, 5, 6]

# С условием
nested = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
evens = [item for sublist in nested for item in sublist if item % 2 == 0]
print(evens)  # [2, 4, 6, 8]

# Транспонирование матрицы
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
print(transposed)
# [[1, 4, 7],
#  [2, 5, 8],
#  [3, 6, 9]]
```

#### 2. Dictionary и Set Comprehensions
```python
# Dictionary comprehension
squares_dict = {x: x**2 for x in range(5)}
print(squares_dict)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Инвертирование словаря
original = {'a': 1, 'b': 2, 'c': 3}
inverted = {v: k for k, v in original.items()}
print(inverted)  # {1: 'a', 2: 'b', 3: 'c'}

# С условием
words = ['apple', 'banana', 'cherry', 'date']
lengths = {word: len(word) for word in words if len(word) > 5}
print(lengths)  # {'banana': 6, 'cherry': 6}

# Set comprehension
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_squares = {x**2 for x in numbers}
print(unique_squares)  # {16, 1, 4, 9}

# Фильтрация уникальных букв
text = "Hello World"
unique_chars = {char.lower() for char in text if char.isalpha()}
print(unique_chars)  # {'e', 'd', 'h', 'l', 'o', 'r', 'w'}
```

#### 3. Продвинутое использование zip()
```python
# zip с разной длиной - останавливается на кратчайшем
list1 = [1, 2, 3, 4, 5]
list2 = ['a', 'b', 'c']
result = list(zip(list1, list2))
print(result)  # [(1, 'a'), (2, 'b'), (3, 'c')]

# zip_longest для обработки всех элементов
from itertools import zip_longest
result = list(zip_longest(list1, list2, fillvalue='X'))
print(result)  # [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'X'), (5, 'X')]

# Распаковка zip для транспонирования
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]
numbers, letters = zip(*pairs)
print(numbers)  # (1, 2, 3)
print(letters)  # ('a', 'b', 'c')

# Создание словаря из двух списков
keys = ['name', 'age', 'city']
values = ['Алиса', 25, 'Москва']
person = dict(zip(keys, values))
print(person)  # {'name': 'Алиса', 'age': 25, 'city': 'Москва'}

# Параллельная итерация трех списков
names = ['Алиса', 'Боб', 'Виктор']
ages = [25, 30, 28]
cities = ['Москва', 'СПб', 'Казань']
for name, age, city in zip(names, ages, cities):
    print(f"{name}, {age} лет, {city}")
```

#### 4. Стек и очередь - продвинутые операции
```python
from collections import deque

# Двусторонняя очередь (deque)
dq = deque([1, 2, 3])

# Операции с обеих сторон O(1)
dq.append(4)       # [1, 2, 3, 4]
dq.appendleft(0)   # [0, 1, 2, 3, 4]
dq.pop()           # [0, 1, 2, 3]
dq.popleft()       # [1, 2, 3]

# Rotate - циклический сдвиг
dq = deque([1, 2, 3, 4, 5])
dq.rotate(2)       # [4, 5, 1, 2, 3]
dq.rotate(-1)      # [5, 1, 2, 3, 4]

# Ограниченная очередь (FIFO с максимальным размером)
limited_queue = deque(maxlen=3)
for i in range(5):
    limited_queue.append(i)
    print(list(limited_queue))
# [0]
# [0, 1]
# [0, 1, 2]
# [1, 2, 3]  # 0 вытеснен
# [2, 3, 4]  # 1 вытеснен

# Реализация LRU cache на deque
class LRUCache:
    def __init__(self, capacity):
        self.cache = {}
        self.capacity = capacity
        self.order = deque()
    
    def get(self, key):
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return None
    
    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.popleft()
            del self.cache[oldest]
        
        self.cache[key] = value
        self.order.append(key)
```

### 💡 Практические примеры

#### Пример 1: Создание таблицы умножения
```python
# Таблица Пифагора
multiplication_table = [
    [i * j for j in range(1, 11)]
    for i in range(1, 11)
]

# Красивый вывод
for row in multiplication_table:
    print(' '.join(f'{x:3}' for x in row))
```

#### Пример 2: Группировка элементов по условию
```python
# Разделение на четные и нечетные
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_odd = {
    'even': [x for x in numbers if x % 2 == 0],
    'odd': [x for x in numbers if x % 2 != 0]
}
print(even_odd)
# {'even': [2, 4, 6, 8, 10], 'odd': [1, 3, 5, 7, 9]}

# Категоризация по диапазонам
scores = [45, 67, 89, 92, 56, 78, 34, 91]
categories = {
    'A': [s for s in scores if s >= 90],
    'B': [s for s in scores if 80 <= s < 90],
    'C': [s for s in scores if 70 <= s < 80],
    'D': [s for s in scores if 60 <= s < 70],
    'F': [s for s in scores if s < 60]
}
```

#### Пример 3: Реализация истории браузера (стек)
```python
class BrowserHistory:
    def __init__(self):
        self.history = []
        self.forward_stack = []
    
    def visit(self, url):
        """Посетить новую страницу"""
        self.history.append(url)
        self.forward_stack.clear()  # Очищаем forward при новом визите
    
    def back(self):
        """Вернуться назад"""
        if len(self.history) > 1:
            current = self.history.pop()
            self.forward_stack.append(current)
            return self.history[-1]
        return None
    
    def forward(self):
        """Вперед"""
        if self.forward_stack:
            page = self.forward_stack.pop()
            self.history.append(page)
            return page
        return None

# Использование
browser = BrowserHistory()
browser.visit("google.com")
browser.visit("python.org")
browser.visit("github.com")
print(browser.back())     # python.org
print(browser.back())     # google.com
print(browser.forward())  # python.org
```

#### Пример 4: Система задач с приоритетами
```python
import heapq

class PriorityQueue:
    def __init__(self):
        self.queue = []
        self.counter = 0
    
    def add_task(self, priority, task):
        """Добавить задачу (меньшее число = выше приоритет)"""
        heapq.heappush(self.queue, (priority, self.counter, task))
        self.counter += 1
    
    def get_task(self):
        """Получить задачу с наивысшим приоритетом"""
        if self.queue:
            _, _, task = heapq.heappop(self.queue)
            return task
        return None

# Использование
pq = PriorityQueue()
pq.add_task(3, "Низкий приоритет")
pq.add_task(1, "Высокий приоритет")
pq.add_task(2, "Средний приоритет")

print(pq.get_task())  # Высокий приоритет
print(pq.get_task())  # Средний приоритет
print(pq.get_task())  # Низкий приоритет
```

### 🚨 Частые ошибки

**Ошибка 1: Слишком сложные list comprehensions**
```python
# ❌ ПЛОХО - трудно читать
result = [x*y for x in range(10) if x % 2 == 0 for y in range(10) if y % 3 == 0 if x*y > 20]

# ✅ ЛУЧШЕ - разбить на части или использовать циклы
evens = [x for x in range(10) if x % 2 == 0]
threes = [y for y in range(10) if y % 3 == 0]
result = [x*y for x in evens for y in threes if x*y > 20]

# ИЛИ обычный цикл для сложной логики
result = []
for x in range(10):
    if x % 2 == 0:
        for y in range(10):
            if y % 3 == 0:
                product = x * y
                if product > 20:
                    result.append(product)
```

**Ошибка 2: Использование списка вместо deque для очереди**
```python
# ❌ НЕЭФФЕКТИВНО - O(n) для удаления с начала
queue = [1, 2, 3]
queue.append(4)     # O(1)
first = queue.pop(0)  # O(n) - медленно!

# ✅ ЭФФЕКТИВНО - deque с O(1) для обеих операций
from collections import deque
queue = deque([1, 2, 3])
queue.append(4)       # O(1)
first = queue.popleft()  # O(1) - быстро!
```

**Ошибка 3: Изменение списка в comprehension**
```python
# ❌ НЕПРАВИЛЬНО - побочные эффекты в comprehension
data = [1, 2, 3]
[data.append(x*2) for x in data]  # Плохая практика!

# ✅ ПРАВИЛЬНО - создаем новый список
data = [1, 2, 3]
doubled = [x*2 for x in data]
data.extend(doubled)
```

**Ошибка 4: Неправильное понимание zip() с разными длинами**
```python
# ❌ ПРОБЛЕМА - теряются данные
list1 = [1, 2, 3, 4, 5]
list2 = ['a', 'b']
result = list(zip(list1, list2))
print(result)  # [(1, 'a'), (2, 'b')] - потеряли 3, 4, 5!

# ✅ РЕШЕНИЕ - используем zip_longest если нужны все данные
from itertools import zip_longest
result = list(zip_longest(list1, list2, fillvalue=None))
print(result)  # [(1, 'a'), (2, 'b'), (3, None), (4, None), (5, None)]
```

### 📌 Полезные ресурсы
- [Документация: List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [Документация: zip()](https://docs.python.org/3/library/functions.html#zip)
- [Документация: collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)
- [PEP 289: Generator Expressions](https://www.python.org/dev/peps/pep-0289/)
- [itertools recipes](https://docs.python.org/3/library/itertools.html#itertools-recipes)
