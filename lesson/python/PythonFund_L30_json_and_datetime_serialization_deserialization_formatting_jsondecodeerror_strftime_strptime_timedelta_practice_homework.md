# Python Fundamentals — Урок 30: JSON-файлы и модуль `datetime` (сериализация/десериализация, форматирование, ошибки, работа с датами)

## 0) План урока
- JSON: что это и где используется
- Модуль `json`: сериализация и десериализация
- Сравнение типов Python и JSON
- Форматирование JSON (`indent`, `ensure_ascii`, `sort_keys`)
- Ошибка `JSONDecodeError` и обработка через `try/except`
- Модуль `datetime`: `now()`, `strftime()`, `strptime()`, сравнение дат, `timedelta`
- Практика + Домашнее задание

---

## 1) JSON — что это
**JSON (JavaScript Object Notation)** — текстовый формат для хранения и передачи структурированных данных.

Пример JSON-объекта:
```json
{
  "name": "Alice",
  "age": 25,
  "is_student": false,
  "courses": ["Math", "Physics"]
}
```

### Особенности JSON
- Структура данных: **объекты** (ключ-значение) и **массивы**.
- Типы: числа, строки, boolean, массивы, объекты, `null`.
- **Строки только в двойных кавычках** `"`.
- Данные хранятся как **текст**, поэтому формат универсален.

### Где используется JSON
- API (обмен данными клиент ↔ сервер)
- Базы данных (документные, например MongoDB)
- Конфигурационные файлы
- Frontend ↔ Backend обмен

---

## 2) Модуль `json`: сериализация и десериализация
```py
import json
```

### 2.1 Сериализация (Python → JSON)
Сериализация — преобразование объекта Python в JSON для хранения/передачи.

Две основные функции:
- `json.dumps(obj)` → **JSON-строка**
- `json.dump(obj, file)` → запись JSON **в файл**

**`json.dumps` (в строку)**
```py
import json

data = {"name": "Alice", "age": 25, "is_student": False}
json_string = json.dumps(data)
print(type(json_string))  # <class 'str'>
print(json_string)
```

**`json.dump` (в файл)**
```py
import json

data = {"name": "Alice", "age": 25, "is_student": False}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f)
```

Когда использовать:
- `dumps()` — если нужно передать JSON по сети или сохранить как текст (в БД/логах)
- `dump()` — если нужно записать объект сразу в `.json` файл

---

### 2.2 Десериализация (JSON → Python)
Десериализация — обратное преобразование JSON в объект Python.

Две основные функции:
- `json.loads(json_string)` → из **строки**
- `json.load(file)` → из **файла**

**`json.loads` (из строки)**
```py
import json

json_object = '{"name": "Alice", "age": 25, "is_student": false}'
data_dict = json.loads(json_object)
print(type(data_dict))  # <class 'dict'>
print(data_dict)
```

**`json.load` (из файла)**
```py
import json

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
print(type(data))
print(data)
```

Когда использовать:
- `loads()` — если JSON пришёл строкой (например, из API)
- `load()` — если JSON хранится в файле

---

## 3) Сравнение типов Python и JSON
| Python | JSON | Пример Python | Пример JSON |
|---|---|---|---|
| `dict` | object | `{"name": "Alice"}` | `{"name": "Alice"}` |
| `list` | array | `["apple","banana"]` | `["apple","banana"]` |
| `tuple` | array | `("a","b")` | `["a","b"]` |
| `str` | string | `"Hello"` | `"Hello"` |
| `int` | number | `42` | `42` |
| `float` | number | `3.14` | `3.14` |
| `bool` | boolean | `True/False` | `true/false` |
| `None` | null | `None` | `null` |

Важно:
- `True/False` в JSON пишутся как `true/false` (в нижнем регистре).
- `tuple` превратится в массив (list).
- `set`/`frozenset` **не поддерживаются JSON**.

Пример: запись “всех типов” в файл:
```py
import json

data = {
    "dict_example": {"key": "value"},
    "list_example": ["apple", "banana"],
    "tuple_example": ("apple", "banana"),
    "string_example": "Hello",
    "int_example": 42,
    "float_example": 3.14,
    "bool_example_true": True,
    "bool_example_false": False,
    "none_example": None
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
```

---

## 4) Форматирование JSON
По умолчанию `json.dumps()`/`json.dump()` делают JSON **в одну строку** (нечитабельно).

Главные параметры форматирования:
- `indent` — отступы (красивое представление)
- `ensure_ascii` — как хранить Unicode (кириллица)
- `sort_keys` — сортировка ключей по алфавиту

