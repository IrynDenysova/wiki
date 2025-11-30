# MySQL — Урок 7.2. Табличные выражения CTE (Common Table Expression)

## 1) Что такое CTE
**CTE (Common Table Expression)** — конструкция SQL, которая позволяет создать *временный набор данных* (виртуальную таблицу) и использовать его в основном запросе.  
CTE объявляется через `WITH` и существует **только в рамках одного SQL-запроса**. fileciteturn23file0turn23file1

---

## 2) Зачем нужны CTE (польза)
CTE особенно полезны, когда: fileciteturn23file0turn23file1
- запрос сложный и его нужно разбить на логические части (**читабельность**);
- один и тот же набор данных нужно использовать несколько раз (**повторное использование логики**);
- хочется упростить длинные подзапросы и сделать запрос поддерживаемым.

---

## 3) Синтаксис CTE
Шаблон: fileciteturn23file0turn23file1
```sql
WITH cte_name AS (
  SELECT column1, column2, ...
  FROM table_name
  WHERE conditions
)
SELECT column1, column2, ...
FROM cte_name
WHERE conditions;
```

### Несколько CTE в одном запросе (идея)
```sql
WITH cte1 AS (...),
     cte2 AS (...)
SELECT ...
FROM cte1
JOIN cte2 ON ...;
```

---

## 4) Плюсы и минусы CTE
### Плюсы fileciteturn23file0turn23file1
- Читаемость
- Модульность (разбивка на блоки)
- Лёгкость использования (не нужно создавать/удалять временные таблицы)

### Минусы fileciteturn23file0turn23file1
- Ограниченная область действия: CTE доступно только в одном запросе и не “живёт” между запросами.

---

## 5) Когда использовать CTE, а когда подзапрос
### Используй CTE, когда: fileciteturn23file0turn23file1
- запрос сложный и его нужно структурировать;
- требуется повторное использование логики внутри одного запроса.

### Используй подзапросы, когда: fileciteturn23file0turn23file1
- запрос простой и вложенный `SELECT` логично смотрится внутри `WHERE`/`FROM`;
- важна производительность и ты знаешь, что движок лучше оптимизирует подзапрос.

---

## 6) Частая ошибка (важно)
Если используешь CTE в `IN`, нужно указывать столбец, а не имя CTE.

❌ Неправильно: fileciteturn23file1
```sql
WITH LA_clients AS (
  SELECT id
  FROM customers
  WHERE city = 'Los Angelas'
)
SELECT *
FROM orders
WHERE customer_id IN LA_clients;
```

✅ Правильно: fileciteturn23file1
```sql
WITH LA_clients AS (
  SELECT id
  FROM customers
  WHERE city = 'Los Angelas'
)
SELECT *
FROM orders
WHERE customer_id IN (SELECT id FROM LA_clients);
```

---

## 7) Задания/примеры из урока (готовые решения)

### 7.1. Топ-10 продуктов по количеству заказов + суммарная выручка fileciteturn23file0turn23file1
```sql
WITH product_summary AS (
  SELECT
    product_id,
    COUNT(*) AS total_orders,
    SUM(unit_price * quantity) AS total_revenue
  FROM order_details
  GROUP BY product_id
)
SELECT product_name, total_orders, total_revenue
FROM product_summary
JOIN products p ON product_summary.product_id = p.id
ORDER BY total_orders DESC
LIMIT 10;
```

### 7.2. Выбрать строки `order_details`, где `unit_price` больше среднего fileciteturn23file0turn23file1
```sql
WITH avg_price AS (
  SELECT AVG(unit_price) AS ap
  FROM order_details
)
SELECT *
FROM order_details
WHERE unit_price > (SELECT ap FROM avg_price);
```

### 7.3. unit_price: больше среднего и меньше среднего * 1.5 fileciteturn23file0turn23file1
```sql
WITH avg_price AS (
  SELECT AVG(unit_price) AS ap
  FROM order_details
)
SELECT *
FROM order_details
WHERE unit_price > (SELECT ap FROM avg_price)
  AND unit_price < (SELECT ap * 1.5 FROM avg_price);
```

### 7.4. Заказы, оформленные сотрудниками Sales Representative fileciteturn23file0turn23file1
```sql
WITH sales_repr AS (
  SELECT id
  FROM employees
  WHERE job_title = 'Sales Representative'
)
SELECT *
FROM orders
WHERE employee_id IN (SELECT id FROM sales_repr);
```

---

## 8) ДЗ (формулировки из материалов)
1) Вывести названия продуктов (`products`) и количество заказанных единиц `quantity` для каждого продукта (`order_details`). Решить **через CTE** и **через подзапрос**. fileciteturn23file0turn23file1  
2) Найти заказы (`orders`), сделанные **после** даты самого первого заказа клиента **Lee** (`customers`). fileciteturn23file0turn23file1  
3) Найти продукты (`products`) с **максимальным** `target_level`. fileciteturn23file0turn23file1  

---

## 9) Мини-шпаргалка
```sql
-- базовый CTE
WITH x AS (
  SELECT ...
)
SELECT ...
FROM x;

-- CTE как источник для IN
WITH ids AS (SELECT id FROM t WHERE ...)
SELECT * FROM t2
WHERE t2.id IN (SELECT id FROM ids);
```
