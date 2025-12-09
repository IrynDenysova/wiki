# Словари dict frozenset comprehension

## 📖 Быстрая навигация по операторам и функциям

- [[#1) Set comprehension (создание множества через выражение)]](#1-set-comprehension-создание-множества-через-выражение)
- [[#2) `frozenset` — неизменяемое множество]](#2-frozenset-—-неизменяемое-множество)
- [[#3) Словарь (`dict`) — что это]](#3-словарь-dict-—-что-это)
- [[#4) Создание словаря]](#4-создание-словаря)
- [[#5) Хеширование и “ловушка” `1`, `1.0`, `True`]](#5-хеширование-и-“ловушка”-1-10-true)
- [[#6) Доступ к значениям по ключу]](#6-доступ-к-значениям-по-ключу)
- [[#7) Оператор `in` для словаря]](#7-оператор-in-для-словаря)
- [[#8) Цикл по словарю]](#8-цикл-по-словарю)
- [[#9) Добавление и обновление данных]](#9-добавление-и-обновление-данных)
- [[#10) Удаление данных]](#10-удаление-данных)
- [[#11) Преобразование в словарь: `dict(...)`]](#11-преобразование-в-словарь-dict)
- [[#12) Ответы на задания из урока (квиз)]](#12-ответы-на-задания-из-урока-квиз)
- [[#13) Практика (решения)]](#13-практика-решения)
- [[#14) Домашнее задание (решения)]](#14-домашнее-задание-решения)
- [[#15) Мини-шпаргалка]](#15-мини-шпаргалка)
- [[#Дополнительная информация]](#дополнительная-информация)


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


---

## Дополнительная информация

### Важные концепции для изучения

#### 1. Dictionary comprehensions - создание словарей
```python
# Базовый синтаксис: {key: value for item in iterable}
squares = {x: x**2 for x in range(1, 6)}
print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# С условием
even_squares = {x: x**2 for x in range(1, 11) if x % 2 == 0}
print(even_squares)  # {2: 4, 4: 16, 6: 36, 8: 64, 10: 100}

# Инвертирование словаря
original = {'a': 1, 'b': 2, 'c': 3}
inverted = {v: k for k, v in original.items()}
print(inverted)  # {1: 'a', 2: 'b', 3: 'c'}

# Из двух списков
keys = ['name', 'age', 'city']
values = ['Алиса', 30, 'Москва']
person = {k: v for k, v in zip(keys, values)}
print(person)  # {'name': 'Алиса', 'age': 30, 'city': 'Москва'}

# Фильтрация словаря
data = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
filtered = {k: v for k, v in data.items() if v > 2}
print(filtered)  # {'c': 3, 'd': 4}

# Вложенные comprehensions
matrix = [[1, 2], [3, 4], [5, 6]]
flat_dict = {i: value for i, row in enumerate(matrix) for value in row}
print(flat_dict)  # {0: 1, 0: 2, 1: 3, 1: 4, 2: 5, 2: 6}
```

#### 2. Методы dict для объединения и обновления
```python
# dict.update() - обновление существующего словаря
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}
d1.update(d2)
print(d1)  # {'a': 1, 'b': 3, 'c': 4} - 'b' перезаписан

# Оператор | (Python 3.9+) - создает новый словарь
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}
d3 = d1 | d2
print(d3)  # {'a': 1, 'b': 3, 'c': 4}
print(d1)  # {'a': 1, 'b': 2} - не изменился

# Оператор |= (Python 3.9+) - обновляет на месте
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}
d1 |= d2
print(d1)  # {'a': 1, 'b': 3, 'c': 4}

# Объединение нескольких словарей
dicts = [{'a': 1}, {'b': 2}, {'c': 3}]
merged = {}
for d in dicts:
    merged.update(d)
print(merged)  # {'a': 1, 'b': 2, 'c': 3}

# Или с помощью **
merged = {**{'a': 1}, **{'b': 2}, **{'c': 3}}
print(merged)  # {'a': 1, 'b': 2, 'c': 3}
```

#### 3. Вложенные словари и структуры данных
```python
# Вложенные словари
users = {
    'user1': {
        'name': 'Алиса',
        'age': 30,
        'skills': ['Python', 'SQL']
    },
    'user2': {
        'name': 'Боб',
        'age': 25,
        'skills': ['Java', 'C++']
    }
}

# Доступ к вложенным данным
print(users['user1']['name'])  # Алиса
print(users['user2']['skills'][0])  # Java

# Безопасный доступ с get()
print(users.get('user3', {}).get('name', 'Неизвестно'))  # Неизвестно

# Изменение вложенных данных
users['user1']['age'] = 31
users['user1']['skills'].append('JavaScript')

# Создание вложенной структуры
from collections import defaultdict

# Граф смежности
graph = defaultdict(dict)
graph['A']['B'] = 5
graph['A']['C'] = 3
graph['B']['C'] = 2
print(dict(graph))  # {'A': {'B': 5, 'C': 3}, 'B': {'C': 2}}

# Многоуровневый defaultdict
def nested_dict():
    return defaultdict(nested_dict)

tree = nested_dict()
tree['level1']['level2']['level3'] = 'value'
print(dict(tree))  # {'level1': {'level2': {'level3': 'value'}}}
```

#### 4. Словари как конфигурация и маппинг
```python
# Словарь для замены if-elif
def get_discount(customer_type):
    discounts = {
        'regular': 0.05,
        'premium': 0.10,
        'vip': 0.20
    }
    return discounts.get(customer_type, 0)

print(get_discount('vip'))  # 0.2
print(get_discount('unknown'))  # 0

# Словарь функций (dispatch table)
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b): return a / b if b != 0 else None

operations = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide
}

result = operations['*'](5, 3)
print(result)  # 15

# Конфигурация приложения
config = {
    'database': {
        'host': 'localhost',
        'port': 5432,
        'name': 'mydb'
    },
    'api': {
        'timeout': 30,
        'retries': 3
    },
    'features': {
        'debug': True,
        'cache': False
    }
}

# Получение значений конфигурации
def get_config(path, default=None):
    """Получить значение по пути 'section.key'"""
    keys = path.split('.')
    value = config
    for key in keys:
        value = value.get(key, {})
        if not value:
            return default
    return value

print(get_config('database.host'))  # localhost
print(get_config('api.timeout'))    # 30
print(get_config('unknown.key', 'default'))  # default
```

### 💡 Практические примеры

#### Пример 1: Группировка данных
```python
def group_by(items, key_func):
    """Группирует элементы по результату key_func"""
    groups = {}
    for item in items:
        key = key_func(item)
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    return groups

# Группировка слов по длине
words = ['apple', 'banana', 'cat', 'dog', 'elephant', 'ant']
by_length = group_by(words, len)
print(by_length)
# {5: ['apple'], 6: ['banana'], 3: ['cat', 'dog', 'ant'], 8: ['elephant']}

# Группировка чисел: четные/нечетные
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
by_parity = group_by(numbers, lambda x: 'even' if x % 2 == 0 else 'odd')
print(by_parity)
# {'odd': [1, 3, 5, 7, 9], 'even': [2, 4, 6, 8]}

# Или с помощью defaultdict
from collections import defaultdict

def group_by_v2(items, key_func):
    groups = defaultdict(list)
    for item in items:
        groups[key_func(item)].append(item)
    return dict(groups)

# Группировка студентов по оценке
students = [
    {'name': 'Алиса', 'grade': 'A'},
    {'name': 'Боб', 'grade': 'B'},
    {'name': 'Виктор', 'grade': 'A'},
    {'name': 'Дарья', 'grade': 'C'}
]
by_grade = group_by_v2(students, lambda s: s['grade'])
for grade, group in by_grade.items():
    names = [s['name'] for s in group]
    print(f"{grade}: {', '.join(names)}")
```

#### Пример 2: Подсчет частоты элементов
```python
def count_frequency(items):
    """Подсчитывает частоту каждого элемента"""
    freq = {}
    for item in items:
        freq[item] = freq.get(item, 0) + 1
    return freq

# Частота букв
text = "hello world"
letter_freq = count_frequency(text.replace(' ', ''))
print(letter_freq)
# {'h': 1, 'e': 1, 'l': 3, 'o': 2, 'w': 1, 'r': 1, 'd': 1}

# Топ-3 самых частых букв
sorted_freq = sorted(letter_freq.items(), key=lambda x: x[1], reverse=True)
print(sorted_freq[:3])  # [('l', 3), ('o', 2), ('h', 1)]

# Или с Counter (более эффективно)
from collections import Counter

counter = Counter("hello world".replace(' ', ''))
print(counter.most_common(3))  # [('l', 3), ('o', 2), ('h', 1)]

# Подсчет слов в тексте
text = "Python is great Python is powerful Python is easy"
word_count = Counter(text.lower().split())
print(word_count)
# Counter({'python': 3, 'is': 3, 'great': 1, 'powerful': 1, 'easy': 1})
```

#### Пример 3: Кэширование результатов функции
```python
class Memoize:
    """Декоратор для кэширования результатов функции"""
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]

@Memoize
def fibonacci(n):
    """Вычисляет n-ое число Фибоначчи"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Быстрое вычисление благодаря кэшированию
print(fibonacci(100))  # Моментально!

# Или используем functools.lru_cache
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(x, y):
    """Имитация долгой операции"""
    import time
    time.sleep(0.1)
    return x ** y

# Первый вызов - медленный
import time
start = time.time()
result = expensive_function(2, 10)
print(f"Первый вызов: {time.time() - start:.3f} сек")

# Второй вызов - из кэша
start = time.time()
result = expensive_function(2, 10)
print(f"Второй вызов: {time.time() - start:.6f} сек")

# Информация о кэше
print(expensive_function.cache_info())
```

#### Пример 4: Инвентарь и управление товарами
```python
class Inventory:
    """Управление инвентарем товаров"""
    def __init__(self):
        self.items = {}  # {item_id: {'name': str, 'quantity': int, 'price': float}}
    
    def add_item(self, item_id, name, quantity, price):
        """Добавляет товар или обновляет количество"""
        if item_id in self.items:
            self.items[item_id]['quantity'] += quantity
        else:
            self.items[item_id] = {
                'name': name,
                'quantity': quantity,
                'price': price
            }
    
    def remove_item(self, item_id, quantity):
        """Удаляет указанное количество товара"""
        if item_id not in self.items:
            return False
        
        if self.items[item_id]['quantity'] >= quantity:
            self.items[item_id]['quantity'] -= quantity
            if self.items[item_id]['quantity'] == 0:
                del self.items[item_id]
            return True
        return False
    
    def get_total_value(self):
        """Вычисляет общую стоимость инвентаря"""
        return sum(item['quantity'] * item['price'] 
                  for item in self.items.values())
    
    def low_stock_items(self, threshold=5):
        """Возвращает товары с низким запасом"""
        return {item_id: item for item_id, item in self.items.items()
                if item['quantity'] < threshold}
    
    def get_report(self):
        """Генерирует отчет по инвентарю"""
        total_items = len(self.items)
        total_quantity = sum(item['quantity'] for item in self.items.values())
        total_value = self.get_total_value()
        
        return {
            'total_items': total_items,
            'total_quantity': total_quantity,
            'total_value': total_value,
            'items': self.items.copy()
        }

# Использование
inv = Inventory()
inv.add_item('A001', 'Ноутбук', 10, 50000)
inv.add_item('A002', 'Мышь', 50, 500)
inv.add_item('A003', 'Клавиатура', 3, 1500)

print(f"Общая стоимость: {inv.get_total_value()} руб.")
print(f"Товары с низким запасом: {inv.low_stock_items()}")

report = inv.get_report()
print(f"Всего товаров: {report['total_items']}")
```

### 🚨 Частые ошибки

**Ошибка 1: Изменяемые значения по умолчанию**
```python
# ❌ НЕПРАВИЛЬНО - общий словарь для всех вызовов!
def add_item(item, inventory={}):
    inventory[item] = inventory.get(item, 0) + 1
    return inventory

print(add_item('apple'))  # {'apple': 1}
print(add_item('banana'))  # {'apple': 1, 'banana': 1} - ошибка!

# ✅ ПРАВИЛЬНО - используем None
def add_item(item, inventory=None):
    if inventory is None:
        inventory = {}
    inventory[item] = inventory.get(item, 0) + 1
    return inventory

print(add_item('apple'))  # {'apple': 1}
print(add_item('banana'))  # {'banana': 1} - корректно!
```

**Ошибка 2: Изменение словаря во время итерации**
```python
# ❌ НЕПРАВИЛЬНО - RuntimeError
d = {'a': 1, 'b': 2, 'c': 3}
# for key in d:
#     if d[key] > 1:
#         del d[key]  # RuntimeError!

# ✅ ПРАВИЛЬНО - итерация по копии ключей
d = {'a': 1, 'b': 2, 'c': 3}
for key in list(d.keys()):
    if d[key] > 1:
        del d[key]
print(d)  # {'a': 1}

# ✅ ИЛИ создать новый словарь
d = {'a': 1, 'b': 2, 'c': 3}
d = {k: v for k, v in d.items() if v <= 1}
print(d)  # {'a': 1}
```

**Ошибка 3: Потеря данных при инвертировании**
```python
# ❌ ПРОБЛЕМА - дублирующиеся значения теряются
original = {'a': 1, 'b': 2, 'c': 1}
inverted = {v: k for k, v in original.items()}
print(inverted)  # {1: 'c', 2: 'b'} - 'a' потерян!

# ✅ ПРАВИЛЬНО - сохраняем все ключи
from collections import defaultdict

inverted = defaultdict(list)
for k, v in original.items():
    inverted[v].append(k)
print(dict(inverted))  # {1: ['a', 'c'], 2: ['b']}
```

**Ошибка 4: Копирование вложенных словарей**
```python
# ❌ ПРОБЛЕМА - shallow copy не копирует вложенные структуры
original = {'a': [1, 2, 3], 'b': [4, 5, 6]}
copied = original.copy()
copied['a'].append(4)
print(original)  # {'a': [1, 2, 3, 4], 'b': [4, 5, 6]} - изменился!

# ✅ ПРАВИЛЬНО - используем deepcopy
import copy

original = {'a': [1, 2, 3], 'b': [4, 5, 6]}
copied = copy.deepcopy(original)
copied['a'].append(4)
print(original)  # {'a': [1, 2, 3], 'b': [4, 5, 6]} - не изменился
print(copied)    # {'a': [1, 2, 3, 4], 'b': [4, 5, 6]}
```

### 📌 Полезные ресурсы
- [Документация: dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
- [Документация: collections](https://docs.python.org/3/library/collections.html)
- [Dictionary Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
- [PEP 584 - Dictionary Merge Operators](https://peps.python.org/pep-0584/)
- [functools.lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache)
