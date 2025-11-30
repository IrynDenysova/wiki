# Python Fundamentals — Урок 18: словари (`dict`) + `frozenset`, set comprehension, преобразование в словарь, оператор `in`

## 1) Set comprehension (создание множества через выражение)
Это как list comprehension, но с `{}`.

**Синтаксис:**
```py
new_set = {expression for item in iterable}
```

**Примеры:**
```py
numbers = [1, 2, 2, 4, 7, 8, 8, 10]
even_numbers_set = {n for n in numbers if n % 2 == 0}
print(even_numbers_set)  # {2, 4, 8, 10} (порядок не гарантирован)

words = ["apple", "banana", "cherry", "apple"]
unique_lengths = {len(w) for w in words}
print(unique_lengths)    # {5, 6}
```

---

## 2) `frozenset` — неизменяемое множество
`frozenset` — **immutable** аналог `set`: после создания нельзя добавить/удалить элементы.

**Создание:**
```py
immutable_set = frozenset([1, 2, 3, 4, 5])
immutable_from_range = frozenset(range(10))
print(immutable_set)
print(immutable_from_range)
```

### 2.1 Почему это полезно
`frozenset` **хешируемый**, поэтому:
- может быть **элементом** другого множества
- может быть **ключом** словаря

```py
f1 = frozenset([1, 2, 3])
f2 = frozenset([4, 5, 6])
set_of_frozensets = {f1, f2}
print(set_of_frozensets)
```

### 2.2 set vs frozenset (главное отличие)
- `set` — изменяемый (`add/remove/discard/pop/clear`)
- `frozenset` — неизменяемый (методов изменения нет), но операции типа `union` возвращают **новый** объект

---

## 3) Словарь (`dict`) — что это
**Словарь** — изменяемая коллекция пар **ключ → значение**.

Главное:
- ключи **уникальные** и **хешируемые** (обычно: `str`, `int`, `float`, `bool`, `tuple`, `frozenset`)
- значения могут быть любыми (в т.ч. списки/множества/словари)
- начиная с Python 3.7 словарь сохраняет **порядок вставки** элементов

---

## 4) Создание словаря
```py
person = {"name": "Alice", "age": 30, "city": "New York"}
print(person)

empty1 = {}
empty2 = dict()
print(empty1, empty2)
```

---

## 5) Хеширование и “ловушка” `1`, `1.0`, `True`
В Python:
- `1 == 1.0 == True`
- и у них одинаковые `hash(...)`

Поэтому **они считаются одним и тем же ключом**:
```py
my_dict = {1: "one", 1.0: "float one", True: "boolean one"}
print(my_dict)  # {1: 'boolean one'}  (значение перезапишется последним)
```

---

## 6) Доступ к значениям по ключу
```py
my_dict = {"name": "Alice", "age": 30}
print(my_dict["name"])  # Alice

# Если ключа нет — будет KeyError:
# print(my_dict["city"])
```

---

## 7) Оператор `in` для словаря
`in` проверяет **наличие ключа** (не значения).

```py
my_dict = {"name": "Alice", "age": 30}

if "name" in my_dict:
    print(my_dict["name"])

if "city" in my_dict:
    print(my_dict["city"])  # не выполнится
```

---

## 8) Цикл по словарю
По умолчанию `for` перебирает **ключи**:
```py
my_dict = {"name": "Alice", "age": 30, "city": "New York"}
for key in my_dict:
    print(f"Ключ={key}, значение={my_dict[key]}")
```

---

## 9) Добавление и обновление данных
### 9.1 Через присваивание по ключу
```py
my_dict = {"name": "Alice", "age": 30}
my_dict["city"] = "New York"  # добавить
my_dict["age"] = 31           # обновить
print(my_dict)
```

### 9.2 `update()`
Можно передавать:
- другой словарь
- список/кортеж пар `(key, value)`
- именованные аргументы

```py
my_dict = {"name": "Alice", "age": 30}

my_dict.update({"age": 32, "country": "USA"})
my_dict.update([("name", "Bob"), ("email", "bob@example.com")])
my_dict.update(city="New York", orders=[])

print(my_dict)
```

---

## 10) Удаление данных
### 10.1 `del` (ошибка, если ключа нет)
```py
my_dict = {"name": "Alice", "age": 30, "city": "New York"}
del my_dict["age"]
print(my_dict)

# del my_dict["email"]  # KeyError
```

### 10.2 `clear()` — очистить словарь
```py
my_dict = {"name": "Alice", "age": 30}
my_dict.clear()
print(my_dict)  # {}
```

### 10.3 `pop(key[, default])` — удалить и вернуть значение
```py
my_dict = {"name": "Alice", "age": 30}
age = my_dict.pop("age")
print(age)      # 30
print(my_dict)  # {'name': 'Alice'}

# my_dict.pop("email")  # KeyError (если default не указан)
```

