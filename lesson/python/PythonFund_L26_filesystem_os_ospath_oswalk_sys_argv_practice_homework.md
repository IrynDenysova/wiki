# Python Fundamentals — Урок 26: Работа с файловой системой (`os`, `os.path`, `os.walk`, `sys.argv`)

## 0) План урока

- Что такое файловая система
- Абсолютные и относительные пути, спец‑обозначения (`.`, `..`, `~`, разделители)
- Модуль `os`: навигация и работа с файлами/директориями
- Работа с путями: `os.path.*`
- Рекурсивный обход директорий: `os.walk`
- Модуль `sys` и аргументы командной строки (`sys.argv`)
- Практика + задания / ДЗ

---

## 1) Файловая система и структура каталогов

**Файловая система** — способ хранения и организации данных на диске.  
Состоит из **файлов** и **папок (директорий)**, которые можно:

- читать;
- изменять;
- удалять;
- перемещать.

Пример структуры (Linux):
```text
/home/user/
├── PycharmProjects/
│   ├── project1/
│   │   ├── data/
│   │   │   └── file.txt
│   │   └── main.py
│   └── project2/
│       └── main.py
├── documents/
└── downloads/
```

---

## 2) Абсолютные и относительные пути

### 2.1 Абсолютный путь

**Абсолютный путь** — полный путь от корневой директории до файла/папки.

- Linux/macOS: начинается с `/`
- Windows: с буквы диска + `:\`

```py
# Linux / macOS
absolute_path = "/home/user/documents/file.txt"

# Windows
absolute_path = "C:\Users\User\Documents\file.txt"
```

### 2.2 Относительный путь

**Относительный путь** — путь относительно **текущей рабочей директории**.

Спец‑обозначения:

- `.` — текущая директория
- `..` — родительская директория

Пример (текущая директория `/home/user/PycharmProjects/project1/data`):

```text
./file.txt
# -> /home/user/PycharmProjects/project1/data/file.txt

../file.txt
# -> /home/user/PycharmProjects/project1/file.txt
```

### 2.3 Когда что использовать

**Абсолютный путь** удобно использовать:

- когда путь фиксирован (конфиги, системные файлы);
- когда скрипт должен работать независимо от того, **откуда** его запустили.

**Относительный путь** удобно использовать:

- в пределах одного проекта/репозитория;
- в переносимых скриптах.

---

## 3) Специальные обозначения в путях

| Знак | Значение                 | Пример                                        |
|------|--------------------------|-----------------------------------------------|
| `.`  | текущая директория       | `./file.txt`                                  |
| `..` | родительская директория  | `../file.txt`, `../../file.txt`              |
| `/`  | разделитель (Linux/mac)  | `/home/user/file.txt`                         |
| `\` | разделитель (Windows)    | `C:\Users\User\Documents\file.txt`       |
| `~`  | домашняя директория (Unix)| `~/documents/file.txt`                       |

---

## 4) Модуль `os`: работа с файловой системой

```py
import os
```

### 4.1 Текущая директория: `os.getcwd()`

```py
import os

current_dir = os.getcwd()
print(f"Текущая директория: {current_dir}")
```

### 4.2 Смена директории: `os.chdir(path)`

```py
import os

# переход в поддиректорию (относительный путь)
os.chdir("./subdirectory")
print(os.getcwd())

# переход в родительскую директорию
os.chdir("..")
print(os.getcwd())

# переход по абсолютному пути
os.chdir("/home/user/documents")   # подставь существующий путь
print(os.getcwd())
```

> Если директории нет — будет `FileNotFoundError`.

---

### 4.3 Проверка существования пути: `os.path.exists(path)`

```py
import os

file_path = "example.txt"
if os.path.exists(file_path):
    print(f"Файл '{file_path}' существует.")
else:
    print(f"Файл '{file_path}' не найден.")

directory_path = "example_folder"
if os.path.exists(directory_path):
    print(f"Директория '{directory_path}' существует.")
else:
    print(f"Директория '{directory_path}' не найдена.")
```

---

### 4.4 Список файлов и папок: `os.listdir(path)`

```py
import os

# содержимое текущей директории
contents = os.listdir(".")
print("Содержимое текущей директории:", contents)

# содержимое конкретной директории
specific_dir = "parent_folder"
if os.path.exists(specific_dir):
    print(f"Содержимое '{specific_dir}':", os.listdir(specific_dir))
```

---

### 4.5 Создание директорий: `os.mkdir` и `os.makedirs`

```py
import os

dir_path = "example_folder"
if not os.path.exists(dir_path):
    os.mkdir(dir_path)   # создаёт ОДНУ директорию
    print(f"Директория '{dir_path}' создана.")

