# MySQL Python подключение курсор with

> Работа с MySQL из Python: подключение, выполнение запросов, безопасная подстановка параметров, обработка ошибок и использование контекстных менеджеров.

---

## 0) План урока

- Зачем вообще база данных в приложении
- Подключение к MySQL из Python (PyMySQL)
- Работа с курсором
- Получение результатов запроса
- Параметризованные запросы (`%s`)
- Именованные параметры (`%(name)s`)
- Обработка ошибок (`try/except`, `pymysql.MySQLError`)
- Контекстный менеджер `with` для соединения и курсора

---

## 1) Зачем использовать БД из Python

Когда программа растёт, появляются:
- заказы, пользователи, сообщения, логи и т.д.  
- нужно **хранить много данных**, быстро искать/обновлять, давать доступ нескольким пользователям.

База данных (MySQL):
- хранит структурированные данные вне программы;
- позволяет работать с очень большими объёмами без загрузки всего в память;
- даёт многопользовательский доступ и защиту;
- делает систему надёжной и масштабируемой.

Для Python есть библиотеки-клиенты, которые:
- устанавливают соединение с MySQL,
- отправляют SQL-запросы и возвращают результаты,
- превращают ошибки БД в исключения Python.

---

## 2) Библиотеки для MySQL и установка PyMySQL

Популярные варианты:

| Библиотека               | Особенности                                      |
|--------------------------|--------------------------------------------------|
| `PyMySQL`                | Простая, полностью на Python, легко ставится    |
| `mysql-connector-python` | Официальный драйвер от MySQL                    |
| `MySQLdb (mysqlclient)`  | Очень быстрая, но сложнее установка (особенно Windows) |

В курсе используется **PyMySQL** (кроссплатформенно и без боли).

Установка:

```bash
pip install pymysql
```

---

## 3) Подключение к базе данных

### Базовый вариант

```py
import pymysql  # импорт модуля

connection = pymysql.connect(
    host="localhost",        # адрес сервера
    user="root",             # пользователь
    password="yourpassword", # пароль
    database="yourdatabase", # имя БД (можно опустить)
    charset="utf8mb4",       # кодировка соединения (для русского текста)
)
```

### Конфиг словарём + распаковка `**`

Удобно, если параметры переиспользуются/лежат в файле `.env`, JSON, YAML и т.п.:

```py
import pymysql

config = {
    "host": "ich-db.edu.itcareerhub.de",
    "user": "ich1",
    "password": "password",
    "database": "hr",
}

connection = pymysql.connect(**config)  # распаковка словаря аргументами
```

### Проверка соединения и закрытие

```py
if connection.open:
    print("Connection successful!")

connection.close()
```

Почему важно закрывать соединение:
- каждое подключение занимает ресурсы сервера;
- есть лимит одновременных соединений;
- хорошая практика: закрывать сразу, как только не нужно.

---

## 4) Курсор: выполнение SQL из Python

После подключения нужен **курсор** — объект, через который:
- отправляются SQL-запросы,
- читаются результаты.

### Создание и закрытие курсора

```py
cursor = connection.cursor()   # создать
# ...
cursor.close()                 # закрыть
```

- один курсор можно использовать для **нескольких запросов**;
- после закрытия курсора, для новых запросов нужно создать новый;
- курсор сам по себе **не создаётся** — только явно через `connection.cursor()`.

### Выполнение запросов

```py
cursor = connection.cursor()
cursor.execute("SELECT * FROM departments")
```

Особенности:
- `cursor.execute(sql)` отправляет строку SQL на сервер;
- можно выполнять любые запросы: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `CREATE` и т.д.;
- при ошибке в SQL выбрасывается исключение;
- некоторые драйверы требуют, чтобы перед новым запросом были прочитаны результаты старого.

---

## 5) Получение результатов: `fetchone`, `fetchmany`, `fetchall`, итерация по курсору

После `SELECT` данные остаются в курсоре, пока вы их не заберёте.

### Основные методы

| Метод             | Что делает                            |
|-------------------|---------------------------------------|
| `fetchone()`      | вернуть **одну** следующую строку     |
| `fetchall()`      | вернуть **все оставшиеся** строки     |
| `fetchmany(size)` | вернуть указанное количество строк    |

