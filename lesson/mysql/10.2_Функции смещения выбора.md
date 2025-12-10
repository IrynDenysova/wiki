# MySQL — Урок 10.2. Оконные функции смещения и выбора
*(LEAD / LAG / FIRST_VALUE / LAST_VALUE / NTH_VALUE)*

## 0) Доступ к учебной БД (read-only)
- hostname: `ich-db.edu.itcareerhub.de`
- username: `ich1`
- password: `password`

---

## 1) Идея функций смещения и выбора
Эти оконные функции позволяют брать значения **из других строк** в пределах окна:  
- из **предыдущей** / **следующей** строки,
- **первое** / **последнее** значение в группе,
- **n-е** значение в группе.

Они полезны для:
- сравнения текущей строки с предыдущей/следующей (рост/падение, разница),
- анализа “первого/последнего” события в периоде,
- поиска ключевых точек (например, 3-я продажа в месяце),
- вычисления интервалов между событиями.

---

## 2) Общий синтаксис
```sql
SELECT
  column1,
  window_function(column2) OVER (
    PARTITION BY column3
    ORDER BY column4
  ) AS result_column
FROM table_name;
```

- `PARTITION BY ...` — делит строки на группы (окна)
- `ORDER BY ...` — задаёт порядок внутри окна (очень важно для LEAD/LAG)

---

## 3) LEAD() — значение из следующей строки
### 3.1. Синтаксис (MySQL)
```sql
LEAD(expr [, offset [, default]]) OVER (PARTITION BY ... ORDER BY ...)
```
- `offset` (по умолчанию 1) — на сколько строк “вперёд”
- `default` — что вернуть, если “следующей строки нет” (иначе будет NULL)

### 3.2. Пример
**Задача:** показать сумму следующей продажи по дате.
```sql
SELECT
  SaleID,
  SaleDate,
  SaleAmount,
  LEAD(SaleAmount, 1) OVER (ORDER BY SaleDate) AS NextSaleAmount
FROM Sales;
```

---

## 4) LAG() — значение из предыдущей строки
### 4.1. Синтаксис (MySQL)
```sql
LAG(expr [, offset [, default]]) OVER (PARTITION BY ... ORDER BY ...)
```

### 4.2. Пример
**Задача:** показать сумму предыдущей продажи по дате.
```sql
SELECT
  SaleID,
  SaleDate,
  SaleAmount,
  LAG(SaleAmount, 1) OVER (ORDER BY SaleDate) AS PrevSaleAmount
FROM Sales;
```

---

## 5) FIRST_VALUE() — первое значение в окне
Возвращает первое значение в окне (или в группе `PARTITION`) при заданном порядке.

### Пример: первая цена в каждом месяце
```sql
SELECT
  OrderID, OrderDate, UnitPrice,
  FIRST_VALUE(UnitPrice) OVER (
    PARTITION BY EXTRACT(YEAR FROM OrderDate), EXTRACT(MONTH FROM OrderDate)
    ORDER BY OrderDate
  ) AS FirstPriceOfMonth
FROM OrderDetails;
```

---

## 6) LAST_VALUE() — последнее значение в окне
Возвращает последнее значение в окне.

⚠️ В MySQL есть важная тонкость:
- Если в окне есть `ORDER BY`, то по умолчанию рамка окна заканчивается **на текущей строке**.
- Тогда `LAST_VALUE()` часто возвращает **текущее значение**, а не “последнее в группе”.

✅ Чтобы получить “последнее в группе”, обычно добавляют рамку:
```sql
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
```

### Пример: последняя цена в каждом месяце (правильный вариант для MySQL)
```sql
SELECT
  OrderID, OrderDate, UnitPrice,
  LAST_VALUE(UnitPrice) OVER (
    PARTITION BY EXTRACT(YEAR FROM OrderDate), EXTRACT(MONTH FROM OrderDate)
    ORDER BY OrderDate
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS LastPriceOfMonth
FROM OrderDetails;
```

---

## 7) NTH_VALUE() — n-е значение в окне
Возвращает n-е значение (например, 3-е) в рамках окна.

⚠️ Как и `LAST_VALUE`, в MySQL часто нужна рамка окна, чтобы функция “видела” все строки группы.

### Пример: третья цена продажи в каждом месяце (правильный вариант для MySQL)
```sql
SELECT
  OrderID, OrderDate, UnitPrice,
  NTH_VALUE(UnitPrice, 3) OVER (
    PARTITION BY EXTRACT(YEAR FROM OrderDate), EXTRACT(MONTH FROM OrderDate)
    ORDER BY OrderDate
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS ThirdPriceOfMonth
FROM OrderDetails;
```

---

## 8) Практика (таблица purchase_orders) — решения

