# Декораторы args kwargs return wraps фабрика

## 0) План занятия
- Где применяются декораторы
- Декораторы для функций с аргументами (`*args`, `**kwargs`)
- Возврат результата из `wrapper`
- `functools.wraps` (сохранение метаданных)
- Декораторы **с аргументами** (декоратор-фабрика)
- Использование **нескольких** декораторов и порядок выполнения

---

## 1) Где применяются декораторы
Основные сценарии:
- **Логирование** вызовов функций (аргументы/результат).
- **Измерение времени** выполнения.
- **Ограничение частоты вызовов** (throttling).
- **Проверка и валидация** входных данных.
- **Ограничение доступа** (permissions/roles).
- **Автоповтор при ошибках** (retry).
- **Кеширование** результатов.
- **Авто-изменение данных** (форматирование результата).

---

## 2) Декораторы для функций с аргументами: `*args` и `**kwargs`
Если декорируемая функция может принимать аргументы, `wrapper` должен уметь:
- принять любые позиционные/именованные аргументы,
- передать их в исходную функцию.

Шаблон:
```py
def decorator(func):
    def wrapper(*args, **kwargs):
        # до
        result = func(*args, **kwargs)
        # после
        return result
    return wrapper
```

### Пример: логирование в файл через `logging`
```py
import logging
from functools import wraps

logging.basicConfig(
    filename="functions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Функция {func.__name__} вызвана с аргументами: {args}, {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"Функция {func.__name__} вернула: {result}")
        return result
    return wrapper

@log_decorator
def add(a, b):
    return a + b

@log_decorator
def say_hello():
    print("Привет!")

print(add(3, 5))
say_hello()
```

---

## 3) Важно: возвращайте результат из `wrapper`
Если исходная функция возвращает значение, важно его **не потерять**.

### Ошибка: результат “теряется”
```py
def upper_decorator(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs).upper()  # вызвали и выбросили
        # нет return -> вернётся None
    return wrapper
```

### Правильно: вернуть преобразованный результат
```py
def upper_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper
```

---

## 4) `functools.wraps`: зачем нужен
Проблема: при декорировании функция **заменяется** на `wrapper`, поэтому:
- меняется `__name__`,
- пропадает/меняется `__doc__` и другие метаданные.

Решение: `functools.wraps(func)` переносит метаданные на обёртку.

```py
from functools import wraps

def simple_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

## 5) Декораторы с аргументами (декоратор-фабрика)
Если нужно передавать параметры **в декоратор**, создают *функцию-фабрику*, которая возвращает настоящий декоратор.

Шаблон:
```py
def decorator_factory(arg1, arg2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            ... # используем arg1/arg2
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### Пример: декоратор с сообщением
```py
from functools import wraps

def message_decorator(message):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(message)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

Использование:
```py
@message_decorator("Начинаем выполнение")
def analyse_data():
    print("Данные проанализированы")

analyse_data()
```

### Пример: `retry(attempts)` — повтор при ошибках
```py
import time
from functools import wraps

def retry(attempts, delay=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    print(f"Попытка {i+1} не удалась: {e}")
                    time.sleep(delay)
            print("Все попытки исчерпаны.")
            # можно вернуть None, или пробросить ошибку:
            # raise last_error
            return None
        return wrapper
    return decorator
```

---

## 6) Несколько декораторов: порядок выполнения
Если декораторов несколько, они применяются **снизу вверх** (ближайший к функции — первым).

```py
def deco_a(func):
    def wrapper():
        print("A before")
        func()
        print("A after")
    return wrapper

def deco_b(func):
    def wrapper():
        print("B before")
        func()
        print("B after")
    return wrapper

@deco_a      # применяется вторым
@deco_b      # применяется первым
def f():
    print("RUN")

f()
```

Порядок вывода будет:
- B before → RUN → B after → A before/after (в зависимости от логики декораторов)

---

# 7) Задания для закрепления — ответы
1) Что делает `functools.wraps`? → **сохраняет имя и документацию исходной функции**.  
2) Почему без `wraps` теряется документация? → потому что `wrapper` **заменяет** функцию, метаданные не переносятся.  
3) Для чего нужны `*args` и `**kwargs` в декораторах? → для совместимости **с любыми аргументами**.

Доп. вопросы:
- Декоратор `custom_decorator(message)` печатает сообщение **при возникновении ошибки** в декорируемой функции.
- Задать аргументы декоратору можно так: `@decor("info")`.

---

# 8) Практическая работа — решения

## 8.1 Декоратор `framed`: рамка `=` шириной 40
```py
from functools import wraps

def framed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("=" * 40)
        result = func(*args, **kwargs)
        print("=" * 40)
        return result
    return wrapper

@framed
def show_title():
    print("== Menu ==")

show_title()
```

## 8.2 Настраиваемая рамка: `@framed(width, symbol="=")`
```py
from functools import wraps

def framed(width, symbol="="):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(symbol * width)
            result = func(*args, **kwargs)
            print(symbol * width)
            return result
        return wrapper
    return decorator

@framed(30, "-")
def show_title():
    print("== Menu ==")

show_title()
```

---

# 9) Домашнее задание — решения

## ДЗ 1) `measure_time`: среднее время за 5 вызовов
Требования:
- выполнить функцию 5 раз,
- вывести среднее время,
- вывести результат.

✅ Практичный вариант: `time.perf_counter()` (точнее для измерений)
```py
import time
from functools import wraps

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        repeats = 5
        total = 0.0
        result = None

        for _ in range(repeats):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            total += time.perf_counter() - start

        avg = total / repeats
        print(f"Среднее время выполнения для {repeats} вызовов:")
        print(f"{avg:.4f} секунд")
        print(f"Результат: {result}")
        return result

    return wrapper
```

Пример:
```py
@measure_time
def compute():
    total = 0
    for i in range(10_000_00):
        total += i
    return total

compute()
```

## ДЗ 2) `measure_time(repeats)`: среднее время за N вызовов
```py
import time
from functools import wraps

def measure_time(repeats):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            total = 0.0
            result = None

            for _ in range(repeats):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                total += time.perf_counter() - start

            avg = total / repeats if repeats else 0.0
            print(f"Среднее время выполнения для {repeats} вызовов:")
            print(f"{avg:.4f} секунд")
            print(f"Результат: {result}")
            return result
        return wrapper
    return decorator
```

Пример:
```py
@measure_time(10)
def compute():
    total = 0
    for i in range(10_000_00):
        total += i
    return total

compute()
```

---

## Мини-шпаргалка
```text
Декоратор = функция, которая принимает функцию и возвращает wrapper.

def deco(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ...before...
        result = func(*args, **kwargs)
        ...after...
        return result
    return wrapper

Декоратор с аргументами:
def deco_factory(x):
    def deco(func):
        def wrapper(...): ...
        return wrapper
    return deco

Несколько декораторов:
@A
@B
def f(): ...
=> сначала применяется B, потом A (снизу вверх).
```
