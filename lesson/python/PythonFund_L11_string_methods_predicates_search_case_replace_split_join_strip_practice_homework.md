# Python Fundamentals — Урок 11: методы строк (str)

## 1) Важно помнить
- Строки **неизменяемые (immutable)**: методы строк возвращают **новую** строку и не меняют исходную.
- Методы строк вызываются так: `text.method(...)`.

---

## 2) Предикатные методы (возвращают `True` / `False`)
Используются, чтобы проверить “какая это строка”.

### 2.1 Базовые
- `isalpha()` — только буквы (без пробелов, цифр, знаков)
- `isdigit()` — только цифры
- `isalnum()` — только буквы и цифры
- `isspace()` — только пробельные символы (пробел, таб, перенос строки и т.п.)
- `islower()` — все буквенные символы в нижнем регистре
- `isupper()` — все буквенные символы в верхнем регистре
- `istitle()` — каждое слово начинается с заглавной буквы
- `startswith(prefix)` — начинается с подстроки `prefix`
- `endswith(suffix)` — заканчивается подстрокой `suffix`

### 2.2 Более специфичные
- `isdecimal()` — только десятичные цифры (строже, чем `isdigit`)
- `isnumeric()` — “числовые” символы (может включать дробные/надстрочные символы)
- `isascii()` — только ASCII-символы
- `isprintable()` — все символы “печатаемые” (например, `
` сделает `False`)
- `isidentifier()` — можно ли использовать строку как имя переменной в Python

Примеры:
```py
print("Hello".isalpha())       # True
print("Python3".isalpha())     # False

print("12345".isdigit())       # True
print("12345.1".isdigit())     # False (точка мешает)

print("Hello123".isalnum())    # True
print(" ".isspace())           # True

print("HELLO".isupper())       # True
print("Hello".islower())       # False
print("Hello World".istitle()) # True/False зависит от регистра слов

print("Hello world".startswith("Hello"))  # True
print("Hello world!".endswith("world"))   # False (есть "!")
```

---

## 3) Поиск подстроки в строке
### 3.1 `find()` / `rfind()`
- `find(sub)` — индекс **первого** вхождения, если нет — `-1`
- `rfind(sub)` — индекс **последнего** вхождения, если нет — `-1`

```py
text = "Python is awesome. Python is dynamic."
print(text.find("Python"))   # 0
print(text.rfind("Python"))  # 19 (примерно, зависит от текста)
print(text.find("Java"))     # -1
```

### 3.2 `index()` / `rindex()`
То же, что `find/rfind`, но если подстроки нет — будет **ошибка `ValueError`**.

```py
text = "Python is awesome. Python is dynamic."
print(text.index("Python"))   # 0
print(text.rindex("Python"))  # 19 (примерно)
# print(text.index("Java"))   # ValueError
```

### 3.3 `count()`
`count(sub)` — количество вхождений.
- безопасно: если нет подстроки → `0`
- считает **без пересечений** (overlap не учитывается)

```py
print("33333".count("33"))     # 2 (позиции 0-1 и 2-3)
print("hahahahahaha".count("ha"))   # 6
print("hahahahahaha".count("haha")) # 3
```

---

## 4) Методы изменения регистра
- `upper()` — всё в верхний регистр
- `lower()` — всё в нижний регистр
- `capitalize()` — первая буква заглавная, остальные строчные
- `title()` — первая буква каждого слова заглавная
- `swapcase()` — меняет регистр на противоположный
- `casefold()` — “усиленный lower” для корректного сравнения (языковые особенности)

```py
text = "Hello, worlD!"
print(text.upper())       # HELLO, WORLD!
print(text.lower())       # hello, world!
print(text.capitalize())  # Hello, world!
print(text.title())       # Hello, World!
print(text.swapcase())    # hELLO, WORLd!

print("Straße".casefold()) # strasse
```

---

## 5) `replace()` — замена подстроки
Синтаксис:
```py
new_text = text.replace(old, new, count=-1)
```

