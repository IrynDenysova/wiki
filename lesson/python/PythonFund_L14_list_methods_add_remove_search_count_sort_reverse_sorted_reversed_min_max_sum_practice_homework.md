# Python Fundamentals — Урок 14: методы списков (add/remove/search/sort), `sorted/reversed`, `min/max/sum`

## План урока
- Методы добавления элементов: `append`, `extend`, `insert`
- Удаление элементов: `remove`, `pop`, `clear`
- Поиск и подсчёт: `index`, `count`
- Разворот и сортировка: `reverse`, `sort`, функции `reversed`, `sorted`
- Встроенные функции для коллекций: `min`, `max`, `sum`
- Практика + домашка (с решениями)

---

## 1) Добавление элементов в список

### 1.1 `append(item)` — добавить **один** элемент в конец
```py
numbers = [1, 2, 3]
numbers.append(4)
print(numbers)  # [1, 2, 3, 4]
```

✅ Важно: `append` добавляет объект **целиком** (в том числе список):
```py
lst = [1, 2, 3]
lst.append([4, 5])
print(lst)  # [1, 2, 3, [4, 5]]
```

⚠️ `append(4, 5)` вызовет ошибку: `append` принимает **ровно 1** аргумент.

---

### 1.2 `extend(iterable)` — добавить элементы из другой коллекции **по одному**
```py
numbers = [1, 2, 3]
numbers.extend([4, 5, 6])
print(numbers)  # [1, 2, 3, 4, 5, 6]
```

✅ `extend` принимает **итерируемый объект** (список/кортеж/строку/range и т. д.):
```py
fruits = ["apple", "banana"]
fruits.extend("grape")
print(fruits)  # ["apple", "banana", "g", "r", "a", "p", "e"]
```

⚠️ `extend(4)` или `extend(4, 5)` → ошибка (int не итерируемый / нужно 1 аргумент).

---

### 1.3 `insert(index, item)` — вставить элемент по индексу
```py
fruits = ["apple", "banana"]
fruits.insert(0, "blueberry")
print(fruits)  # ["blueberry", "apple", "banana"]
```

Полезные особенности:
- если `index` больше длины списка — вставка произойдёт **в конец**
- отрицательный индекс вставляет **перед** указанной позицией

```py
letters = ["a", "b", "c"]
letters.insert(-1, "x")
print(letters)  # ["a", "b", "x", "c"]
```

---

## 2) Удаление элементов

### 2.1 `remove(item)` — удалить **первое** вхождение элемента
```py
fruits = ["apple", "banana", "cherry", "banana"]
fruits.remove("banana")
print(fruits)  # ["apple", "cherry", "banana"]
```

⚠️ Если элемента нет → `ValueError`.

Безопасный вариант:
```py
item = "banana"
if item in fruits:
    fruits.remove(item)
```

---

### 2.2 `pop(index=-1)` — удалить по индексу и **вернуть** элемент
```py
numbers = [10, 20, 30, 40]
last_item = numbers.pop()
print(numbers)    # [10, 20, 30]
print(last_item)  # 40

second = numbers.pop(1)
print(numbers)  # [10, 30]
print(second)   # 20
```

⚠️ Если индекс вне диапазона → `IndexError` (а не `ValueError`).

---

### 2.3 `clear()` — очистить список полностью
```py
fruits = ["apple", "banana", "cherry"]
fruits.clear()
print(fruits)  # []
```

---

## 3) Поиск и подсчёт элементов

### 3.1 `index(item, start=0, stop=len)` — найти индекс первого вхождения
```py
fruits = ["apple", "banana", "cherry", "banana"]
print(fruits.index("banana"))      # 1
print(fruits.index("banana", 2))   # 3
print(fruits.index("cherry", 1, 4)) # 2
```

⚠️ Если элемента нет → `ValueError`.

---

### 3.2 `count(item)` — сколько раз встречается элемент
```py
fruits = ["apple", "banana", "cherry", "banana"]
print(fruits.count("banana"))  # 2
print(fruits.count("orange"))  # 0
```

---

## 4) Разворот и сортировка

### 4.1 `reverse()` — развернуть список **на месте**
```py
numbers = [4, 1, 7, 2, 9]
numbers.reverse()
print(numbers)  # [9, 2, 7, 1, 4]
```
> `reverse()` меняет список и возвращает `None`.

---

### 4.2 `sort(key=None, reverse=False)` — сортировка **на месте**
```py
numbers = [4, 1, 7, 2, 9]
numbers.sort()
print(numbers)  # [1, 2, 4, 7, 9]

numbers.sort(reverse=True)
print(numbers)  # [9, 7, 4, 2, 1]
```

Сортировка с `key` (функция без скобок!):
```py
fruits = ["banana", "apple", "cherry", "blueberry"]
fruits.sort(key=len)
print(fruits)  # по длине строк

tuples = [(3, 6), (1, 7, 9), (12, 5), (1, 3, 7)]
tuples.sort(key=max, reverse=True)  # по максимальному элементу кортежа
print(tuples)
```

> `sort()` меняет список и возвращает `None`.

---

### 4.3 `sorted(iterable, key=None, reverse=False)` — сортировка **без изменения** исходного объекта
```py
numbers = [3, 1, 4, 1, 5]
sorted_numbers = sorted(numbers)
print(sorted_numbers)  # [1, 1, 3, 4, 5]
print(numbers)         # исходный список не изменился
```

---

### 4.4 `reversed(iterable)` — разворот **без изменения** исходного объекта
`reversed()` возвращает **итератор**, а не список.

