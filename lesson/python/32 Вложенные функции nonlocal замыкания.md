# Вложенные функции nonlocal замыкания

## 📖 Быстрая навигация по операторам и функциям

- [Вложенные функции (nested functions)](#1-вложенные-функции-nested-functions)
- [Область видимости: Enclosing и правило LEGB](#2-область-видимости-enclosing-и-правило-legb)
- [`nonlocal`: изменение переменной внешней функции](#3-nonlocal-изменение-переменной-внешней-функции)
- [Замыкание (closure)](#4-замыкание-closure)
- [Функция как объект](#5-функция-как-объект)
- [Декораторы: идея и шаблон](#6-декораторы-идея-и-шаблон)

**[📚 Дополнительная информация и примеры](#дополнительная-информация)**


## План урока
- Вложенные функции (nested functions)
- Область видимости **Enclosing** и правило **LEGB**
- Ключевое слово **`nonlocal`**
- **Замыкание (closure)**
- Функция как объект (`__name__`, `__doc__`)
- **Декораторы** и синтаксис `@decorator`

---

## 1) Вложенные функции (nested functions)
**Вложенная функция** — функция, определённая внутри другой функции.

Зачем используют:
- **Инкапсуляция логики** (вспомогательная логика не “торчит” наружу)
- **Локальная область видимости** (меньше конфликтов имён)
- **Избегание дублирования** (внутренний хелпер используется только тут)

Пример:
```py
def outer_function():
    print("Внутри внешней функции")

    def inner_function():
        print("Внутри вложенной функции")

    inner_function()

outer_function()
# inner_function()  # NameError: вложенная функция снаружи не видна
```

---

## 2) Область видимости: Enclosing и правило LEGB
**Enclosing** — охватывающая область (внешняя функция), внутри которой определена вложенная.

Правило поиска имён **LEGB**:
1) **L**ocal — внутри текущей функции
2) **E**nclosing — внутри внешних функций (если есть вложенность)
3) **G**lobal — модуль (файл)
4) **B**uilt-in — встроенные имена (`len`, `print`, ...)

Пример чтения переменных из Enclosing:
```py
def outer_function(repeat):
    message = "Внешняя функция
"

    def inner_function():
        print(message * repeat)  # берёт message и repeat из enclosing

    inner_function()

outer_function(3)
```

### Локальная “тень” переменной
Если во вложенной функции создать переменную с тем же именем, это **не изменит** внешнюю — создастся новая локальная.
```py
def outer_function():
    message = "Внешняя функция"

    def inner_function():
        message = "Вложенная функция"  # новая локальная переменная

    inner_function()
    print(message)  # Внешняя функция

outer_function()
```

---

## 3) `nonlocal`: изменение переменной внешней функции
Если нужно **изменить** переменную из enclosing-области, используем `nonlocal`.

```py
def outer_function():
    message = "Внешняя функция"

    def inner_function():
        nonlocal message
        message = "Изменено во вложенной функции"

    inner_function()
    print(message)  # Изменено во вложенной функции

outer_function()
```

Особенности:
- `nonlocal` работает **только с ближайшей внешней функцией**
- не “дотягивается” до глобальной области (для глобальной есть `global`)

Пример многоуровневой вложенности:
```py
def outer_function():
    message = "Внешняя функция"

    def middle_function():
        def inner_function():
            nonlocal message  # возьмёт message именно из outer_function
            message = "Изменено во вложенной функции"

        inner_function()

    middle_function()
    print(message)

outer_function()
```

---

## 4) Замыкание (closure)
**Замыкание** — это объект, который содержит **вложенную функцию** и “захваченное” окружение (значения из Enclosing), доступные даже после завершения внешней функции.

### 4.1 Базовый пример
```py
def outer_function(text):
    def inner_function():
        print(text)  # text сохраняется в замыкании
    return inner_function  # возвращаем функцию, не вызывая её

closure = outer_function("Переданный текст")
closure()  # можно вызвать позже
```

### 4.2 Замыкание-счётчик (с `nonlocal`)
```py
def counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

counter_function = counter()
print(counter_function())  # 1
print(counter_function())  # 2
print(counter_function())  # 3
```

### 4.3 “Фабрики функций”: фильтр или умножитель
```py
def create_filter(border):
    def filter_value(value):
        return value > border
    return filter_value

greater_than_five = create_filter(5)
print(greater_than_five(7))  # True
print(greater_than_five(3))  # False
```

```py
def multiplier(factor):
    def multiply(number):
        return number * factor
    return multiply

double = multiplier(2)
triple = multiplier(3)
print(double(4))  # 8
print(triple(4))  # 12
```

### 4.4 Кэширование через замыкание (memoize-идея)
```py
import time

def long_function(num):
    time.sleep(3)
    return list(range(num))

def memoize():
    cache = {}

    def get_or_compute(key, compute_function):
        if key not in cache:
            cache[key] = compute_function(key)
        return cache[key]

    return get_or_compute

cached_computation = memoize()

start = time.time()
print(cached_computation(10, long_function))  # долго
print("Время расчёта:", time.time() - start)

start = time.time()
print(cached_computation(10, long_function))  # быстро (из кэша)
print("Время из кэша:", time.time() - start)
```

---

## 5) Функция как объект
У функции есть атрибуты, например имя и документация:

```py
def greet():
    """Функция приветствия"""
    print("Привет!")

print(greet.__name__)  # greet
print(greet.__doc__)   # Функция приветствия
```

То же самое работает и для вложенных функций:
```py
def outer():
    def inner():
        """Вложенная функция"""
        pass
    return inner

func = outer()
print(func.__name__)  # inner
print(func.__doc__)   # Вложенная функция
```

---

## 6) Декораторы: идея и шаблон
**Декоратор** — функция, которая принимает функцию, добавляет к ней логику и возвращает “обёртку”, **не меняя тело исходной функции**.

Шаблон:
```py
def decorator(func):
    def wrapper():
        # до
        func()
        # после
    return wrapper
```

Пример:
```py
def simple_decorator(func):
    def wrapper():
        print("Перед вызовом функции")
        func()
        print("После вызова функции")
    return wrapper

def say_hello():
    print("Привет!")

say_hello = simple_decorator(say_hello)
say_hello()
```

### Синтаксис `@decorator`
То же самое, но короче:
```py
def simple_decorator(func):
    def wrapper():
        print("Перед вызовом функции")
        func()
        print("После вызова функции")
    return wrapper

@simple_decorator
def say_hello():
    print("Привет!")

say_hello()
```

> Смысл: `@decorator_name` **заменяет функцию** на результат работы декоратора.

### Частый кейс: замер времени
```py
import time

def timing_decorator(func):
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print(f"Функция {func.__name__} выполнялась {end - start:.5f} секунд")
    return wrapper

@timing_decorator
def slow_function():
    time.sleep(2)
    print("Функция выполнена")

slow_function()
```

**Важно на практике:** чтобы сохранить имя/докстринг функции после декоратора, обычно добавляют `functools.wraps`:
```py
from functools import wraps

def deco(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

# Задания для закрепления — ответы

## 1) Что произойдёт?
```py
def outer():
    def inner():
        print("Hi")
    return inner()      # inner вызывается здесь и возвращает None

result = outer()        # result = None
result()                # попытка вызвать None
```
Ответ: **d — будет ошибка `NoneType object is not callable`**.

## 2) Сопоставление понятий
- 1) Вложенная функция → **b** (функция внутри другой)
- 2) `nonlocal` → **a** (ключевое слово)
- 3) Enclosing → **d** (область для вложенной функции)
- 4) Замыкание → **c** (функция + сохранённые переменные внешней области)

## 3) Что делает декоратор?
Ответ: **b — добавляет логику без изменения тела функции**.

## 4) Что делает `@decorator_name`?
Ответ: **заменяет функцию на результат работы декоратора**.

---

# Практическая работа — решения

## 1) Фабрика функций расчёта НДС
```py
def vat_calculator(rate):
    def calculate(price):
        return round(price * (1 + rate), 2)
    return calculate

vat_20 = vat_calculator(0.2)
vat_10 = vat_calculator(0.1)

print(vat_20(100))  # 120.0
print(vat_10(200))  # 220.0
```

## 2) Калькулятор скидок по категориям
```py
def discount_maker(category_discounts):
    def apply_discount(category, price):
        discount = category_discounts.get(category, 0)
        return round(price * (1 - discount), 2)
    return apply_discount

discounts = {"food": 0.1, "clothes": 0.2}
friday_discount = discount_maker(discounts)

print(friday_discount("food", 100))        # 90.0
print(friday_discount("clothes", 250))     # 200.0
print(friday_discount("electronics", 500)) # 500.0
```

## 3) Настроенная функция вывода (custom printer)
```py
def custom_printer(sep, end):
    def print_func(*args):
        print(*args, sep=sep, end=end)
    return print_func

printer = custom_printer(sep=" | ", end=" -->\n")
printer("Hello", "World")
printer("Python", "Java", "C++")
```

## 4) Декоратор нумерации вызовов
```py
def call_counter(func):
    count = 0

    def wrapper():
        nonlocal count
        count += 1
        print(f"Вызов функции '{func.__name__}' №{count}:")
        func()

    return wrapper

@call_counter
def greet():
    print("Привет!")

greet()
greet()
greet()
```

---

# Домашнее задание — решения

## ДЗ 1) Фабрика функций округления
```py
def make_rounder(digits):
    def round_value(x):
        return round(x, digits)
    return round_value

round2 = make_rounder(2)
round0 = make_rounder(0)

print(round2(3.14159))  # 3.14
print(round2(2.71828))  # 2.72
print(round0(9.999))    # 10.0
```

## ДЗ 2) Расширяемый логгер событий (замыкание + время)
```py
from datetime import datetime

def make_logger():
    events = []

    def log(message=None, ts=None):
        # Если вызвали log() без message — просто вернём список событий
        if message is None:
            return events

        if ts is None:
            ts = datetime.now()

        events.append(f"{message}: {ts.strftime('%Y-%m-%d %H:%M:%S')}")
        return events

    return log

log = make_logger()
log("Загрузка данных")
log("Обработка завершена")
log("Сохранение файла")

for event in log():
    print(event)
```

## ДЗ 3) Декоратор “рамка” вокруг вывода
```py
from functools import wraps

def frame(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("-" * 50)
        result = func(*args, **kwargs)
        print("-" * 50)
        return result
    return wrapper

@frame
def say_hello():
    print("Привет, игрок!")

say_hello()
```

---

## Мини-шпаргалка
```text
Nested: функция внутри функции
Enclosing: внешняя функция для inner
LEGB: Local -> Enclosing -> Global -> Builtin

nonlocal x: изменить x из ближайшей внешней функции

Closure: outer возвращает inner, а inner “помнит” переменные outer

Decorator: def deco(func): def wrapper(...): ...; return wrapper
@deco: заменяет функцию на wrapper (результат декоратора)
```


---

## 📚 Дополнительная информация

_Этот раздел будет дополнен практическими примерами и дополнительной информацией._
