# Python Fundamentals — Урок 31: Регулярные выражения (RegEx) и модуль `re`

## 1) Что такое RegEx и зачем он нужен
**Регулярные выражения (RegEx)** — инструмент для **поиска**, **сравнения**, **замены** и **проверки** строк по заданному шаблону.

Используется для:
- проверки формата (email/телефон/пароль),
- поиска по шаблону (в тексте/логах/коде),
- разбиения строк,
- замены/очистки данных.

---

## 2) Модуль `re`: основные функции
```py
import re
```

- `re.search(pattern, string)` — находит **первое** совпадение **в любом месте** строки, возвращает `Match` или `None`.
- `re.match(pattern, string)` — проверяет совпадение **только в начале** строки, возвращает `Match` или `None`.
- `re.findall(pattern, string)` — возвращает **список всех** совпадений.
- `re.finditer(pattern, string)` — возвращает **итератор** объектов `Match`.
- `re.sub(pattern, repl, string)` — заменяет совпадения.
- `re.split(pattern, string)` — разбивает строку по шаблону.
- `re.compile(pattern)` — компилирует шаблон (удобно для многократного использования).

### 2.1 Объект `Match`
Если `match` найден, можно получить детали:
- `match.group()` — совпавший текст,
- `match.start()` / `match.end()` — границы,
- `match.span()` — `(start, end)`.

---

## 3) `findall()` — быстрый старт
**Синтаксис:**
```py
re.findall(pattern, string)
```

Пример: найти все числа в тексте:
```py
import re
text = "Python 3.9, Java 17, C++ 14"
numbers = re.findall(r"\d+", text)
print(numbers)   # ['3', '9', '17', '14']
```

---

## 4) Базовые спец-символы
| Шаблон | Значение |
|---|---|
| `\d` | цифра `0-9` |
| `\D` | не-цифра |
| `\w` | буква/цифра/`_` |
| `\W` | не `\w` |
| `\s` | пробельный символ (` `, `\t`, `\n`) |
| `\S` | не-пробельный |
| `.` | любой символ, кроме `\n` |

Пример:
```py
import re
text = "\tPython 3.12, Java 17, C++ 14!\n"
print(re.findall(r"\d", text))      # все цифры
print(re.findall(r"\d\d", text))   # пары цифр
print(re.findall(r"\w", text))      # буквы/цифры/_
print(re.findall(r"\s", text))      # пробельные
print(re.findall(r".", text))        # все, кроме \n
```

---

## 5) Почему важно писать `r"..."` (raw string)
В regex много `\d`, `\w`, `\s` и т.д.  
В Python обратный слэш `\` — управляющий символ в строках. Чтобы Python не “съедал” слэши, шаблон лучше писать как **сырой литерал**:

✅ правильно:
```py
re.findall(r"\d+", "Value: 123")
```

⚠️ потенциально проблемно:
```py
re.findall("\d+", "Value: 123")
```

---

## 6) Классы символов: `[...]`
Класс символов — “один из перечисленных”.
| Шаблон | Значение |
|---|---|
| `[afc]` | `a` или `f` или `c` |
| `[0-9]` | цифра (аналог `\d`) |
| `[a-z]` | строчная латиница |
| `[A-Z]` | заглавная латиница |
| `[a-zA-Z]` | любая латинская буква |
| `[^abc]` | любой символ, кроме `a/b/c` |
| `[^0-9]` | любой символ, кроме цифр |

Пример:
```py
import re
text = "Report, report, report2, report10"
print(re.findall(r"[rR]eport", text))
print(re.findall(r"report\d*", text))
```

---

## 7) Квантификаторы (сколько повторений)
| Квантификатор | Значение |
|---|---|
| `+` | 1 или больше |
| `*` | 0 или больше |
| `?` | 0 или 1 |
| `{n}` | ровно `n` |
| `{n,}` | `n` или больше |
| `{n,m}` | от `n` до `m` |

Пример:
```py
import re
text = "Orders: ID123, ID4567, ID89"
print(re.findall(r"ID\d{2,}", text))  # 2+ цифр после ID
```

### 7.1 Жадные и ленивые
По умолчанию квантификаторы **жадные** (берут максимум).  
Чтобы сделать **ленивым**, добавьте `?`:

- жадный: `.*`
- ленивый: `.*?`

Пример:
```py
import re
text = "<div>Hello</div><div>World</div>"
print(re.findall(r"<.*>", text))    # жадно
print(re.findall(r"<.*?>", text))  # лениво
```

---

## 8) Экранирование спец-символов
Спец-символы regex: `. + * { } [ ] ( ) | ^ $` — имеют значение.  
Если нужно искать их “как текст” — экранируем `\`.

Например, точка `.`:
- `\w+.txt` — точка означает “любой символ” (не строго `.txt`)
- `\w+\.txt` — точка как символ

Пример:
```py
import re
text = "report.txt, report2.txt, report10.txt"
print(re.findall(r"\w+\.txt", text))
```

---

## 9) Якоря: позиция, а не символ
| Якорь | Значение |
|---|---|
| `^` | начало строки |
| `$` | конец строки |
| `\b` | граница слова |
| `\B` | НЕ граница слова |

Пример:
```py
import re
text = "Hello world! Welcome to world"
print(re.findall(r"^\w+", text))   # первое слово
print(re.findall(r"\w+$", text))   # последнее слово

