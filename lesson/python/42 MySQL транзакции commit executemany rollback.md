# MySQL транзакции commit executemany rollback

## 📖 Быстрая навигация по операторам и функциям

- [[#0) План урока]](#0-план-урока)
- [[#1) Подключение без указания базы данных]](#1-подключение-без-указания-базы-данных)
- [[#2) Выбор базы данных после подключения: команда `USE`]](#2-выбор-базы-данных-после-подключения-команда-use)
- [[#3) DictCursor — результаты как словари]](#3-dictcursor-—-результаты-как-словари)
- [[#4) `commit()` — фиксация изменений]](#4-commit-—-фиксация-изменений)
- [[#5) Подключение с правами на изменения (создание БД/таблиц)]](#5-подключение-с-правами-на-изменения-создание-бдтаблиц)
- [[#6) `executemany()` — массовые операции]](#6-executemany-—-массовые-операции)
- [[#7) Транзакции: атомарность “всё или ничего”]](#7-транзакции-атомарность-“всё-или-ничего”)
- [[#8) `rollback()` — откат изменений]](#8-rollback-—-откат-изменений)
- [[#Закрепление 1]](#закрепление-1)
- [[#Закрепление 2]](#закрепление-2)
- [[#1) Добавление товаров в таблицу `market.products`]](#1-добавление-товаров-в-таблицу-marketproducts)
- [[#2) Массовое повышение цен на 20% одним UPDATE]](#2-массовое-повышение-цен-на-20-одним-update)
- [[#ДЗ 1) Создание базы `notes_app_<your_group>_<your_full_name>`]](#дз-1-создание-базы-notesappyourgroupyourfullname)
- [[#ДЗ 2) Добавление заметок]](#дз-2-добавление-заметок)
- [[#Мини-шпаргалка урока]](#мини-шпаргалка-урока)
- [[#📚 Дополнительная информация]](#📚-дополнительная-информация)

**[[#📚 Дополнительная информация]](#дополнительная-информация)**

---

## 0) План урока
- Подключение без указания базы
- Выбор базы данных после подключения (`USE ...`)
- `DictCursor`
- `commit()` и почему без него изменения не сохраняются
- Подключение к серверу с правами на изменения (создание БД/таблиц)
- `executemany()`
- Транзакции
- `rollback()`

---

## 1) Подключение без указания базы данных
При подключении к MySQL через `pymysql.connect()` **параметр `database=...` не обязателен**.

Это полезно, если вы:
- хотите подключиться, а **базу выбрать позже** вручную;
- выполняете **админские задачи** (создание/удаление баз);
- хотите **переключаться между базами** в одном соединении.

Пример: посмотреть базы на сервере
```py
import pymysql

config = {
    "host": "ich-db.edu.itcareerhub.de",
    "user": "ich1",
    "password": "password",
}

connection = pymysql.connect(**config)

with connection.cursor() as cursor:
    cursor.execute("SHOW DATABASES")
    for db in cursor:
        print(db)

connection.close()
```

---

## 2) Выбор базы данных после подключения: команда `USE`
Если не указали `database` при подключении — базу можно выбрать SQL-командой:

```py
cursor.execute("USE hr")
```

Особенности:
- `USE` выбирает базу **только на время текущего соединения**.
- Если база не выбрана, запрос к таблице даст ошибку **`No database selected`**.
- Можно переключать базу когда угодно: `USE другой_базы`.

Пример:
```py
import pymysql

config = {
    "host": "ich-db.edu.itcareerhub.de",
    "user": "ich1",
    "password": "password",
}

with pymysql.connect(**config) as connection:
    with connection.cursor() as cursor:
        cursor.execute("USE hr")
        cursor.execute("SHOW TABLES")
        for row in cursor:
            print(row)
```

---

## 3) DictCursor — результаты как словари
По умолчанию курсор возвращает строки как **кортежи**.  
`DictCursor` позволяет получать строки как **словарь**, где ключи — имена колонок.

Подключение с `DictCursor`:
```py
import pymysql
from pymysql.cursors import DictCursor

config = {
    "host": "ich-db.edu.itcareerhub.de",
    "user": "ich1",
    "password": "password",
    "database": "hr",
    "cursorclass": DictCursor,
}

connection = pymysql.connect(**config)
```

Пример чтения:
```py
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM employees")
    row = cursor.fetchone()
    print(row)                 # dict
    print(row["first_name"])   # доступ по имени колонки
```

---

## 4) `commit()` — фиксация изменений
Для запросов, которые меняют данные:
- `INSERT`
- `UPDATE`
- `DELETE`

…изменения сначала попадают во **временное хранилище транзакции**. Чтобы записать их окончательно, нужен:

```py
connection.commit()
```

Почему важно:
- без `commit()` изменения **не сохраняются** и будут потеряны при закрытии соединения;
- это “страховка”: изменения применяются только после явного подтверждения.

Важно: `CREATE DATABASE` и `CREATE TABLE` (DDL) **обычно не требуют** `commit()` — такие команды сохраняются сразу (как в материалах урока).

---

## 5) Подключение с правами на изменения (создание БД/таблиц)
Чтобы создавать базы/таблицы в учебной среде, нужно подключаться к серверу с правами на изменения:

```py
config = {
    "host": "ich-edit.edu.itcareerhub.de",
    "user": "ich1",
    "password": "ich1_password_ilovedbs",
}
```

Пример: создание БД и таблицы `sales`
```py
import pymysql

config = {
    "host": "ich-edit.edu.itcareerhub.de",
    "user": "ich1",
    "password": "ich1_password_ilovedbs",
}

with pymysql.connect(**config) as connection:
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS market")
        cursor.execute("USE market")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item_name VARCHAR(100),
            quantity INT,
            price DECIMAL(10, 2),
            sale_date DATE
        )
        """)
```

Вставка / обновление / удаление (нужен `commit()`):
```py
# INSERT
cursor.execute(
    "INSERT INTO sales (item_name, quantity, price, sale_date) VALUES (%s, %s, %s, %s)",
    ("Keyboard", 2, 45.50, "2024-06-15")
)
connection.commit()

# UPDATE
cursor.execute(
    "UPDATE sales SET quantity = %s WHERE item_name = %s",
    (3, "Keyboard")
)
connection.commit()

# DELETE
cursor.execute(
    "DELETE FROM sales WHERE item_name = %s",
    ("Keyboard",)
)
connection.commit()
```

---

## 6) `executemany()` — массовые операции
`executemany()` выполняет **один и тот же SQL** много раз с разными данными. Это быстрее и удобнее при массовых вставках/обновлениях/удалениях.

Особенности:
- работает с изменяющими запросами (`INSERT/UPDATE/DELETE`);
- вторым аргументом — **список кортежей**;
- запрос компилируется один раз → экономия ресурсов.

Пример:
```py
cursor.executemany(
    "INSERT INTO sales (item_name, quantity, price, sale_date) VALUES (%s, %s, %s, %s)",
    [
        ("Notebook", 3, 19.99, "2024-06-15"),
        ("Pen", 10, 1.99, "2024-06-16"),
        ("Bag", 1, 49.90, "2024-06-17"),
    ]
)
connection.commit()
```

---

## 7) Транзакции: атомарность “всё или ничего”
**Транзакция** — последовательность запросов, которая должна выполниться как единое целое.

Если хоть один шаг упал с ошибкой — **все изменения отменяются**.

Преимущества:
- защита от частичных обновлений при сбоях;
- атомарность: всё или ничего;
- особенно полезно при связанных изменениях (например, “списать деньги” + “уменьшить склад” + “создать запись покупки”).

---

## 8) `rollback()` — откат изменений
Если в процессе операций возникла ошибка — делаем откат:

```py
connection.rollback()
```

Правило:
- если транзакция не подтверждена `commit()`, `rollback()` отменяет все действия с момента начала транзакции (то есть с момента последнего `commit()` или открытия соединения).

### Большой пример: покупка товара (проверка баланса и наличия)
Сценарий:
- таблицы `customers`, `products`, `purchases`
- покупка удаётся только если есть деньги и есть товар
- если ошибка → откат, база остаётся консистентной

Создание таблиц:
```py
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    balance DECIMAL(10, 2) NOT NULL CHECK (balance >= 0)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10, 2),
    stock INT NOT NULL CHECK (stock >= 0)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS purchases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    purchase_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
)
""")
```

Заполнение данными (пример):
```py
cursor.execute("DELETE FROM purchases")
cursor.execute("DELETE FROM customers")
cursor.execute("DELETE FROM products")

cursor.executemany(
    "INSERT INTO customers (name, balance) VALUES (%s, %s)",
    [("Alice", 20.00), ("Bob", 200.00)]
)

cursor.executemany(
    "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
    [("Headphones", 99.99, 3), ("Mouse", 25.00, 5)]
)

connection.commit()
```

Попытка покупки (шаблон транзакции: `try -> commit`, `except -> rollback`):
```py
try:
    # товар
    cursor.execute("SELECT id, price, stock FROM products WHERE name = %s", ("Headphones",))
    product_id, price, stock = cursor.fetchone()

    if stock < 1:
        raise ValueError("Out of stock")

    cursor.execute("UPDATE products SET stock = stock - 1 WHERE id = %s", (product_id,))

    # клиент
    cursor.execute("SELECT id, balance FROM customers WHERE name = %s", ("Alice",))
    customer_id, balance = cursor.fetchone()

    if balance < price:
        raise ValueError("Insufficient funds")

    cursor.execute(
        "UPDATE customers SET balance = balance - %s WHERE id = %s",
        (price, customer_id)
    )

    # запись покупки
    cursor.execute(
        "INSERT INTO purchases (customer_id, product_id, purchase_date) VALUES (%s, %s, CURDATE())",
        (customer_id, product_id)
    )

    connection.commit()
    print("Purchase successful.")
except Exception as e:
    connection.rollback()
    print("Transaction failed:", e)
```

---

# Задания для закрепления — ответы

## Закрепление 1
1) Почему полезно не указывать базу при подключении? → **b, d**  
- b: чтобы создавать/удалять базы  
- d: чтобы выбрать базу позже вручную

2) Что будет, если обратиться к таблице без выбора базы? → **c**  
- c: ошибка `No database selected`

## Закрепление 2
1) После чего нужен `commit()`? → **b, c, d** (`INSERT`, `UPDATE`, `DELETE`)  
2) Что делает `executemany()`? → **c** (один SQL с разными данными)  
3) Что будет, если после `INSERT` не вызвать `commit()`? → **c** (изменения потеряются после закрытия соединения)

---

# Практическая работа (как в уроке) — готовое решение

## 1) Добавление товаров в таблицу `market.products`
Дано:
```py
products = [("Notebook", 10.00), ("Pencil", 1.00), ("Bag", 25.00)]
```

Решение:
```py
import pymysql
from pymysql.cursors import DictCursor

config = {
    "host": "ich-edit.edu.itcareerhub.de",
    "user": "ich1",
    "password": "ich1_password_ilovedbs",
}

with pymysql.connect(**config, cursorclass=DictCursor) as connection:
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS market")
        cursor.execute("USE market")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            price DECIMAL(10, 2)
        )
        """)

        products = [("Notebook", 10.00), ("Pencil", 1.00), ("Bag", 25.00)]

        cursor.executemany(
            "INSERT INTO products (name, price) VALUES (%s, %s)",
            products
        )
        connection.commit()

        print("Products added:")
        cursor.execute("SELECT id, name, price FROM products")
        for row in cursor.fetchall():
            print(f"{row['id']}. {row['name']} — ${row['price']:.2f}")
```

## 2) Массовое повышение цен на 20% одним UPDATE
```py
with pymysql.connect(**config, cursorclass=DictCursor) as connection:
    with connection.cursor() as cursor:
        cursor.execute("USE market")
        cursor.execute("UPDATE products SET price = price * 1.2")
        connection.commit()

        print("Prices updated.\n\nProducts after update:")
        cursor.execute("SELECT id, name, price FROM products")
        for row in cursor.fetchall():
            print(f"{row['id']}. {row['name']} — ${row['price']:.2f}")
```

---

# Домашнее задание (как в уроке)

## ДЗ 1) Создание базы `notes_app_<your_group>_<your_full_name>`
Написать программу, которая:
- создаёт БД `notes_app_<your_group>_<your_full_name>`
- выбирает её через `USE ...`
- выводит сообщение о результате

## ДЗ 2) Добавление заметок
Продолжить программу:
- создать таблицу `notes` с полями: `id`, `title`, `content`
- вставить одну заметку
- выполнить `commit()`
- вывести все заметки используя `DictCursor`

Подсказка к структуре таблицы:
```sql
CREATE TABLE IF NOT EXISTS notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT
);
```

---

## Мини-шпаргалка урока
```text
Подключение без database -> можно SHOW DATABASES, потом USE db

USE:
- выбирает базу на время соединения
- без USE: No database selected

DictCursor:
- cursorclass=DictCursor
- row["column_name"]

commit():
- обязателен после INSERT/UPDATE/DELETE
- без commit изменения потеряются при закрытии соединения

executemany():
- один SQL + список кортежей данных
- быстрее массовых циклов execute()

Транзакции:
try:
    ... несколько запросов ...
    commit()
except:
    rollback()
```


---

## 📚 Дополнительная информация

_Этот раздел будет дополнен практическими примерами и дополнительной информацией._
