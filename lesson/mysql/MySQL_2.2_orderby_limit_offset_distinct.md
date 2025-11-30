# MySQL — Урок 2.2. Ограничение выборки. Уникальные значения  
*(ORDER BY / LIMIT / OFFSET / DISTINCT и их комбинации)*

## 1) ORDER BY — сортировка результата
`ORDER BY` сортирует строки результата запроса по одному или нескольким столбцам.  
По умолчанию сортировка **по возрастанию** (`ASC`), но можно указать **по убыванию** (`DESC`). fileciteturn14file0

**Шаблон:**
```sql
SELECT column1, column2, ...
FROM table_name
ORDER BY column1 [ASC|DESC], column2 [ASC|DESC], ...;
``` fileciteturn14file0turn14file1

### Примеры из урока
Сортировка продуктов по убыванию `standard_cost`:
```sql
SELECT product_name, standard_cost
FROM products
ORDER BY standard_cost DESC;
``` fileciteturn14file0turn14file1

Сортировка по двум столбцам по возрастанию:
```sql
SELECT product_name, standard_cost, list_price
FROM products
ORDER BY standard_cost ASC, list_price ASC;
``` fileciteturn14file0turn14file1

Сортировка клиентов: сначала по компании, потом по городу:
```sql
SELECT company, city
FROM customers
ORDER BY company ASC, city ASC;
``` fileciteturn14file0turn14file1

---

## 2) LIMIT — ограничение количества строк
`LIMIT` задаёт максимальное число строк в результате запроса. fileciteturn14file0turn14file1

**Шаблон:**
```sql
SELECT ...
FROM ...
LIMIT n;
``` fileciteturn14file0turn14file1

### Примеры из урока
5 самых дешёвых продуктов по `standard_cost` (сначала сортировка, потом LIMIT):
```sql
SELECT product_name, standard_cost
FROM products
ORDER BY standard_cost ASC
LIMIT 5;
``` fileciteturn14file0turn14file1

10 последних заказов по дате:
```sql
SELECT id
FROM orders
ORDER BY order_date DESC
LIMIT 10;
``` fileciteturn14file0turn14file1

Первые 5 строк таблицы:
```sql
SELECT *
FROM customers
LIMIT 5;
``` fileciteturn14file0turn14file1

---

## 3) OFFSET — пропуск строк (пагинация)
`OFFSET` пропускает указанное число строк в результате. Обычно применяется вместе с `LIMIT` для постраничного вывода (pagination). fileciteturn14file0turn14file1

**Шаблон:**
```sql
SELECT ...
FROM ...
ORDER BY ...
LIMIT rows OFFSET offset_value;
``` fileciteturn14file0turn14file1

### Пример из урока: “2-я страница по 10 товаров”
Если товары сортируются по имени от A до Z, и на странице 10 товаров:
```sql
SELECT product_name
FROM products
ORDER BY product_name ASC
LIMIT 10 OFFSET 10;
``` fileciteturn14file0turn14file1

> Правило:  
> `OFFSET = (page_number - 1) * page_size`  
> Например, 3-я страница по 10 → `OFFSET 20`.

---

## 4) DISTINCT — уникальные значения
`DISTINCT` убирает дубликаты строк в результате запроса (возвращает уникальные значения). fileciteturn14file0turn14file1

**Шаблон:**
```sql
SELECT DISTINCT column1, column2, ...
FROM table_name;
``` fileciteturn14file0turn14file1

### Пример из урока: уникальные города клиентов
```sql
SELECT DISTINCT city
FROM customers;
``` fileciteturn14file0turn14file1

---

## 5) Комбинирование DISTINCT + ORDER BY + LIMIT + OFFSET
В SQL эти операторы можно комбинировать: выбрать уникальные значения, отсортировать, затем взять “кусок” результата. fileciteturn14file0turn14file1

Пример из материалов:
```sql
SELECT DISTINCT city
FROM customers
ORDER BY first_name
LIMIT 3 OFFSET 2;
``` fileciteturn14file0turn14file1

Практическая рекомендация: обычно `ORDER BY` делают по тому, что влияет на смысл результата (например, `ORDER BY city`), чтобы сортировка “уникальных” была однозначной.

---

## 6) Частые ошибки и правила (коротко)
- **LIMIT без ORDER BY**: “первые N строк” могут быть непредсказуемы, потому что без сортировки порядок не гарантирован.
- **LIMIT + OFFSET** почти всегда используем вместе с **ORDER BY**.
- `DISTINCT` работает по **всем** выбранным столбцам:  
  `SELECT DISTINCT city, country` возвращает уникальные пары *(city,country)*.

---

## 7) ДЗ (по слайдам)
1) `USE northwind;` и вывести все строки из `suppliers`. fileciteturn14file0turn14file1  
2) Таблица `order_details`: вывести `id`, `order_id` + вычисляемый столбец `category` по `unit_price` (>10 → 'Expensive', иначе 'Cheap') — **двумя способами**: `IF` и `CASE`. fileciteturn14file0turn14file1  
3) Вывести строки, где `purchase_order_id` не указано (`IS NULL`), добавить `total_price = quantity * unit_price`. fileciteturn14file0turn14file1  
4) `employees`: один столбец “Имя Фамилия” через пробел, вывести **3 строки начиная со второй** (то есть `LIMIT 3 OFFSET 1`). fileciteturn14file0turn14file1  
5) `orders`: вывести один столбец `год-месяц` из `order_date` (формат 'YYYY-MM'). fileciteturn14file0turn14file1  
6) `customers`: вывести **уникальные** названия компаний, отсортировать по **убыванию**. fileciteturn14file0turn14file1  
7) Отформатировать стиль SQL.
8) Сохранить запросы в файл `.sql` и загрузить на платформу. fileciteturn14file0turn14file1  

---

## 8) Мини-шпаргалка урока
```sql
-- сортировка
SELECT * FROM t ORDER BY col1 DESC, col2 ASC;

-- топ/лимит
SELECT * FROM t ORDER BY col LIMIT 10;

-- пагинация
SELECT * FROM t ORDER BY col LIMIT 10 OFFSET 20;

-- уникальные значения
SELECT DISTINCT col FROM t;

-- уникальные + сортировка + кусок
SELECT DISTINCT col
FROM t
ORDER BY col
LIMIT 5 OFFSET 5;
```
