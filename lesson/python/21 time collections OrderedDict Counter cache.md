# time collections OrderedDict Counter cache

## 📖 Быстрая навигация по операторам и функциям

- [План занятия](#0-план-занятия)
- [Модуль `time`](#1-модуль-time)
- [Модуль `collections`](#2-модуль-collections)
- [`OrderedDict`](#3-ordereddict)
- [`OrderedDict.popitem(last=True)`](#4-ordereddictpopitemlasttrue)
- [`OrderedDict.move_to_end(key, last=True)`](#5-ordereddictmovetoendkey-lasttrue)

**[📚 Дополнительная информация и примеры](#дополнительная-информация)**


## 0) План занятия
- Модуль `time`: измерение времени, `time()` и `sleep()`
- Модуль `collections`
  - `OrderedDict`: порядок, `popitem()`, `move_to_end()`
  - `defaultdict`: значения по умолчанию без `KeyError`
  - `Counter`: частотный анализ + методы + операции
- Кэш и LRU-кэш (`functools.lru_cache`)
- Практика + домашнее задание (решения)

---

## 1) Модуль `time`
Модуль `time` нужен для:
- получения текущего времени (в секундах от 01.01.1970),
- измерения интервалов,
- задержек выполнения кода.

### 1.1 `time.time()`
```py
import time

current_time = time.time()
print(current_time)  # float секунд с 1970-01-01
```

### 1.2 `time.sleep(seconds)`
```py
import time

time.sleep(2)
print("2 секунды спустя...")
```

### 1.3 Пример: измерение времени выполнения (range vs list)
```py
import time

start_time = time.time()
range_million = range(1_000_000)
end_time = time.time()
print(f"Время создания range: {end_time - start_time:.10f} секунд")

start_time = time.time()
lst = [x for x in range(1_000_000)]
end_time = time.time()
print(f"Время создания list: {end_time - start_time:.10f} секунд")
```

---

## 2) Модуль `collections`
`collections` даёт дополнительные структуры данных, которые дополняют стандартные типы Python и часто удобнее/эффективнее для конкретных задач.

---

## 3) `OrderedDict`
`OrderedDict` — словарь, который **гарантированно сохраняет порядок вставки**.

> Исторически нужен был до Python 3.7, где обычный `dict` не гарантировал порядок. Сейчас `dict` порядок сохраняет, но `OrderedDict` всё ещё полезен из-за некоторых “фишек”.

### 3.1 Создание
```py
from collections import OrderedDict

od = OrderedDict()
od["a"] = 1
od["b"] = 2
od["c"] = 3

print(od)  # OrderedDict([('a', 1), ('b', 2), ('c', 3)])
```

---

## 4) `OrderedDict.popitem(last=True)`
Удаляет и возвращает пару `(key, value)`.

- `last=True` (по умолчанию) — забирает **последний** добавленный элемент
- `last=False` — забирает **первый** добавленный элемент

```py
from collections import OrderedDict

od = OrderedDict()
od["a"] = 1
od["b"] = 2
od["c"] = 3
od["d"] = 4

print(od.popitem())            # ('d', 4)
print(od.popitem(last=False))  # ('a', 1)
print(od)
```

### 4.1 Как сделать очередь на `OrderedDict`
```py
from collections import OrderedDict

queue = OrderedDict()
queue["first"] = 1
queue["second"] = 2
queue["third"] = 3

while queue:
    print(queue.popitem(last=False))  # FIFO
```

---

## 5) `OrderedDict.move_to_end(key, last=True)`
Перемещает элемент:
- `last=True` → в **конец**
- `last=False` → в **начало**

```py
from collections import OrderedDict

fruits = OrderedDict()
fruits["apple"] = 3
fruits["banana"] = 5
fruits["orange"] = 2

fruits.move_to_end("apple")            # apple -> конец
fruits.move_to_end("orange", last=False)  # orange -> начало

print(list(fruits.keys()))
# ['orange', 'banana', 'apple']
```

---

## 6) Кэш и LRU-кэш
### 6.1 Что такое кэш
**Кэш** — хранение результатов вычислений/часто используемых данных, чтобы:
- ускорить повторные запросы,
- уменьшить нагрузку на “медленные” ресурсы (БД, API, диск),
- снизить время ответа.

### 6.2 LRU-кэш (Least Recently Used)
LRU хранит фиксированное количество элементов. Когда место заканчивается, удаляется элемент, который **давно не использовался**.

---

## 7) `functools.lru_cache`
Python имеет встроенный LRU-кэш для функций: декоратор `@lru_cache`.

### 7.1 Синтаксис
```py
from functools import lru_cache

@lru_cache(maxsize=128, typed=False)
def function_name(...):
    ...
```

- `maxsize`: сколько результатов хранить (если `None` — без ограничения)
- `typed`: если `True`, различает типы аргументов (`1` и `1.0` — разные ключи)

### 7.2 Пример (видно, когда функция “выполняется”, а когда берётся из кэша)
```py
from time import time, sleep
from functools import lru_cache

@lru_cache(maxsize=2)
def compute_square(n):
    print(f"Вычисляю квадрат числа {n}...")
    sleep(2)               # имитация долгого расчёта
    return n * n

start = time()
print(compute_square(2))   # вычисляет
print(f"Время: {time() - start:.2f} сек
")

start = time()
print(compute_square(3))   # вычисляет (и кэш теперь заполнен 2 значениями)
print(f"Время: {time() - start:.2f} сек
")

start = time()
print(compute_square(2))   # берёт из кэша → моментально
print(f"Время: {time() - start:.2f} сек
")
```

---

## 8) `defaultdict`
`defaultdict` — словарь, который **автоматически создаёт значение по умолчанию** для отсутствующего ключа.

### 8.1 Синтаксис
```py
from collections import defaultdict

dd = defaultdict(default_type)
```
`default_type` — функция/класс, который создаёт значение (например `int`, `list`, `set`, `str`, пользовательская функция).

### 8.2 Пример: `defaultdict(int)` (по умолчанию 0)
```py
from collections import defaultdict

dd = defaultdict(int)
print(dd["missing"])  # 0 (ключ добавится автоматически)

dd["a"] += 1
dd["b"] += 10
print(dd)  # defaultdict(<class 'int'>, {'missing': 0, 'a': 1, 'b': 10})
```

### 8.3 Пример: `defaultdict(list)` (удобно для группировки)
```py
from collections import defaultdict

dd = defaultdict(list)
dd["x"].append(1)
dd["y"].extend([2, 3])

print(dd["z"])  # []  (ключ 'z' создан автоматически)
print(dd)
```

### 8.4 Кастомное значение по умолчанию
```py
from collections import defaultdict

def default_value():
    return "default"

dd = defaultdict(default_value)
print(dd["missing_key"])  # "default"
```

---

## 9) `Counter`
`Counter` — словарь “элемент → количество”. Очень удобен для частотного анализа.

### 9.1 Создание
```py
from collections import Counter

c1 = Counter("hello world")                 # по символам
c2 = Counter(["apple", "banana", "apple"])  # по элементам списка
c3 = Counter({"apple": 3, "banana": 2})     # из mapping

print(c1)
print(c2)
print(c3)
```

### 9.2 Методы Counter
#### `most_common([n])`
Топ-N самых частых:
```py
from collections import Counter

counter = Counter("banana")
print(counter.most_common(2))  # [('a', 3), ('n', 2)]
```

#### `elements()`
Повторяет элементы столько раз, сколько их количество (нули/отрицательные игнорируются):
```py
from collections import Counter

counter = Counter({"a": 3, "b": 1, "c": 0})
print(list(counter.elements()))  # ['a', 'a', 'a', 'b']
```

#### `subtract(...)`
Уменьшает количества (значения могут стать отрицательными):
```py
from collections import Counter

counter = Counter("banana")
counter.subtract("an")
print(counter)
```

#### `update(...)`
Увеличивает количества:
```py
from collections import Counter

counter = Counter("banana")
counter.update("nan")
print(counter)
```

### 9.3 Операции между Counter
> Важно: результат операций обычно **отбрасывает отрицательные и нулевые** количества (кроме `subtract`, который может делать отрицательные).

```py
from collections import Counter

c1 = Counter("banana")
c2 = Counter("an")

print(c1 + c2)  # сложение (сумма)
print(c1 - c2)  # вычитание (отрицательные игнорируются)
print(c1 & c2)  # пересечение (минимальные количества)
print(c1 | c2)  # объединение (максимальные количества)
```

---

# Ответы на задания (из урока)
- `unique_lengths = {len(word) for word in ["apple","banana","cherry","apple"]}` → **`{5, 6}`**
- `defaultdict(list)` и `print(dd["z"])` → **`[]`**
- подсчёт `apple` в списке `["apple","banana","apple","orange","banana"]` → **`2`**
- группировка `("class1","Alice") ... ("class1","Charlie")` → для `"class1"` получится **`["Alice", "Charlie"]`**
- Counter: метод для самых частых → **`most_common()`**

---

# Практическая работа (решения)

## 1) Частотный анализ слов (игнорировать регистр, убрать `.` и `,`)
Дано:
```py
text = "This is a test. This test is only a test."
```

Решение:
```py
from collections import Counter

text = "This is a test. This test is only a test."
words = text.lower().replace(".", "").replace(",", "").split()
word_count = Counter(words)

print(dict(word_count))
# {'this': 2, 'is': 2, 'a': 2, 'test': 3, 'only': 1}
```

## 2) Список студентов по факультетам (группировка)
Дано:
```py
students = [
 ("Иван", "Физика"),
 ("Мария", "Математика"),
 ("Пётр", "Физика"),
 ("Анна", "Математика"),
 ("Олег", "Информатика"),
 ("Наталья", "Физика"),
]
```

Решение:
```py
from collections import defaultdict

def group_students_by_faculty(students):
    faculty_dict = defaultdict(list)
    for name, faculty in students:
        faculty_dict[faculty].append(name)
    return dict(faculty_dict)

students = [
 ("Иван", "Физика"),
 ("Мария", "Математика"),
 ("Пётр", "Физика"),
 ("Анна", "Математика"),
 ("Олег", "Информатика"),
 ("Наталья", "Физика"),
]

result = group_students_by_faculty(students)
for faculty, names in result.items():
    print(f"{faculty}: {names}")
```

---

# Домашнее задание (решения)

## ДЗ 1) Подсчёт букв в тексте (игнорировать регистр)
Дано:
```py
text = "Programming is fun!"
```

Решение (через Counter):
```py
from collections import Counter

text = "Programming is fun!"
letters = [ch for ch in text.lower() if ch.isalpha()]
counts = Counter(letters)
print(dict(counts))
```

## ДЗ 2) Группировка студентов по классам
Дано:
```py
students = [("class1", "Alice"), ("class2", "Bob"), ("class1", "Charlie"), ("class3", "Daisy")]
```

Решение (через defaultdict(list)):
```py
from collections import defaultdict

students = [("class1", "Alice"), ("class2", "Bob"), ("class1", "Charlie"), ("class3", "Daisy")]

grouped = defaultdict(list)
for cls, name in students:
    grouped[cls].append(name)

print(dict(grouped))
# {'class1': ['Alice', 'Charlie'], 'class2': ['Bob'], 'class3': ['Daisy']}
```

---

## Мини-шпаргалка
```text
time:
- time.time()  -> текущее время (сек с 1970)
- time.sleep() -> пауза

OrderedDict:
- popitem(last=True/False)
- move_to_end(key, last=True/False)

Cache / LRU:
- functools.lru_cache(maxsize=..., typed=...)

defaultdict:
- defaultdict(int)  -> 0
- defaultdict(list) -> []
- default создаётся при обращении к отсутствующему ключу

Counter:
- Counter(iterable/mapping)
- most_common(n), elements(), update(), subtract()
- операции: +  -  &  |
```


---

## 📚 Дополнительная информация

_Этот раздел будет дополнен практическими примерами и дополнительной информацией._
