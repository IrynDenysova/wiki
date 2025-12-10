# MySQL — Урок 5.1. Агрегирующие функции и `GROUP BY`

## 1) Что такое агрегация
**Агрегация** — это объединение данных, чтобы получить *обобщённое* представление о наборе строк (итоги, средние, минимумы/максимумы и т.д.). 

---

## 2) Агрегирующие функции (Aggregate functions)
Агрегирующие функции выполняют вычисления над **набором строк** и возвращают **одно итоговое значение**. 

### 2.1. Основные агрегаты
- `COUNT()` — количество строк/значений  
  - `COUNT(*)` считает **все строки**  
  - `COUNT(col)` считает строки, где `col IS NOT NULL` (NULL не учитывается) 
- `SUM(col)` — сумма (только числовые типы) 
- `AVG(col)` — среднее (NULL игнорируются) 
- `MIN(col)` — минимум (числа, строки, даты) 
- `MAX(col)` — максимум (числа, строки, даты) 

### 2.2. DISTINCT внутри агрегатов
Можно учитывать **только уникальные значения**:
```sql
SELECT COUNT(DISTINCT customer_id) AS unique_customers
FROM orders;
```


### 2.3. `GROUP_CONCAT()` (специфично для MySQL)
`GROUP_CONCAT()` объединяет значения из нескольких строк в одну строку с разделителем. 

Пример (в материалах — перечислить имена):
```sql
SELECT GROUP_CONCAT(first_name) AS names
FROM employees;
```


> Важно: агрегатные функции игнорируют `NULL` значения (кроме `COUNT(*)`, а `COUNT(col)` просто не считает NULL). 

---

## 3) Оператор `GROUP BY`
`GROUP BY` группирует строки с одинаковыми значениями в одном или нескольких столбцах.  
Затем агрегатные функции применяются **к каждой группе отдельно**. 

### 3.1. Шаблон
```sql
SELECT column_name,
       AGGREGATE_FUNCTION(column_name)
FROM table_name
GROUP BY column_name;
```


### 3.2. Главное правило `GROUP BY`
Все столбцы в `SELECT`, которые **не** внутри агрегатных функций, должны быть перечислены в `GROUP BY`. 

---

## 4) Практика (короткие решения из урока)

### 4.1. Общее количество товаров (сумма quantity) в `order_details`
```sql
SELECT SUM(quantity) AS total_quantity
FROM order_details;
```


### 4.2. Количество уникальных `order_id` в `order_details`
```sql
SELECT COUNT(DISTINCT order_id) AS unique_orders
FROM order_details;
```


### 4.3. Среднее / минимум / максимум `unit_price` в `order_details`
```sql
SELECT AVG(unit_price) AS avg_price,
       MIN(unit_price) AS min_price,
       MAX(unit_price) AS max_price
FROM order_details;
```


---

## 5) Практика `GROUP BY` (основные кейсы)

### 5.1. Сколько сотрудников в каждом городе (таблица `employees`)
```sql
SELECT city,
       COUNT(id) AS number_employees
FROM employees
GROUP BY 1
ORDER BY 2 DESC;
```


> `GROUP BY 1` означает “группируй по 1-му столбцу в SELECT”.  
> `ORDER BY 2` — “сортируй по 2-му столбцу в SELECT”.  
> Это сокращает запись, но в реальных проектах чаще пишут явные имена для читаемости.

### 5.2. Сколько товаров (сумма quantity) в каждом заказе (`order_details`)
```sql
SELECT order_id,
       SUM(quantity) AS total_quantity
FROM order_details
GROUP BY 1
ORDER BY 2 DESC;
```


### 5.3. Количество сотрудников по компании и должности (`employees`)
```sql
SELECT company,
       job_title,
       COUNT(id) AS cnt
FROM employees
GROUP BY company, job_title;
```


### 5.4. Важно про “группировку по уникальному ключу”
Если группировать по первичному ключу (PK), где значения уникальны, то смысла в `GROUP BY` почти нет: каждая группа будет из одной строки, и агрегаты дадут “то же самое”. 

---

## 6) Мини-шпаргалка урока
```sql
-- агрегаты
SELECT COUNT(*) FROM t;
SELECT COUNT(col) FROM t;                 -- без NULL
SELECT COUNT(DISTINCT col) FROM t;        -- только уникальные
SELECT SUM(x), AVG(x), MIN(x), MAX(x) FROM t;

-- group by
SELECT group_col, COUNT(*)
FROM t
GROUP BY group_col
ORDER BY 2 DESC;

-- group_concat (MySQL)
SELECT GROUP_CONCAT(name) FROM t;
```
