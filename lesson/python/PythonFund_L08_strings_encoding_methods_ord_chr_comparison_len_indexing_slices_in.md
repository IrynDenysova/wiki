# Python Fundamentals — Урок 8: строки (str) — основы, кодировки, индексы, срезы

## 1) Что такое строка
**Строка (`str`)** — последовательность символов: текст, который мы обрабатываем в программах.

Пример:
```py
text = "Hello, Python!"
```

---

## 2) Неизменяемость строк (immutable)
Строки **нельзя менять “на месте”**. Любое “изменение” создаёт **новую** строку.

```py
s = "Hello"
s = s + " world!"   # создаётся новая строка
print(s)            # Hello world!
```

---

## 3) Кодировки: ASCII, Unicode, UTF‑8
### 3.1 Кодировка — что это
Кодировка — способ превратить символы в числа (коды), чтобы компьютер мог хранить и обрабатывать текст.

### 3.2 ASCII
- Историческая кодировка для английских букв/цифр/основных символов
- **0..127** (7 бит)

### 3.3 Unicode
Unicode — стандарт, который назначает каждому символу **кодовую точку** (число).
Он покрывает символы разных языков, математику, эмодзи и т.д.

### 3.4 UTF‑8
UTF‑8 — популярная кодировка для хранения Unicode:
- ASCII-символы (0..127) занимают **1 байт**
- другие символы могут занимать **2–4 байта**

---

## 4) Метод vs функция (важное различие)
- **Функция** вызывается так: `func(x)`
- **Метод** вызывается у объекта: `obj.method(...)`

Строка — объект `str`, у неё есть методы обработки текста.

---

## 5) `encode()` и `decode()`: строка ↔ байты
### 5.1 `encode()` — строка → bytes
```py
text = "Привет"
b = text.encode("utf-8")
print(b)  # b'...'
```

### 5.2 `decode()` — bytes → строка
```py
decoded = b.decode("utf-8")
print(decoded)  # Привет
```

Где это нужно:
- чтение/запись файлов с текстом
- передача данных по сети
- международные приложения

---

## 6) `ord()` и `chr()` (символ ↔ код)
### `ord(char)` → число (код Unicode)
```py
print(ord("A"))  # 65
print(ord("a"))  # 97
print(ord(" "))  # 32
```

### `chr(code)` → символ
```py
print(chr(65))  # A
print(chr(97))  # a
print(chr(32))  # пробел
```

---

## 7) Сравнение строк (лексикографически)
Строки можно сравнивать операторами: `==`, `!=`, `<`, `>`, `<=`, `>=`.

Сравнение идёт **символ за символом** по их Unicode-кодам:
```py
print("apple" < "banana")  # True (a < b)
print("abc" < "aca")       # True (b < c)
```

### Важно про регистр
В Unicode заглавные буквы обычно имеют “меньший” код, чем строчные:
```py
print("Zoo" < "zoo")  # True
print("apple" > "Apple")  # True
```

### Строки разной длины
Если одна строка — префикс другой, то более короткая считается “меньше”:
```py
print("app" < "apple")   # True
print("cat" > "catalog") # False
```

✅ Для сравнения “без учёта регистра” делай нормализацию:
```py
a = "Python"
b = "python"
print(a.lower() == b.lower())  # True
```

---

## 8) `len()` — длина строки
```py
text = "Python"
print(len(text))  # 6
```

---

## 9) Индексация строк
Индексы начинаются с **0**:
```py
text = "Python"
print(text[0])  # P
print(text[2])  # t
```

### Отрицательные индексы (с конца)
```py
print(text[-1])  # n
print(text[-3])  # h
```

### Ошибка индекса (out of range)
Если индекс вне диапазона — будет `IndexError`:
```py
# text = "hello" (5 символов)
# print(text[10])  # IndexError
```

Как проверить безопасно:
```py
text = "hello"
idx = 4
if 0 <= idx < len(text):
    print(text[idx])
else:
    print("Индекс вне диапазона")
```

---

## 10) Срезы строк (substring)
Срез: `s[start:end]`
- `start` включительно
- `end` **не включительно**

```py
text = "Python programming"
print(text[0:6])  # Python
```

### Срезы “по умолчанию”
```py
print(text[:6])   # от начала
print(text[7:])   # до конца
print(text[:])    # копия всей строки
```

### Отрицательные индексы в срезах
```py
print(text[-11:])   # последние 11 символов
```

### Ошибка индексов в срезах
Если `end <= start` (при положительном шаге) — получится пустая строка:
```py
print(text[14:7])  # ""
```

---

## 11) Срезы с шагом (step)
Форма: `s[start:end:step]`

```py
text = "Python programming"
print(text[0:12:2])  # каждый 2-й символ
```

### Обратный порядок (шаг -1)
Полная “перевёрнутая” строка:
```py
text = "Python"
print(text[::-1])  # nohtyP
```

Важно: при отрицательном шаге обычно `start` должен быть больше `end`.

---

## 12) Оператор принадлежности `in` / `not in`
Проверка подстроки:
```py
text = "Python programming"
print("Python" in text)   # True
print("Hello" in text)    # False
print("Java" not in text) # True
```

⚠️ `in` чувствителен к регистру:
```py
text = "Python programming"
print("python" in text)  # False
```

---

## 13) Практика (готовые решения)

### 13.1 Палиндром
```py
text = input("Введите строку: ")
if text == text[::-1]:
    print("Строка является палиндромом")
else:
    print("Строка не является палиндромом")
```

### 13.2 Дешифровка шифра Цезаря (только латиница a-z)
Идея: сдвигать символы назад на `shift` позиций по алфавиту.

```py
encrypted = input("Введите зашифрованный текст: ").strip().lower()
shift = int(input("Введите сдвиг: "))

alphabet = "abcdefghijklmnopqrstuvwxyz"
result = []

for ch in encrypted:
    if ch in alphabet:
        idx = alphabet.index(ch)
        new_idx = (idx - shift) % len(alphabet)
        result.append(alphabet[new_idx])
    else:
        result.append(ch)  # пропускаем пробелы/знаки
print("Расшифрованный текст:", "".join(result))
```

---

## 14) Домашка (шаблон)
### Проверка: символ в ASCII?
ASCII диапазон: **0..127**.
```py
ch = input("Введите один символ: ")
code = ord(ch)
print("Код Unicode:", code)
print("ASCII?", 0 <= code <= 127)
```
