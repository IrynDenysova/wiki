# Словари fromkeys get keys values items

## 📖 Быстрая навигация по операторам и функциям

- [[#0) План урока]](#0-план-урока)
- [[#1) `dict.fromkeys(iterable, value=None)`]](#1-dictfromkeysiterable-valuenone)
- [[#2) `dict.get(key, default=None)`]](#2-dictgetkey-defaultnone)
- [[#3) `dict.setdefault(key, default=None)`]](#3-dictsetdefaultkey-defaultnone)
- [[#4) `keys()`, `values()`, `items()` = view-объекты]](#4-keys-values-items-view-объекты)
- [[#5) Итерация по словарю]](#5-итерация-по-словарю)
- [[#6) Словари со вложенными структурами (nested dict)]](#6-словари-со-вложенными-структурами-nested-dict)
- [[#7) Копирование словарей: `copy()` vs `deepcopy()`]](#7-копирование-словарей-copy-vs-deepcopy)
- [[#8) Dict comprehension]](#8-dict-comprehension)
- [[#9) Сравнение словарей]](#9-сравнение-словарей)
- [[#A) Переводчик EN ⇄ RU (по словарю)]](#a-переводчик-en-⇄-ru-по-словарю)
- [[#B) Проверка правильности скобок (словарь + стек)]](#b-проверка-правильности-скобок-словарь-стек)
- [[#1) Реверс словаря (значения повторяются → список ключей)]](#1-реверс-словаря-значения-повторяются-→-список-ключей)
- [[#2) Счётчик букв в словах (слово → {буква: количество})]](#2-счётчик-букв-в-словах-слово-→-буква-количество)
- [[#3) Распределение студентов по группам (вложенный словарь)]](#3-распределение-студентов-по-группам-вложенный-словарь)
- [[#Мини-шпаргалка]](#мини-шпаргалка)
- [[#Дополнительная информация]](#дополнительная-информация)


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


---

## Дополнительная информация

### Важные концепции для изучения

#### 1. dict.fromkeys() - создание словарей с одинаковыми значениями
```python
# Синтаксис: dict.fromkeys(keys, value=None)

# Базовое использование
keys = ['a', 'b', 'c']
d = dict.fromkeys(keys)
print(d)  # {'a': None, 'b': None, 'c': None}

# С начальным значением
d = dict.fromkeys(keys, 0)
print(d)  # {'a': 0, 'b': 0, 'c': 0}

# Создание счетчика для слов
words = ['apple', 'banana', 'apple', 'cherry']
word_count = dict.fromkeys(set(words), 0)
for word in words:
    word_count[word] += 1
print(word_count)  # {'apple': 2, 'banana': 1, 'cherry': 1}

# ВНИМАНИЕ: Изменяемые объекты как значения
# ❌ НЕПРАВИЛЬНО
d = dict.fromkeys(['a', 'b', 'c'], [])
d['a'].append(1)
print(d)  # {'a': [1], 'b': [1], 'c': [1]} - все ссылаются на один список!

# ✅ ПРАВИЛЬНО - используем comprehension
d = {k: [] for k in ['a', 'b', 'c']}
d['a'].append(1)
print(d)  # {'a': [1], 'b': [], 'c': []}
```

#### 2. Методы поиска и доступа: get(), pop(), setdefault()
```python
# dict.get(key, default=None)
# Безопасное получение значения
d = {'a': 1, 'b': 2}
print(d.get('a'))          # 1
print(d.get('c'))          # None
print(d.get('c', 'absent')) # absent

# Часто используется для конфигурации
config = {'timeout': 30}
timeout = config.get('timeout', 60)  # 30
retries = config.get('retries', 3)   # 3

# dict.pop(key, default=None)
# Удаляет и возвращает значение
d = {'a': 1, 'b': 2, 'c': 3}
value = d.pop('b')
print(value)  # 2
print(d)      # {'a': 1, 'c': 3}

# С значением по умолчанию
value = d.pop('z', 'not found')
print(value)  # not found
print(d)      # {'a': 1, 'c': 3} - не изменился

# dict.setdefault(key, default=None)
# Возвращает значение, если есть, иначе устанавливает и возвращает default
d = {'a': 1}
result = d.setdefault('a', 0)
print(result)  # 1
print(d)       # {'a': 1} - не изменился

result = d.setdefault('b', 0)
print(result)  # 0
print(d)       # {'a': 1, 'b': 0} - добавился новый ключ

# Полезно для инициализации вложенных структур
data = {}
data.setdefault('users', []).append('Алиса')
data.setdefault('users', []).append('Боб')
print(data)  # {'users': ['Алиса', 'Боб']}
```

#### 3. Проверка наличия ключей и значений
```python
# Проверка ключей
d = {'a': 1, 'b': 2, 'c': 3}
print('a' in d)      # True - проверка по ключам (быстро, O(1))
print('x' in d)      # False
print('x' not in d)  # True

# Проверка значений (медленнее, O(n))
print(1 in d.values())  # True
print(5 in d.values())  # False

# Проверка пар
print(('a', 1) in d.items())  # True
print(('a', 2) in d.items())  # False

# Практический пример: валидация данных
def validate_user(user_dict):
    required_fields = ['name', 'email', 'age']
    missing = [field for field in required_fields if field not in user_dict]
    
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    return True, "Valid"

user1 = {'name': 'Алиса', 'email': 'alice@example.com', 'age': 30}
user2 = {'name': 'Боб', 'email': 'bob@example.com'}

print(validate_user(user1))  # (True, 'Valid')
print(validate_user(user2))  # (False, 'Missing fields: age')
```

#### 4. Перебор словаря: keys(), values(), items()
```python
d = {'a': 1, 'b': 2, 'c': 3}

# keys() - возвращает представление ключей (не список!)
keys = d.keys()
print(list(keys))  # ['a', 'b', 'c']
print(type(keys))  # <class 'dict_keys'>

# values() - возвращает представление значений
values = d.values()
print(list(values))  # [1, 2, 3]

# items() - возвращает представление пар (ключ, значение)
items = d.items()
print(list(items))  # [('a', 1), ('b', 2), ('c', 3)]

# Итерация по элементам (наиболее эффективно)
for key in d:
    print(f"{key}: {d[key]}")

# То же самое
for key, value in d.items():
    print(f"{key}: {value}")

# Слияние двух словарей в один список
d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}
merged = list(d1.items()) + list(d2.items())
print(merged)  # [('a', 1), ('b', 2), ('c', 3), ('d', 4)]

# Сортировка словаря по ключам или значениям
d = {'z': 3, 'a': 1, 'b': 2}
sorted_by_key = dict(sorted(d.items()))
print(sorted_by_key)  # {'a': 1, 'b': 2, 'z': 3}

sorted_by_value = dict(sorted(d.items(), key=lambda x: x[1]))
print(sorted_by_value)  # {'a': 1, 'b': 2, 'z': 3}

# Сортировка в обратном порядке
sorted_desc = dict(sorted(d.items(), reverse=True))
print(sorted_desc)  # {'z': 3, 'b': 2, 'a': 1}
```

### 💡 Практические примеры

#### Пример 1: Создание индекса для быстрого поиска
```python
class DataIndex:
    """Индекс для быстрого поиска по значениям"""
    def __init__(self):
        self.index = {}
    
    def add_record(self, id, name, email, age):
        """Добавляет запись"""
        record = {'name': name, 'email': email, 'age': age}
        self.index[id] = record
    
    def find_by_email(self, email):
        """Находит запись по email"""
        for id, record in self.index.items():
            if record['email'] == email:
                return id, record
        return None, None
    
    def find_by_name(self, name):
        """Находит все записи с именем"""
        results = {}
        for id, record in self.index.items():
            if record['name'] == name:
                results[id] = record
        return results
    
    def find_by_age_range(self, min_age, max_age):
        """Находит записи в диапазоне возраста"""
        results = {}
        for id, record in self.index.items():
            if min_age <= record['age'] <= max_age:
                results[id] = record
        return results

# Использование
index = DataIndex()
index.add_record('001', 'Алиса', 'alice@example.com', 30)
index.add_record('002', 'Боб', 'bob@example.com', 25)
index.add_record('003', 'Виктор', 'victor@example.com', 30)

print(index.find_by_email('alice@example.com'))
# ('001', {'name': 'Алиса', 'email': 'alice@example.com', 'age': 30})

print(index.find_by_age_range(25, 30))
# {'001': {...}, '002': {...}, '003': {...}}
```

#### Пример 2: Конфигурация с fallback значениями
```python
class Config:
    """Конфигурация с поддержкой наследования и defaults"""
    def __init__(self, default_config=None):
        self.config = default_config or {}
    
    def get(self, path, default=None):
        """Получить значение по пути 'section.key.subkey'"""
        keys = path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, path, value):
        """Установить значение по пути"""
        keys = path.split('.')
        current = self.config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def update(self, other):
        """Объединить с другой конфигурацией"""
        for key, value in other.items():
            if key in self.config and isinstance(self.config[key], dict):
                if isinstance(value, dict):
                    self.config[key].update(value)
                else:
                    self.config[key] = value
            else:
                self.config[key] = value

# Использование
defaults = {
    'app': {
        'name': 'MyApp',
        'version': '1.0',
        'debug': False
    },
    'db': {
        'host': 'localhost',
        'port': 5432,
        'timeout': 30
    }
}

config = Config(defaults)
print(config.get('app.name'))  # MyApp
print(config.get('db.port'))   # 5432
print(config.get('cache.ttl', 3600))  # 3600 (default)

# Переопределение
config.set('app.debug', True)
print(config.get('app.debug'))  # True
```

#### Пример 3: Группировка и агрегация данных
```python
def group_and_aggregate(items, group_key, aggregates):
    """
    Группирует элементы и вычисляет агрегаты
    
    group_key: функция для получения ключа группы
    aggregates: {имя: функция_агрегации}
    """
    groups = {}
    
    for item in items:
        key = group_key(item)
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    
    result = {}
    for key, group in groups.items():
        result[key] = {}
        for agg_name, agg_func in aggregates.items():
            result[key][agg_name] = agg_func(group)
    
    return result

# Пример: анализ продаж по регионам
sales = [
    {'region': 'North', 'amount': 1000},
    {'region': 'South', 'amount': 1500},
    {'region': 'North', 'amount': 800},
    {'region': 'South', 'amount': 900},
    {'region': 'East', 'amount': 1200},
]

aggregates = {
    'total': lambda group: sum(s['amount'] for s in group),
    'count': lambda group: len(group),
    'average': lambda group: sum(s['amount'] for s in group) / len(group),
    'max': lambda group: max(s['amount'] for s in group),
}

result = group_and_aggregate(sales, lambda x: x['region'], aggregates)

for region, stats in result.items():
    print(f"{region}: Total={stats['total']}, Count={stats['count']}, "
          f"Avg={stats['average']:.0f}, Max={stats['max']}")
```

#### Пример 4: Многоуровневая кэширование с TTL
```python
import time

class Cache:
    """Простой кэш с поддержкой TTL (Time To Live)"""
    def __init__(self):
        self.cache = {}  # {key: (value, expire_time)}
    
    def set(self, key, value, ttl=None):
        """Сохранить значение с опциональным TTL в секундах"""
        expire_time = time.time() + ttl if ttl else None
        self.cache[key] = (value, expire_time)
    
    def get(self, key, default=None):
        """Получить значение, если оно не устарело"""
        if key not in self.cache:
            return default
        
        value, expire_time = self.cache[key]
        
        if expire_time and time.time() > expire_time:
            del self.cache[key]
            return default
        
        return value
    
    def clear(self):
        """Очистить весь кэш"""
        self.cache.clear()
    
    def cleanup_expired(self):
        """Удалить истекшие значения"""
        current_time = time.time()
        expired = [k for k, (_, exp) in self.cache.items() 
                   if exp and current_time > exp]
        for k in expired:
            del self.cache[k]
        return len(expired)

# Использование
cache = Cache()
cache.set('user:1', {'name': 'Алиса'}, ttl=5)
cache.set('user:2', {'name': 'Боб'})  # Без TTL

print(cache.get('user:1'))  # {'name': 'Алиса'}
print(cache.get('user:2'))  # {'name': 'Боб'}
print(cache.get('user:3'))  # None

time.sleep(6)
print(cache.get('user:1'))  # None - истекло
print(cache.get('user:2'))  # {'name': 'Боб'} - остается
```

### 🚨 Частые ошибки

**Ошибка 1: Использование изменяемого значения в fromkeys()**
```python
# ❌ НЕПРАВИЛЬНО
d = dict.fromkeys(['a', 'b', 'c'], [])
d['a'].append(1)
print(d)  # {'a': [1], 'b': [1], 'c': [1]} - все связаны!

# ✅ ПРАВИЛЬНО
d = {k: [] for k in ['a', 'b', 'c']}
d['a'].append(1)
print(d)  # {'a': [1], 'b': [], 'c': []}
```

**Ошибка 2: KeyError вместо использования get()**
```python
# ❌ НЕПРАВИЛЬНО - может вызвать KeyError
d = {'a': 1}
value = d['b']  # KeyError: 'b'

# ✅ ПРАВИЛЬНО
d = {'a': 1}
value = d.get('b')  # None
value = d.get('b', 'default')  # 'default'
```

**Ошибка 3: Изменение словаря во время итерации**
```python
# ❌ НЕПРАВИЛЬНО - RuntimeError
d = {'a': 1, 'b': 2, 'c': 3}
# for key in d.keys():
#     if d[key] > 1:
#         del d[key]  # RuntimeError!

# ✅ ПРАВИЛЬНО - создать список ключей
d = {'a': 1, 'b': 2, 'c': 3}
for key in list(d.keys()):
    if d[key] > 1:
        del d[key]
```

**Ошибка 4: pop() без значения по умолчанию**
```python
# ❌ НЕПРАВИЛЬНО - KeyError если ключа нет
d = {'a': 1}
value = d.pop('b')  # KeyError: 'b'

# ✅ ПРАВИЛЬНО
d = {'a': 1}
value = d.pop('b', None)  # None
value = d.pop('b', 'not found')  # 'not found'
```

### 📌 Полезные ресурсы
- [Документация: dict методы](https://docs.python.org/3/library/stdtypes.html#dictionary-methods)
- [Документация: dict.get()](https://docs.python.org/3/library/stdtypes.html#dict.get)
- [Документация: dict.setdefault()](https://docs.python.org/3/library/stdtypes.html#dict.setdefault)
- [Документация: dict.pop()](https://docs.python.org/3/library/stdtypes.html#dict.pop)
- [Документация: dict.fromkeys()](https://docs.python.org/3/library/stdtypes.html#dict.fromkeys)