### 4.1 `indent`
```py
json.dumps(data, indent=4)
```

### 4.2 `ensure_ascii`
- `ensure_ascii=True` (по умолчанию) — не ASCII символы кодируются как `\u....`
- `ensure_ascii=False` — кириллица и Unicode сохраняются “по-человечески”

```py
import json

data = {"город": "Берлин", "страна": "Германия"}
print(json.dumps(data))                   # ensure_ascii=True
print(json.dumps(data, ensure_ascii=False))
```

### 4.3 `sort_keys`
```py
json.dumps(data, indent=4, sort_keys=True)
```

---

## 5) `JSONDecodeError`: что это и почему возникает
`json.JSONDecodeError` возникает, если JSON имеет неверный формат и не может быть разобран.

Типичные причины:
- пропущены кавычки/запятые
- одинарные кавычки вместо двойных (`'` вместо `"`)
- лишняя запятая
- неполные/повреждённые данные

Примеры проблем:
```text
{"name": "Alice", "age": 25, "is_student": false,}   # лишняя запятая
{'name': 'Alice'}                                    # одинарные кавычки
{"name": "Alice", "age": 25                          # нет закрывающей скобки
```

### 5.1 Правильно: `try/except` при загрузке JSON
```py
import json

invalid_json = '{"name": "Alice", "age": 25, "is_student": false,'

try:
    data = json.loads(invalid_json)
except json.JSONDecodeError as e:
    print(f"Ошибка декодирования JSON: {e}")
```

---

## 6) Модуль `datetime`
Модуль `datetime` — инструменты для дат/времени:
- текущее время
- форматирование (в строку)
- парсинг (из строки)
- сравнение дат
- разница дат (`timedelta`)

```py
from datetime import datetime, timedelta
```

### 6.1 `datetime.now()` — текущее дата/время
```py
from datetime import datetime

now = datetime.now()
print(type(now))  # <class 'datetime.datetime'>
print(now)
```

Компоненты даты:
```py
print(now.year, now.month, now.day)
print(now.hour, now.minute, now.second)
```

Зачем:
- временные метки (timestamps)
- логи, отчёты
- время создания/обновления объектов

---

### 6.2 `strftime()` — datetime → строка
`strftime()` форматирует дату/время в строку:

```py
formatted = now.strftime("%d.%m.%Y %H:%M:%S")
print(formatted)
```

Часто используемые коды:
- `%d` день (01–31)
- `%m` месяц (01–12)
- `%Y` год (4 цифры), `%y` (2 цифры)
- `%H` часы 00–23, `%M` минуты, `%S` секунды
- `%A` день недели (полное), `%B` месяц (полное)

Примеры:
```py
print(now.strftime("%Y-%m-%d"))                  # ISO
print(now.strftime("%d/%m/%Y"))                  # европейский
print(now.strftime("%I:%M %p"))                  # 12-часовой
print(now.strftime("%A, %B %d, %Y"))             # Friday, February 28, 2025
```

---

### 6.3 `strptime()` — строка → datetime
Используется, когда дата хранится как текст и нужна для вычислений/фильтрации.

```py
from datetime import datetime

date_string = "28|02|2025 14-30-15"
dt = datetime.strptime(date_string, "%d|%m|%Y %H-%M-%S")
print(dt)
```

Важно: форматные коды и **разделители** должны совпадать со строкой.

---

### 6.4 Сравнение дат
`datetime` можно сравнивать операторами `> < == != >= <=`:

```py
from datetime import datetime

now = datetime.now()
deadline = datetime.strptime("01.12.2025", "%d.%m.%Y")

if now > deadline:
    print("Срок истёк!")
else:
    print("До дедлайна ещё есть время.")
```

---

### 6.5 Разница между датами: `timedelta`
Вычитание дат возвращает `timedelta`:

```py
from datetime import datetime

date1 = datetime(2025, 2, 28)
date2 = datetime(2025, 3, 5)

diff = date2 - date1
print(diff)         # days=...
print(diff.days)    # количество дней
```

Если нужно в секундах:
```py
print(diff.total_seconds())
```

Сдвиг даты:
```py
from datetime import datetime, timedelta

start = datetime(2025, 2, 28)
deadline = start + timedelta(weeks=2)
print(deadline.strftime("%d.%m.%Y"))
```

---

# 7) Ответы на задания для закрепления (с урока)

## Задания 1 (JSON)
1) `json.dumps(data)` → строка, `json.loads(...)` → словарь  
**Ответ:** `<class 'str'>`, `<class 'dict'>` (вариант **b**).

