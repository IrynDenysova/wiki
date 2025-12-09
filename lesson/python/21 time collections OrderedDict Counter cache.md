# time collections OrderedDict Counter cache

## 📖 Быстрая навигация по операторам и функциям

- [[#0) План занятия]](#0-план-занятия)
- [[#1) Модуль `time`]](#1-модуль-time)
- [[#2) Модуль `collections`]](#2-модуль-collections)
- [[#3) `OrderedDict`]](#3-ordereddict)
- [[#4) `OrderedDict.popitem(last=True)`]](#4-ordereddictpopitemlasttrue)
- [[#5) `OrderedDict.move_to_end(key, last=True)`]](#5-ordereddictmovetoendkey-lasttrue)
- [[#6) Кэш и LRU-кэш]](#6-кэш-и-lru-кэш)
- [[#7) `functools.lru_cache`]](#7-functoolslrucache)
- [[#8) `defaultdict`]](#8-defaultdict)
- [[#9) `Counter`]](#9-counter)
- [[#1) Частотный анализ слов (игнорировать регистр, убрать `.` и `,`)]](#1-частотный-анализ-слов-игнорировать-регистр-убрать-и)
- [[#2) Список студентов по факультетам (группировка)]](#2-список-студентов-по-факультетам-группировка)
- [[#ДЗ 1) Подсчёт букв в тексте (игнорировать регистр)]](#дз-1-подсчёт-букв-в-тексте-игнорировать-регистр)
- [[#ДЗ 2) Группировка студентов по классам]](#дз-2-группировка-студентов-по-классам)
- [[#Мини-шпаргалка]](#мини-шпаргалка)
- [[#Дополнительная информация]](#дополнительная-информация)


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

## Дополнительная информация

### Важные концепции для изучения

#### 1. Модуль time - работа со временем и производительностью
```python
import time

# time.time() - текущее время в секундах с эпохи Unix
current_time = time.time()
print(f"Секунды с 1970-01-01: {current_time}")

# time.sleep() - пауза на указанное время
print("Начало")
time.sleep(2)  # Пауза на 2 секунды
print("Конец (спустя 2 сек)")

# Измерение времени выполнения кода
start = time.time()

# Какой-то долгий процесс
for i in range(1000000):
    x = i ** 2

elapsed = time.time() - start
print(f"Время выполнения: {elapsed:.4f} сек")

# time.perf_counter() - более точное измерение (не зависит от системного времени)
start = time.perf_counter()
for i in range(1000000):
    x = i ** 2
elapsed = time.perf_counter() - start
print(f"Точное время: {elapsed:.6f} сек")

# Структурирование времени
import datetime
now = datetime.datetime.now()
print(f"Дата и время: {now}")
print(f"День: {now.day}, Месяц: {now.month}, Год: {now.year}")
print(f"Час: {now.hour}, Минута: {now.minute}")

# Форматирование времени
formatted = now.strftime("%d.%m.%Y %H:%M:%S")
print(f"Отформатировано: {formatted}")

# Разница времени
from datetime import timedelta
future = now + timedelta(days=5, hours=3)
difference = future - now
print(f"Разница: {difference.days} дней, {difference.seconds} секунд")
```

#### 2. collections.OrderedDict - словарь с сохранением порядка
```python
from collections import OrderedDict

# В Python 3.7+ обычные dict сохраняют порядок,
# но OrderedDict явно показывает это намерение

# Создание OrderedDict
od = OrderedDict()
od['z'] = 1
od['a'] = 2
od['m'] = 3

print(od)  # OrderedDict([('z', 1), ('a', 2), ('m', 3)])
print(list(od.items()))  # [('z', 1), ('a', 2), ('m', 3)] - порядок сохранен!

# Сравнение с обычным dict
regular_dict = {'z': 1, 'a': 2, 'm': 3}
print(dict(od) == regular_dict)  # True

# Методы, уникальные для OrderedDict
od = OrderedDict([('first', 1), ('second', 2), ('third', 3)])

# move_to_end() - переместить элемент в конец
od.move_to_end('first')
print(list(od.keys()))  # ['second', 'third', 'first']

# move_to_end(..., last=False) - переместить в начало
od.move_to_end('second', last=False)
print(list(od.keys()))  # ['second', 'third', 'first']

# popitem() - удалить последний элемент
last = od.popitem()
print(last)  # ('first', 3)
print(list(od.keys()))  # ['second', 'third']

# Практический пример: кэш с порядком доступа (LRU)
class LRUCache(OrderedDict):
    """LRU кэш с максимальным размером"""
    def __init__(self, size_limit):
        self.size_limit = size_limit
        super().__init__()
    
    def __getitem__(self, key):
        # При доступе переместить в конец
        self.move_to_end(key)
        return super().__getitem__(key)
    
    def __setitem__(self, key, value):
        if key in self:
            self.move_to_end(key)
        super().__setitem__(key, value)
        
        # Если превышен размер, удалить самый старый
        if len(self) > self.size_limit:
            oldest = next(iter(self))
            del self[oldest]

cache = LRUCache(3)
cache['a'] = 1
cache['b'] = 2
cache['c'] = 3
print(list(cache.keys()))  # ['a', 'b', 'c']

cache['a']  # Переместить 'a' в конец
print(list(cache.keys()))  # ['b', 'c', 'a']

cache['d'] = 4  # Превышен размер, удалить 'b'
print(list(cache.keys()))  # ['c', 'a', 'd']
```

#### 3. collections.Counter - подсчет частоты элементов
```python
from collections import Counter

# Создание Counter
words = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
counter = Counter(words)
print(counter)  # Counter({'apple': 3, 'banana': 2, 'cherry': 1})

# Доступ как словарь
print(counter['apple'])  # 3
print(counter['grape'])  # 0 - не вызывает KeyError!

# most_common() - самые частые элементы
print(counter.most_common(2))  # [('apple', 3), ('banana', 2)]

# Арифметические операции с Counter
c1 = Counter({'a': 2, 'b': 1})
c2 = Counter({'a': 1, 'c': 3})

print(c1 + c2)  # Counter({'a': 3, 'c': 3, 'b': 1}) - сумма
print(c1 - c2)  # Counter({'b': 1, 'a': 1}) - вычитание
print(c1 & c2)  # Counter({'a': 1}) - пересечение
print(c1 | c2)  # Counter({'a': 2, 'c': 3, 'b': 1}) - объединение

# Практический пример: анализ текста
text = "Python is great. Python is powerful. Python is easy to learn."
words = text.lower().split()

# Удалить пунктуацию
import string
words = [word.strip(string.punctuation) for word in words]

counter = Counter(words)

# Найти самые частые слова
print("Топ-5 слов:")
for word, count in counter.most_common(5):
    print(f"  {word}: {count}")

# Обновление счетчика
counter.update(['python', 'java', 'python'])
print(counter['python'])  # Увеличилось

# Удаление элементов с нулевым или отрицательным счетом
counter['deleted'] = 0
print(counter)  # 0 остается видимым
del counter['deleted']
print(counter)  # Удалено

# Получение всех элементов с их повторениями
print(list(counter.elements()))  # [слова повторены по count раз]
```

#### 4. Встроенное кэширование с functools
```python
from functools import lru_cache
import time

# lru_cache - кэширование результатов функции (Least Recently Used)

@lru_cache(maxsize=128)
def fibonacci(n):
    """Вычисляет n-ое число Фибоначчи с кэшированием"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Первый вызов - долгий
start = time.perf_counter()
result = fibonacci(35)
elapsed = time.perf_counter() - start
print(f"Результат: {result}, Время: {elapsed:.4f} сек")

# Второй вызов - из кэша - моментально
start = time.perf_counter()
result = fibonacci(35)
elapsed = time.perf_counter() - start
print(f"Результат: {result}, Время: {elapsed:.6f} сек")

# Информация о кэше
info = fibonacci.cache_info()
print(f"Попадания: {info.hits}, Промахи: {info.misses}, Размер: {info.currsize}")

# Очистка кэша
fibonacci.cache_clear()

# @lru_cache(maxsize=None) - неограниченный кэш
@lru_cache(maxsize=None)
def expensive_computation(x):
    time.sleep(0.1)
    return x ** 2

result = expensive_computation(5)
print(result)  # 25

# Python 3.9+: @cache - простой вариант без ограничений
try:
    from functools import cache
    
    @cache
    def simple_function(x):
        return x * 2
    
    print(simple_function(5))  # 10
except ImportError:
    print("@cache доступен в Python 3.9+")

# Кастомное кэширование с сохранением времени жизни (TTL)
import time
from functools import wraps

def timed_cache(ttl_seconds):
    """Декоратор для кэширования с TTL"""
    def decorator(func):
        cache = {}
        cache_times = {}
        
        @wraps(func)
        def wrapper(*args):
            current_time = time.time()
            
            # Проверить, есть ли в кэше и не истекло ли время
            if args in cache:
                cached_time = cache_times[args]
                if current_time - cached_time < ttl_seconds:
                    return cache[args]
            
            # Вычислить и кэшировать
            result = func(*args)
            cache[args] = result
            cache_times[args] = current_time
            return result
        
        return wrapper
    return decorator

@timed_cache(ttl_seconds=2)
def get_current_second():
    return time.time()

print(get_current_second())
time.sleep(0.5)
print(get_current_second())  # Из кэша - одно и то же

time.sleep(2)
print(get_current_second())  # Новое значение - кэш истек
```

### 💡 Практические примеры

#### Пример 1: Логирование и профилирование функции
```python
import time
from functools import wraps
from collections import Counter

class FunctionProfiler:
    """Профилирует вызовы функции"""
    def __init__(self):
        self.calls = Counter()
        self.times = {}
    
    def profile(self, func):
        """Декоратор для профилирования"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed = time.perf_counter() - start
                
                self.calls[func.__name__] += 1
                if func.__name__ not in self.times:
                    self.times[func.__name__] = []
                self.times[func.__name__].append(elapsed)
        
        return wrapper
    
    def report(self):
        """Печать отчета профилирования"""
        print("=== Отчет профилирования ===")
        for func_name, times in self.times.items():
            count = self.calls[func_name]
            total = sum(times)
            avg = total / count
            print(f"\n{func_name}:")
            print(f"  Вызовов: {count}")
            print(f"  Всего: {total:.6f} сек")
            print(f"  Среднее: {avg:.6f} сек")
            print(f"  Макс: {max(times):.6f} сек")

# Использование
profiler = FunctionProfiler()

@profiler.profile
def slow_operation(n):
    time.sleep(n)
    return n

slow_operation(0.1)
slow_operation(0.2)
slow_operation(0.15)

profiler.report()
```

#### Пример 2: Расписание задач с отслеживанием времени
```python
import time
from datetime import datetime, timedelta
from collections import OrderedDict

class TaskScheduler:
    """Планировщик задач с отслеживанием времени"""
    def __init__(self):
        self.tasks = OrderedDict()  # Сохраняет порядок добавления
    
    def schedule(self, task_name, interval_seconds, function, *args):
        """Планирует задачу на повторяющееся выполнение"""
        self.tasks[task_name] = {
            'function': function,
            'args': args,
            'interval': interval_seconds,
            'last_run': None,
            'run_count': 0
        }
    
    def run(self, max_iterations=None):
        """Запускает планировщик"""
        iteration = 0
        
        while True:
            current_time = time.time()
            any_task_ran = False
            
            for task_name, task in self.tasks.items():
                should_run = (
                    task['last_run'] is None or
                    current_time - task['last_run'] >= task['interval']
                )
                
                if should_run:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                          f"Выполняю: {task_name}")
                    
                    try:
                        task['function'](*task['args'])
                    except Exception as e:
                        print(f"  Ошибка: {e}")
                    
                    task['last_run'] = current_time
                    task['run_count'] += 1
                    any_task_ran = True
            
            if not any_task_ran:
                time.sleep(0.1)
            
            iteration += 1
            if max_iterations and iteration >= max_iterations:
                break
    
    def report(self):
        """Отчет о выполнении задач"""
        print("\n=== Отчет задач ===")
        for task_name, task in self.tasks.items():
            print(f"{task_name}: Выполнено {task['run_count']} раз")

# Использование
scheduler = TaskScheduler()

def task1():
    print("  Задача 1 выполняется")

def task2():
    print("  Задача 2 выполняется")

scheduler.schedule("Task 1", 1, task1)  # Каждую секунду
scheduler.schedule("Task 2", 2, task2)  # Каждые 2 секунды

# scheduler.run(max_iterations=10)  # Раскомментируйте для запуска
```

#### Пример 3: Анализ логов с Counter
```python
from collections import Counter
import re

class LogAnalyzer:
    """Анализирует логи и выполняет статистику"""
    def __init__(self, log_content):
        self.logs = log_content.split('\n')
        self.logs = [l for l in self.logs if l.strip()]
    
    def extract_level(self):
        """Извлекает уровни логирования"""
        levels = []
        for log in self.logs:
            match = re.search(r'\[(INFO|WARNING|ERROR|DEBUG)\]', log)
            if match:
                levels.append(match.group(1))
        return Counter(levels)
    
    def extract_errors(self):
        """Находит все ошибки"""
        errors = []
        for log in self.logs:
            if '[ERROR]' in log:
                # Извлечь сообщение ошибки
                match = re.search(r'\[ERROR\]\s+(.*)', log)
                if match:
                    errors.append(match.group(1))
        return errors
    
    def most_common_errors(self, top=5):
        """Самые частые ошибки"""
        error_counter = Counter(self.extract_errors())
        return error_counter.most_common(top)
    
    def report(self):
        """Полный отчет"""
        levels = self.extract_level()
        print("=== Отчет по логам ===")
        print("\nУровни логирования:")
        for level, count in levels.most_common():
            print(f"  {level}: {count}")
        
        print("\nТоп-3 ошибки:")
        for error, count in self.most_common_errors(3):
            print(f"  {count}x - {error}")

# Использование
logs = """
[INFO] Приложение запущено
[DEBUG] Инициализация БД
[ERROR] Не удалось подключиться к БД
[WARNING] Низкая память
[ERROR] Не удалось подключиться к БД
[INFO] Повтор подключения
[ERROR] Timeout соединения
[ERROR] Не удалось подключиться к БД
[WARNING] Кэш переполнен
"""

analyzer = LogAnalyzer(logs)
analyzer.report()
```

#### Пример 4: Кэш для сложных вычислений
```python
from functools import lru_cache
import math

class MathCalculations:
    """Математические вычисления с кэшированием"""
    
    @lru_cache(maxsize=128)
    def factorial(self, n):
        """Факториал с кэшированием"""
        if n < 0:
            raise ValueError("n должен быть >= 0")
        if n == 0 or n == 1:
            return 1
        return n * self.factorial(n - 1)
    
    @lru_cache(maxsize=128)
    def is_prime(self, n):
        """Проверка на простоту с кэшированием"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def primes_up_to(self, limit):
        """Находит все простые числа до limit"""
        return [n for n in range(2, limit + 1) if self.is_prime(n)]
    
    def cache_stats(self):
        """Статистика кэша"""
        return {
            'factorial': self.factorial.cache_info(),
            'is_prime': self.is_prime.cache_info()
        }

# Использование
calc = MathCalculations()

print(f"10! = {calc.factorial(10)}")  # Вычислено
print(f"10! = {calc.factorial(10)}")  # Из кэша

print(f"Простые числа до 50: {calc.primes_up_to(50)}")
print(f"Статистика: {calc.cache_stats()}")
```

### 🚨 Частые ошибки

**Ошибка 1: Забыли распаковать Counter в список**
```python
from collections import Counter

c = Counter(['a', 'b', 'a', 'c', 'b', 'a'])

# ❌ НЕПРАВИЛЬНО - Counter не итерируется как обычный счетчик
# for item in c:
#     print(item)  # Печатает только ключи!

# ✅ ПРАВИЛЬНО - используйте elements() для повторений
print(list(c.elements()))  # ['a', 'a', 'a', 'b', 'b', 'c']
```

**Ошибка 2: OrderedDict в Python < 3.7**
```python
# ❌ В Python < 3.7 обычные dict не сохраняли порядок
# d = {'z': 1, 'a': 2}  # Порядок не гарантирован

# ✅ Используйте OrderedDict для совместимости
from collections import OrderedDict
d = OrderedDict([('z', 1), ('a', 2)])  # Порядок сохранен
```

**Ошибка 3: LRU_CACHE с изменяемыми аргументами**
```python
from functools import lru_cache

# ❌ НЕПРАВИЛЬНО - списки не хешируются
# @lru_cache(maxsize=128)
# def process(items):  # items должен быть кортежом!
#     return sum(items)

# ✅ ПРАВИЛЬНО - использовать неизменяемые типы
@lru_cache(maxsize=128)
def process(items):  # items - кортеж
    return sum(items)

result = process((1, 2, 3, 4, 5))
print(result)  # 15
```

**Ошибка 4: Изменение значения из кэша Counter**
```python
from collections import Counter

c = Counter(['a', 'b', 'a'])
c['a'] = 0  # Устанавливаем в 0

# ❌ ПРОБЛЕМА - 0 остается видимым
print(c)  # Counter({'b': 1, 'a': 0})

# ✅ ПРАВИЛЬНО - удалить элемент
del c['a']
print(c)  # Counter({'b': 1})
```

### 📌 Полезные ресурсы
- [Документация: time](https://docs.python.org/3/library/time.html)
- [Документация: collections](https://docs.python.org/3/library/collections.html)
- [Документация: functools.lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache)
- [Документация: datetime](https://docs.python.org/3/library/datetime.html)
- [Статья про Big O сложность операций с collections](https://wiki.python.org/moin/TimeComplexity)