### 10.4 `popitem()` — удалить и вернуть последнюю добавленную пару
```py
my_dict = {"name": "Alice", "age": 30}
last_item = my_dict.popitem()
print(last_item)  # ('age', 30)  (для Python 3.7+)
print(my_dict)
```

---

## 11) Преобразование в словарь: `dict(...)`
### 11.1 Через именованные аргументы
```py
person = dict(name="Bob", age=25, city="London")
print(person)
```

### 11.2 Из последовательности пар
Каждый элемент должен быть парой из **двух** значений: `(key, value)`.

```py
pairs = [("name", "Charlie"), ("age", 35), ("city", "Paris")]
person = dict(pairs)
print(person)
```

Можно смешивать кортежи и списки-пары:
```py
pairs = [("name", "Charlie"), ["age", 35], ["city", "Paris"]]
print(dict(pairs))
```

⚠️ Ошибки:
- если где-то не 2 элемента → `ValueError`
- если ключ не хешируемый → `TypeError`

---

## 12) Ответы на задания из урока (квиз)
1) `unique_lengths = {len(word) for word in words}` → **`{5, 6}`**  
2) `frozenset` верно: **неизменяемый** и **хешируемый**, методов `add/remove` нет  
3) `immutable_set.union({4, 5})` возвращает **`frozenset({1, 2, 3, 4, 5})`**  
4) Ключами словаря могут быть: **int, bool, float, tuple, frozenset** (а `list/set/dict` — нельзя)  
5) `{1: "one", 1.0: "...", True: "..."}` → **`{1: 'boolean one'}`**  
6) `dict(pairs)` с повтором `("name", ...)` → возьмёт **последнее**: `"Bob"`  
7) `not_pairs` с `["city", "Paris", "Berlin"]` → **ошибка** (элемент длиной 3)  
8) `update({"city": "...", "age": 35})` → `age` станет **35**, ключ не дублируется  
9) `del my_dict["age"]` → останется `{"name": "Alice"}`  
10) `my_dict.pop("age")` → вернёт **30**

---

## 13) Практика (решения)

### 13.1 Инверсия словаря (ключи ↔ значения)
```py
original_dict = {"a": 1, "b": 2, "c": 3}

inverted_dict = {}
for key in original_dict:
    inverted_dict[original_dict[key]] = key

print("Инверсированный словарь:", inverted_dict)
# {1: 'a', 2: 'b', 3: 'c'}
```

### 13.2 Замена чисел на слова по словарю сопоставлений
```py
number_to_word = {1: "один", 2: "два", 3: "три"}
data = {"x": 1, "y": 2, "z": 3}

for key in data:
    if data[key] in number_to_word:
        data[key] = number_to_word[data[key]]

print(data)
# {'x': 'один', 'y': 'два', 'z': 'три'}
```

---

## 14) Домашнее задание (решения)

### 14.1 Не уникальные числа (повторяются > 1 раза) + по убыванию
Дано:
```py
numbers = [4, 7, 3, 7, 8, 3, 4, 2, 7, 3, 8, 4]
```

Решение (через словарь частот):
```py
numbers = [4, 7, 3, 7, 8, 3, 4, 2, 7, 3, 8, 4]

freq = {}
for x in numbers:
    freq[x] = freq.get(x, 0) + 1

result = [x for x, c in freq.items() if c > 1]
result.sort(reverse=True)

print("Числа, встречающиеся более одного раза:", result)
# [8, 7, 4, 3] (в примере — [7, 4, 3, 8], но по условию нужно убывание)
```

---

### 14.2 Проверка: один словарь — подмножество другого (по парам key-value)
Дано:
```py
dict1 = {"a": 1, "b": 2}
dict2 = {"a": 1, "b": 2, "c": 3}
```

Решение:
```py
dict1 = {"a": 1, "b": 2}
dict2 = {"a": 1, "b": 2, "c": 3}

is_subset = True
for k, v in dict1.items():
    if k not in dict2 or dict2[k] != v:
        is_subset = False
        break

if is_subset:
    print("Первый словарь является подмножеством второго.")
else:
    print("Первый словарь НЕ является подмножеством второго.")
```

---

## 15) Мини-шпаргалка
```text
dict:
d = {"k": "v"} / d = dict(...)
ключи: уникальные + хешируемые (str/int/float/bool/tuple/frozenset)
значения: любые

доступ:
d[key] -> KeyError если ключа нет
key in d -> проверка ключа

обход:
for k in d: ...
for k, v in d.items(): ...

добавить/обновить:
d[key] = value
d.update({...}) / d.update([("k","v")]) / d.update(k=v)

удалить:
del d[key] -> KeyError если нет
d.pop(key[, default]) -> вернуть значение
d.popitem() -> вернуть последнюю пару (Py3.7+)
d.clear()

ловушка:
1, 1.0, True — считаются одним и тем же ключом
```
