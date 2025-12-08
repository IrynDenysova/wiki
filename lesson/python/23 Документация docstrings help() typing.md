# Документация docstrings help() typing

## 1) Документация и docstrings
**Документация** — описание кода, которое помогает понять, как работают функции/классы/модули, и облегчает поддержку.

**Docstring** — строка документации в тройных кавычках `"""..."""` (или `'''...'''`), которая является частью объекта и доступна через `help()`.

### 1.1 Шаблон docstring (простая форма)
```py
def function_name(param1, param2):
    """
    Описание функции.

    :param param1: Описание первого параметра.
    :param param2: Описание второго параметра.
    :return: Описание возвращаемого значения.
    """
    ...
```

### 1.2 Пример
```py
def greet(name: str) -> str:
    """
    Принимает имя и возвращает строку приветствия.

    :param name: Имя пользователя.
    :return: Приветственное сообщение.
    """
    return f"Hello, {name}!"
```

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
