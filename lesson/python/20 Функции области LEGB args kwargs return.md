# Функции области LEGB args kwargs return

## 📖 Быстрая навигация по операторам и функциям

- [[#0) О чём урок]](#0-о-чём-урок)
- [[#1) Функция: определение и польза]](#1-функция-определение-и-польза)
- [[#2) `def` и правила именования]](#2-def-и-правила-именования)
- [[#3) `pass` — заглушка]](#3-pass-—-заглушка)
- [[#4) Вызов функции]](#4-вызов-функции)
- [[#5) Аргументы функций]](#5-аргументы-функций)
- [[#6) Упаковка аргументов: `*args` и `**kwargs`]](#6-упаковка-аргументов-args-и-kwargs)
- [[#7) Комбинация типов аргументов (порядок)]](#7-комбинация-типов-аргументов-порядок)
- [[#8) `return` — возврат значения из функции]](#8-return-—-возврат-значения-из-функции)
- [[#9) Области видимости и правило LEGB]](#9-области-видимости-и-правило-legb)
- [[#10) `global`: изменение глобальной переменной из функции]](#10-global-изменение-глобальной-переменной-из-функции)
- [[#1) Конвертер температуры]](#1-конвертер-температуры)
- [[#2) Фильтрация строк по длине (`*args`)]](#2-фильтрация-строк-по-длине-args)
- [[#3) Проверка знака числа]](#3-проверка-знака-числа)
- [[#ДЗ 1) Простое число]](#дз-1-простое-число)
- [[#ДЗ 2) Фильтрация чисел (“even” / “odd”)]](#дз-2-фильтрация-чисел-“even”-“odd”)
- [[#ДЗ 3) Объединение словарей (`**kwargs`-идея на практике)]](#дз-3-объединение-словарей-kwargs-идея-на-практике)
- [[#Мини-шпаргалка]](#мини-шпаргалка)
- [[#Дополнительная информация]](#дополнительная-информация)


---

## 1) Функция: определение и польза
**Функция** — именованный блок кода для выполнения конкретной задачи.

Зачем:
- **переиспользование** кода;
- **читабельность** (разбиваем программу на части);
- **модульность** (отдельные независимые блоки);
- проще **отлаживать** (поправил функцию → исправилось во всех местах вызова).

---

## 2) `def` и правила именования
### 2.1 Базовый синтаксис
```py
def function_name(parameters):
    # тело функции
    return result  # опционально
```

### 2.2 Правила именования (PEP 8)
- имя начинается с буквы или `_`, не с цифры;
- не использовать ключевые слова (`def`, `return`, `if`…);
- не переопределять встроенные имена (`print`, `sum`, `list`…);
- `snake_case`, часто глагол: `calculate_total()`, `get_user()`, `filter_items()`.

---

## 3) `pass` — заглушка
`pass` — “ничего не делает”, но сохраняет корректный синтаксис там, где нужен блок кода.

```py
def later():
    pass

if True:
    pass

for _ in range(3):
    pass
```

✅ Важно: функция с `pass` **не возвращает значение явно**, значит возвращает `None`.

**Вопрос из занятия:**
```py
def example():
    pass

print(example())
```
Выведет: **`None`**

---

## 4) Вызов функции
Вызов = выполнение функции по имени:

```py
def greet():
    print("Hello!")

greet()
```

С аргументом:
```py
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Alice")
```

---

## 5) Аргументы функций

### 5.1 Позиционные аргументы
Передаются по порядку:
```py
def greet(name, age):
    print(f"My name is {name} and I am {age} years old.")

greet("Alice", 25)
```

Если передать **меньше** или **больше**, чем ожидается → часто будет `TypeError`.

### 5.2 Именованные (keyword) аргументы
Передаются с указанием имени параметра — порядок не важен:
```py
greet(age=30, name="Bob")
```

### 5.3 Аргументы по умолчанию (default)
Можно задать значение по умолчанию:
```py
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")         # greeting не передан -> "Hello"
greet("Bob", "Hi")     # greeting задан -> "Hi"
```

⚠️ Правило: **сначала обязательные**, потом параметры со значениями по умолчанию.

---

## 6) Упаковка аргументов: `*args` и `**kwargs`

### 6.1 `*args` — любое число позиционных
Аргументы упаковываются в **кортеж**:
```py
def calculate_sum(*args):
    return sum(args)

print(calculate_sum(1, 2, 3))  # 6
print(calculate_sum())         # 0
```

### 6.2 `**kwargs` — любое число именованных
Аргументы упаковываются в **словарь**:
```py
def print_user_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_user_info(name="Alice", age=25, city="New York")
print_user_info()
```

---

## 7) Комбинация типов аргументов (порядок)
В одной функции можно использовать разные виды аргументов, но важно соблюдать порядок:

1) позиционные  
2) `*args`  
3) аргументы по умолчанию  
4) `**kwargs`

Пример:
```py
def show_full_info(name, *args, age=25, **kwargs):
    print(f"Name: {name}")
    print(f"Other details: {args}")
    print(f"Age: {age}")
    print(f"Additional info: {kwargs}")

show_full_info("Alice", "Developer", age=30, city="New York", hobby="Reading")
```

---

## 8) `return` — возврат значения из функции
`return`:
- возвращает значение в место вызова;
- **завершает** выполнение функции;
- если `return` без значения → возвращается `None`;
- если `return` отсутствует → по факту тоже вернуть `None`.

### 8.1 Возврат значения
```py
def add(a, b):
    return a + b

result = add(3, 5)
print(result)  # 8
```

### 8.2 Несколько `return`
```py
def check_positive(number):
    if number > 0:
        return "Положительное число"
    return "Отрицательное или ноль"
```

### 8.3 Возврат `None`
```py
def say_hello():
    print("Hello, World!")

x = say_hello()
print(x)  # None
```

### 8.4 Множественный возврат
Возвращается кортеж:
```py
def calculate(a, b):
    return a + b, a - b

print(calculate(10, 5))  # (15, 5)
```

### 8.5 Пустой `return` (ранний выход)
```py
def factorial(n):
    if n < 0:
        return  # None
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
```

---

## 9) Области видимости и правило LEGB
**Область видимости** — где переменная доступна.

Python ищет переменную по правилу **LEGB**:
- **L**ocal — внутри текущей функции
- **E**nclosing — во внешних (окружающих) функциях
- **G**lobal — на уровне модуля
- **B**uilt-in — встроенные имена (`len`, `print`, `int`…)

### 9.1 Local
```py
def my_function():
    local_var = 10
    print(local_var)

my_function()
# print(local_var)  # NameError
```

### 9.2 Global
```py
global_var = 20

def show_global():
    print(global_var)

show_global()
print(global_var)
```

### 9.3 Built-in
```py
print(len("Hello"))
```

### 9.4 Перекрытие глобальной переменной локальной
```py
x = 10

def f():
    x = 5
    print("local:", x)

f()
print("global:", x)  # глобальная не изменилась
```

---

## 10) `global`: изменение глобальной переменной из функции
Если внутри функции сделать присваивание переменной с именем глобальной, Python считает её **локальной**.
Если при этом попытаться использовать её “до присваивания” → будет `UnboundLocalError`.

### 10.1 Плохой пример (без `global`)
```py
count = 0

def increment_counter():
    count = count + 1  # UnboundLocalError
    print(count)
```

### 10.2 Рабочий пример (с `global`)
```py
count = 0

def increment_counter():
    global count
    count += 1

increment_counter()
print(count)  # 1
increment_counter()
print(count)  # 2
```

### 10.3 Почему чаще лучше НЕ использовать `global`
Лучше передавать значения через параметры:
- понятнее, откуда берутся данные;
- проще тестировать;
- меньше неожиданных побочных эффектов.

---

# Задания для закрепления (ответы)
1) `example()` с `pass` → печатает **`None`**  
2)
```py
def func(a, b, c=10):
    return a + b + c
print(func(2, 3))
```
Ответ: **15**

3)
```py
def check_number(n):
    if n > 0:
        return "Positive"
    return "Non-positive"
print(check_number(-1))
```
Ответ: **"Non-positive"**

4)
```py
def info(**kwargs):
    return kwargs
print(info(name="Alice", age=30))
```
Ответ: **{"name": "Alice", "age": 30}**

---

# Практические задания (решения)

## 1) Конвертер температуры
```py
def convert_temperature(temp, scale):
    if scale.upper() == "C":
        return f"{temp}C = {temp * 9/5 + 32}F"
    elif scale.upper() == "F":
        return f"{temp}F = {(temp - 32) * 5/9}C"

temp = 100
scale = "C"
print(convert_temperature(temp, scale))  # 100C = 212.0F
```

## 2) Фильтрация строк по длине (`*args`)
Функция принимает `n` и любое количество строк (не списком):
```py
def filter_strings(min_len, *words):
    return [s for s in words if len(s) > min_len]

strings = ["apple", "banana", "cherry", "date", "fig"]
n = 5
print(filter_strings(n, *strings))  # ['banana', 'cherry']
```

## 3) Проверка знака числа
```py
def check_number(num):
    if num > 0:
        return "Число положительное"
    elif num < 0:
        return "Число отрицательное"
    return "Число равно нулю"

num = -3
print(check_number(num))
```

---

# Домашнее задание (решения)

## ДЗ 1) Простое число
Проверить, является ли `n` простым (делится только на 1 и на себя):
```py
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


n = 17
print(is_prime(n))
```

---

## ДЗ 2) Фильтрация чисел (“even” / “odd”)
Функция принимает `filter_type` и произвольное число аргументов:

```py
def filter_numbers(filter_type: str, *nums):
    ft = filter_type.lower()

    if ft == "even":
        return [x for x in nums if x % 2 == 0]
    if ft == "odd":
        return [x for x in nums if x % 2 != 0]

    return "Некорректный фильтр"


print(filter_numbers("even", 1, 2, 3, 4, 5, 6))  # [2, 4, 6]
print(filter_numbers("odd", 10, 15, 20, 25))     # [15, 25]
print(filter_numbers("prime", 2, 3, 5, 7))       # Некорректный фильтр
```

---

## ДЗ 3) Объединение словарей (`**kwargs`-идея на практике)
Если ключи повторяются — берём значение **из последнего словаря**:

```py
def merge_dicts(*dicts):
    result = {}
    for d in dicts:
        result.update(d)
    return result


dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}
dict3 = {"d": 5}

print(merge_dicts(dict1, dict2, dict3))  # {'a': 1, 'b': 3, 'c': 4, 'd': 5}
```

---

## Мини-шпаргалка
```text
def name(...):              -> объявление функции
pass                        -> заглушка (ничего не делает)
return value / return       -> вернуть значение / вернуть None и завершить

Аргументы:
positional                  -> по порядку
keyword                     -> по имени
default                     -> параметры со значением по умолчанию
*args                       -> кортеж позиционных
**kwargs                    -> словарь именованных

Порядок в сигнатуре:
positional -> *args -> default -> **kwargs

LEGB:
Local -> Enclosing -> Global -> Built-in

global x                     -> позволяет менять глобальную x внутри функции
(обычно лучше передавать данные параметрами)
```


---

## Дополнительная информация

### Важные концепции для изучения

#### 1. Углубленное изучение области видимости LEGB
```python
# L - Local (локальная область функции)
# E - Enclosing (охватывающая область вложенных функций)
# G - Global (глобальная область модуля)
# B - Built-in (встроенная область Python)

x = "global"

def outer():
    x = "enclosing"
    
    def inner():
        x = "local"
        print(x)  # Ищет в порядке: L -> E -> G -> B
    
    inner()
    print(x)

outer()
print(x)
# Вывод:
# local (L - локальная переменная inner)
# enclosing (E - переменная outer)
# global (G - глобальная переменная)

# Демонстрация порядка поиска
print(len)  # <built-in function len> - B (Built-in)

def demo():
    print(len)  # Находит из B
    
demo()

# Использование globals() и locals()
global_var = "глобальная"

def show_scopes():
    local_var = "локальная"
    print("Глобальные:", list(globals().keys())[:3], "...")
    print("Локальные:", list(locals().keys()))

show_scopes()

# Практический пример: замыкание с доступом к разным областям
def create_multiplier(multiplier):
    """Создает функцию-множитель, использующую область enclosing"""
    def multiply(x):
        return x * multiplier  # multiplier из области E (enclosing)
    return multiply

times_3 = create_multiplier(3)
times_5 = create_multiplier(5)

print(times_3(10))  # 30
print(times_5(10))  # 50
```

#### 2. *args - переменное количество позиционных аргументов
```python
# *args собирает дополнительные позиционные аргументы в кортеж

def print_args(*args):
    print(f"Получено {len(args)} аргументов")
    for i, arg in enumerate(args, 1):
        print(f"  Аргумент {i}: {arg}")

print_args(1)
print_args(1, 2, 3)
print_args('a', 'b', 'c', 'd')

# Практический пример: функция с переменным числом аргументов
def sum_all(*numbers):
    """Суммирует все переданные числа"""
    total = 0
    for num in numbers:
        total += num
    return total

print(sum_all(1, 2, 3))        # 6
print(sum_all(10, 20, 30, 40))  # 100

# Или используя встроенную функцию
def sum_all_v2(*numbers):
    return sum(numbers)

# Распаковка списков при передаче аргументов
numbers = [1, 2, 3, 4, 5]
print(sum_all(*numbers))  # 15

# Комбинирование обычных аргументов с *args
def greet(greeting, *names):
    """Приветствует множество людей"""
    for name in names:
        print(f"{greeting}, {name}!")

greet("Привет", "Алиса", "Боб", "Виктор")
# Привет, Алиса!
# Привет, Боб!
# Привет, Виктор!

# *args должен быть после обычных аргументов
# ✅ ПРАВИЛЬНО
def func(a, b, *args):
    pass

# ❌ НЕПРАВИЛЬНО
# def func(*args, a, b):  # SyntaxError!
#     pass
```

#### 3. **kwargs - переменное количество именованных аргументов
```python
# **kwargs собирает именованные аргументы в словарь

def print_kwargs(**kwargs):
    print(f"Получено {len(kwargs)} именованных аргументов")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print_kwargs(name="Алиса", age=30, city="Москва")
# Получено 3 именованных аргументов
#   name: Алиса
#   age: 30
#   city: Москва

# Практический пример: конфигурация функции
def create_profile(name, **options):
    """Создает профиль с дополнительными опциями"""
    profile = {'name': name}
    profile.update(options)
    return profile

profile1 = create_profile("Алиса", age=30, city="Москва", language="Python")
print(profile1)
# {'name': 'Алиса', 'age': 30, 'city': 'Москва', 'language': 'Python'}

# Работа с конфигурацией
def connect_database(**config):
    """Подключается к БД с переданными параметрами"""
    defaults = {
        'host': 'localhost',
        'port': 5432,
        'timeout': 30,
        'retries': 3
    }
    defaults.update(config)
    
    connection_string = (
        f"Host: {defaults['host']}, "
        f"Port: {defaults['port']}, "
        f"Timeout: {defaults['timeout']}"
    )
    return connection_string

print(connect_database(host='example.com', port=3306))
# Host: example.com, Port: 3306, Timeout: 30

# Распаковка словаря при передаче аргументов
config = {'host': 'db.example.com', 'port': 5432, 'timeout': 60}
print(connect_database(**config))
```

#### 4. Комбинирование *args, **kwargs и обычных аргументов
```python
# Правильный порядок: обычные аргументы -> *args -> **kwargs

def complex_function(a, b, *args, **kwargs):
    """Демонстрирует использование всех типов аргументов"""
    print(f"Обычные: a={a}, b={b}")
    print(f"*args: {args}")
    print(f"**kwargs: {kwargs}")

complex_function(1, 2)
# Обычные: a=1, b=2
# *args: ()
# **kwargs: {}

complex_function(1, 2, 3, 4, 5)
# Обычные: a=1, b=2
# *args: (3, 4, 5)
# **kwargs: {}

complex_function(1, 2, 3, 4, name="Алиса", age=30)
# Обычные: a=1, b=2
# *args: (3, 4)
# **kwargs: {'name': 'Алиса', 'age': 30}

# Практический пример: логирование функции
def log_function_call(func, *args, **kwargs):
    """Логирует вызов функции и ее результат"""
    print(f"Вызов функции: {func.__name__}")
    print(f"  Аргументы: {args}")
    print(f"  Параметры: {kwargs}")
    
    result = func(*args, **kwargs)
    print(f"  Результат: {result}")
    return result

def add(a, b):
    return a + b

log_function_call(add, 5, 3)
# Вызов функции: add
#   Аргументы: (5, 3)
#   Параметры: {}
#   Результат: 8

# Распаковка при вызове
args = [10, 20]
kwargs = {}
result = log_function_call(add, *args, **kwargs)
```

#### 5. Различные типы return
```python
# Функция без return или return без значения возвращает None
def no_return():
    x = 5

print(no_return())  # None

# Возврат одного значения
def get_single():
    return 42

print(get_single())  # 42

# Возврат нескольких значений (как кортеж)
def get_coordinates():
    return 10, 20  # Неявно возвращает кортеж (10, 20)

x, y = get_coordinates()
print(f"x={x}, y={y}")  # x=10, y=20

# Возврат словаря с несколькими значениями
def get_user_info():
    return {
        'name': 'Алиса',
        'age': 30,
        'email': 'alice@example.com'
    }

user = get_user_info()
print(user['name'])  # Алиса

# Возврат None явно для ранного выхода
def find_item(items, target):
    """Ищет элемент и возвращает индекс или None"""
    for i, item in enumerate(items):
        if item == target:
            return i
    return None

print(find_item([1, 2, 3, 4, 5], 3))  # 2
print(find_item([1, 2, 3, 4, 5], 10))  # None

# Практический пример: функция с несколькими путями return
def divide(a, b):
    """Делит a на b с обработкой ошибок"""
    if b == 0:
        return None, "Division by zero"
    
    if a % b == 0:
        return a // b, None
    else:
        return a / b, None

result, error = divide(10, 2)
if error:
    print(f"Ошибка: {error}")
else:
    print(f"Результат: {result}")  # Результат: 5

result, error = divide(10, 0)
if error:
    print(f"Ошибка: {error}")  # Ошибка: Division by zero
```

### 💡 Практические примеры

#### Пример 1: Декоратор с *args и **kwargs
```python
def timing_decorator(func):
    """Декоратор, измеряющий время выполнения функции"""
    import time
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Вызов функции: {func.__name__}")
        start = time.time()
        
        result = func(*args, **kwargs)
        
        elapsed = time.time() - start
        print(f"Время выполнения: {elapsed:.4f} сек")
        return result
    
    return wrapper

@timing_decorator
def slow_function(n):
    """Имитирует долгую операцию"""
    import time
    time.sleep(n)
    return f"Завершено за {n} сек"

slow_function(0.5)

@timing_decorator
def add(a, b, verbose=False):
    if verbose:
        print(f"Суммирование {a} + {b}")
    return a + b

add(5, 3, verbose=True)
```

#### Пример 2: Функция для обработки данных с гибкими аргументами
```python
def filter_data(*arrays, operation='all', **filters):
    """
    Фильтрует данные по условиям
    
    *arrays: переменное количество массивов данных
    operation: 'all' (все условия) или 'any' (любое условие)
    **filters: условия фильтрации {поле: значение}
    """
    if not arrays:
        return None
    
    # Предполагаем, что это массивы словарей
    data = arrays[0]
    
    result = []
    for item in data:
        if operation == 'all':
            # Все условия должны быть выполнены
            match = all(
                item.get(key) == value
                for key, value in filters.items()
            )
        else:  # 'any'
            # Любое из условий должно быть выполнено
            match = any(
                item.get(key) == value
                for key, value in filters.items()
            )
        
        if match:
            result.append(item)
    
    return result

# Использование
users = [
    {'name': 'Алиса', 'age': 30, 'city': 'Москва'},
    {'name': 'Боб', 'age': 25, 'city': 'СПб'},
    {'name': 'Виктор', 'age': 30, 'city': 'СПб'},
    {'name': 'Дарья', 'age': 25, 'city': 'Москва'},
]

# Все условия (AND)
result = filter_data(users, operation='all', age=30, city='Москва')
print(result)  # [{'name': 'Алиса', ...}]

# Любое условие (OR)
result = filter_data(users, operation='any', age=30, city='Москва')
print(result)  # [{'name': 'Алиса', ...}, {'name': 'Боб', ...}, ...]
```

#### Пример 3: Функция-фабрика с замыканием
```python
def create_account(initial_balance=0):
    """
    Создает счет с методами для работы с деньгами
    Демонстрирует область видимости E (enclosing)
    """
    balance = initial_balance
    transactions = []
    
    def deposit(amount):
        """Пополнить счет"""
        nonlocal balance
        if amount > 0:
            balance += amount
            transactions.append(('deposit', amount))
            return True
        return False
    
    def withdraw(amount):
        """Снять деньги со счета"""
        nonlocal balance
        if 0 < amount <= balance:
            balance -= amount
            transactions.append(('withdraw', amount))
            return True
        return False
    
    def get_balance():
        """Получить баланс"""
        return balance
    
    def get_statement():
        """Получить выписку"""
        return {
            'balance': balance,
            'transactions': transactions.copy(),
            'total_transactions': len(transactions)
        }
    
    # Возвращаем словарь функций
    return {
        'deposit': deposit,
        'withdraw': withdraw,
        'balance': get_balance,
        'statement': get_statement
    }

# Использование
account = create_account(1000)

account['deposit'](500)
print(f"Баланс: {account['balance']()}")  # 1500

account['withdraw'](200)
print(f"Баланс: {account['balance']()}")  # 1300

print(account['statement']())
# {'balance': 1300, 'transactions': [('deposit', 500), ('withdraw', 200)], ...}
```

#### Пример 4: Построитель (Builder) с гибкими параметрами
```python
class QueryBuilder:
    """Построитель SQL запросов с гибкими параметрами"""
    def __init__(self, table):
        self.table = table
        self.conditions = []
        self.selected_fields = ['*']
        self.limit_value = None
        self.offset_value = None
    
    def select(self, *fields):
        """Выбрать поля"""
        self.selected_fields = list(fields) if fields else ['*']
        return self
    
    def where(self, **conditions):
        """Добавить условия WHERE"""
        for key, value in conditions.items():
            if isinstance(value, str):
                self.conditions.append(f"{key} = '{value}'")
            else:
                self.conditions.append(f"{key} = {value}")
        return self
    
    def limit(self, limit, offset=0):
        """Добавить LIMIT и OFFSET"""
        self.limit_value = limit
        self.offset_value = offset
        return self
    
    def build(self):
        """Построить SQL запрос"""
        fields = ', '.join(self.selected_fields)
        query = f"SELECT {fields} FROM {self.table}"
        
        if self.conditions:
            query += " WHERE " + " AND ".join(self.conditions)
        
        if self.limit_value:
            query += f" LIMIT {self.limit_value}"
            if self.offset_value:
                query += f" OFFSET {self.offset_value}"
        
        return query

# Использование (method chaining)
query = (QueryBuilder('users')
         .select('id', 'name', 'email')
         .where(age=30, city='Москва')
         .limit(10, offset=0)
         .build())

print(query)
# SELECT id, name, email FROM users WHERE age = 30 AND city = 'Москва' LIMIT 10
```

### 🚨 Частые ошибки

**Ошибка 1: Неправильный порядок параметров**
```python
# ❌ НЕПРАВИЛЬНО - *args должны быть перед **kwargs
# def func(*args, **kwargs, c):
#     pass

# ✅ ПРАВИЛЬНО
def func(a, *args, **kwargs):
    pass

def func(a, b=2, *args, **kwargs):
    pass
```

**Ошибка 2: Забыли распаковать аргументы**
```python
def add(a, b):
    return a + b

numbers = [5, 3]

# ❌ НЕПРАВИЛЬНО
result = add(numbers)  # TypeError: add() missing 1 required positional argument

# ✅ ПРАВИЛЬНО
result = add(*numbers)  # 8
```

**Ошибка 3: Использование nonlocal без необходимости**
```python
# ❌ НЕПРАВИЛЬНО - не нужен nonlocal для чтения
def outer():
    x = 10
    
    def inner():
        # nonlocal x  # Не нужен здесь!
        print(x)  # Можно просто прочитать
    
    inner()

# ✅ ПРАВИЛЬНО - nonlocal нужен для изменения
def outer():
    x = 10
    
    def inner():
        nonlocal x  # Нужен для изменения
        x += 1
    
    inner()
    print(x)  # 11
```

**Ошибка 4: Return в цикле прерывает функцию**
```python
# ❌ ПРОБЛЕМА - функция завершается при первом совпадении
def find_all_matches(items, target):
    for item in items:
        if item == target:
            return item  # Вернет только первый!

# ✅ ПРАВИЛЬНО
def find_all_matches(items, target):
    matches = []
    for item in items:
        if item == target:
            matches.append(item)
    return matches
```

### 📌 Полезные ресурсы
- [Документация: функции](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Документация: *args и **kwargs](https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions)
- [PEP 3102 - Keyword-Only Arguments](https://www.python.org/dev/peps/pep-3102/)
- [functools.wraps](https://docs.python.org/3/library/functools.html#functools.wraps)
- [globals() и locals()](https://docs.python.org/3/library/functions.html#globals)
