# MySQL — Урок 10.1. Основные оконные функции ранжирования  
*(ROW_NUMBER / RANK / DENSE_RANK / NTILE)*

Материалы: презентация и конспект урока. fileciteturn26file0turn26file1

## 0) Доступ к учебной БД (read-only)
- `hostname`: ich-db.edu.itcareerhub.de  
- `username`: ich1  
- `password`: password fileciteturn26file0turn26file1

---

## 1) Что такое ранжирующие оконные функции
Это оконные функции, которые **присваивают номер/ранг** каждой строке в рамках окна `OVER(...)` — обычно в заданном порядке `ORDER BY` и (опционально) внутри группы `PARTITION BY`. fileciteturn26file0turn26file1

---

## 2) Основные функции ранжирования

### 2.1. `ROW_NUMBER()`
Присваивает **уникальный номер** каждой строке в пределах окна.  
Даже если значения одинаковые, номера всё равно разные. fileciteturn26file0turn26file1

### 2.2. `RANK()`
Присваивает ранги, но **пропускает номера рангов** при одинаковых значениях. fileciteturn26file0turn26file1  
Пример: значения `500, 300, 300, 200` → ранги `1, 2, 2, 4` (тройка “пропущена”).

### 2.3. `DENSE_RANK()`
Присваивает ранги **без пропусков** при одинаковых значениях. fileciteturn26file0turn26file1  
Пример: `500, 300, 300, 200` → `1, 2, 2, 3`.

### 2.4. `NTILE(n)`
Делит строки на **n примерно равных групп** (квантили) и присваивает номер группы `1..n`. fileciteturn26file0turn26file1  
Полезно для квартилей/децилей и “разбить на группы по цене”.

---

## 3) Где применяют (из урока)
- рейтинг товаров/сотрудников  
- анализ позиций и рангов  
- упрощение сложных запросов (иногда вместо подзапросов)  
- группировка и упорядочение данных внутри `PARTITION BY`  
- создание отчётов (например, распределение по квартилям через `NTILE`) fileciteturn26file0turn26file1

---

## 4) Общий синтаксис
```sql
SELECT
  column1,
  ranking_function(column2) OVER (
    PARTITION BY column3
    ORDER BY column4
  ) AS rank_column
FROM table_name;
```
Пояснение:
- `ranking_function(...)` — одна из ранжирующих функций (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`)  
- `PARTITION BY` — (опционально) разделяет данные на группы  
- `ORDER BY` — задаёт порядок в рамках окна, по которому и считается ранжирование fileciteturn26file0turn26file1

---

## 5) Примеры из урока

### 5.1. Пример 1 — `ROW_NUMBER()` по дате продажи
```sql
SELECT
  SaleID, SaleDate, SaleAmount,
  ROW_NUMBER() OVER (ORDER BY SaleDate) AS RowNum
FROM Sales;
```
fileciteturn26file0turn26file1

### 5.2. Пример 2 — `RANK()` внутри отдела по убыванию продаж
```sql
SELECT
  ProductID, DepartmentID, SaleAmount,
  RANK() OVER (PARTITION BY DepartmentID ORDER BY SaleAmount DESC) AS Rank
FROM ProductSales;
```
fileciteturn26file0turn26file1

### 5.3. Пример 3 — `DENSE_RANK()` по убыванию продаж
```sql
SELECT
  ProductID, SaleAmount,
  DENSE_RANK() OVER (ORDER BY SaleAmount DESC) AS DenseRank
FROM ProductSales;
```
fileciteturn26file0turn26file1

### 5.4. Пример 4 — `NTILE(3)` (разделить на 3 группы по сумме)
```sql
SELECT
  SaleID, SaleAmount,
  NTILE(3) OVER (ORDER BY SaleAmount) AS Quartile
FROM Sales;
```
fileciteturn26file0turn26file1

---

## 6) Практическая работа (таблица `products`) + решения

### 6.1. ТОП-10 продуктов: ранг без пропусков по убыванию `standard_cost`
```sql
SELECT
  product_name,
  DENSE_RANK() OVER (ORDER BY standard_cost DESC) AS rnk
FROM products
LIMIT 10;
```
fileciteturn26file1

### 6.2. Пронумеровать продукты по названию от A до Z
```sql
SELECT
  product_name,
  ROW_NUMBER() OVER (ORDER BY product_name) AS rownum
FROM products;
```
fileciteturn26file1

### 6.3. Разделить продукты на 4 равные группы по `list_price`
```sql
SELECT
  product_name,
  list_price,
  NTILE(4) OVER (ORDER BY list_price) AS price_group
FROM products;
```
fileciteturn26file1

---

## 7) Мини-шпаргалка: что выбрать
- Нужен уникальный номер строки → `ROW_NUMBER()`
- Нужны ранги с “дырками” при одинаковых значениях → `RANK()`
- Нужны ранги без пропусков → `DENSE_RANK()`
- Нужно разбить на равные группы (квантили) → `NTILE(n)`
