# Функции области LEGB args kwargs return

## 0) О чём урок
- Что такое **функция** и зачем она нужна
- `def`, `pass`, **вызов** функции
- Аргументы: позиционные, именованные, по умолчанию, `*args`, `**kwargs` + порядок
- `return`: возврат значения, `None`, множественный возврат
- Области видимости: **LEGB**
- Ключевое слово **`global`**: когда нужно и когда лучше не использовать
- Практика + домашнее задание (с решениями)

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