Пример:

```py
cursor.execute("SELECT * FROM departments")

row = cursor.fetchone()    # одна строка
print("One row:", row)

rows_5 = cursor.fetchmany(5)
print("Five rows:")
for r in rows_5:
    print("   ", r)

rows = cursor.fetchall()   # все оставшиеся строки
print("All rows:")
for r in rows:
    print("   ", r)
```

Особенности:
- после того как строки считаны, повторный `fetchall()` вернёт **пустой список**, `fetchone()` — `None`;
- `fetchmany(size)` удобно на больших выборках — читаем порциями;
- данные не загружаются заранее — читаются по мере вызовов методов;
- курсор — это **итератор**: можно просто писать

```py
cursor.execute("SELECT * FROM employees")
for row in cursor:
    print(row)
```

Это эквивалентно последовательным вызовам `fetchone()`, но короче.

---

## 6) Параметризованные запросы (позиционные параметры `%s`)

Никогда не вставляем пользовательский ввод прямо в SQL-строку — это приводит к **SQL‑инъекциям**.

Плохо:

```py
user_input = "1 OR 1=1"
sql = f"SELECT * FROM employees WHERE employee_id = {user_input}"
cursor.execute(sql)  # выполнится "… WHERE employee_id = 1 OR 1=1"
```

Вместо этого используем **плейсхолдеры** `%s` и передаём значения отдельно:

```py
cursor.execute(
    "SELECT * FROM table_name WHERE column1 = %s AND column2 > %s",
    (value1, value2),
)
```

- первый аргумент — SQL с `%s` на месте значений;
- второй — кортеж/список значений в **том же порядке**, что и плейсхолдеры.

### Пример с двумя параметрами

```py
cursor.execute(
    "SELECT * FROM employees WHERE department_id = %s OR salary > %s",
    (60, 20000),
)
for r in cursor:
    print(r)
```

### Один параметр → не забываем запятую

```py
cursor.execute(
    "SELECT * FROM employees WHERE department_id = %s",
    (100,),      # кортеж из одного элемента
)
```

### Плюсы параметризованных запросов

- защита от SQL‑инъекций;
- библиотека сама экранирует строки и приводит типы;
- один и тот же SQL можно выполнять с разными данными;
- сервер может кэшировать план запроса → выше производительность.

---

## 7) Именованные параметры: `%(name)s` + словарь

Когда параметров много, удобнее **именованные** плейсхолдеры:

```py
cursor.execute(
    """
    SELECT * FROM table_name
    WHERE column1 = %(param1)s AND column2 > %(param2)s
    """,
    {"param1": value1, "param2": value2},
)
```

- в SQL используем `%(имя)s`;
- вторым аргументом отдаём словарь с такими же ключами;
- порядок ключей не важен — важны именно имена.

Пример:

```py
cursor.execute(
    """
    SELECT * FROM employees
    WHERE department_id = %(dep_id)s OR salary > %(min_salary)s
    """,
    {"min_salary": 20000, "dep_id": 60},
)
for r in cursor:
    print(r)
```

Плюсы:
- лучше читается запрос;
- удобно, когда данные уже приходят в виде словаря;
- меньше риска перепутать порядок аргументов.

---

## 8) Обработка ошибок (`try/except` и `pymysql.MySQLError`)

Типичные ошибки:
- неверный пароль/хост;
- неправильный SQL;
- нет таблицы;
- нарушение ограничений (уникальность и т.п.).

Чтобы программа не падала, оборачиваем операции в `try/except`.

### Ошибка подключения

```py
import pymysql

try:
    connection = pymysql.connect(
        host="ich-db.edu.itcareerhub.de",
        user="root",
        password="wrong_password",   # неправильный пароль
        database="test",
    )
    print("Connected!")
except pymysql.MySQLError as e:
    print("Connection error:", e)
```

### Ошибка запроса

```py
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM non_existing_table")
        result = cursor.fetchall()
except pymysql.MySQLError as e:
    print("Query error:", e)
```

Особенности:
- базовый класс всех исключений PyMySQL: `pymysql.MySQLError`;
- при необходимости можно ловить более конкретные:  
  `pymysql.ProgrammingError`, `pymysql.OperationalError` и т.д.