- `old` — что заменить
- `new` — на что заменить
- `count` — сколько замен сделать (если не задано, заменяет **все**)

```py
text = "I love Python, Python is great"
print(text.replace("Python", "Java"))

text = "apple apple apple"
print(text.replace("apple", "orange", 1))  # заменит только первое
```

---

## 6) `split()` и `join()`
### 6.1 `split(sep, maxsplit=-1)` — строка → список строк
```py
text = "apple banana cherry"
print(text.split())           # по любым пробельным символам

text = "apple,banana,cherry"
print(text.split(","))        # по запятым

text = "apple---banana---cherry"
print(text.split("---", 1))   # максимум 1 разбиение
```

**Важная разница:**
- `text.split()` (без аргументов) — режет по *любым* пробельным символам и “схлопывает” подряд идущие пробелы
- `text.split(" ")` — режет *строго по пробелам* и может возвращать пустые строки, если пробелов несколько

```py
text = "apple  banana	 cherry
"

print(text.split())      # ['apple', 'banana', 'cherry']
print(text.split(" "))   # ['apple', '', 'banana\t', 'cherry\n']
```

### 6.2 `separator.join(iterable)` — список строк → строка
```py
fruits = ["apple", "banana", "cherry"]
print(" ".join(fruits))     # apple banana cherry
print(", ".join(fruits))    # apple, banana, cherry

letters = ["a", "b", "c"]
print("".join(letters))     # abc
```

---

## 7) `strip()`, `lstrip()`, `rstrip()` — убрать “мусор” по краям
- `strip()` — убирает символы слева и справа
- `lstrip()` — только слева
- `rstrip()` — только справа

Синтаксис:
```py
text.strip([chars])
```
Если `chars` не задан — убирает пробелы/таб/переводы строк и прочие пробельные символы.

```py
text = "\t hello world\n "
print(text.strip())          # "hello world"

text_with_chars = "***hello***"
print(text_with_chars.strip("*"))   # "hello"

text_with_chars = "**--*hello---***"
print(text_with_chars.strip("*-"))  # "hello"
```

---

## 8) Практика / домашка — готовые решения

### 8.1 Звёздочки вместо чисел
Заменить все цифры `0-9` на `*`.
```py
text = "My number is 123-456-789"

result = ""
for ch in text:
    result += "*" if ch.isdigit() else ch

print("Строка:", text)
print("Результат:", result)
```

### 8.2 Повторяющиеся символы (игнорируя регистр)
Нужно вывести только символы, которые встречаются **более 1 раза**, без дублей.
```py
text = "Programming in python"

counts = {}
for ch in text.lower():
    if ch.isspace():        # чаще всего пробелы не считают
        continue
    counts[ch] = counts.get(ch, 0) + 1

for ch, cnt in counts.items():
    if cnt > 1:
        print(f"{ch}: {cnt}")
```

### 8.3 Увеличение чисел в строке (x10)
Заменить все числа в тексте на число * 10. Подходит для целых и десятичных.
```py
import re

text = "I have 5 apples and 10 oranges, price is 0.5 each. Card number is ....3672."

def mul10(m: re.Match) -> str:
    s = m.group(0)
    if "." in s:
        return str(float(s) * 10)
    return str(int(s) * 10)

result = re.sub(r"\d+(?:\.\d+)?", mul10, text)
print(result)
```

---

## 9) Мини-шпаргалка
```text
Проверки:
isalpha isdigit isalnum isspace islower isupper istitle
startswith endswith isdecimal isnumeric isascii isprintable isidentifier

Поиск:
find/rfind -> индекс или -1
index/rindex -> индекс или ValueError
count -> количество (без пересечений)

Регистр:
upper lower capitalize title swapcase casefold

Замена:
replace(old, new, count=-1)

Разбить/склеить:
split(sep, maxsplit=-1)
sep.join(iterable)

Обрезать края:
strip([chars]) lstrip([chars]) rstrip([chars])
```
