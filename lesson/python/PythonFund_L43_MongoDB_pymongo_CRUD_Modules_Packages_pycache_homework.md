# Python Fundamentals — Урок 43: MongoDB + Python (pymongo, CRUD) + Модули и пакеты

> Конспект по уроку: работа с MongoDB из Python (подключение, CRUD, фильтры, курсор, проекции, обработка ошибок) + базовые понятия модулей/пакетов (`__init__.py`, `__pycache__`, `if __name__ == "__main__":`).

---

## 1) MongoDB и Python: база и подготовка

### Что такое MongoDB
MongoDB — **документоориентированная** база данных: данные хранятся в **документах** (по сути, Python-словарях), объединённых в **коллекции**.

Ключевые особенности:
- Документ = `dict`, структура **не обязана быть фиксированной** заранее.
- Коллекции и базы могут создаваться **автоматически** при первой вставке.
- В отличие от SQL: не нужно `CREATE TABLE ...` до первой записи (в базовом сценарии).

### Библиотека для Python
Используем `pymongo`:

```bash
pip install pymongo
```

---

## 2) Подключение к серверу MongoDB

### MongoClient и строка подключения
Для подключения создаём объект `MongoClient` и передаём connection string:

```py
from pymongo import MongoClient

client = MongoClient(
    "mongodb://USER:PASSWORD@HOST/?readPreference=primary&ssl=false&authMechanism=DEFAULT&authSource=DB_AUTH"
)
```

Где обычно:
- `USER` / `PASSWORD` — логин/пароль,
- `HOST` — адрес сервера,
- `authSource=...` — база, где хранятся учётные данные (часто отличается от целевой базы).

### Проверка подключения (ping)
```py
client.admin.command("ping")
print("Connection successful!")
```

### Выбор базы и коллекции
```py
db = client["ich_edit"]          # база
products = db["products"]        # коллекция
```

Особенности:
- если базы/коллекции не существует — она появится при первой вставке;
- подключение **ленивое**: реальное соединение происходит при первом запросе.

### Закрытие соединения
```py
client.close()
```
Обычно MongoClient закроется и сам при завершении программы, но вручную закрывать — хорошая практика.

---

## 3) Добавление данных (Create)

### insert_one — один документ
```py
product = {"name": "Notebook", "price": 5.99, "stock": 120}
result = products.insert_one(product)
print("Inserted ID:", result.inserted_id)
```

### insert_many — несколько документов
```py
items = [
    {"name": "Pen", "price": 1.50, "stock": 300},
    {"name": "Pencil", "price": 0.99, "stock": 500},
    {"name": "Eraser", "price": 0.75, "stock": 200},
]
result = products.insert_many(items)
print("Inserted IDs:", result.inserted_ids)
```

Важно:
- если `_id` не указан — MongoDB создаёт его автоматически;
- документы могут иметь разную структуру (если вы это допускаете).

---

## 4) Чтение данных (Read): find_one / find + курсор

### find_one — один документ
```py
doc = products.find_one()
print(doc)  # dict или None
```

### find — много документов
`find()` возвращает **курсор (итератор)**, а не список:

```py
cursor = products.find()
for item in cursor:
    print(item)
```

Фильтрация — словарём, например `price < 5`:
```py
for item in products.find({"price": {"$lt": 5}}):
    print(item)
```

### Почему это важно: курсор одноразовый
После полного перебора курсор “заканчивается” и повторно уже не отдаст документы.
Если нужно использовать результаты несколько раз — делайте `list(...)`:

```py
results = list(products.find({"price": {"$lt": 5}}))
```

### sort / skip / limit
```py
for doc in products.find().sort("price", -1).skip(1).limit(2):
    print(doc)
```

Памятка:
- `.sort("field", 1)` — по возрастанию
- `.sort("field", -1)` — по убыванию
- `.skip(n)` — пропустить
- `.limit(n)` — ограничить количество

---

## 5) Проекция полей (выбор нужных полей)

По умолчанию возвращаются **все поля**. Проекция позволяет оставить нужные:

```py
# Вернёт только name, price и _id (по умолчанию)
for doc in products.find({}, {"name": 1, "price": 1}):
    print(doc)
```

Исключить `_id`:
```py
for doc in products.find({}, {"_id": 0}):
    print(doc)
```

