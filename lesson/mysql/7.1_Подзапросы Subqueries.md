# MySQL — Урок 7.1. Подзапросы (Subqueries)

## 1) Что такое подзапрос
**Подзапрос (вложенный запрос)** — это `SELECT`, который выполняется **внутри** другого SQL-запроса.  
Подзапрос всегда заключают в круглые скобки `(...)`.

Пример общей формы:
```sql
SELECT *
FROM t1
WHERE column1 = (SELECT column1 FROM t2);
```
- `SELECT ... FROM t1 ...` — внешний запрос
- `(SELECT ... FROM t2)` — подзапрос

---

## 2) Зачем используют подзапросы (плюсы и минусы)

### Плюсы
- Разбивает сложную задачу на более простые шаги.
- “Инкапсулирует” логику: отдельный кусок можно понять и проверить отдельно.
- Иногда проще читать, чем большой JOIN/UNION с множеством условий.

### Минусы
- **Производительность:** некоторые подзапросы могут работать медленнее, чем эквивалент через JOIN/агрегации.
- **Читаемость:** если подзапросов много и они вложены друг в друга — запрос становится тяжёлым.

---

## 3) Виды подзапросов (классификация)

### 3.1. По месту использования
1) **Подзапрос в WHERE** — используется для фильтрации строк внешнего запроса.  
2) **Подзапрос в FROM** — создаёт “временную таблицу” (derived table), которую дальше можно JOIN-ить, сортировать, ограничивать.

### 3.2. По возвращаемому значению
1) **Однострочный (scalar)** — возвращает **одно значение** (одна строка, один столбец).  
2) **Многострочный (multi-row)** — возвращает **несколько значений** (обычно один столбец, много строк) → чаще всего применяется с `IN`.

---

## 4) Подзапрос в WHERE (фильтрация)

### Задача: найти все заказы клиентов из Лос-Анджелеса
Шаг 1: найдём клиентов из нужного города:
```sql
USE northwind;

SELECT id
FROM customers
WHERE city = 'Los Angelas';
```

Шаг 2: отфильтруем заказы по найденным `customer_id`:
```sql
SELECT *
FROM orders
WHERE customer_id IN (
  SELECT id
  FROM customers
  WHERE city = 'Los Angelas'
);
```

---

## 5) Подзапрос в FROM (как “временная таблица”)

### Задача: топ-10 продуктов по количеству заказов + выручка
Идея:  
1) внутри подзапроса посчитать по `order_details`:
   - `total_orders` = сколько раз продукт встречался
   - `total_revenue` = сумма `unit_price * quantity`
2) затем JOIN с `products`, чтобы получить `product_name`

```sql
SELECT product_name, total_orders, total_revenue
FROM (
  SELECT
    product_id,
    COUNT(*) AS total_orders,
    SUM(unit_price * quantity) AS total_revenue
  FROM order_details
  GROUP BY product_id
) AS product_summary
JOIN products p ON product_summary.product_id = p.id
ORDER BY total_orders DESC
LIMIT 10;
```

**Важно:** подзапрос в `FROM` почти всегда требует **алиас**:
```sql
FROM (SELECT ...) AS alias_name
```

---

## 6) Однострочный подзапрос (Scalar Subquery)

### Задача: выбрать позиции заказа, где цена выше среднего
Сначала “среднее” (это одна цифра):
```sql
SELECT AVG(unit_price)
FROM order_details;
```

Потом сравниваем `unit_price` с подзапросом:
```sql
SELECT *
FROM order_details
WHERE unit_price > (
  SELECT AVG(unit_price)
  FROM order_details
);
```

Правило:
- если подзапрос возвращает **одно значение**, обычно используют `=`, `>`, `<`, `>=`, `<=`, `<>`.

---

## 7) Многострочный подзапрос (Multi-row)

### Задача: найти все заказы, оформленные сотрудниками с должностью Sales Representative
Подзапрос возвращает **список id сотрудников**, значит нужен `IN`:

```sql
SELECT *
FROM orders
WHERE employee_id IN (
  SELECT id
  FROM employees
  WHERE job_title = 'Sales Representative'
);
```

Правило:
- если подзапрос возвращает **много значений**, обычно используют `IN` (или другие операторы для множеств, но базовый — `IN`).

---

## 8) Быстрые правила (чтобы не ловить ошибки)
1) Подзапрос всегда в `(...)`.
2) Если ожидаешь **одно значение** — убедись, что подзапрос реально вернёт одно (иначе будет ошибка).
3) Если подзапрос может вернуть **много строк** — используй `IN`.
4) Подзапрос в `FROM` обязательно именуем алиасом: `AS alias`.
5) Если запрос начинает “тормозить” — проверь альтернативу через `JOIN`.

---

## 9) Мини-шпаргалка шаблонов

### WHERE + scalar
```sql
SELECT *
FROM t
WHERE col > (SELECT AVG(col) FROM t);
```

### WHERE + multi-row (IN)
```sql
SELECT *
FROM orders
WHERE customer_id IN (SELECT id FROM customers WHERE city='X');
```

### FROM (derived table) + JOIN
```sql
SELECT p.product_name, s.total_orders
FROM (
  SELECT product_id, COUNT(*) AS total_orders
  FROM order_details
  GROUP BY product_id
) AS s
JOIN products p ON p.id = s.product_id
ORDER BY s.total_orders DESC;
```
