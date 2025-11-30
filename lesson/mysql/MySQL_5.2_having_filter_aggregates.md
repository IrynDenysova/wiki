# MySQL — Урок 5.2. HAVING: фильтрация агрегированных данных

## 1) Зачем нужна фильтрация после GROUP BY
**Фильтрация данных** — отбор строк/групп по условиям. В SQL есть два похожих оператора, но используются они на **разных этапах** запроса: `WHERE` и `HAVING`. fileciteturn19file0turn19file1

---

## 2) WHERE vs HAVING — главное отличие

### WHERE
- фильтрует **строки таблицы** *до* группировки
- НЕ может фильтровать по агрегатам (нельзя `WHERE COUNT(*) > 1`) fileciteturn19file0turn19file1

### HAVING
- фильтрует **группы** *после* `GROUP BY`
- может содержать агрегатные функции (`COUNT`, `SUM`, `AVG`, …) fileciteturn19file0turn19file1
- `GROUP BY` может быть без `HAVING`, но `HAVING` **не бывает** без `GROUP BY` fileciteturn19file0turn19file1

---

## 3) Синтаксис запроса с HAVING
```sql
SELECT столбец1, агрегатная_функция(столбец2)
FROM таблица
WHERE условия
GROUP BY столбец1
HAVING условие_для_группы;
```
Где:
- `столбец1` — по чему группируем,
- `агрегатная_функция(столбец2)` — что считаем по группам,
- `условие_для_группы` — какие группы оставить. fileciteturn19file0turn19file1

---

## 4) Типовые сценарии (из урока)

### 4.1. Оставить только поставщиков, у которых товаров > 2
Таблица: `products`
```sql
SELECT supplier_ids
FROM products
GROUP BY supplier_ids
HAVING COUNT(id) > 2;
```
fileciteturn19file0turn19file1

### 4.2. Несколько условий в HAVING (группировка по 2 столбцам)
Сгруппировать продукты по `standard_cost` и `list_price`, посчитать товары и оставить только группы, где количество ≥ 2:
```sql
SELECT standard_cost, list_price, COUNT(product_name) AS cnt
FROM products
GROUP BY 1, 2
HAVING COUNT(product_name) > 1;
```
fileciteturn19file0turn19file1

### 4.3. WHERE + HAVING вместе (правильный “паттерн”)
Сначала сузить строки `WHERE`, потом отфильтровать группы `HAVING`:
- оставить только продукты, где в `quantity_per_unit` встречается `oz` (в любом регистре),
- сгруппировать по `standard_cost`,
- оставить группы, где товаров ≥ 3.

```sql
SELECT standard_cost, COUNT(product_name) AS cnt
FROM products
WHERE LOWER(quantity_per_unit) LIKE '%oz%'
GROUP BY 1
HAVING COUNT(product_name) > 2;
```
fileciteturn19file0turn19file1

---

## 5) Важная заметка про производительность
`HAVING` может быть **медленнее**, чем `WHERE`, потому что применяется **после** группировки и расчёта агрегатов. Поэтому, если часть фильтра можно сделать на уровне строк — делай это в `WHERE`, а условия по агрегатам оставляй для `HAVING`. fileciteturn19file0turn19file1

---

## 6) “Порядок написания” vs “фактический порядок выполнения”
### 6.1. Как мы пишем запрос (синтаксис)
```sql
SELECT ...
FROM ...
WHERE ...
GROUP BY ...
HAVING ...
ORDER BY ...
LIMIT ...
```
fileciteturn19file0turn19file1

### 6.2. Как СУБД реально выполняет
1) `FROM` — берёт исходные данные  
2) `WHERE` — фильтрует строки  
3) `GROUP BY` — группирует  
4) `HAVING` — фильтрует группы  
5) `SELECT` — формирует столбцы результата  
6) `ORDER BY` — сортирует  
7) `LIMIT` — ограничивает количество строк fileciteturn19file0turn19file1

> Это очень полезно, чтобы понимать, почему `WHERE` “не видит” агрегаты, а `HAVING` — видит.

---

## 7) Домашнее задание (из материалов)
1) Посчитать основные статистики `AVG/SUM/MIN/MAX` для `unit_cost`. fileciteturn19file0turn19file1  
2) Посчитать количество уникальных заказов `purchase_order_id`. fileciteturn19file0turn19file1  
3) Посчитать количество продуктов `product_id` в каждом заказе `purchase_order_id`, отсортировать по убыванию количества. fileciteturn19file0turn19file1  
4) Посчитать заказы по `date_received`, считая только строки, где `quantity > 30`. fileciteturn19file0turn19file1  
5) Посчитать суммарную стоимость заказов по датам: `quantity * unit_cost`. fileciteturn19file0turn19file1  
6) Сгруппировать товары по `unit_cost` и вычислить `AVG` и `MAX` для `quantity`, только для `purchase_order_id <= 100`. fileciteturn19file0turn19file1  
7) Оставить только строки где `inventory_id IS NOT NULL`:
   - создать `category`: если `unit_cost > 20` → `'Expensive'`, иначе `'others'`
   - посчитать количество продуктов в каждой категории. fileciteturn19file0turn19file1

---

## 8) Мини-шпаргалка
```sql
-- WHERE (до группировки)
SELECT col, COUNT(*)
FROM t
WHERE col2 > 0
GROUP BY col
HAVING COUNT(*) >= 2;   -- HAVING (после GROUP BY)

-- несколько условий в HAVING
HAVING COUNT(*) >= 2 AND AVG(price) > 10;

-- лучший паттерн: WHERE сужаем строки, HAVING фильтруем группы
SELECT group_col, SUM(x) AS s
FROM t
WHERE x IS NOT NULL
GROUP BY group_col
HAVING SUM(x) > 100;
```