# вложенные директории за раз
os.makedirs("parent_folder/child_folder", exist_ok=True)
print("Вложенные директории созданы.")
```

Разница:

- `os.mkdir(path)` — только одну папку, без родителей.
- `os.makedirs(path, exist_ok=True)` — создаёт всех родителей, не падает, если уже существует.

---

### 4.6 Создание файла (через `open`)

```py
file_name = "example.txt"
open(file_name, "w").close()   # создаст или перезапишет файл
print(f"Файл '{file_name}' создан или перезаписан.")
```

---

### 4.7 Проверка типа объекта: файл или директория

```py
import os

path = "example.txt"     # или "parent_folder"

if os.path.isfile(path):
    print(f"'{path}' существует и это файл.")
elif os.path.isdir(path):
    print(f"'{path}' существует и это директория.")
else:
    print(f"'{path}' не существует.")
```

- `os.path.isfile(path)` — путь указывает на файл
- `os.path.isdir(path)` — путь указывает на директорию

---

### 4.8 Переименование: `os.rename(src, dst)`

```py
import os

# файл
old_file_name = "example.txt"
new_file_name = "renamed.txt"
if os.path.exists(old_file_name):
    os.rename(old_file_name, new_file_name)
    print(f"Файл переименован в '{new_file_name}'.")

# директория
old_dir_name = "example_folder"
new_dir_name = "renamed_folder"
if os.path.exists(old_dir_name):
    os.rename(old_dir_name, new_dir_name)
    print(f"Директория переименована в '{new_dir_name}'.")
```

---

### 4.9 Удаление: `os.remove` и `os.rmdir`

```py
import os

# удалить файл
file_to_delete = "renamed.txt"
if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"Файл '{file_to_delete}' удалён.")

# удалить ПУСТУЮ директорию
empty_dir_to_delete = "renamed_folder"
if os.path.exists(empty_dir_to_delete):
    os.rmdir(empty_dir_to_delete)
    print(f"Пустая директория '{empty_dir_to_delete}' удалена.")
```

> `os.rmdir` удаляет только **пустую** папку. Для рекурсивного удаления удобно использовать `shutil.rmtree`, но это уже другой модуль.

---

## 5) Работа с путями: `os.path`

### 5.1 Разделение пути

```py
import os

path = "/subdirectory/example.txt"

directory, file = os.path.split(path)
print(f"Директория: {directory}, файл: {file}")    # /subdirectory, example.txt

print(os.path.basename(path))   # example.txt
print(os.path.dirname(path))    # /subdirectory
```

### 5.2 Абсолютный путь: `os.path.abspath`

```py
import os

relative_path = "example.txt"
absolute_path = os.path.abspath(relative_path)
print(f"Абсолютный путь: {absolute_path}")
```

### 5.3 Склейка путей: `os.path.join`

```py
import os

current_dir = os.getcwd()
sub_dir = "docs"
file_name = "data.txt"

full_path = os.path.join(current_dir, sub_dir, file_name)
print(f"Путь: {full_path}")
```

Плюс `os.path.join` в том, что он сам использует правильный разделитель для ОС (`/` или `\`).

---

## 6) Рекурсивный обход: `os.walk`

`os.walk(root)` возвращает **генератор** кортежей `(root, dirs, files)`:

- `root` — текущая директория;
- `dirs` — поддиректории;
- `files` — файлы.

### 6.1 Базовый пример

```py
import os

for root, dirs, files in os.walk("."):
    print(f"Текущая директория: {root}")
    print(f"Поддиректории: {dirs}")
    print(f"Файлы: {files}")
    print("-" * 40)
```

### 6.2 Поиск файлов по расширению

```py
import os

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".txt"):
            print(f"Найден файл: {os.path.join(root, file)}")
```

---

## 7) Модуль `sys` и аргументы командной строки

```py
import sys
```

### 7.1 Что такое `sys.argv`

- `sys.argv` — список **строк**, переданных скрипту при запуске.
- `sys.argv[0]` — имя скрипта.
- `sys.argv[1:]` — аргументы пользователя.

```py
import sys

print("Все аргументы:", sys.argv)
if len(sys.argv) > 1:
    print(f"Первый аргумент: {sys.argv[1]}")
else:
    print("Аргументы не переданы.")
```

Запуск из консоли:

```bash
python script.py arg1 arg2 arg3
```

Тогда `sys.argv == ["script.py", "arg1", "arg2", "arg3"]`.

### 7.2 Перебор нескольких аргументов

```py
import sys

if len(sys.argv) > 1:
    for i, arg in enumerate(sys.argv[1:], start=1):
        print(f"Аргумент {i}: {arg}")
else:
    print("Аргументы не переданы.")
```

---

### 7.3 Практика: удаление файлов с указанным расширением

```py
import sys
import os

