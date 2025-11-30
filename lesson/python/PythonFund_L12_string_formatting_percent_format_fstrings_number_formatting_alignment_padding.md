# Python Fundamentals — Урок 12: строки — форматирование (`%`, `format()`, f-строки) + формат чисел и выравнивание

## 1) Что такое форматирование строк
**Форматирование строк** — способ вставить значения переменных (или результаты выражений) внутрь строки.

В Python чаще всего используют:
1) старый стиль **C-style** через оператор `%`
2) метод **`str.format()`**
3) **f-строки** (Python 3.6+)

---

## 2) C-style форматирование (оператор `%`)
### 2.1 Синтаксис
```py
"форматирующая строка" % (значения)
```

Форматирующая строка содержит **спецификаторы**, начинающиеся с `%`.

### 2.2 Частые спецификаторы
- `%s` — строка (на практике: почти любое значение превратится в строку)
- `%d` — целое число (`int`)
- `%f` — число с плавающей точкой (`float`)
- `%.2f` — float с 2 знаками после запятой

### 2.3 Примеры
```py
name = "Alice"
age = 30
text = "My name is %s and I am %d years old." % (name, age)
print(text)

pi = 3.14159
text = "The value of pi is approximately %.2f." % pi
print(text)
```

### 2.4 Важно: типы должны подходить
`%d` ждёт число, не строку. Если перепутать — будет ошибка.

```py
name = "Alice"
age = 30

# Ошибка: %d ожидает число, но получит строку name
text = "My name is %d and I am %s years old." % (name, age)
```

---

## 3) Метод `format()`
### 3.1 База: плейсхолдеры `{}` в строке
```py
text = "My name is {} and I am {} years old."
print(text.format("Alice", 30))
```

### 3.2 Именованные аргументы
```py
text = "My name is {name} and I am {age} years old. Are you also {age}?"
print(text.format(name="Bob", age=25))
```

### 3.3 Индексы (позиции)
```py
text = "Her name is {0} and she is {1} years old. {0} loves Python."
print(text.format("Anna", 28))
```

### 3.4 Комбинация позиционных и именованных
```py
text = "The {0} is {color}."
print(text.format("sky", color="blue"))
```

---

## 4) f-строки (рекомендуемый стиль)
### 4.1 Синтаксис
```py
name = "Alice"
age = 25
text = f"My name is {name} and I am {age} years old."
print(text)
```

### 4.2 Вставка выражений и вызовов функций
```py
x = 10
y = 20
print(f"The sum of {x} and {y} is {x + y}.")

text = "Python"
print(f"Length: {len(text)}, upper: {text.upper()}")
```

### 4.3 Многострочные f-строки
```py
name = "Charlie"
age = 30

info = f"""Info
Name: {name}
Age: {age}
"""
print(info)
```

---

## 5) Форматирование чисел (точность, тысячи, выравнивание)
Форматирование чисел одинаково работает в:
- `format()` → `"{:.2f}".format(pi)`
- f-строках → `f"{pi:.2f}"`

### 5.1 Количество знаков после запятой (`.nf`)
```py
pi = 3.14159
print(f"Pi: {pi:.2f}")                 # 3.14
print("Pi: {:.2f}".format(pi))         # 3.14
print("Pi: {num:.2f}".format(num=pi))  # 3.14
```

### 5.2 Разделители тысяч (`,`)
```py
large_number = 1234567890
print(f"{large_number:,}")         # 1,234,567,890
print("{:,}".format(large_number)) # 1,234,567,890
```

---

## 6) Выравнивание и ширина поля (в формат-спеке)
Формат-спека в `{...:spec}`:
- `<` — влево
- `>` — вправо
- `^` — по центру
- число = **ширина поля**
- можно указать символ заполнения **до** выравнивания

### 6.1 Примеры выравнивания
```py
print(f"start_{'text':>10}_end")  # вправо
print(f"start_{'text':<10}_end")  # влево
print(f"start_{'text':^10}_end")  # по центру
```

То же через `format()`:
```py
print("start_{:>10}_end".format("text"))
print("start_{:<10}_end".format("text"))
print("start_{:^10}_end".format("text"))
```

### 6.2 Минимальная ширина без явного выравнивания
- для чисел по умолчанию чаще “вправо”
- для строк чаще “влево”

```py
number = 40
print(f"start_{number:5}_end")       # поле шириной 5
print("start_{:5}_end".format("hi")) # строка в поле шириной 5
```

### 6.3 Заполнение (padding) другим символом
```py
number = 40
print(f"{number:0>5}")      # 00040 (заполнение нулями слева)

print(f"{'Python':_^10}")   # __Python__ (подчёркивания, центр)
```

---

## 7) Методы выравнивания строк: `ljust`, `rjust`, `center`
Иногда проще использовать методы строки:

- `s.ljust(width, fillchar=' ')` — влево
- `s.rjust(width, fillchar=' ')` — вправо
- `s.center(width, fillchar=' ')` — по центру

```py
text = "Python"

print(text.ljust(15))
print(text.ljust(15, '-'))

print(text.rjust(15))
print(text.rjust(15, '-'))

print(text.center(15))
print(text.center(15, '-'))
```

---

## 8) Практическая работа (готовые решения)

### 8.1 Счётчик слов (нумерация, Capitalize, выравнивание влево 15)
Задача: вводим строку → выводим каждое слово: `N. Word` и выравниваем слово по левому краю в 15 символов.

```py
text = input("Введите строку: ")
words = text.split()

for i, word in enumerate(words, start=1):
    print(f"{i}. {word.capitalize():<15}")
```

### 8.2 Формат даты `dd/mm/yyyy` (день и месяц — 2 цифры)
```py
day = int(input("Введите день: "))
month = int(input("Введите месяц: "))
year = int(input("Введите год: "))

formatted_date = "{:02}/{:02}/{}".format(day, month, year)
print(f"Дата: {formatted_date}")
```

---

## 9) Домашнее задание (решения)

### 9.1 Сумма положительных чисел + формат “деньги”
Дано:
```py
numbers = [1245.4435, -302.1403, 87459.99, -520.8265, 1450.001]
```

Нужно:
- суммировать только положительные
- вывести как деньги: **`$` в начале**, **2 знака**, **разделители тысяч запятой**

```py
numbers = [1245.4435, -302.1403, 87459.99, -520.8265, 1450.001]

total = 0.0
for x in numbers:
    if x > 0:
        total += x

print(f"Сумма положительных чисел: ${total:,.2f}")
```

### 9.2 “Счета клиентов” (парсинг строк + выравнивание)
Дано:
```py
data_list = [
    "John 23 12345.678",
    "Alice 30 200.50",
    "Bob 35 15000.3",
    "Charlie 40 500.75"
]
```

Нужно вывести:
- имя — 10 символов
- возраст — 3 символа
- баланс — 10 символов, 2 знака после запятой

```py
data_list = [
    "John 23 12345.678",
    "Alice 30 200.50",
    "Bob 35 15000.3",
    "Charlie 40 500.75"
]

for row in data_list:
    name, age, balance = row.split()
    age = int(age)
    balance = float(balance)

    print(f"Имя: {name:<10} | Возраст: {age:>3} | Баланс: {balance:>10.2f}")
```

---

## 10) Мини-шпаргалка формат-спеки
```text
{value:.2f}   -> 2 знака после запятой (float)
{value:,}     -> разделители тысяч
{value:>10}   -> вправо ширина 10
{value:<10}   -> влево ширина 10
{value:^10}   -> центр ширина 10
{value:0>5}   -> заполнение нулями слева ширина 5
{'Python':_^10} -> центр + заполнение '_'
```