text2 = "category wildcat education _cat_ catalog"
print(re.findall(r"\bcat\w*", text2))  # cat в начале слова
print(re.findall(r"\w*cat\b", text2))  # cat в конце слова
```

---

## 10) Альтернативы: `|` (ИЛИ)
```py
import re
text = "Meeting on 2024-05-10 or 10/05/2024 at 14:30"
pattern = r"(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})"
print(re.findall(pattern, text))
```

---

## 11) Группы: `(...)` и негруппирующие `(?:...)`
### 11.1 Обычные группы (захватывают)
```py
import re
text = "Order ID: 12345, Invoice No: 67890"
m = re.search(r"Order ID: (\d+), Invoice No: (\d+)", text)
if m:
    print(m.group(1))  # 12345
    print(m.group(2))  # 67890
```

### 11.2 Негруппирующие (для логики, но без захвата)
```py
import re
text = "USD 100, EUR 200, GBP 300"
print(re.findall(r"(?:USD|EUR|GBP) (\d+)", text))  # только суммы
```

Если нужны и валюта, и сумма:
```py
print(re.findall(r"(USD|EUR|GBP) (\d+)", text))
```

---

## 12) Флаги (пример: `re.IGNORECASE`)
`re.IGNORECASE` (или `re.I`) — поиск без учёта регистра:
```py
import re
text = "Python is popular."
m = re.search(r"python", text, re.I)
print(m.group())
```

---

## 13) `re.compile()` — когда полезно
Если один и тот же шаблон используется много раз — компилируем:
```py
import re

number_pattern = re.compile(r"\d+")
texts = [
    "Order ID: 12345, Invoice No: 67890, Ref: ABC9876",
    "Shipment ID: 54321, Tracking No: 98765, Customer Ref: XYZ123",
]
for t in texts:
    print(number_pattern.findall(t))
```

---

# Ответы на задания (из урока)
## Закрепление 1
Сопоставление:
- `\d+` → последовательность цифр → **c**
- `[a-zA-Z0-9]+` → буквы и цифры → **b**
- `\s+` → несколько пробельных → **a**
- `[^a-zA-Z0-9]+` → НЕ буквы и НЕ цифры → **d**

Ошибка в шаблоне:
```py
re.findall("\d+", "Value: 123")
```
Правильно: использовать raw string → `re.findall(r"\d+", ...)`

Ленивый квантификатор: **`<.*?>`**

## Закрепление 2
Якоря:
- `^` → начало строки
- `$` → конец строки
- `\b` → граница слова
- `\B` → не граница слова

Отличие `re.match()` от `re.search()`:
- `match()` проверяет **только начало**,
- `search()` ищет **в любой части** строки.

---

# Практическая работа (решения)

## 1) Проверка надёжности пароля
Условия:
- минимум 8 символов
- хотя бы 1 заглавная
- хотя бы 1 строчная
- хотя бы 1 цифра

```py
import re

password = input("Введите пароль: ")

if (re.search(r"[A-Z]", password) and
    re.search(r"[a-z]", password) and
    re.search(r"\d", password) and
    len(password) >= 8):
    print("Пароль надёжен.")
else:
    print("Пароль не соответствует требованиям.")
```

## 2) Извлечение IPv4-адресов (с фильтрацией 0–255)
```py
import re

text = "Server1: 192.168.1.1, Server2: 10.0.0.254, Invalid: 999.123.456.78"
pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"

candidates = re.findall(pattern, text)
valid_ips = [ip for ip in candidates if all(0 <= int(part) <= 255 for part in ip.split("."))]

for ip in valid_ips:
    print(ip)
```

---

# Домашнее задание (решения)

## ДЗ 1) Извлечение дат (DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY)
```py
import re

text = """The events N 123456 happened on
15/03/2025, 01.12.2024 and 09-09-2023.
Deadline: 28/02/2022."""

pattern = r"\b\d{2}[\/\-.]\d{2}[\/\-.]\d{4}\b"
dates = re.findall(pattern, text)
for d in dates:
    print(d)
```

## ДЗ 2) Разделение списка тегов (разделители: `, ; / пробелы`)
```py
import re

tag_input = "python, data-science / machine-learning; AI neural-networks"
tags = re.split(r"[,;/\s]+", tag_input)
tags = [t.strip() for t in tags if t.strip()]
print(tags)
```

---

## Мини-шпаргалка (самое важное)
```text
re.findall(r"\d+", text)  -> все числа
re.search(pattern, text)   -> первое совпадение в любом месте
re.match(pattern, text)    -> совпадение только в начале

Символы: \d \w \s .
Классы: [a-z] [A-Z] [0-9] [^0-9]
Квантификаторы: + * ? {n} {n,} {n,m}
Ленивый: *? +? {n,m}?
Экранирование: \. \+ \? \( \) \[ \] \{ \}
Якоря: ^ $ \b \B
ИЛИ: (a|b)
Группы: (...)  негрупп: (?:...)
```