---

## 9) Контекстный менеджер `with` для соединения и курсора

Чтобы не забывать закрывать соединение и курсоры, используем `with`.

```py
import pymysql

with pymysql.connect(
    host="ich-db.edu.itcareerhub.de",
    user="ich1",
    password="password",
    database="hr",
) as connection:                   # по выходу из блока connection.close()
    with connection.cursor() as cursor:   # по выходу cursor.close()
        cursor.execute("SELECT * FROM employees")
        for row in cursor:
            print(row)
```

Плюсы `with`:
- автоматически вызывает `close()` даже при исключениях;
- код становится короче и безопаснее;
- внутри можно выполнять любые запросы, не только `SELECT`.

---

## 10) Задания с урока — ответы (коротко)

### Закрепление 1 (подключение и курсор)

1. Сопоставьте понятие с описанием:

1. `pymysql.connect()`  
2. `cursor.execute()`  
3. `connection.close()`  
4. `cursor = connection.cursor()`  

→ **Ответ:** 1–d, 2–b, 3–a, 4–c  

- d: создаёт подключение к MySQL  
- b: выполняет SQL‑запрос  
- a: закрывает соединение  
- c: создаёт курсор

2. Выберите корректные утверждения:

- верные: **c, e**  
  - c: один курсор можно использовать для нескольких запросов  
  - e: `connection.open` проверяет статус соединения

### Закрепление 2 (параметры, fetch, with)

1. Зачем использовать параметризованные запросы?  
   → **b, c:** защита от SQL‑инъекций + правильная подстановка значений и экранирование.

2. Что будет, если вызвать `fetchall()` ещё раз после чтения всех строк?  
   → Вернётся **пустая коллекция** (список).

3. Какие утверждения верны для `with`?  
   → **a, b, c:**  
   - соединение автоматически закрывается после блока `with`;  
   - внутри можно использовать вложенный `with connection.cursor()`;  
   - `with` помогает автоматически закрыть соединение даже при ошибке.

---

## 11) Домашнее задание — идеи решений

> Домашка использует базу **world** (таблицы `country`, `city`). Примеры ниже — общий шаблон, параметры подключения подставь свои.

### ДЗ 1. Список всех стран с нумерацией

**Задача:** вывести все страны из `country` в формате:

```text
1. Aruba
2. Afghanistan
...
```

Пример решения:

```py
import pymysql

config = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "world",
    "charset": "utf8mb4",
}

with pymysql.connect(**config) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT Name FROM country ORDER BY Name")
        countries = cursor.fetchall()

for i, (name,) in enumerate(countries, start=1):
    print(f"{i}. {name}")
```

### ДЗ 2. Города выбранной страны

**Задача:**
1. спросить у пользователя название страны;
2. вывести города этой страны и население (`city.Name`, `city.Population`).

Пример решения:

```py
import pymysql

config = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "world",
    "charset": "utf8mb4",
}

country_name = input("Введите страну: ")

with pymysql.connect(**config) as connection:
    with connection.cursor() as cursor:
        sql = """
        SELECT city.Name, city.Population
        FROM city
        JOIN country ON city.CountryCode = country.Code
        WHERE country.Name = %s
        ORDER BY city.Population DESC
        """
        cursor.execute(sql, (country_name,))
        rows = cursor.fetchall()

if not rows:
    print("Города не найдены (проверьте название страны).")
else:
    for name, population in rows:
        print(f"{name} — {population}")
```

---

## Мини-шпаргалка урока

```text
Подключение:
import pymysql
conn = pymysql.connect(host=..., user=..., password=..., database=...)
cursor = conn.cursor()
cursor.execute("SELECT ...")

Получение данных:
fetchone()   -> одна строка или None
fetchmany(n) -> n строк
fetchall()   -> список всех оставшихся строк
for row in cursor: ...  # курсор как итератор

Параметры:
cursor.execute("... WHERE id = %s", (value,))
cursor.execute("... WHERE x = %(x)s", {"x": value})

Ошибки:
try/except pymysql.MySQLError

Контекстные менеджеры:
with pymysql.connect(...) as conn:
    with conn.cursor() as cursor:
        cursor.execute(...)
```
