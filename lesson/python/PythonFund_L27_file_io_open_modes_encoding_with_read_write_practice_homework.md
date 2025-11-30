# Python Fundamentals — Урок 27: основы работы с файлами (File I/O) — `open()`, режимы, `encoding`, `with`, чтение/запись

## 1) Зачем уметь работать с файлами
Файлы нужны для:
- **хранения данных** между запусками программы;
- **обмена данными** между программами (CSV/JSON/XML и т.д.);
- **обработки больших объёмов** по частям (не загружая всё в RAM);
- **автоматизации** работы с документами/логами/отчётами. 

---

## 2) Типы файлов
### 2.1 Текстовые файлы
- читаемы человеком;
- зависят от **кодировки** (UTF‑8, CP1251…);
- примеры: `.txt`, `.csv`, `.json`, `.html`, `.py`. 

### 2.2 Бинарные файлы
- двоичный формат (не читается “как текст”);
- изображения/видео/архивы/исполняемые/БД;
- примеры: `.jpg`, `.png`, `.mp4`, `.exe`, `.zip`. 

---

## 3) `open()` — как открыть файл
Функция `open()` открывает файл и возвращает **файловый объект**. 

### 3.1 Синтаксис
```py
open(file, mode="mode", encoding="encoding")
```

- `file` — путь (абсолютный или относительный) **обязателен**;
- `mode` — режим (по умолчанию чтение текста `rt`);
- `encoding` — кодировка (важно для текста). 

---

## 4) Режимы работы с файлами (таблица)
| Режим | Что делает |
|------|------------|
| `"r"` | чтение (ошибка, если файла нет) |
| `"w"` | запись (создаёт или перезаписывает) |
| `"a"` | добавление в конец (создаёт, если нет) |
| `"x"` | создать новый (ошибка, если уже существует) |
| `"b"` | бинарный режим (`"rb"`, `"wb"`) |
| `"t"` | текстовый режим (по умолчанию) |
| `"+"` | чтение и запись (`"r+"`, `"w+"`, `"a+"`, `"x+"`) | 

Примеры комбинаций: `"rb"`, `"wt"`, `"a+"`. 

---

## 5) `encoding` — почему важно
`encoding` указывают **для текстовых файлов**, чтобы:
- корректно читать/писать кириллицу и любые символы;
- код был переносимым между ОС;
- избегать `UnicodeDecodeError`. 

Популярные кодировки: `utf-8`, `cp1251`, `ascii`, `utf-16`, `utf-32`, `iso-8859-1`. 

---

## 6) Закрытие файла: `close()`
Файл важно закрывать, чтобы:
- освободить ресурсы;
- гарантировать сохранение данных;
- избежать блокировок (часто в Windows). 

Пример (ручное закрытие):
```py
file = open("example.txt", "r", encoding="utf-8")
content = file.read()
print(content)
file.close()
```

---

## 7) Контекстный менеджер `with` (рекомендуемый способ)
`with open(...) as f:` автоматически закрывает файл **после выхода из блока**, даже если случилась ошибка. Код чище и безопаснее. 

```py
with open("example.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)
```

---

## 8) Чтение из файла
Когда файл открыт, есть **указатель (позиция)** — откуда идёт следующее чтение/запись. 

### 8.1 `read()` — прочитать всё
```py
with open("example.txt", "r", encoding="utf-8") as file:
    content = file.read()
```
Особенности:
- читает весь файл целиком (может быть тяжело для больших файлов),
- указатель становится в конец,
- переносы строк внутри текста — `\n`. 

### 8.2 `read(n)` — прочитать первые `n` символов
```py
with open("example.txt", "r", encoding="utf-8") as file:
    first_10 = file.read(10)
```
Полезно читать большие файлы кусками. 

### 8.3 `readline()` — читать по одной строке
```py
with open("example.txt", "r", encoding="utf-8") as file:
    print(file.readline())
    print(file.readline())
```
Каждый вызов двигает указатель дальше. 

### 8.4 `readlines()` — список строк
```py
with open("example.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
```
Возвращает `list[str]`, строки обычно содержат `\n`. 

### 8.5 Чтение в цикле (лучше для больших файлов)
Файл итерируемый: можно читать построчно без загрузки всего в память. 

```py
with open("example.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line, end="")
```

---

## 9) Запись в файл
### 9.1 `write()` — записать одну строку
```py
with open("users.txt", "w", encoding="utf-8") as file:
    file.write("ID: 201 | Name: John | Age: 25 | Status: Active\n")
```
Особенности:
- создаёт файл, если его нет;
- **перезаписывает** файл целиком (`w`);
- `write()` **не добавляет `\n` автоматически**. 

### 9.2 `writelines()` — записать список строк
```py
data = [
    "ID: 202 | Name: Alice | Age: 30 | Status: Inactive\n",
    "ID: 203 | Name: Bob | Age: 27 | Status: Active\n",
]
with open("users.txt", "w", encoding="utf-8") as file:
    file.writelines(data)
```
Важно: `\n` вставляете сами, иначе строки “склеятся”. 

---

## 10) Другие полезные режимы
### 10.1 `"a"` — дописать в конец
```py
with open("users.txt", "a", encoding="utf-8") as file:
    file.write("Дополнительная строка\n")
```
Не перезаписывает существующие данные. 

### 10.2 `"r+"` — чтение + запись без очистки
```py
with open("users.txt", "r+", encoding="utf-8") as file:
    content = file.read()
    file.write("\nДобавленный текст")
```
Особенность: запись идёт **с текущей позиции указателя**, возможна частичная перезапись, если позицию не контролировать. 