### 8.1. Для каждого supplier_id: дата создания, дата предыдущего заказа, разница в днях
```sql
SELECT
  supplier_id,
  creation_date,
  LAG(creation_date) OVER (PARTITION BY supplier_id ORDER BY creation_date) AS previous_created_date,
  DATEDIFF(
    creation_date,
    LAG(creation_date) OVER (PARTITION BY supplier_id ORDER BY creation_date)
  ) AS date_diff_days
FROM purchase_orders;
```

### 8.2. Среднее время между заказами (по всем поставщикам)
```sql
SELECT AVG(date_diff_days) AS avg_days_between_orders
FROM (
  SELECT
    supplier_id,
    creation_date,
    DATEDIFF(
      creation_date,
      LAG(creation_date) OVER (PARTITION BY supplier_id ORDER BY creation_date)
    ) AS date_diff_days
  FROM purchase_orders
) a
WHERE date_diff_days IS NOT NULL;
```

### 8.3. То же самое, но через LEAD (сравнить результаты)
**Важно:** чтобы разница была положительной, удобнее считать “следующая - текущая”:
```sql
SELECT AVG(date_diff_days) AS avg_days_between_orders
FROM (
  SELECT
    supplier_id,
    creation_date,
    DATEDIFF(
      LEAD(creation_date) OVER (PARTITION BY supplier_id ORDER BY creation_date),
      creation_date
    ) AS date_diff_days
  FROM purchase_orders
) a
WHERE date_diff_days IS NOT NULL;
```

### 8.4. Самая ранняя submitted_date для каждого created_by: MIN и FIRST_VALUE
```sql
SELECT
  created_by,
  MIN(submitted_date) OVER (PARTITION BY created_by) AS min_submitted_date,
  FIRST_VALUE(submitted_date) OVER (
    PARTITION BY created_by
    ORDER BY submitted_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS first_value_submitted_date
FROM purchase_orders;
```

---

## 9) Домашнее задание — подсказки/решения (таблица purchase_order_details)

### 9.1. Для каждого product_id: inventory_id и предыдущий/следующий inventory_id по убыванию quantity
```sql
SELECT
  product_id,
  inventory_id,
  quantity,
  LAG(inventory_id)  OVER (PARTITION BY product_id ORDER BY quantity DESC) AS prev_inventory_id,
  LEAD(inventory_id) OVER (PARTITION BY product_id ORDER BY quantity DESC) AS next_inventory_id
FROM purchase_order_details;
```

### 9.2. Максимальный и минимальный unit_price для каждого order_id через FIRST_VALUE
✅ Для MAX и MIN можно менять сортировку, плюс ставить рамку окна:
```sql
SELECT
  order_id,
  unit_price,
  FIRST_VALUE(unit_price) OVER (
    PARTITION BY order_id
    ORDER BY unit_price ASC
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS min_unit_price,
  FIRST_VALUE(unit_price) OVER (
    PARTITION BY order_id
    ORDER BY unit_price DESC
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS max_unit_price
FROM order_details;
```

### 9.3. Разница между unit_price и минимальным unit_price в заказе (2 способа)
**Способ 1: через FIRST_VALUE**
```sql
SELECT
  order_id,
  unit_price,
  unit_price - FIRST_VALUE(unit_price) OVER (
    PARTITION BY order_id
    ORDER BY unit_price ASC
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS diff_from_min
FROM order_details;
```

**Способ 2: через MIN**
```sql
SELECT
  order_id,
  unit_price,
  unit_price - MIN(unit_price) OVER (PARTITION BY order_id) AS diff_from_min
FROM order_details;
```

### 9.4. Присвоить ранг по убыванию quantity (RANK)
```sql
SELECT
  *,
  RANK() OVER (ORDER BY quantity DESC) AS rnk
FROM purchase_order_details;
```

### 9.5. Оставить только строки с рангом до 10 включительно
В MySQL нельзя использовать алиас окна напрямую в WHERE, поэтому делаем подзапрос/CTE:
```sql
WITH ranked AS (
  SELECT
    *,
    RANK() OVER (ORDER BY quantity DESC) AS rnk
  FROM purchase_order_details
)
SELECT *
FROM ranked
WHERE rnk <= 10;
```

---

## 10) Мини-шпаргалка
```sql
-- предыдущая/следующая строка
LAG(x, 1, 0)  OVER (PARTITION BY g ORDER BY dt)
LEAD(x, 1, 0) OVER (PARTITION BY g ORDER BY dt)

-- первое значение в группе
FIRST_VALUE(x) OVER (PARTITION BY g ORDER BY dt)

-- последнее / n-е (в MySQL чаще нужна рамка)
LAST_VALUE(x) OVER (
  PARTITION BY g ORDER BY dt
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)

NTH_VALUE(x, n) OVER (
  PARTITION BY g ORDER BY dt
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```
