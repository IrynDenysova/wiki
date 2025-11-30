# Python Fundamentals — Урок 19: словари (продолжение) — `fromkeys`, `get`, `setdefault`, `keys/values/items`, вложенные словари, copy/deepcopy, dict comprehension

## 0) План урока
- `dict.fromkeys()`
- `dict.get()`
- `dict.setdefault()`
- `keys()`, `values()`, `items()` (view-объекты) + итерация
- Словари со вложенными структурами
- Копирование словаря: `copy()` vs `copy.deepcopy()`
- `dict` comprehension
- Сравнение словарей (`==`, `!=`)
- Практика + ДЗ (с решениями)

---

## 1) `dict.fromkeys(iterable, value=None)`
Создаёт словарь, где каждому ключу из `iterable` присваивается одно и то же значение.

### Синтаксис
```py
dict.fromkeys(iterable, value)
```

### Примеры
```py
keys = ["x", "y", "z"]
d = dict.fromkeys(keys)
print(d)  # {'x': None, 'y': None, 'z': None}

keys = [1, 2, 3]
d = dict.fromkeys(keys, "default")
print(d)  # {1: 'default', 2: 'default', 3: 'default'}
```

### ⚠️ Важная ловушка: изменяемое значение (общая ссылка)
```py
keys = ["a", "b", "c"]
shared_list = []
d = dict.fromkeys(keys, shared_list)

d["a"].append(1)
print(d)  # {'a': [1], 'b': [1], 'c': [1]}  <-- у всех ключей один и тот же список
```

**Как сделать “отдельный список каждому ключу”:**
```py
keys = ["a", "b", "c"]
d = {k: [] for k in keys}
d["a"].append(1)
print(d)  # {'a': [1], 'b': [], 'c': []}
```

---

## 2) `dict.get(key, default=None)`
Безопасный способ получить значение по ключу:
- если ключ есть → вернёт значение
- если ключа нет → вернёт `default` (по умолчанию `None`)
- **не бросает `KeyError`** (в отличие от `d[key]`)

### Синтаксис
```py
value = d.get(key, default)
```

### Примеры
```py
d = {"name": "Alice", "age": 30}

print(d.get("name"))                 # Alice
print(d.get("city"))                 # None
print(d.get("city", "Unknown"))      # Unknown
```

✅ Ответ на вопрос из урока: `my_dict.get("city")` → вернёт **None**.

---

## 3) `dict.setdefault(key, default=None)`
Похоже на `get`, но **если ключа нет — добавляет его** в словарь.

- ключ есть → возвращает текущее значение, словарь не меняется
- ключа нет → добавляет `key: default`, возвращает `default`

### Синтаксис
```py
value = d.setdefault(key, default)
```

### Примеры
```py
d = {"name": "Alice", "age": 30}

age = d.setdefault("age", 25)
print(age)  # 30
print(d)    # {'name': 'Alice', 'age': 30}

city = d.setdefault("city", "Unknown")
print(city)  # Unknown
print(d)     # {'name': 'Alice', 'age': 30, 'city': 'Unknown'}
```

✅ Ответ на вопрос из урока: `setdefault("age", 25)` при уже существующем `"age"` → вернёт **30**, словарь останется **неизменным**.

---

## 4) `keys()`, `values()`, `items()` = view-объекты
Эти методы возвращают **представления (view objects)**, которые:
- “смотрят” на исходный словарь
- автоматически отражают изменения словаря
- можно преобразовать в `list(...)`, чтобы получить “снимок” на текущий момент

### 4.1 `keys()` — ключи
```py
d = {"name": "Alice", "age": 30}
keys_view = d.keys()

d["city"] = "New York"
print(keys_view)  # обновилось автоматически

keys_list = list(keys_view)
d["country"] = "USA"
print(keys_list)  # НЕ обновится (это уже отдельный список)
```

### 4.2 `values()` — значения
```py
d = {"name": "Alice", "age": 30}
values_view = d.values()

d["age"] = 31
print(values_view)  # обновилось
```

