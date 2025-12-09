# JSON datetime сериализация форматирование

## 📖 Быстрая навигация по операторам и функциям

- [[#0) План урока]](#0-план-урока)
- [[#1) JSON — что это]](#1-json-—-что-это)
- [[#2) Модуль `json`: сериализация и десериализация]](#2-модуль-json-сериализация-и-десериализация)
- [[#3) Сравнение типов Python и JSON]](#3-сравнение-типов-python-и-json)
- [[#4) Форматирование JSON]](#4-форматирование-json)
- [[#5) `JSONDecodeError`: что это и почему возникает]](#5-jsondecodeerror-что-это-и-почему-возникает)
- [[#6) Модуль `datetime`]](#6-модуль-datetime)
- [[#Задания 1 (JSON)]](#задания-1-json)
- [[#Задания 2 (datetime)]](#задания-2-datetime)
- [[#Задача]](#задача)
- [[#Решение]](#решение)
- [[#Требования]](#требования)
- [[#Решение]](#решение)
- [[#Мини-шпаргалка]](#мини-шпаргалка)
- [[#Дополнительная информация]](#дополнительная-информация)



## 1) JSON — что это
**JSON (JavaScript Object Notation)** — текстовый формат для хранения и передачи структурированных данных.
### Важные концепции для изучения

#### 1. json.dumps/json.loads — ключевые параметры
```python
import json

data = {"name": "Алиса", "age": 30, "skills": ["python", "sql"]}

text = json.dumps(
    data,
    ensure_ascii=False,  # не экранировать кириллицу
    indent=2,            # форматирование
    sort_keys=True       # сортировать ключи
)
print(text)

restored = json.loads(text)
print(restored["name"])

# Работа с файлами
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)
```

#### 2. Сериализация нестандартных типов (datetime, Decimal, set)
```python
from datetime import datetime, timezone
from decimal import Decimal
import json

def default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, set):
        return list(obj)
    raise TypeError(f"Не сериализуемый тип: {type(obj)}")

payload = {
    "ts": datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc),
    "price": Decimal("10.5"),
    "tags": {"python", "json"},
}

text = json.dumps(payload, default=default, ensure_ascii=False)
print(text)
```

#### 3. datetime: aware vs naive, форматирование и парсинг
```python
from datetime import datetime, timedelta, timezone

now_naive = datetime.now()               # naive (без TZ)
now_utc = datetime.now(timezone.utc)     # aware (с TZ)

# Форматирование и парсинг
fmt = "%Y-%m-%d %H:%M:%S%z"
text = now_utc.strftime(fmt)
parsed = datetime.strptime(text, fmt)
print(parsed.tzinfo)  # UTC

# ISO 8601
iso = now_utc.isoformat()  # 2024-01-01T12:00:00+00:00
parsed_iso = datetime.fromisoformat(iso)

# Операции со временем
future = now_utc + timedelta(days=3, hours=2)
delta = future - now_utc
print(delta.total_seconds())

# Перевод в timestamp и обратно
ts = now_utc.timestamp()
print(datetime.fromtimestamp(ts, tz=timezone.utc))
```

#### 4. Безопасный парсинг и валидация JSON
```python
import json
from typing import Any, Dict

def load_json_safe(text: str) -> Dict[str, Any]:
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Невалидный JSON: {e}")
    if not isinstance(obj, dict):
        raise ValueError("Ожидался объект JSON")
    return obj

bad = "{name: 123}"  # невалидный JSON
try:
    load_json_safe(bad)
except ValueError as e:
    print(e)
```

### 💡 Практические примеры

#### Пример 1: JSON Lines обработка больших логов
```python
import json
from typing import Iterable

def read_jsonl(path: str) -> Iterable[dict]:
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def write_jsonl(path: str, records: Iterable[dict]):
    with open(path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

# Применение
records = [{"id": 1}, {"id": 2}]
write_jsonl("out.jsonl", records)
print(list(read_jsonl("out.jsonl")))
```

#### Пример 2: Человекочитаемые даты и time zones
```python
from datetime import datetime, timezone, timedelta

def format_human(dt: datetime) -> str:
    return dt.strftime("%d.%m.%Y %H:%M")

dt_local = datetime.now()  # naive локальное
dt_utc = datetime.now(timezone.utc)

print(format_human(dt_local))
print(format_human(dt_utc.astimezone(timezone(timedelta(hours=3)))))
```

#### Пример 3: Кэширование ответов с датой истечения
```python
from datetime import datetime, timedelta, timezone

cache = {}

def set_cache(key, value, ttl_seconds=60):
    expires = datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)
    cache[key] = {"value": value, "expires": expires}

def get_cache(key):
    item = cache.get(key)
    if not item:
        return None
    if datetime.now(timezone.utc) > item["expires"]:
        cache.pop(key, None)
        return None
    return item["value"]

set_cache("user:1", {"name": "Алиса"}, ttl_seconds=2)
print(get_cache("user:1"))
```

#### Пример 4: Валидация и нормализация дат
```python
from datetime import datetime

def parse_date(value: str) -> datetime:
    formats = ["%Y-%m-%d", "%d.%m.%Y", "%Y/%m/%d"]
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError("Не удалось распарсить дату")

print(parse_date("2024-01-10"))
print(parse_date("10.01.2024"))
```

### 🚨 Частые ошибки

**Ошибка 1: Потеря кириллицы при JSON-сериализации**
```python
# ❌ По умолчанию ensure_ascii=True
json.dumps({"text": "Привет"})  # "\u041f..."

# ✅
json.dumps({"text": "Привет"}, ensure_ascii=False)
```

**Ошибка 2: Использование datetime.now() без TZ для хранения**
```python
# ❌ naive время, непереносимо между зонами
dt = datetime.now()

# ✅ всегда храните в UTC
dt = datetime.now(timezone.utc)
```

**Ошибка 3: json.loads на огромных строках в память**
```python
# ❌ загрузка всего файла в память
data = json.loads(open("huge.json").read())

# ✅ потоковое чтение JSONL или парсер с потоковой обработкой
```

**Ошибка 4: Ошибка при сериализации нестандартных типов**
```python
from datetime import datetime
import json

obj = {"ts": datetime.now()}
# ❌ TypeError: Object of type datetime is not JSON serializable

# ✅ default или свой encoder
json.dumps(obj, default=lambda o: o.isoformat())
```

### 📌 Полезные ресурсы
- [Документация: json](https://docs.python.org/3/library/json.html)
- [Документация: datetime](https://docs.python.org/3/library/datetime.html)
- [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
- [json.JSONDecodeError](https://docs.python.org/3/library/json.html#json.JSONDecodeError)
- [Работа с часовыми поясами](https://docs.python.org/3/library/datetime.html#timezone-objects)
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


---

## Дополнительная информация

_Этот раздел будет дополнен практическими примерами и дополнительной информацией._