2) Ошибка в коде:
```py
with open("user.json", "w", encoding="utf-8") as f:
    json.dumps(data, f)  # ❌
```
Исправление:
```py
with open("user.json", "w", encoding="utf-8") as f:
    json.dump(data, f)   # ✅
```

3) `json.loads("{'x': 1, 'y': 2}")`  
**Ответ:** будет `JSONDecodeError` (вариант **d**, потому что одинарные кавычки).

4) Почему падает `json.dumps({"values": {1,2,3}})`?  
**Ответ:** JSON не поддерживает множества (`set`) (вариант **b**).

## Задания 2 (datetime)
1) Тип `datetime.now()` → **`datetime`** (вариант **b**)  
2) Формат для `"01|12|2025 14-30-00"` → **`"%d|%m|%Y %H-%M-%S"`** (вариант **c**)  
3) `strftime()` → **преобразует дату в строку** (вариант **d**)

---

# 8) Практическая работа: поиск “низких оценок” за период (готовое решение)

## Задача
- прочитать `grades.json`
- функция `filter_low_scores(threshold, start_date, end_date)`:
  - даты в формате `дд-мм-гггг`
  - выбрать записи, где `grade < threshold` и дата в диапазоне
  - сохранить в `filtered_low_scores.json`

## Решение
```py
import json
from datetime import datetime

def filter_low_scores(threshold: int, start_date_str: str, end_date_str: str) -> list[dict]:
    start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
    end_date = datetime.strptime(end_date_str, "%d-%m-%Y")

    with open("grades.json", "r", encoding="utf-8") as file:
        records = json.load(file)

    filtered = []
    for record in records:
        record_date = datetime.strptime(record["date"], "%d-%m-%Y")
        if record["grade"] < threshold and start_date <= record_date <= end_date:
            filtered.append(record)

    with open("filtered_low_scores.json", "w", encoding="utf-8") as file:
        json.dump(filtered, file, indent=4, ensure_ascii=False)

    print(f"Найдено записей: {len(filtered)}. Сохранено в 'filtered_low_scores.json'.")
    return filtered

filter_low_scores(70, "01-01-2025", "31-03-2025")
```

---

# 9) Домашнее задание: анализ курсов студентов (решение)

## Требования
Прочитать `student_courses.json`, где у каждого студента:
- `name`
- `birth_date` (дд.мм.гггг)
- `enrollment_date` (дд.мм.гггг)
- `courses` (список)

Посчитать:
1) общее количество студентов
2) средний возраст **на момент поступления**
3) количество студентов на каждом курсе

Сохранить отчёт в `student_courses_report.json`.

## Решение
```py
import json
from datetime import datetime
from collections import Counter

DATE_FMT = "%d.%m.%Y"

def years_between(birth: datetime, enroll: datetime) -> float:
    # возраст в годах (приблизительно): дни / 365.25
    return (enroll - birth).days / 365.25

def build_report(input_path="student_courses.json", output_path="student_courses_report.json") -> dict:
    with open(input_path, "r", encoding="utf-8") as f:
        students = json.load(f)

    total_students = len(students)

    ages = []
    course_counter = Counter()

    for s in students:
        birth = datetime.strptime(s["birth_date"], DATE_FMT)
        enroll = datetime.strptime(s["enrollment_date"], DATE_FMT)
        ages.append(years_between(birth, enroll))

        for course in s.get("courses", []):
            course_counter[course] += 1

    avg_age = round(sum(ages) / len(ages), 2) if ages else 0.0

    report = {
        "total_students": total_students,
        "avg_age_at_enrollment_years": avg_age,
        "students_per_course": dict(course_counter),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=4, sort_keys=True)

    return report

if __name__ == "__main__":
    build_report()
```

---

## Мини-шпаргалка
```text
JSON:
- dumps(obj) -> JSON-строка (str)
- dump(obj, file) -> запись в файл
- loads(str) -> объект Python
- load(file) -> объект Python из файла
Форматирование:
- indent=4
- ensure_ascii=False (кириллица)
- sort_keys=True

Ошибки:
- json.JSONDecodeError -> неверный формат JSON
- try/except обязателен при чтении “внешнего” JSON

datetime:
- datetime.now() -> текущая дата+время
- dt.strftime(fmt) -> dt -> str
- datetime.strptime(str, fmt) -> str -> datetime
- dt2 - dt1 -> timedelta
- timedelta.days / total_seconds()
```
