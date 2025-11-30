# Python Fundamentals — Урок 28: итераторы, `iter()`/`next()`, StopIteration, `itertools`, генераторные выражения

## 0) План занятия
- Итерируемый объект (iterable) и итератор (iterator)
- Магические методы `__iter__()` и `__next__()` и их аналоги `iter()`/`next()`
- StopIteration и как его избегать
- Как работает цикл `for` “под капотом”
- Оценка потребления памяти (`sys.getsizeof`)
- Модуль `itertools` (count/cycle/chain/product/permutations)
- Генераторное выражение (generator expression) и сравнение со списковым включением

---

## 1) Термины: iterable vs iterator
### Итерируемый объект (iterable)
Объект, который можно перебирать по элементам (список, строка, словарь, set, tuple и т.д.).  
Главное: у него есть способ **создать итератор**.

### Итератор (iterator)
Объект, который:
- возвращает элементы по одному,
- **помнит текущую позицию**,
- заканчивается исключением `StopIteration`.

Итератор содержит:
- ссылку на источник данных,
- текущую позицию,
- логику получения следующего элемента.

**Ключевая мысль:** все итераторы — итерируемые, но не все итерируемые — итераторы.

---

## 2) Магические методы итерации и аналоги
Итерация в Python основана на dunder-методах:

- `obj.__iter__()` → получить итератор
- `it.__next__()` → получить следующий элемент

Обычно так не пишут напрямую, потому что есть встроенные функции:

- `iter(obj)` вызывает `obj.__iter__()`
- `next(it)` вызывает `it.__next__()`

### Пример: “потраченный” итератор
```py
numbers = [10, 20, 30]
it = iter(numbers)

print(list(it))  # [10, 20, 30]
print(list(it))  # []  (итератор уже исчерпан)
```

### Пример: поэлементно через `next()`
```py
numbers = [10, 20, 30]
it = iter(numbers)

print(next(it))  # 10
print(next(it))  # 20
print(next(it))  # 30
```

---

## 3) StopIteration и как его избегать
Когда элементы закончились, `next()` выбрасывает `StopIteration`:
```py
numbers = [1, 2, 3]
it = iter(numbers)
print(next(it))
print(next(it))
print(next(it))
print(next(it))  # StopIteration
```

### Без ошибки: второй аргумент у `next()`
`next(it, default)` возвращает `default`, если итератор закончился:
```py
numbers = [1, 2, 3]
it = iter(numbers)

print(next(it, None))  # 1
print(next(it, None))  # 2
print(next(it, None))  # 3
print(next(it, None))  # None вместо StopIteration
```

---

## 4) Как работает `for` внутри
Цикл:
```py
for x in iterable:
    ...
```
эквивалентен “по смыслу”:
```py
it = iter(iterable)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    ...
```

**Из этого следует:** если вы один раз прошли `for` по итератору, повторный `for` по тому же итератору ничего не выведет (он исчерпан).

---

## 5) Итераторы и память (`sys.getsizeof`)
Итераторы экономят память, потому что **не хранят всю последовательность сразу**.

Пример сравнения:
```py
import sys

lst = [x for x in range(1_000_000)]
it = iter(lst)

print("Размер списка:", sys.getsizeof(lst), "байт")
print("Размер итератора:", sys.getsizeof(it), "байт")
```

---

## 6) Iterable vs Iterator — краткое сравнение
| Характеристика | Iterable | Iterator |
|---|---|---|
| Методы | `__iter__()` | `__iter__()` + `__next__()` |
| `next()` | нельзя (TypeError) | можно |
| Память | чаще хранит все элементы | выдаёт по одному |
| Повторный перебор | можно | нельзя (однократный) |
| Конец | не зависит от StopIteration | заканчивается StopIteration |

---

## 7) `itertools` — полезные итераторные инструменты
`itertools` помогает строить эффективные “ленивые” последовательности.

### 7.1 `count(start, step)` — бесконечный счётчик
```py
import itertools

counter = itertools.count(start=1, step=10)
print(next(counter))  # 1
print(next(counter))  # 11
print(next(counter))  # 21
```

### 7.2 `cycle(iterable)` — бесконечное повторение
```py
import itertools

cycler = itertools.cycle(["A", "B", "C"])
print(next(cycler))  # A
print(next(cycler))  # B
print(next(cycler))  # C
print(next(cycler))  # A
```

### 7.3 `chain(a, b, ...)` — объединение итерируемых
```py
import itertools

merged = itertools.chain([1, 2, 3], [100, 200, 300])
print(list(merged))  # [1, 2, 3, 100, 200, 300]
```

### 7.4 `product()` — декартово произведение
```py
import itertools

pairs = itertools.product([1, 2, 3], ["A", "B", "C"])
print(list(pairs))  # (1,'A'), (1,'B'), ...
```

### 7.5 `permutations(iterable, r=None)` — перестановки
```py
import itertools

letters = ["A", "B", "C"]
print(list(itertools.permutations(letters)))      # r = 3 по умолчанию
print(list(itertools.permutations(letters, 2)))   # r = 2
```

---

## 8) Генераторное выражение (generator expression)
Генераторное выражение создаёт **генератор**, который вычисляет значения “по запросу” (лениво).

Синтаксис:
```py
gen = (expression for item in iterable)
```

Пример:
```py
squares = (x**2 for x in range(5))
print(next(squares))  # 0
print(next(squares))  # 1
```