### 10.3 `"x"` — создать новый (не перезаписывает)
```py
try:
    with open("new_file.txt", "x", encoding="utf-8") as file:
        file.write("Этот файл создан в режиме 'x'.\n")
except FileExistsError:
    print("Файл уже существует.")
```

---

## 11) `with` для нескольких файлов
Можно открывать несколько файлов одновременно: 
```py
with (
    open("example.txt", "r", encoding="utf-8") as infile,
    open("output.txt", "w", encoding="utf-8") as outfile
):
    for line in infile:
        outfile.write(line.upper())
```

---

# Ответы на задания из урока
1) Какой режим даст ошибку, если файл уже существует? → **`"x"`**. 
2) Какой параметр обязателен для `open()`? → **`file`** (путь к файлу). 
3) Какой метод возвращает список строк? → **`readlines()`**. 
4) Что делает код с режимом `"a"` и `write()`? → **добавляет строку в конец** и **создаёт файл, если его нет**. 

---

# Практическая работа (готовые решения)

## Практика 1) Подсчёт частоты слов в файле (без учёта регистра)
Требования:
- спросить имя файла и число топ-слов,
- обработать `FileNotFoundError`,
- обработать `ValueError` для количества. 

```py
from collections import Counter

filename = input("Введите имя файла: ")

def count_words_in_file(filename: str) -> Counter:
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read().lower()
        punctuation = '.,!?;:"-'
        for ch in punctuation:
            text = text.replace(ch, " ")
        return Counter(text.split())

try:
    word_counts = count_words_in_file(filename)
    num_words = int(input("Введите количество популярных слов: "))

    print("\nПопулярные слова:")
    for word, count in word_counts.most_common(num_words):
        print(f"{word}: {count}")

except FileNotFoundError:
    print("Ошибка: Файл не найден.")
except ValueError:
    print("Ошибка: Введите целое число для количества популярных слов.")
```

---

## Практика 2) Удаление пустых строк и сохранение в `<oldname>_cleaned.txt`
Требования:
- имя нового файла автоматически,
- если файла нет → ошибка. 

```py
import os

filename = input("Введите имя файла: ")

# Генерация имени нового файла: <oldname>_cleaned.txt
new_filename = f"{os.path.splitext(filename)[0]}_cleaned.txt"

try:
    with (
        open(filename, "r", encoding="utf-8") as infile,
        open(new_filename, "w", encoding="utf-8") as outfile
    ):
        for line in infile:
            if line.strip():
                outfile.writelines(line)

    print(f"Пустые строки удалены, сохранено в {new_filename}.")
except FileNotFoundError:
    print(f"Ошибка: файл '{filename}' не найден.")
```

---

## Практика 3) Найти файлы по расширению (аргументы командной строки)
Требования:
- `python script.py /path/to/dir .py`
- вывести список найденных файлов. 

```py
import os
import sys

if len(sys.argv) != 3:
    print("Использование: python script.py <директория> <расширение>")
    sys.exit(1)

directory, extension = sys.argv[1], sys.argv[2]

found = []
for root, dirs, files in os.walk(directory):
    for name in files:
        if name.endswith(extension):
            found.append(name)

if found:
    print(f"Найденные файлы в директории '{directory}':")
    print(", ".join(found))
else:
    print("Файлы не найдены.")
```

---

# Домашнее задание (решения)

## ДЗ 1) Фильтрация строк по ключевому слову → файл `<keyword>_<original_filename>`
Условия:
- спросить имя файла и ключевое слово;
- если файла нет — вывести ошибку;
- если совпадений нет — **новый файл не создавать**. 

```py
import os

filename = input("Введите имя файла для поиска: ").strip()
keyword = input("Введите ключевое слово: ").strip()

out_name = f"{keyword}_{os.path.basename(filename)}"
matches = []

try:
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if keyword in line:
                matches.append(line)

    if not matches:
        print("Совпадения не найдены. Новый файл не создан.")
    else:
        with open(out_name, "w", encoding="utf-8") as out:
            out.writelines(matches)
        print(f"Строки, содержащие '{keyword}', сохранены в {out_name}.")

except FileNotFoundError:
    print("Ошибка: Файл не найден.")
```

---

## ДЗ 2) Удаление дубликатов строк → `unique_<original_filename>` (с сохранением порядка)
Условия:
- спросить имя файла;
- если файла нет — ошибка;
- **сохранить порядок**;
- если дубликатов нет — сделать точную копию. 

```py
import os

filename = input("Введите имя файла: ").strip()
out_name = f"unique_{os.path.basename(filename)}"

try:
    seen = set()
    unique_lines = []

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            # сравнение с учётом точного текста строки (включая \n)
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)

    with open(out_name, "w", encoding="utf-8") as out:
        out.writelines(unique_lines)

    print(f"Результат сохранён в {out_name}.")

except FileNotFoundError:
    print("Ошибка: Файл не найден.")
```

---

## Мини-шпаргалка
```text
open(path, mode, encoding)

Режимы:
r  - чтение (файл должен существовать)
w  - запись (создаёт/перезаписывает)
a  - дописать в конец (создаёт)
x  - создать новый (ошибка если существует)
b  - бинарный режим
+  - чтение и запись

Лучше так:
with open(...) as f:
    ...

Чтение:
read()        - всё
read(n)       - n символов
readline()    - 1 строка
readlines()   - list[str]
for line in f - построчно, экономно

Запись:
write(str)      - строка (\n вручную)
writelines(list) - список строк
```
