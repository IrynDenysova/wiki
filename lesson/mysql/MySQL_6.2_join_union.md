# MySQL — Урок 6.2. Операторы JOIN и UNION

## План занятия
- `UNION` и `UNION ALL`
- `JOIN`: `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `CROSS JOIN`
- Общий синтаксис JOIN, примеры на northwind fileciteturn21file0turn21file1

---

## 1) UNION и UNION ALL (вертикальное объединение строк)
`UNION` / `UNION ALL` объединяют результаты **двух и более SELECT** в **один набор строк**. fileciteturn21file0turn21file1

### 1.1. UNION
- объединяет строки
- **удаляет полные дубликаты строк**
- требует больше ресурсов/памяти (по сравнению с UNION ALL) fileciteturn21file0turn21file1

```sql
SELECT * FROM table1
UNION
SELECT * FROM table2;
```
fileciteturn21file0turn21file1

### 1.2. UNION ALL
- объединяет строки
- **сохраняет все строки**, включая дубликаты (быстрее) fileciteturn21file0turn21file1

```sql
SELECT * FROM table1
UNION ALL
SELECT * FROM table2;
```

### 1.3. Главные правила UNION
1) В каждом SELECT должно быть **одинаковое количество столбцов**. fileciteturn21file0turn21file1  
2) Соответствующие столбцы должны иметь **совместимые типы данных**. fileciteturn21file0turn21file1  
3) Имена столбцов в результате берутся из **первого SELECT**.

---

## 2) Практика UNION (из урока)

### 2.1. Объединить сотрудников и клиентов (имя + фамилия)
```sql
USE northwind;

SELECT first_name, last_name
FROM employees
UNION ALL
SELECT first_name, last_name
FROM customers;
```
fileciteturn21file0turn21file1

### 2.2. Добавить столбец “кто это” (employee / customer)
```sql
USE northwind;

SELECT first_name, last_name, 'employee' AS status
FROM employees
UNION ALL
SELECT first_name, last_name, 'customer' AS status
FROM customers;
```
fileciteturn21file0turn21file1

---

## 3) JOIN (горизонтальное объединение столбцов)
`JOIN` используют, когда нужно объединить строки из двух (или более) таблиц по логической связи, обычно по общему полю (ключу). fileciteturn21file0turn21file1

---

## 4) Виды JOIN (что возвращают)

### 4.1. INNER JOIN (внутреннее соединение)
Возвращает только строки, у которых есть совпадения **в обеих таблицах**. fileciteturn21file0turn21file1

### 4.2. LEFT JOIN (левое внешнее)
Возвращает **все** строки из левой таблицы + совпавшие из правой.  
Если совпадений нет — поля правой таблицы будут `NULL`. fileciteturn21file0turn21file1

### 4.3. RIGHT JOIN (правое внешнее)
Возвращает **все** строки из правой таблицы + совпавшие из левой.  
Если совпадений нет — поля левой таблицы будут `NULL`. fileciteturn21file0turn21file1

> На практике часто RIGHT JOIN не используют, потому что его легко заменить LEFT JOIN, просто поменяв таблицы местами. fileciteturn21file1

### 4.4. CROSS JOIN (декартово произведение)
Каждая строка из первой таблицы соединяется с каждой строкой из второй.  
Редко используется: очень быстро “взрывает” количество строк. fileciteturn21file0turn21file1

### 4.5. FULL JOIN
В MySQL **не реализован** как отдельный оператор. fileciteturn21file1  
Обычно эмулируют так (идея): *LEFT JOIN* + *RIGHT JOIN* через `UNION`, оставляя строки без совпадений.

---

## 5) Общий синтаксис JOIN
```sql
SELECT столбцы
FROM таблица1
INNER/LEFT/RIGHT JOIN таблица2
  ON таблица1.колонка = таблица2.колонка;
```
fileciteturn21file0turn21file1

---

## 6) Примеры JOIN (из урока)

### 6.1. employees + employee_privileges (сравнить INNER/LEFT/RIGHT)
```sql
SELECT *
FROM employees AS e
JOIN employee_privileges AS ep;

SELECT *
FROM employees AS e
LEFT JOIN employee_privileges AS ep;

SELECT *
FROM employees AS e
RIGHT JOIN employee_privileges AS ep;
```
Как понимать результат:
- `JOIN` (INNER) покажет только сотрудников, у которых найдены привилегии, и наоборот — только совпавшие пары.
- `LEFT JOIN` сохранит **всех сотрудников**; если привилегий нет → поля `ep.*` будут `NULL`.
- `RIGHT JOIN` сохранит **все привилегии**; если сотрудник “не найден” → поля `e.*` будут `NULL`. fileciteturn21file0turn21file1

### 6.2. order_details + products: вместо product_id показать product_name
```sql
SELECT od.order_id, p.product_name
FROM order_details AS od
JOIN products AS p
  ON od.product_id = p.id;
```
fileciteturn21file0turn21file1

### 6.3. Сколько заказов для каждого товара (GROUP BY после JOIN)
```sql
SELECT p.product_name, COUNT(od.order_id) AS orders_cnt
FROM order_details AS od
JOIN products AS p
  ON od.product_id = p.id
GROUP BY p.product_name;
```
fileciteturn21file0turn21file1

### 6.4. order_details + products + purchase_orders (оставить все строки order_details)
```sql
SELECT p.product_name, od.order_id, po.payment_amount
FROM order_details AS od
LEFT JOIN products AS p
  ON od.product_id = p.id
LEFT JOIN purchase_orders AS po
  ON od.purchase_order_id = po.id;
```
fileciteturn21file0turn21file1

---

## 7) Домашнее задание (по слайдам)
1) `UNION`: `orders.id, orders.employee_id` + `purchase_orders.id, purchase_orders.created_by` (как employee_id). fileciteturn21file0turn21file1  
2) В прошлом запросе убрать строки, где employee_id = NULL, и добавить столбец “source_table”. fileciteturn21file0turn21file1  
3) `order_details.*` + `purchase_orders.payment_method`, оставить только где payment_method известен. fileciteturn21file0turn21file1  
4) Вывести `orders` и фамилии клиентов `customers` для тех заказов, по которым есть инвойсы `invoices`. fileciteturn21file0turn21file1  
5) Подсчитать количество инвойсов для каждого клиента из п.4. fileciteturn21file0turn21file1  

---

## 8) Мини-шпаргалка
```sql
-- UNION
SELECT a, b FROM t1
UNION ALL
SELECT a, b FROM t2;

-- INNER JOIN
SELECT *
FROM t1
JOIN t2 ON t1.id = t2.t1_id;

-- LEFT JOIN
SELECT *
FROM t1
LEFT JOIN t2 ON t1.id = t2.t1_id;

-- RIGHT JOIN (обычно заменяют на LEFT JOIN, поменяв местами)
SELECT *
FROM t1
RIGHT JOIN t2 ON t1.id = t2.t1_id;

-- CROSS JOIN (осторожно!)
SELECT *
FROM t1
CROSS JOIN t2;
```