Оставить только `name` и убрать `_id`:
```py
for doc in products.find({}, {"_id": 0, "name": 1}):
    print(doc)
```

---

## 6) Обновление данных (Update): update_one / update_many

MongoDB обновляет документы через модификаторы (`$set`, `$inc`, …).

### update_one — обновить один (первый подходящий)
```py
result = products.update_one(
    {"name": "Notebook"},          # фильтр
    {"$set": {"price": 24.99}}     # изменение
)
print("Matched:", result.matched_count)
print("Modified:", result.modified_count)
```

### update_many — обновить все подходящие
Например, увеличить цену на 1 для всех:
```py
result = products.update_many(
    {},
    {"$inc": {"price": 1}}
)
print("Matched:", result.matched_count)
print("Modified:", result.modified_count)
```

---

## 7) Удаление данных (Delete): delete_one / delete_many

### delete_one — удалить один документ
```py
result = products.delete_one({"name": "Notebook"})
print("Deleted:", result.deleted_count)   # 0 или 1
```

### delete_many — удалить все по фильтру
```py
result = products.delete_many({"price": {"$lt": 2}})
print("Deleted:", result.deleted_count)
```

---

## 8) Обработка ошибок (try/except) в pymongo

Типичные проблемы:
- сервер недоступен;
- неправильный пароль/авторизация;
- дубликат ключа `_id` (или другого уникального индекса).

Пример:
```py
from pymongo import MongoClient, errors

try:
    client = MongoClient("mongodb://USER:WRONG_PASS@HOST/?authSource=ich_edit")
    db = client["store"]
    products = db["products"]
    products.insert_one({"name": "Lamp", "price": 15.99})
except errors.ConnectionFailure:
    print("Ошибка подключения к MongoDB")
except errors.OperationFailure:
    print("Ошибка авторизации или запроса")
except errors.DuplicateKeyError:
    print("Дубликат ключа (_id или уникальный индекс)")
except errors.PyMongoError as e:
    print("Другая ошибка pymongo:", e)
```

Полезные классы исключений:
- `errors.ConnectionFailure`
- `errors.OperationFailure`
- `errors.DuplicateKeyError`
- `errors.PyMongoError` (базовый для всех ошибок)

---

# Задания для закрепления 1 — ответы

1) Способы добавить данные в коллекцию MongoDB: **insert_one(), insert_many()**  
2) Какой тип данных возвращает `find()`? **Курсор (итератор)**

---

# Практическая работа (урок)

## Задача 1: найти заказы с amount < 10
```py
from pymongo import MongoClient

client = MongoClient("mongodb://USER:PASSWORD@HOST/?readPreference=primary&ssl=false&authSource=ich_edit")
db = client["ich_edit"]
orders = db["orders"]

results = list(orders.find({"amount": {"$lt": 10}}))
for order in results:
    print(order)

client.close()
```

## Задача 2: сохранить найденное в orders_lesson_43
```py
orders_lesson_43 = db["orders_lesson_43"]
orders_lesson_43.delete_many({})  # очистить перед вставкой

if results:
    insert_result = orders_lesson_43.insert_many(results)
    print(f"{len(insert_result.inserted_ids)} documents inserted into 'orders_lesson_43'.")
else:
    print("No documents to insert.")
```

---

## 9) Модули в Python

### Что такое модуль
**Модуль** — это любой файл `.py`, в котором есть переменные/функции/классы и т.д.

### Зачем нужны
- структура проекта и разделение “по смыслу”;
- читаемость и сопровождение;
- переиспользование кода;
- использование модулей стандартной библиотеки;
- упрощение тестирования.

### Виды модулей
- встроенные (stdlib): `math`, `random`, `datetime`
- сторонние: ставятся через `pip` (например `pymongo`)
- пользовательские: ваши `.py` файлы

### Пример: свой модуль `math_utils.py`
`math_utils.py`:
```py
print("Inside math_utils.py")

def average(numbers):
    return sum(numbers) / len(numbers)

def maximum(numbers):
    return max(numbers)
```

`main.py`:
```py
import math_utils
from math_utils import maximum

values = [10, 20, 30]
print(math_utils.average(values))
print(maximum(values))
```

