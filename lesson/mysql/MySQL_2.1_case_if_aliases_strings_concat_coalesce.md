# MySQL — Урок 2.1. Условные конструкции в SQL: CASE и IF + алиасы, строковые функции, CONCAT, COALESCE

## План урока
- `CASE` (условная логика в SQL)
- Алиасы (`AS`)
- `IF()` (только MySQL)
- Новые столбцы на основе имеющихся (математика)
- Строковые функции: `LEFT`, `RIGHT`, `SUBSTRING`
- Конкатенация: `CONCAT`
- Замена NULL: `COALESCE` fileciteturn13file0turn13file1

---

## 1) CASE — условная логика в SQL

### 1.1. Что делает CASE
`CASE` работает как `if / else if / else`: возвращает разные значения в зависимости от условий.  
**Важно:** `CASE` создаёт **новый столбец в выборке**, **не меняя** данные в таблице. fileciteturn13file0turn13file1

### 1.2. Синтаксис
```sql
CASE
  WHEN condition1 THEN result1
  WHEN condition2 THEN result2
  ...
  ELSE resultN
END
```
- `ELSE` **необязателен**: если его нет и ни одно условие не подошло → будет `NULL`. fileciteturn13file1

### 1.3. Пример 1 — категория цены товара (products.standard_cost)
**Полный вариант (с явными интервалами):**
```sql
SELECT
  product_name,
  standard_cost,
  CASE
    WHEN standard_cost > 50 THEN 'Дорогой'
    WHEN standard_cost > 20 AND standard_cost <= 50 THEN 'Средний'
    ELSE 'Дешевый'
  END AS price_category
FROM products;
```
fileciteturn13file0turn13file1

**Оптимизация:** SQL читает `WHEN` сверху вниз, поэтому интервалы можно упростить:
```sql
SELECT
  product_name,
  standard_cost,
  CASE
    WHEN standard_cost > 50 THEN 'Дорогой'
    WHEN standard_cost > 20 THEN 'Средний'
    ELSE 'Дешевый'
  END AS price_category
FROM products;
```
fileciteturn13file0turn13file1

### 1.4. Пример 2 — скидка по региону (customers.state_province)
```sql
SELECT
  *,
  CASE
    WHEN state_province IN ('WA', 'CA') THEN 5
    WHEN state_province IN ('ID', 'OR') THEN 7
    WHEN state_province IN ('UT', 'NV') THEN 13
    ELSE 0
  END AS discount
FROM customers;
```
fileciteturn13file0turn13file1

### 1.5. Пример 3 — статус заказа (orders) с проверкой NULL
```sql
SELECT
  id,
  order_date,
  shipped_date,
  CASE
    WHEN shipped_date IS NULL THEN 'Ожидание отправки'
    WHEN shipped_date = order_date THEN 'Отправлено в день заказа'
    ELSE 'Отправлено'
  END AS order_status
FROM orders;
```
fileciteturn13file0turn13file1

---

## 2) Алиасы (AS) — понятные имена столбцов

### 2.1. Зачем нужны
Если вы создаёте вычисляемый столбец или используете функцию, без алиаса имя будет “кривым” (формула/функция).  
Алиас делает результат читаемым. fileciteturn13file0turn13file1

### 2.2. Синтаксис
```sql
SELECT
  expression1 AS name1,
  expression2 AS name2
FROM table;
```
`AS` можно **не писать**, но лучше оставлять для читабельности. fileciteturn13file1

---

## 3) IF() — условие в MySQL

### 3.1. Что это
`IF(condition, true_result, false_result)` — короткий способ условной логики, **поддерживается только MySQL**.  
Для переносимых запросов чаще используют `CASE` (это стандарт SQL и поддерживается в большинстве СУБД). fileciteturn13file0turn13file1

### 3.2. Пример
```sql
SELECT
  product_name,
  IF(standard_cost > 20, 'Expensive', 'Affordable') AS PriceCategory
FROM products;
```
fileciteturn13file0turn13file1

---

## 4) Новые столбцы из существующих: математика

Можно создавать вычисляемые поля математикой (только для числовых столбцов).  
Пример: общая стоимость позиции заказа:
```sql
SELECT
  product_id,
  unit_price,
  quantity,
  (unit_price * quantity) AS total_price
FROM order_details;
```
fileciteturn13file0turn13file1

---

## 5) Строковые функции (работа со строками)

### 5.1. LEFT / RIGHT
- `LEFT(str, n)` — взять `n` символов **с начала**
- `RIGHT(str, n)` — взять `n` символов **с конца** fileciteturn13file0turn13file1

Пример:
```sql
SELECT
  company,
  RIGHT(company, 2) AS ShortName
FROM customers;
```
fileciteturn13file0turn13file1

### 5.2. SUBSTRING (SUBSTR)
`SUBSTRING(str, start, len)` — извлечь подстроку с позиции `start` длиной `len`. fileciteturn13file0turn13file1

Пример (вытянуть 3 цифры из business_phone):
```sql
SELECT
  *,
  SUBSTRING(business_phone, 6, 3) AS phone_part
FROM customers;
```
fileciteturn13file0turn13file1

---

## 6) CONCAT — склеивание строк

`CONCAT(a, b, c...)` объединяет строки в одно значение. fileciteturn13file0turn13file1

Пример: полное имя сотрудника:
```sql
SELECT
  CONCAT(first_name, ' ', last_name) AS full_name
FROM employees;
```
fileciteturn13file0turn13file1

---

## 7) COALESCE — замена NULL

`COALESCE(x, y, z...)` возвращает **первое НЕ-NULL** значение из списка.  
Полезно, чтобы заменить пропуски в выводе. fileciteturn13file0turn13file1

Пример: заменить NULL в `notes` на `'Not filled'`:
```sql
SELECT
  notes,
  COALESCE(notes, 'Not filled') AS notes_filled
FROM employees;
```
fileciteturn13file0turn13file1

---

## 8) Быстрая таблица функций (часто пригодится)
- `CONCAT(a, b, ...)` — объединить строки  
- `SUBSTRING(str, start, len)` — часть строки  
- `LEFT(str, n)` / `RIGHT(str, n)` — n символов слева/справа  
- `LENGTH(str)` — длина строки (в байтах)  
- `TRIM(str)` / `LTRIM(str)` / `RTRIM(str)` — убрать пробелы
- `REPLACE(str, from, to)` — заменить подстроку
- `UPPER(str)` / `LOWER(str)` — регистр fileciteturn13file0turn13file1

---

## 9) Мини-шпаргалка урока
```sql
-- CASE
SELECT
  col,
  CASE
    WHEN col > 50 THEN 'A'
    WHEN col > 20 THEN 'B'
    ELSE 'C'
  END AS category
FROM t;

-- IF (только MySQL)
SELECT IF(col > 0, 'yes', 'no') AS flag FROM t;

-- Алиас
SELECT (unit_price * quantity) AS total_price FROM order_details;

-- Строковые
SELECT LEFT(name, 3), RIGHT(name, 2), SUBSTRING(phone, 6, 3) FROM t;

-- CONCAT + COALESCE
SELECT CONCAT(first_name,' ',last_name) AS full_name,
       COALESCE(notes,'Not filled') AS notes_filled
FROM employees;
```