### 4.3 `items()` — пары (key, value)
```py
d = {"x": 10, "y": 20}
items_view = d.items()
print(type(items_view))  # dict_items
```

✅ Ответ на вопрос из урока: `items()` возвращает тип **dict_items**.

---

## 5) Итерация по словарю
### 5.1 По ключам
```py
for key in d:
    ...
# то же самое, что:
for key in d.keys():
    ...
```

### 5.2 По значениям
```py
for value in d.values():
    ...
```

### 5.3 По парам
```py
for key, value in d.items():
    ...
```

---

## 6) Словари со вложенными структурами (nested dict)
Словарь может содержать внутри:
- списки / кортежи / множества / другие словари

### Примеры
Списки в значениях:
```py
student_scores = {
    "Alice": [90, 85, 88],
    "Bob": [72, 75, 80],
    "Charlie": [95, 100, 98],
}
print(student_scores["Alice"][1])  # 85
```

Вложенные словари:
```py
school = {
    "class1": {"students": ["Alice", "Bob", "Charlie"], "teacher": "Mrs. Smith"},
    "class2": {"students": ["David", "Eva"], "teacher": "Mr. Johnson"},
}

print(school["class2"]["teacher"])          # Mr. Johnson
print(school["class1"]["students"][0])      # Alice
```

### Итерация по вложенному словарю (вложенные циклы)
```py
for class_name, details in school.items():
    print(f"Class: {class_name}")
    for key, value in details.items():
        print(f"  {key}: {value}")
```

### Изменение вложенных структур
```py
school["class1"]["students"].append("Daisy")
del school["class2"]["teacher"]
```

✅ Ответ на задание из урока:
```py
company["department2"]["employees"].append("Miller")
```
выведет: **["Jane", "Smith", "Miller"]**

---

## 7) Копирование словарей: `copy()` vs `deepcopy()`

### 7.1 Поверхностная копия: `dict.copy()`
Копирует верхний уровень, но вложенные объекты остаются общими по ссылке.

```py
original = {"name": "Alice", "age": 30, "scores": [90, 85, 88]}
copied = original.copy()

original["age"] = 31              # copied не изменится (immutable)
original["scores"].append(80)     # copied изменится (shared list!)

print(original)
print(copied)
```

### 7.2 Глубокая копия: `copy.deepcopy()`
Создаёт независимую копию всей вложенности.

```py
import copy

original = {"name": "Alice", "age": 30, "scores": [90, 85, 88]}
deep = copy.deepcopy(original)

original["scores"].append(80)
print(original)
print(deep)  # deep не изменился
```

---

## 8) Dict comprehension
Удобный способ создавать/преобразовывать словари, как list comprehension.

### Синтаксис
```py
new_dict = {key_expr: value_expr for item in iterable}
```

### Примеры
Квадраты чисел:
```py
numbers = [1, 2, 3, 4]
squared = {n: n**2 for n in numbers}
```

Фильтрация по значениям:
```py
original = {"a": 5, "b": 2, "c": 0, "d": 3, "e": 0, "f": 3}
filtered = {k: v for k, v in original.items() if v > 0}
```

Словарь “слово → длина”:
```py
words = ["apple", "banana", "cherry"]
lengths = {w: len(w) for w in words}
```

---

## 9) Сравнение словарей
В Python доступны сравнения:
- `==` (равенство)
- `!=` (неравенство)

❗ Порядок добавления ключей не влияет на сравнение:
```py
d1 = {"a": 1, "b": 2}
d2 = {"b": 2, "a": 1}
print(d1 == d2)  # True
```

Если хотя бы одна пара отличается:
```py
d1 = {"a": 1, "b": 2}
d2 = {"a": 1, "b": 2, "c": 3}
print(d1 == d2)  # False
```

Если значения — списки, сравниваются **значения**, а не “ссылки”:
```py
d1 = {"a": 1, "b": [2, 1, 5]}
d2 = {"b": [2, 1, 5], "a": 1}
print(d1 == d2)  # True
```

---

# Практика (решения)

