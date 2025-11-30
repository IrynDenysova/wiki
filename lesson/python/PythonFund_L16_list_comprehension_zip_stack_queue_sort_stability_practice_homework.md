# Python Fundamentals — Урок 16: List Comprehension, `zip()`, стек и очередь, устойчивость сортировки

## 0) План урока
- List comprehension (генератор списка)
- `zip()` — объединение последовательностей
- Стек (LIFO) и очередь (FIFO)
- Устойчивость сортировки (stable sort)
- Практика + домашнее задание (с решениями)

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