### Прямой запуск модуля: `if __name__ == "__main__":`
Эта конструкция помогает отличить:
- импорт как библиотека (код НЕ должен выполняться “побочно”),
- запуск напрямую как скрипт.

```py
if __name__ == "__main__":
    print("Run only when executed directly")
```

---

## 10) __pycache__ и .pyc
При импорте модуля Python компилирует его в байт-код и кладёт в:

- `__pycache__/module.cpython-312.pyc` (пример имени)

Когда `.pyc` пересоздаётся:
- при первом импорте модуля,
- если изменился `.py` файл,
- если обновилась версия Python.

---

## 11) Пакеты и папки (packages)

### Что такое пакет
**Пакет** — папка с модулями + файл `__init__.py`.

`__init__.py`:
- “объявляет” папку пакетом,
- часто управляет тем, что будет доступно при `import package`.

### Пример структуры
```
modules/
├── main.py
├── analyzer.py
└── tools/
    ├── __init__.py
    ├── text_utils.py
    └── helpers/
        ├── __init__.py
        └── string_tools.py
```

`tools/text_utils.py`:
```py
def count_words(text):
    return len(text.split())
```

`tools/helpers/string_tools.py`:
```py
def reverse(text):
    return text[::-1]
```

`tools/__init__.py` (собираем удобный публичный интерфейс):
```py
from .text_utils import count_words
from .helpers.string_tools import reverse
```

`analyzer.py` (вне пакета):
```py
import tools

text = "What a beautiful day to learn Python!"
print(tools.count_words(text))
print(tools.reverse(text))
```

---

# Задания для закрепления 2 — ответы

1) Термин → определение: **1-b, 2-a, 3-d, 4-c**  
- 1. модуль → b  
- 2. пакет → a  
- 3. __pycache__ → d  
- 4. __init__.py → c  

2) Что делает `__pycache__/...pyc`? → **b** (скомпилированная версия `.py` файла)

---

# Домашнее задание (по уроку)

## ДЗ 1: добавить товары
Нужно:
- подключиться к MongoDB,
- выбрать базу `ich_edit`,
- коллекцию `products_<your_group>_<your_full_name>`,
- очистить коллекцию,
- добавить 3 товара (name, price, stock),
- вывести “сколько добавлено”.

Шаблон:
```py
from pymongo import MongoClient

client = MongoClient("mongodb://USER:PASSWORD@HOST/?readPreference=primary&ssl=false&authSource=ich_edit")
db = client["ich_edit"]

coll = db["products_<your_group>_<your_full_name>"]
coll.delete_many({})

items = [
    {"name": "Pen", "price": 1.50, "stock": 300},
    {"name": "Notebook", "price": 3.99, "stock": 120},
    {"name": "Backpack", "price": 25.00, "stock": 15},
]

result = coll.insert_many(items)
print(f"{len(result.inserted_ids)} products inserted.")

client.close()
```

## ДЗ 2: увеличить цены на 20% и вывести всё
Идея: массовое обновление `update_many`.
Чаще всего удобнее использовать `$mul`:

```py
# увеличить все цены на 20%
upd = coll.update_many({}, {"$mul": {"price": 1.2}})
print(f"Prices updated for {upd.modified_count} products.")

print("Updated products:")
for p in coll.find({}, {"_id": 0, "name": 1, "price": 1}).sort("name", 1):
    print(f"- {p['name']} — ${p['price']:.2f}")
```

---

## Мини-шпаргалка урока
```text
MongoDB + pymongo:
- client = MongoClient("mongodb://...")
- db = client["db_name"]
- coll = db["collection_name"]

Create:
- insert_one(dict), insert_many([dict, ...])

Read:
- find_one(filter?), find(filter?) -> cursor (итератор)
- sort(field, 1/-1), skip(n), limit(n)
- projection: find({}, {"field": 1, "_id": 0})

Update:
- update_one(filter, {"$set": {...}})
- update_many(filter, {"$inc": {...}}), {"$mul": {...}}

Delete:
- delete_one(filter), delete_many(filter)

Errors:
from pymongo import errors
errors.ConnectionFailure / OperationFailure / DuplicateKeyError / PyMongoError

Modules & packages:
- module = любой .py
- package = папка + __init__.py
- if __name__ == "__main__": ...
- __pycache__/...pyc = байткод при импорте
```
