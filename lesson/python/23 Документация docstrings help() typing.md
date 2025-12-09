# Документация docstrings help() typing

## 📖 Быстрая навигация по операторам и функциям

- [[#1) Документация и docstrings]](#1-документация-и-docstrings)
- [[#2) Автогенерация docstrings в IDE]](#2-автогенерация-docstrings-в-ide)
- [[#3) `help()` — встроенная справка]](#3-help-—-встроенная-справка)
- [[#4) Аннотации типов (type hints)]](#4-аннотации-типов-type-hints)
- [[#5) Any, Union, Optional, Callable]](#5-any-union-optional-callable)
- [[#6) Передача неизменяемых и изменяемых объектов в функции]](#6-передача-неизменяемых-и-изменяемых-объектов-в-функции)
- [[#1) Ошибка в коде]](#1-ошибка-в-коде)
- [[#2) Что будет при неправильном типе аргумента?]](#2-что-будет-при-неправильном-типе-аргумента)
- [[#3) Разница между `tuple[str, int]` и `list[str]`]](#3-разница-между-tuplestr-int-и-liststr)
- [[#Практика 1) Список строк → словарь длин (с docstring и type hints)]](#практика-1-список-строк-→-словарь-длин-с-docstring-и-type-hints)
- [[#Практика 2) Генерация отчёта (Optional список достижений)]](#практика-2-генерация-отчёта-optional-список-достижений)
- [[#Практика 3) Применить функцию ко всем элементам списка (Callable + Any)]](#практика-3-применить-функцию-ко-всем-элементам-списка-callable-any)
- [[#ДЗ 1) Объединение данных в строку через `" | "`]](#дз-1-объединение-данных-в-строку-через)
- [[#ДЗ 2) Сумма вложенных чисел в списке словарей]](#дз-2-сумма-вложенных-чисел-в-списке-словарей)
- [[#Мини-шпаргалка]](#мини-шпаргалка)
- [[#Дополнительная информация]](#дополнительная-информация)


---

## 2) Автогенерация docstrings в IDE
В PyCharm / VS Code часто можно набрать `"""` сразу под строкой `def ...:` и нажать Enter — IDE подставит каркас:
```py
def greet(name):
    """
    :param name:
    :return:
    """
    return f"Hello, {name}!"
```

---

## 3) `help()` — встроенная справка
`help()` показывает документацию по объекту (docstring, методы, атрибуты).

### 3.1 Синтаксис
```py
help(object)
```
Если вызвать **без аргумента** — откроется интерактивный режим:
```py
help()
```

### 3.2 Пример
```py
help(sum)   # справка по встроенной функции
help(str)   # методы и атрибуты строк
help(print) # документация по print()
```

✅ Ответ на вопрос из урока: `help(print)` выведет документацию по `print()`.

---

## 4) Аннотации типов (type hints)
**Аннотации типов** — подсказки, какие типы ожидаются на входе/выходе и у переменных.

Важно:
- Python остаётся **динамически типизированным**.
- Аннотации **не проверяются** автоматически во время выполнения (ошибку поиска типов найдут IDE/линтеры/статические анализаторы).

### 4.1 Синтаксис
```py
def function_name(param: type1, ...) -> return_type:
    ...

variable: type = value
```

### 4.2 Базовые типы
```py
def add(a: int, b: int) -> int:
    return a + b

def convert_to_celsius(f: float) -> float:
    return (f - 32) * 5 / 9

def is_even(n: int) -> bool:
    return n % 2 == 0

def log_message(message: str) -> None:
    print(message)
```

### 4.3 Аннотации для коллекций (Python 3.9+)
- `list[int]`
- `tuple[str, int]` или `tuple[int, ...]`
- `set[str]`
- `frozenset[int]`
- `dict[str, int]`

Примеры:
```py
def process_numbers(numbers: list[int]) -> list[int]:
    return [n ** 2 for n in numbers]

def get_info() -> tuple[str, float]:
    return "Bob", 4.91

def variable_tuple() -> tuple[int, ...]:
    return 5, 8, 2

def unique_chars(text: str) -> set[str]:
    return set(text)

def count_words(text: str) -> dict[str, int]:
    words = text.split()
    return {word: words.count(word) for word in words}
```

### 4.4 Старый стиль (Python < 3.9): модуль `typing`
```py
from typing import List, Dict, Tuple, Set

def process_numbers_old(numbers: List[int]) -> List[int]:
    return [n ** 2 for n in numbers]
```

---

## 5) Any, Union, Optional, Callable
Иногда тип может быть разным — для этого используют `typing`.

### 5.1 `Any` — “любой тип”
```py
from typing import Any

def process_data(data: Any) -> str:
    return f"Данные: {data}"
```

### 5.2 `Union` — один из нескольких типов
```py
from typing import Union

def calculate(value: Union[int, float]) -> float:
    return value ** 2
```

### 5.3 `Optional[T]` — значение может быть `None`
`Optional[str]` = `Union[str, None]`.
```py
from typing import Optional

def get_user_name(user_id: int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)  # может вернуть None
```

### 5.4 `Union` через `|` (Python 3.10+)
```py
def calculate(value: int | float) -> float:
    return value ** 2
```

### 5.5 `Callable` — параметр “ожидается функция”
```py
from typing import Callable

def execute_function(func: Callable[[int, int], int],
                     nums1: list[int],
                     nums2: list[int]) -> list[int]:
    return [func(a, b) for a, b in zip(nums1, nums2)]
```

---

## 6) Передача неизменяемых и изменяемых объектов в функции
Идея:
- В Python передаётся **ссылка на объект**.
- Но эффект зависит от **изменяемости**.

### 6.1 Неизменяемые (immutable): `int`, `float`, `bool`, `str`, `tuple`, `frozenset`
Если “изменить” внутри функции — создаётся новый объект, оригинал остаётся прежним:
```py
def modify_value(n: int) -> None:
    print("До:", n, id(n))
    n += 1           # создаётся новый объект
    print("После:", n, id(n))

num = 10
modify_value(num)
print("Снаружи:", num, id(num))
```

### 6.2 Изменяемые (mutable): `list`, `dict`, `set`
Изменения внутри функции затронут оригинал:
```py
def modify_list(lst: list[int]) -> None:
    print("До:", lst, id(lst))
    lst.append(99)
    print("После:", lst, id(lst))

my_list = [1, 2, 3]
modify_list(my_list)
print("Снаружи:", my_list, id(my_list))
```

### 6.3 Как избежать нежелательных изменений
- поверхностная копия: `copy()`
- глубокая копия: `deepcopy()` для вложенных структур

```py
from copy import deepcopy

def safe_modify_list(lst: list[int]) -> list[int]:
    copy_lst = lst.copy()
    copy_lst.append(99)
    return copy_lst

original = [1, 2, 3]
new_list = safe_modify_list(original)
print("Оригинал:", original)
print("Копия:", new_list)

nested = [[1], [2]]
nested_copy = deepcopy(nested)
nested_copy[0].append(999)
print(nested, nested_copy)
```

---

# Задания для закрепления (короткие ответы)

## 1) Ошибка в коде
Было:
```py
def greet(name: str) -> str:
    print(f"Hello, {name}!")

result = greet("Alice")
print(result.upper())
```
Проблема: `greet()` ничего не возвращает → `result` будет `None`, у `None` нет `.upper()`.

✅ Исправление:
```py
def greet(name: str) -> str:
    return f"Hello, {name}!"

result = greet("Alice")
print(result.upper())
```

## 2) Что будет при неправильном типе аргумента?
Аннотации типов **не проверяются** при выполнении: код может отработать, но возможны неожиданные ошибки/поведение.

## 3) Разница между `tuple[str, int]` и `list[str]`
- `tuple[str, int]` — кортеж **фиксированной длины** из двух элементов: `str` и `int`
- `list[str]` — список **произвольной длины**, где каждый элемент — `str`

---

# Практика (решения)

## Практика 1) Список строк → словарь длин (с docstring и type hints)
```py
def get_word_lengths(words: list[str]) -> dict[str, int]:
    """
    Возвращает словарь, где ключи — строки, а значения — длины этих строк.

    :param words: Список строк.
    :return: Словарь длины слов.
    """
    return {word: len(word) for word in words}

words = ["apple", "banana", "cherry"]
print(get_word_lengths(words))
```

## Практика 2) Генерация отчёта (Optional список достижений)
```py
from typing import Optional

def generate_report(name: str, achievements: Optional[list[str]] = None) -> str:
    """
    Генерирует отчёт о достижениях пользователя.

    :param name: Имя пользователя.
    :param achievements: Список достижений (необязательный).
    :return: Текст отчёта.
    """
    if not achievements:
        return f"{name}: Нет достижений"
    return f"{name}: {', '.join(achievements)}"

print(generate_report("Alice", ["Won chess tournament", "Completed marathon"]))
print(generate_report("Bob"))
```

## Практика 3) Применить функцию ко всем элементам списка (Callable + Any)
```py
from typing import Callable, Any

def apply_to_all(func: Callable[[Any], Any], elements: list[Any]) -> list[Any]:
    """
    Применяет переданную функцию ко всем элементам списка.

    :param func: Функция обработки одного элемента.
    :param elements: Список произвольных элементов.
    :return: Новый список результатов.
    """
    return [func(x) for x in elements]

numbers = [1, 2, 3, 4, 5]
print(apply_to_all(lambda x: x * 2, numbers))
```

---

# Домашнее задание (решения)

## ДЗ 1) Объединение данных в строку через `" | "`
Условие: функция принимает список любых данных и возвращает строковое представление, объединённое через `" | "`. Нужны docstring + type hints.

```py
from typing import Any

def join_as_string(data: list[Any]) -> str:
    """
    Преобразует элементы списка в строки и объединяет их через ' | '.

    :param data: Список элементов любых типов (числа, строки, списки, словари и т.д.).
    :return: Одна строка с объединёнными элементами.
    """
    return " | ".join(str(x) for x in data)

data = [42, "hello", [1, 2, 3], {"a": 1, "b": 2}]
print(join_as_string(data))
```

## ДЗ 2) Сумма вложенных чисел в списке словарей
Условие: список словарей вида `{"name": str, "scores": list[int]}`. Вернуть сумму всех чисел. Нужны docstring + type hints.

```py
def sum_all_scores(data: list[dict[str, object]]) -> int:
    """
    Считает сумму всех чисел из списков scores во входных словарях.

    Ожидается структура:
    - каждый элемент data — словарь с ключами:
      - "name": str
      - "scores": list[int]

    :param data: Список словарей с именем и списком баллов.
    :return: Сумма всех баллов.
    """
    total = 0
    for item in data:
        scores = item.get("scores", [])
        for score in scores:          # score должен быть int
            total += int(score)
    return total

data = [
    {"name": "Alice", "scores": [10, 20, 30]},
    {"name": "Bob", "scores": [5, 15, 25]},
    {"name": "Charlie", "scores": [7, 17, 27]},
]
print("Итоговый балл:", sum_all_scores(data))
```

> Если хочешь “строже” по типам, можно использовать `TypedDict` (это уже следующий уровень).

---

## Мини-шпаргалка
```text
Docstring:
"""Описание..."""  -> доступно через help()

help(obj) -> документация по объекту
help()    -> интерактивная справка

Type hints:
def f(a: int) -> str: ...
x: list[int] = ...

typing:
Any, Union, Optional, Callable
Optional[T] == Union[T, None]
Python 3.10+: int | float

Mutable vs immutable:
- immutable (int/str/tuple/...) “изменяется” через создание нового объекта
- mutable (list/dict/set) меняется на месте, влияет на оригинал
- безопасно: lst.copy() / deepcopy(...)
```


---

## Дополнительная информация

### Важные концепции для изучения

#### 1. Docstring форматы и стандарты
```python
# Google стиль docstring
def add(a, b):
    """Складывает два числа и возвращает результат.
    
    Args:
        a: Первое число
        b: Второе число
    
    Returns:
        Сумма a и b
    
    Raises:
        TypeError: Если a или b не числа
    
    Example:
        >>> add(2, 3)
        5
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Оба аргумента должны быть числами")
    return a + b

# NumPy стиль docstring
def multiply(x, y):
    """Умножает два числа.
    
    Parameters
    ----------
    x : int or float
        Первое число
    y : int or float
        Второе число
    
    Returns
    -------
    int or float
        Произведение x и y
    
    See Also
    --------
    add : Функция сложения
    
    Examples
    --------
    >>> multiply(3, 4)
    12
    """
    return x * y

# reStructuredText (Sphinx) стиль
def divide(a, b):
    """Делит a на b.
    
    :param a: Делимое
    :type a: float
    :param b: Делитель
    :type b: float
    :returns: Результат деления
    :rtype: float
    :raises ZeroDivisionError: Если b равен нулю
    """
    if b == 0:
        raise ZeroDivisionError("Деление на ноль")
    return a / b

# PEP 257 - минимальный стиль
def greet(name):
    """Return a greeting for name."""
    return f"Hello, {name}!"

print(greet.__doc__)  # Доступ к docstring
help(greet)  # Встроенная справка
```

#### 2. Type hints и аннотации типов
```python
from typing import List, Dict, Tuple, Optional, Union, Callable

# Базовые аннотации
def greet(name: str) -> str:
    """Приветствует человека."""
    return f"Привет, {name}!"

# Сложные типы
def process_numbers(numbers: List[int]) -> Dict[str, float]:
    """Обрабатывает список чисел."""
    return {
        'sum': sum(numbers),
        'avg': sum(numbers) / len(numbers) if numbers else 0
    }

# Optional - может быть None
def find_user(user_id: int) -> Optional[Dict]:
    """Находит пользователя или возвращает None."""
    users = {1: {'name': 'Alice'}, 2: {'name': 'Bob'}}
    return users.get(user_id)

# Union - несколько возможных типов
def convert_to_number(value: Union[str, int, float]) -> float:
    """Конвертирует значение в число."""
    return float(value)

# Tuple с конкретными типами
def get_user_info() -> Tuple[str, int, str]:
    """Возвращает (имя, возраст, email)."""
    return "Alice", 30, "alice@example.com"

# Callable - функция как аргумент
def apply_operation(a: int, b: int, operation: Callable[[int, int], int]) -> int:
    """Применяет операцию к двум числам."""
    return operation(a, b)

# Использование
result = apply_operation(5, 3, lambda x, y: x + y)
print(result)  # 8

# TypeVar - общие типы (дженерики)
from typing import TypeVar

T = TypeVar('T')  # Может быть любой тип

def get_first(items: List[T]) -> T:
    """Возвращает первый элемент списка."""
    return items[0]

# Использование
print(get_first([1, 2, 3]))  # 1
print(get_first(['a', 'b']))  # 'a'
```

#### 3. Встроенная функция help()
```python
# help() показывает документацию
def calculate(x: int, y: int) -> int:
    """Складывает два числа.
    
    Args:
        x: Первое число
        y: Второе число
    
    Returns:
        Сумма x и y
    """
    return x + y

# Разные способы вызова help()
help(calculate)  # Справка о функции
help(list.append)  # Справка о методе
help(int)  # Справка о типе
help()  # Интерактивная справка

# Доступ к атрибутам документации
print(calculate.__doc__)  # Docstring
print(calculate.__name__)  # Имя функции
print(calculate.__module__)  # Модуль
print(calculate.__annotations__)  # Типы параметров

# Интроспекция функции
import inspect

sig = inspect.signature(calculate)
print(sig)  # (x: int, y: int) -> int

for param_name, param in sig.parameters.items():
    print(f"{param_name}: {param.annotation}")
```

#### 4. Проверка типов с mypy
```python
# Type checking может выполняться статически инструментом mypy
# Установка: pip install mypy
# Использование: mypy script.py

def process(numbers: List[int]) -> int:
    return sum(numbers)

# ✅ Правильно
result = process([1, 2, 3])

# ❌ mypy предупредит об ошибке типа
# result = process(["1", "2", "3"])  # Error: List[str] incompatible with List[int]

# Cast - явное приведение типа для mypy
from typing import cast

value = "123"
num = cast(int, int(value))  # Говорит mypy что это int
```

### 💡 Практические примеры

#### Пример 1: Самодокументируемый класс
```python
from typing import List, Optional

class Person:
    """Представляет человека с личной информацией.
    
    Attributes:
        name: Имя человека
        age: Возраст в годах
        email: Email адрес
        skills: Список навыков
    """
    
    def __init__(self, name: str, age: int, email: str) -> None:
        """Инициализирует новую персону.
        
        Args:
            name: Полное имя
            age: Возраст (должен быть положительным)
            email: Email адрес
        
        Raises:
            ValueError: Если age отрицательный
        """
        if age < 0:
            raise ValueError("Возраст не может быть отрицательным")
        
        self.name = name
        self.age = age
        self.email = email
        self.skills: List[str] = []
    
    def add_skill(self, skill: str) -> None:
        """Добавляет навык к списку."""
        if skill not in self.skills:
            self.skills.append(skill)
    
    def get_info(self) -> str:
        """Возвращает информацию о персоне."""
        return f"{self.name}, {self.age} лет, {self.email}"
    
    def years_until_retirement(self, retirement_age: int = 65) -> int:
        """Вычисляет годы до пенсии.
        
        Args:
            retirement_age: Возраст выхода на пенсию (по умолчанию 65)
        
        Returns:
            Количество лет до пенсии (может быть отрицательным)
        """
        return retirement_age - self.age

# Использование
person = Person("Alice", 30, "alice@example.com")
person.add_skill("Python")
person.add_skill("SQL")

print(person.get_info())
print(f"Годы до пенсии: {person.years_until_retirement()}")
```

#### Пример 2: Функция с подробной документацией
```python
from typing import List, Dict, Tuple
import re

def analyze_text(text: str) -> Dict[str, any]:
    """Анализирует текст и возвращает статистику.
    
    Функция подсчитывает различные метрики текста включая
    количество слов, предложений, символов и частоту слов.
    
    Args:
        text: Входной текст для анализа
    
    Returns:
        Словарь с ключами:
            - 'characters': Количество символов (без пробелов)
            - 'words': Количество слов
            - 'sentences': Количество предложений
            - 'avg_word_length': Средняя длина слова
            - 'word_frequency': Counter самых частых слов
    
    Raises:
        ValueError: Если text пустой или None
    
    Examples:
        >>> result = analyze_text("Hello. World!")
        >>> result['words']
        2
        >>> result['sentences']
        2
    """
    if not text or not isinstance(text, str):
        raise ValueError("Text должен быть непустой строкой")
    
    # Подсчет метрик
    chars = len(text.replace(' ', ''))
    words = len(text.split())
    sentences = len(re.split(r'[.!?]+', text))
    
    word_list = text.lower().split()
    avg_length = sum(len(w) for w in word_list) / len(word_list) if word_list else 0
    
    from collections import Counter
    word_freq = Counter(word_list).most_common(5)
    
    return {
        'characters': chars,
        'words': words,
        'sentences': sentences,
        'avg_word_length': round(avg_length, 2),
        'word_frequency': word_freq
    }

# Использование с help
help(analyze_text)
```

#### Пример 3: Документирование сложной функции с примерами
```python
def binary_search(sorted_list: List[int], target: int) -> Optional[int]:
    """Бинарный поиск в отсортированном списке.
    
    Использует алгоритм бинарного поиска для эффективного
    поиска элемента в отсортированном списке.
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    Args:
        sorted_list: Отсортированный в возрастающем порядке список
        target: Значение для поиска
    
    Returns:
        Индекс найденного элемента или None если не найден
    
    Raises:
        ValueError: Если список не отсортирован
    
    Examples:
        >>> binary_search([1, 3, 5, 7, 9, 11], 7)
        3
        >>> binary_search([1, 3, 5, 7, 9, 11], 4)
        None
        >>> binary_search([], 5)
        None
    """
    # Проверка сортировки
    if sorted_list != sorted(sorted_list):
        raise ValueError("Список должен быть отсортирован")
    
    left, right = 0, len(sorted_list) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return None

# Примеры из docstring можно тестировать
import doctest
doctest.testmod()  # Проверяет примеры в docstring
```

### 🚨 Частые ошибки

**Ошибка 1: Неправильный формат docstring**
```python
# ❌ НЕПРАВИЛЬНО - неполная информация
def calculate(a, b):
    """Что-то считает."""
    return a + b

# ✅ ПРАВИЛЬНО - подробная документация
def calculate(a: int, b: int) -> int:
    """Складывает два целых числа.
    
    Args:
        a: Первое число
        b: Второе число
    
    Returns:
        Сумма a и b
    """
    return a + b
```

**Ошибка 2: Type hints не проверяются во время выполнения
```python
def add(a: int, b: int) -> int:
    return a + b

# ✅ Type hints не блокируют ошибочный вызов
result = add("5", "3")  # Работает! Возвращает "53"
print(result)  # "53"

# Для проверки типов используйте:
from typing import get_type_hints
hints = get_type_hints(add)
print(hints)  # {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}
```

**Ошибка 3: Забыли описать исключения**
```python
# ❌ НЕПРАВИЛЬНО
def divide(a, b):
    """Делит a на b."""
    return a / b  # Может вызвать ZeroDivisionError!

# ✅ ПРАВИЛЬНО
def divide(a: float, b: float) -> float:
    """Делит a на b.
    
    Args:
        a: Делимое
        b: Делитель
    
    Returns:
        Результат деления
    
    Raises:
        ZeroDivisionError: Если b равен нулю
    """
    if b == 0:
        raise ZeroDivisionError("Деление на ноль")
    return a / b
```

**Ошибка 4: Type hints создают циклические импорты**
```python
# ❌ ПРОБЛЕМА - циклический импорт
# from typing import List
# def func(items: List['MyClass']) -> None:
#     pass
# class MyClass: ...

# ✅ РЕШЕНИЕ - использовать строковый форвард-рефе
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from my_module import MyClass

def func(items: List['MyClass']) -> None:
    pass
```

### 📌 Полезные ресурсы
- [PEP 257 - Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [Модуль typing](https://docs.python.org/3/library/typing.html)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [mypy - Static Type Checker](https://www.mypy-lang.org/)