### Генераторное выражение vs списковое включение
| | `[ ... ]` list comprehension | `( ... )` generator expression |
|---|---|---|
| Результат | список | генератор |
| Память | хранит всё | почти не хранит |
| Доступ | по индексу | только `next()` / `for` |
| Повторный проход | можно | нельзя (исчерпается) |
| Лучше для | малых/средних наборов | больших/потоковых данных |

Проверка на памяти:
```py
import sys

list_comp = [x**2 for x in range(10**6)]
gen_expr  = (x**2 for x in range(10**6))

print(sys.getsizeof(list_comp))
print(sys.getsizeof(gen_expr))
```

### Генераторы в `any()` и `all()`
```py
words = ["apple", "Banana", "cherry", "Apricot"]
print(any(w[0].isupper() for w in words))  # есть ли слово с заглавной?
print(all(len(w) > 3 for w in words))      # все ли длиной > 3?
```

---

# Ответы на задания для закрепления (из урока)
## Задания 1
1) Про итераторы верно: **c, d**  
2) Про StopIteration верно: **a, c**  
3) Два `for` по одному итератору выведут: **b (5, 10, 15)**

## Задания 2
1) `itertools.cycle(["A","B","C"])` выведет: **A, B, C, A**  
2) Про генераторные выражения верно: **a, c**

---

# Практическая работа: генерация безопасных паролей (len=4)
**Условия:**
- длина пароля = 4
- минимум: 1 строчная, 1 заглавная, 1 цифра
- символы **не повторяются**
- **соседние символы не могут идти подряд в таблице символов** (разница `ord(...)` не равна 1)
- все валидные пароли записать в `valid_passwords.txt`

Решение (из урока, аккуратно оформлено):
```py
from itertools import permutations
from string import ascii_lowercase, ascii_uppercase, digits

all_chars = list(ascii_lowercase + ascii_uppercase + digits)

def is_valid(password: tuple[str, ...]) -> bool:
    has_lower = any(c in ascii_lowercase for c in password)
    has_upper = any(c in ascii_uppercase for c in password)
    has_digit = any(c in digits for c in password)
    if not (has_lower and has_upper and has_digit):
        return False

    for i in range(len(password) - 1):
        if abs(ord(password[i]) - ord(password[i + 1])) == 1:
            return False

    return True

all_variants = permutations(all_chars, 4)
valid_passwords = ("".join(p) for p in all_variants if is_valid(p))

with open("valid_passwords.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(valid_passwords))
```

> ⚠️ Примечание: это создаёт очень много вариантов. Для реальных задач обычно ограничивают пространство поиска или генерируют случайные пароли, а не “все возможные”.

---

# Домашнее задание (решения)

## ДЗ 1) Планировщик на неделю (бесконечный вывод по Enter)
Условие: показывать план на следующий день недели, пока пользователь жмёт Enter. Если ввёл `q` — выйти.

```py
import itertools

weekly_schedule = {
    "Monday": ["Gym", "Work", "Read book"],
    "Tuesday": ["Meeting", "Work", "Study Python"],
    "Wednesday": ["Shopping", "Work", "Watch movie"],
    "Thursday": ["Work", "Call parents", "Play guitar"],
    "Friday": ["Work", "Dinner with friends"],
    "Saturday": ["Hiking", "Rest"],
    "Sunday": ["Family time", "Rest"],
}

days = list(weekly_schedule.keys())
cycler = itertools.cycle(days)

while True:
    cmd = input("Нажмите 'Enter' для получения плана (q - выход): ")
    if cmd.strip().lower() == "q":
        break

    day = next(cycler)
    plan = ", ".join(weekly_schedule[day])
    print(f"{day}: {plan}")
```

## ДЗ 2) Объединение списков продуктов → генератор (нижний регистр)
```py
from typing import Iterable, Generator

def merge_products(*lists: Iterable[str]) -> Generator[str, None, None]:
    return (item.lower() for seq in lists for item in seq)

fruits = ["Apple", "Banana", "Orange"]
vegetables = ["Carrot", "Tomato", "Cucumber"]
dairy = ["Milk", "Cheese", "Yogurt"]

gen = merge_products(fruits, vegetables, dairy)
for item in gen:
    print(item)
```

## ДЗ 3) Комбинации одежды (clothes × colors × sizes)
```py
import itertools

clothes = ["T-shirt", "Jeans", "Jacket"]
colors = ["Red", "Blue", "Black"]
sizes = ["S", "M", "L"]

for cl, col, sz in itertools.product(clothes, colors, sizes):
    print(f"{cl} - {col} - {sz}")
```

---

## Мини-шпаргалка
```text
Iterable: можно перебирать (list/str/dict/tuple/...) -> iter(obj)
Iterator: iter(obj) -> it, next(it) -> следующий, в конце StopIteration

iter(obj)  == obj.__iter__()
next(it)   == it.__next__()
next(it, default) -> default вместо StopIteration

for x in iterable:
  it = iter(iterable)
  while True:
    try: x = next(it)
    except StopIteration: break

itertools:
- count(start, step) -> бесконечные числа
- cycle(seq)         -> бесконечный цикл по seq
- chain(a,b,...)     -> склеить итерируемые
- product(a,b,...)   -> декартово произведение
- permutations(seq,r)-> перестановки

Generator expression:
(x for x in iterable) -> лениво, экономит память, одноразовый
```