## A) Переводчик EN ⇄ RU (по словарю)
Дано:
```py
dictionary = {
    "Butterfly": "Бабочка",
    "Training": "Обучение",
    "Restaurant": "Ресторан",
    "Programming": "Программирование",
}
```

Решение (как в уроке: ищем и по ключам, и по значениям):
```py
dictionary = {
    "Butterfly": "Бабочка",
    "Training": "Обучение",
    "Restaurant": "Ресторан",
    "Programming": "Программирование",
}

while True:
    word = input("Введите слово для перевода (или 'exit' для выхода): ").strip().capitalize()

    if word == "Exit":
        print("Программа завершена.")
        break

    if word in dictionary:
        print(f"Перевод: {dictionary[word]}")
    elif word in dictionary.values():
        for k, v in dictionary.items():
            if v == word:
                print(f"Перевод: {k}")
                break
    else:
        print("Перевод отсутствует.")
```

---

## B) Проверка правильности скобок (словарь + стек)
Задача: проверить `()`, `[]`, `{}`.

```py
def is_brackets_valid(string: str) -> bool:
    brackets = {')': '(', ']': '[', '}': '{'}
    stack = []

    for ch in string:
        if ch in brackets.values():                # открывающая
            stack.append(ch)
        elif ch in brackets:                       # закрывающая
            if stack and stack[-1] == brackets[ch]:
                stack.pop()
            else:
                return False

    return len(stack) == 0


print(is_brackets_valid("([)]"))   # False
print(is_brackets_valid("({[]})")) # True
```

---

# Домашнее задание (решения)

## 1) Реверс словаря (значения повторяются → список ключей)
Дано:
```py
data = {"a": 1, "b": 2, "c": 1, "d": 3}
```

Решение:
```py
data = {"a": 1, "b": 2, "c": 1, "d": 3}

rev = {}
for k, v in data.items():
    rev.setdefault(v, []).append(k)

print(rev)  # {1: ['a', 'c'], 2: ['b'], 3: ['d']}
```

---

## 2) Счётчик букв в словах (слово → {буква: количество})
Дано:
```py
words = ["anna", "bennet", "john"]
```

Решение:
```py
words = ["anna", "bennet", "john"]

result = {}
for w in words:
    counts = {}
    for ch in w:
        counts[ch] = counts.get(ch, 0) + 1
    result[w] = counts

print(result)
# {'anna': {'a': 2, 'n': 2}, 'bennet': {'b': 1, 'e': 2, 'n': 2, 't': 1}, 'john': {'j': 1, 'o': 1, 'h': 1, 'n': 1}}
```

---

## 3) Распределение студентов по группам (вложенный словарь)
Условия:
- "Отличники": >= 85
- "Хорошисты": 70–84
- "Троечники": 50–69
- "Не сдали": < 50

Дано:
```py
students = {"Аня": 92, "Боря": 76, "Ваня": 65, "Галя": 48, "Дима": 88, "Ева": 54}
groups = ["Отличники", "Хорошисты", "Троечники", "Не сдали"]
```

Решение:
```py
students = {"Аня": 92, "Боря": 76, "Ваня": 65, "Галя": 48, "Дима": 88, "Ева": 54}
result = {"Отличники": {}, "Хорошисты": {}, "Троечники": {}, "Не сдали": {}}

for name, score in students.items():
    if score >= 85:
        result["Отличники"][name] = score
    elif score >= 70:
        result["Хорошисты"][name] = score
    elif score >= 50:
        result["Троечники"][name] = score
    else:
        result["Не сдали"][name] = score

print(result)
```

---

## Мини-шпаргалка
```text
fromkeys(keys, value) -> один value на все ключи (осторожно со списками!)

get(key, default=None) -> безопасно: нет KeyError
setdefault(key, default=None) -> если нет ключа, добавит его и вернёт default

keys/values/items -> view-объекты (живые представления)
list(d.keys()) -> “снимок”

copy()     -> shallow copy (вложенные объекты общие)
deepcopy() -> deep copy (вложенные объекты независимы)

dict comprehension:
{k: v for k, v in something}
```