```py
numbers = [1, 2, 3]
it = reversed(numbers)
print(list(it))  # [3, 2, 1]

word = "hello"
print("".join(reversed(word)))  # "olleh"
```

---

### 4.5 Быстрое сравнение (когда что использовать)
- `lst.sort()` — сортируем **список на месте**
- `sorted(x)` — получаем **новый** отсортированный список из любой коллекции
- `lst.reverse()` — разворот **списка на месте**
- `reversed(x)` — получаем **итератор** в обратном порядке

---

## 5) `min()`, `max()`, `sum()`

### 5.1 `min(iterable, key=...)` / `max(iterable, key=...)`
```py
numbers = [4, 1, 7, 2, 9]
print(min(numbers))  # 1
print(max(numbers))  # 9

words = ["apple", "banana", "kiwi", "grape"]
print(min(words, key=len))  # "kiwi"
print(max(words, key=len))  # "banana"
```

### 5.2 `sum(iterable, start=0)`
```py
numbers = [4, 1, 7, 2, 9]
print(sum(numbers))        # 23
print(sum(numbers, 1000))  # 1023
```

---

## 6) Мини-тест (частые ловушки) — ответы
### 6.1 `insert`
```py
nested_list = [1, 2, 3]
nested_list.insert(1, "new")
print(nested_list)
```
✅ Результат: `[1, "new", 2, 3]`

### 6.2 `extend` со строкой
```py
fruits = ["apple", "banana"]
fruits.extend("grape")
print(fruits)
```
✅ Результат: `["apple", "banana", "g", "r", "a", "p", "e"]`

### 6.3 `remove` на срезе
```py
fruits = ["apple", "banana", "cherry", "banana"]
fruits[1:].remove("banana")
print(fruits)
```
✅ Результат: исходный список **не изменится** — `['apple', 'banana', 'cherry', 'banana']`  
Потому что `fruits[1:]` создаёт **копию** (новый список), и `remove` работает с копией.

### 6.4 `remove` несуществующего элемента
```py
numbers = [1, 2, 3, 4, 5]
numbers.remove(10)
```
✅ Будет ошибка: `ValueError`

---

## 7) Практическая работа (решения)

### 7.1 “Начало равно концу”
Дано:
```py
strings = ["apple", "banana", "level", "radar", "grape"]
```

Решение:
```py
strings = ["apple", "banana", "level", "radar", "grape"]

result = []
for s in strings:
    if s[0] == s[-1]:
        result.append(s)

print("Строки, которые начинаются и заканчиваются одной и той же буквой:", result)
# ['level', 'radar']
```

### 7.2 “Слова с гласных” (по примеру решения)
⚠️ В формулировке задания иногда путают гласные/согласные, но по решению и примеру — `!` добавляется, если слово начинается с **гласной**.

```py
strings = ["apple", "banana", "cherry", "grape", "orange"]

result = []
for s in strings:
    if s[0].lower() in "aeiou":
        s += "!"
    result.append(s)

print("Результат:", result)
# ['apple!', 'banana', 'cherry', 'grape', 'orange!']
```

---

## 8) Домашнее задание (решения)

### 8.1 “Число в конце”
Добавить только те строки, где цифры встречаются **только в конце**.

```py
strings = ["apple23", "ban1ana45", "12cherry", "grape3", "blue23berry"]

result = []
for s in strings:
    # находим первый индекс цифры
    first_digit = None
    for i, ch in enumerate(s):
        if ch.isdigit():
            first_digit = i
            break

    if first_digit is None:
        continue  # нет цифр — не подходит под условие задачи
    if s[:first_digit].isalpha() and s[first_digit:].isdigit():
        result.append(s)

print("Строки с цифрами только в конце:", result)
# ['apple23', 'grape3']
```

---

### 8.2 “Удаление кратных”
Удалить из списка все элементы, кратные введённому пользователем числу.

✅ Вариант “удалить на месте” безопасно:
```py
numbers = [1, 3, 6, 9, 10, 12, 15, 19, 20]
k = int(input("Введите число для удаления кратных ему элементов: "))

numbers[:] = [x for x in numbers if x % k != 0]
print("Список без кратных значений:", numbers)
```

---

### 8.3 “Порядок чётных”
Нечётные числа остаются на своих местах, а чётные сортируются между собой **по убыванию**.

```py
numbers = [5, 2, 3, 8, 4, 1, 2, 7]

evens = sorted([x for x in numbers if x % 2 == 0], reverse=True)

result = []
ei = 0
for x in numbers:
    if x % 2 != 0:
        result.append(x)          # нечётные на месте
    else:
        result.append(evens[ei])  # вставляем следующий чётный
        ei += 1

print("Список после сортировки:", result)
# [5, 8, 3, 4, 2, 1, 2, 7]
```

---

## 9) Мини-шпаргалка
```text
Добавление:
append(x)   -> +1 элемент в конец (может быть список внутри списка)
extend(it)  -> добавит элементы it по одному
insert(i,x) -> вставка по индексу (i>len -> в конец)

Удаление:
remove(x)   -> удалит первое вхождение x (если нет -> ValueError)
pop(i=-1)   -> удалит и вернёт элемент по индексу (если нет -> IndexError)
clear()     -> очистить список

Поиск/подсчёт:
index(x, start=0, stop=len) -> индекс первого (если нет -> ValueError)
count(x) -> сколько раз встретился

Сорт/реверс:
sort(key=None, reverse=False)  -> на месте, вернёт None
reverse()                      -> на месте, вернёт None
sorted(iterable, ...)          -> новый список
reversed(iterable)             -> итератор (list(...) / ''.join(...))

Функции:
min/max/sum (+ key=..., start=...)
```
