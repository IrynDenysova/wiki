# MySQL — Урок 1.2. Условный оператор WHERE (LIKE / IN / BETWEEN / NULL)

## План урока
- WHERE: фильтрация строк  
- LIKE: поиск по маске  
- IN / BETWEEN: множественный выбор  
- NULL: отсутствие данных, как правильно фильтровать  

---

## 1) WHERE — фильтрация строк

### 1.1. Шаблон
```sql
SELECT column1, column2
FROM table
WHERE column3 <условие>;
```

### 1.2. Операторы сравнения
| Оператор | Смысл |
|---|---|
| `=` | равно |
| `<>` или `!=` | не равно |
| `<` | меньше |
| `<=` | меньше или равно |
| `>` | больше |
| `>=` | больше или равно |

### 1.3. Логические операторы
- `NOT` — инверсия условия  
- `AND` — **оба** условия истинны  
- `OR` — истинно, если **хотя бы одно** истинно  

### 1.4. Приоритет (важно!)
- Сначала **арифметика**, затем **сравнения**, потом **логика**.
- У операторов сравнения один приоритет: выполняются **слева направо**.
- Скобки `()` позволяют задать свой порядок (как в математике).

Пример (как решать такие условия правильно):
```sql
SELECT *
FROM order_details
WHERE (order_id = 30 AND unit_price > 9)
   OR (status_id = 1 AND unit_price > 9);

-- эквивалентный вариант:
SELECT *
FROM order_details
WHERE unit_price > 9
  AND (order_id = 30 OR status_id = 1);
```

---

## 2) LIKE — поиск по маске (wildcards)

### 2.1. Идея
`LIKE` сравнивает строку с шаблоном и возвращает те строки, которые подходят под маску.

### 2.2. Символы подстановки
- `%` — любое количество символов (включая 0)
- `_` — ровно один любой символ

Примеры:
```sql
-- имя начинается на A
WHERE first_name LIKE 'A%'

-- город заканчивается на mond
WHERE city LIKE '%mond'

-- в notes есть слово French
WHERE notes LIKE '%French%'
```

---

## 3) IN и BETWEEN — множественный выбор

### 3.1. IN
`IN(...)` — проверка “входит ли значение в список”.
```sql
SELECT ship_name
FROM orders
WHERE ship_city IN ('Chicago', 'Miami');
```
Это эквивалентно:
```sql
WHERE ship_city = 'Chicago' OR ship_city = 'Miami'
```

### 3.2. BETWEEN ... AND
`BETWEEN a AND b` — диапазон **включая границы** (a и b входят).
```sql
SELECT *
FROM orders
WHERE shipping_fee BETWEEN 10 AND 15;
```
Эквивалент:
```sql
WHERE shipping_fee >= 10 AND shipping_fee <= 15
```

---

## 4) NULL — отсутствие данных

### 4.1. Главное правило
`NULL` — это “неизвестно/нет значения”.  
Он **не равен ничему**, даже другому `NULL`. Поэтому нельзя писать:
```sql
WHERE shipped_date = NULL      -- ❌ неправильно
WHERE shipped_date <> NULL     -- ❌ неправильно
```

### 4.2. Правильная проверка
```sql
WHERE shipped_date IS NULL
WHERE shipped_date IS NOT NULL
```

Пример:
```sql
SELECT *
FROM orders
WHERE shipped_date IS NULL;

SELECT id
FROM orders
WHERE shipped_date IS NULL
  AND shipper_id IS NULL;
```

---

## 5) Практика (запросы из урока)

### 5.1. WHERE (таблица `order_details`)
```sql
USE northwind;

-- 1) unit_price > 20
SELECT *
FROM order_details
WHERE unit_price > 20;

-- 2) product_id = 43 и status_id = 2
SELECT *
FROM order_details
WHERE product_id = 43
  AND status_id = 2;

-- 3) quantity <= 15 или unit_price = 15
SELECT *
FROM order_details
WHERE quantity <= 15
   OR unit_price = 15;

-- 4) inventory_id для заказов, кроме order_id 46 и 79
SELECT inventory_id
FROM order_details
WHERE order_id != 46
  AND order_id != 79;

-- 5) условия со скобками
SELECT *
FROM order_details
WHERE (order_id = 30 AND unit_price > 9)
   OR (unit_price > 9 AND status_id = 1);
```

### 5.2. LIKE (таблица `employees`)
```sql
-- 1) first_name начинается на A
SELECT *
FROM employees
WHERE first_name LIKE 'A%';

-- 2) city заканчивается на mond
SELECT *
FROM employees
WHERE city LIKE '%mond';

-- 3) notes содержит French и/или last_name содержит букву k (вариант из материалов)
SELECT *
FROM employees
WHERE notes LIKE '%French%'
   OR last_name LIKE '%k%';
```

### 5.3. IN / BETWEEN (таблица `orders`)
```sql
-- BETWEEN
SELECT *
FROM orders
WHERE shipping_fee BETWEEN 10 AND 15;

-- IN
SELECT ship_name
FROM orders
WHERE ship_city IN ('Chicago', 'Miami');
```

### 5.4. NULL (таблица `orders`)
```sql
SELECT *
FROM orders
WHERE shipped_date IS NULL;

SELECT id
FROM orders
WHERE shipped_date IS NULL
  AND shipper_id IS NULL;
```

---

## 6) Мини-шпаргалка (самое важное)
```sql
-- WHERE
SELECT * FROM t WHERE a = 1 AND b >= 10;
SELECT * FROM t WHERE (a=1 AND b=2) OR (c=3);

-- LIKE
WHERE name LIKE 'A%';
WHERE city LIKE '%mond';
WHERE code LIKE '__-___'; -- _ = 1 символ

-- IN / BETWEEN
WHERE city IN ('Chicago','Miami');
WHERE fee BETWEEN 10 AND 15;

-- NULL
WHERE col IS NULL;
WHERE col IS NOT NULL;
```
