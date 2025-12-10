# MySQL — Урок 9.2. Агрегирующие оконные функции + кумулятивные значения

Источник: материалы урока 9.2 (презентация/конспект).  

## 0) Быстрый контекст
**Агрегирующие оконные функции** — это `SUM / AVG / MIN / MAX / COUNT`, применённые как оконные функции через `OVER(...)`.  
Они агрегируют данные **внутри окна (набора строк)**, но **не сворачивают** результат как `GROUP BY`: каждая исходная строка остаётся, а итог добавляется отдельным столбцом.

> Важно: если в `OVER(...)` **нет `ORDER BY`**, то агрегат (например, сумма) будет **одинаковым** для всех строк в одном и том же окне (`PARTITION`).  
> Если есть `ORDER BY` — можно считать **кумулятивные/накопительные** значения (running totals/averages).

---

## 1) Основные агрегирующие оконные функции
- `SUM(...) OVER (...)`
- `AVG(...) OVER (...)`
- `MIN(...) OVER (...)`
- `MAX(...) OVER (...)`
- `COUNT(...) OVER (...)`

---

## 2) Базовый синтаксис
### 2.1. По всему набору строк (одно окно на весь результат)
```sql
SELECT
  ...,
  MAX(list_price) OVER () AS max_price_all
FROM products;
```

### 2.2. По группам (окна через PARTITION BY)
```sql
SELECT
  ...,
  SUM(amount) OVER (PARTITION BY customer_id) AS total_by_customer
FROM orders;
```

### 2.3. Кумулятивные (окна с ORDER BY)
```sql
SELECT
  ...,
  SUM(amount) OVER (ORDER BY order_date) AS cumulative_amount
FROM orders;
```

---

## 3) Примеры из урока (на учебных табличках)

### 3.1. Общая сумма заказов для каждого клиента (без учета порядка)
Задача: для каждой строки заказа показать сумму всех заказов клиента.
```sql
SELECT
  OrderID, CustomerID, OrderAmount,
  SUM(OrderAmount) OVER (PARTITION BY CustomerID) AS TotalCustomerOrders
FROM Orders;
```
Идея: всем строкам одного `CustomerID` присваивается одинаковая итоговая сумма.

### 3.2. Количество заказов для каждого клиента
```sql
SELECT
  OrderID, CustomerID, OrderAmount,
  COUNT(*) OVER (PARTITION BY CustomerID) AS OrdersPerCustomer
FROM Orders;
```

---

## 4) Задания по таблице products (готовые решения/шаблоны)

### 4.1. Максимальный list_price по всей таблице — для каждой строки
```sql
SELECT
  product_name,
  list_price,
  MAX(list_price) OVER () AS max_list_price
FROM products;
```

### 4.2. Процентная разница между ценой продукта и максимальной ценой
```sql
SELECT
  product_name,
  (MAX(list_price) OVER () - list_price) / (MAX(list_price) OVER ()) * 100 AS diff_pct
FROM products;
```

### 4.3. Количество продуктов в каждой категории (оконный COUNT)
```sql
SELECT
  category,
  COUNT(id) OVER (PARTITION BY category) AS products_in_category
FROM products;
```
Комментарий: да, так можно. Но если нужна **одна строка на категорию**, то чаще оптимальнее/логичнее `GROUP BY category`.

### 4.4. Разница между standard_cost и средним list_price по всей таблице
```sql
SELECT
  product_name,
  standard_cost - AVG(list_price) OVER () AS diff_from_avg_list
FROM products;
```

### 4.5. То же без оконных функций (через CTE + JOIN “на всё”)
```sql
WITH avg_price AS (
  SELECT AVG(list_price) AS ap
  FROM products
)
SELECT
  p.product_name,
  p.standard_cost - avg_price.ap AS diff_from_avg_list
FROM products p
JOIN avg_price ON 1=1;
```

---

## 5) Кумулятивные (накопительные) значения

### 5.1. Что такое кумулятивная сумма
**Кумулятивная сумма** — сумма “от начала” до текущей строки.

Главное правило из урока:
- Чтобы считать кумулятивные значения, в `OVER(...)` нужно добавить `ORDER BY`.
- Оптимально упорядочивать по **дате** (или другому признаку времени), иначе “накопление” теряет смысл.

### 5.2. Кумулятивная сумма продаж по датам (running total)
```sql
SELECT
  SaleID, SaleDate, SaleAmount,
  SUM(SaleAmount) OVER (ORDER BY SaleDate) AS CumulativeSales
FROM Sales;
```

### 5.3. Текущее среднее по заказам для каждого клиента (running average)
```sql
SELECT
  OrderID, CustomerID, OrderDate, OrderAmount,
  AVG(OrderAmount) OVER (PARTITION BY CustomerID ORDER BY OrderDate) AS RunningAvg
FROM Orders;
```
Идея: для каждого клиента “накопительное” среднее будет меняться по мере появления новых заказов (в порядке дат).

---

## 6) Типовые ошибки/заметки
- `OVER (PARTITION BY ...)` без `ORDER BY` даёт **одно и то же значение** для всех строк в partition (это нормально).
- `ORDER BY` без `PARTITION BY` считает накопление по **всем данным** (по всей выборке).
- Для корректной аналитики с накоплениями сортировка должна быть **однозначной**: если даты могут повторяться, часто добавляют вторичную сортировку (например, по `id`).

---

## 7) Домашнее задание (как в материалах)
1) Для каждого `order_id` вывести `MIN`, `MAX`, `AVG` по `unit_cost`.  
2) Оставить только уникальные строки из п.1.  
3) Посчитать стоимость продукта в заказе: `quantity * unit_cost`.  
   - вывести суммарную стоимость продуктов **оконной функцией**  
   - и сделать то же самое через **GROUP BY**  
4) Посчитать количество заказов по `date_received` и `posted_to_inventory`.  
   - если оно > 1 → вывести `'>1'`, иначе `'<1'`  
5) Вывести `purchase_order_id`, `date_received` и вычисленный столбец из п.4.

---

## 8) Мини-шпаргалка
```sql
-- итог по клиенту (без накопления)
SUM(x) OVER (PARTITION BY customer_id)

-- максимум по всей таблице
MAX(x) OVER ()

-- кумулятивная сумма
SUM(x) OVER (ORDER BY dt)

-- running average в группе
AVG(x) OVER (PARTITION BY customer_id ORDER BY dt)
```