if len(sys.argv) != 2:
    print("Использование: python script.py <расширение>")
    sys.exit(1)

extension = sys.argv[1]

for file_name in os.listdir("."):
    if file_name.endswith(extension):
        os.remove(file_name)
        print(f"Удалён файл: {file_name}")
```

Запуск:

```bash
python script.py .log
```

---

### 7.4 Практика: вывод содержимого директории

```py
import sys
import os

if len(sys.argv) != 2:
    print("Использование: python script.py <директория>")
    sys.exit(1)

directory = sys.argv[1]

if not os.path.isdir(directory):
    print(f"Директория '{directory}' не существует.")
    sys.exit(1)

print(f"Содержимое директории '{directory}':")
for item in os.listdir(directory):
    print(f"- {item}")
```

Запуск:

```bash
python script.py /home/user/documents
```

---

## 8) Практика (примеры решений)

### 8.1 Определение типа объекта по пути

**Задача:**  
Запросить у пользователя путь и вывести, что это: файл, папка или путь не существует.

```py
import os

path = input("Введите путь: ").strip()

if os.path.isfile(path):
    print(f"{path} — это файл.")
elif os.path.isdir(path):
    print(f"{path} — это папка.")
else:
    print(f"{path} — не существует.")
```

---

### 8.2 Поиск файлов с расширением в указанной директории

**Задача:**  
Принять путь к директории и расширение через `sys.argv`, вывести список файлов.

```py
import os
import sys

if len(sys.argv) != 3:
    print("Использование: python script.py <директория> <расширение>")
    sys.exit(1)

directory, extension = sys.argv[1], sys.argv[2]

if not os.path.isdir(directory):
    print(f"Директория '{directory}' не существует.")
    sys.exit(1)

found = []

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(extension):
            found.append(os.path.join(root, file))

if found:
    print(f"Найденные файлы в директории '{directory}':")
    print(", ".join(found))
else:
    print(f"Файлы с расширением '{extension}' не найдены.")
```

---

## 9) Домашка — идеи решений

### 9.1 Список папок и файлов

```py
import os
import sys

if len(sys.argv) != 2:
    print("Использование: python script.py <директория>")
    sys.exit(1)

directory = sys.argv[1]

if not os.path.isdir(directory):
    print(f"Директория '{directory}' не существует.")
    sys.exit(1)

folders = []
files = []

for item in os.listdir(directory):
    full = os.path.join(directory, item)
    if os.path.isdir(full):
        folders.append(item)
    else:
        files.append(item)

print(f"Содержимое директории '{directory}':")
print("Папки:")
for f in folders:
    print(f"- {f}")

print("Файлы:")
for f in files:
    print(f"- {f}")
```

---

### 9.2 Рекурсивный поиск и удаление файлов с расширением

```py
import os
import sys

if len(sys.argv) != 3:
    print("Использование: python script.py <директория> <расширение>")
    sys.exit(1)

directory, extension = sys.argv[1], sys.argv[2]

if not os.path.isdir(directory):
    print(f"Директория '{directory}' не существует.")
    sys.exit(1)

matches = []

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(extension):
            matches.append(os.path.join(root, file))

if not matches:
    print(f"Файлы с расширением '{extension}' не найдены.")
    sys.exit(0)

print(f"Найдены файлы с расширением '{extension}':")
for path in matches:
    print("-", path)

answer = input("Вы хотите удалить эти файлы? (y/n): ").strip().lower()
if answer == "y":
    for path in matches:
        os.remove(path)
    print("Удаление завершено.")
else:
    print("Удаление отменено.")
```

---

## 10) Мини‑шпаргалка по уроку

```text
Файловая система:
- абсолютный путь: /home/user/file.txt, C:\Users\User\file.txt
- относительный: ./file.txt, ../file.txt

os:
- os.getcwd()          -> текущая директория
- os.chdir(path)       -> сменить директорию
- os.listdir(path)     -> список содержимого
- os.path.exists(p)    -> путь существует?
- os.path.isfile(p)    -> это файл?
- os.path.isdir(p)     -> это директория?
- os.mkdir(p)          -> создать директорию
- os.makedirs(p, exist_ok=True) -> создать с родителями
- os.rename(src, dst)  -> переименовать
- os.remove(p)         -> удалить файл
- os.rmdir(p)          -> удалить пустую папку

os.path:
- split(p)    -> (dir, name)
- basename(p) -> имя файла
- dirname(p)  -> директория
- abspath(p)  -> абсолютный путь
- join(a, b)  -> корректная склейка

os.walk(root):
for root, dirs, files in os.walk(root): ...

sys.argv:
- список аргументов командной строки (строки)
- argv[0] — имя скрипта
- argv[1:] — аргументы пользователя
```
