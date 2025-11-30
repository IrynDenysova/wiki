# MySQL — Урок 6.1. Связи между таблицами и ER-диаграммы (ERD)

## 1) Зачем хранить данные в разных таблицах
- **Избежание дублирования**: данные о клиенте не повторяются в каждом заказе — хранятся один раз в `customers`. fileciteturn20file1  
- **Удобство управления**: обновил данные в одном месте — обновилось “везде”. fileciteturn20file1  
- **Целостность данных**: связи и ключи помогают сохранять непротиворечивость. fileciteturn20file1  

---

## 2) Основные типы связей между таблицами
### 2.1. Один к одному (One-to-One, 1:1)
Каждой записи в таблице A соответствует **ровно одна** запись в таблице B (и наоборот). fileciteturn20file0turn20file1  
Пример из урока: `employees` ↔ `employee_privileges` (у сотрудника одна привилегия или её нет). fileciteturn20file1  

### 2.2. Один ко многим (One-to-Many, 1:N)
Одной записи в таблице A может соответствовать **много** записей в таблице B. Это самый частый тип связи. fileciteturn20file0turn20file1  
Пример: `customers` → `orders`: один клиент делает много заказов, но заказ принадлежит одному клиенту. fileciteturn20file1  

### 2.3. Многие ко многим (Many-to-Many, M:N)
Много записей A ↔ много записей B. Почти всегда реализуется через **промежуточную таблицу** (junction/bridge table). fileciteturn20file0turn20file1  
Пример: `orders` ↔ `products` — связь M:N реализуется через `order_details` (в заказе много товаров, и товар встречается во многих заказах). fileciteturn20file1  

---

## 3) Ключи для связи таблиц

### 3.1. Первичный ключ (Primary Key, PK)
Это поле/набор полей, которое **уникально** идентифицирует строку в таблице. fileciteturn20file0turn20file1  

Характеристики PK: fileciteturn20file0turn20file1  
- **уникальность**
- **не допускает NULL**
- **редко меняется** (неизменяемость)

Пример: в `customers` поле `id` — первичный ключ. fileciteturn20file1  

### 3.2. Внешний ключ (Foreign Key, FK)
Поле (или набор полей) в одной таблице, которое **ссылается** на PK другой таблицы. fileciteturn20file0turn20file1  

Зачем нужен FK: fileciteturn20file0turn20file1  
- “скрепляет” таблицы
- обеспечивает **ссылочную целостность** (нельзя создать заказ для несуществующего клиента, если FK настроен)

Примеры в northwind: fileciteturn20file0turn20file1  
- `orders.customer_id` → `customers.id`  
- `order_details.order_id` → `orders.id`  
- `order_details.product_id` → `products.id`

---

## 4) ER-диаграмма (ERD): что это и из чего состоит
**ER-диаграмма (Entity-Relationship Diagram)** — графическое представление структуры БД и связей между сущностями (таблицами). fileciteturn20file0turn20file1  

Основные компоненты ERD: fileciteturn20file0turn20file1  
- **Entities (Сущности)** — таблицы (рисуются прямоугольниками)  
  Примеры: `customers`, `orders`, `products`
- **Attributes (Атрибуты)** — столбцы таблиц  
  Примеры: `id`, `company_name`, `contact_name`
- **Relationships (Связи)** — как сущности связаны: 1:1, 1:N, M:N

---

## 5) ERD для northwind (customers, orders, products, order_details)
Идея связей:
- `customers` **1 → N** `orders`
- `orders` **1 → N** `order_details`
- `products` **1 → N** `order_details`
- значит `orders` **M ↔ N** `products` через `order_details` fileciteturn20file0turn20file1  

Упрощённая текстовая схема:
```text
customers (PK id)
   1
   |
   |  (FK orders.customer_id -> customers.id)
   N
orders (PK id)
   1
   |
   |  (FK order_details.order_id -> orders.id)
   N
order_details (PK id, + FK product_id)
   N
   |
   |  (FK order_details.product_id -> products.id)
   1
products (PK id)
```

---

## 6) Практика: как “увидеть” связи в данных (идея запросов)
Проверить 1:N (клиенты и их заказы):
```sql
SELECT c.id, c.company_name, COUNT(o.id) AS orders_cnt
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.company_name
ORDER BY orders_cnt DESC;
```

Проверить M:N через таблицу-связку (товары внутри заказов):
```sql
SELECT od.order_id, COUNT(DISTINCT od.product_id) AS unique_products
FROM order_details od
GROUP BY od.order_id
ORDER BY unique_products DESC;
```

---

## 7) Задание из урока
1) Изучить таблицы northwind и привести по примеру связей 1:1, 1:N, M:N. fileciteturn20file0turn20file1  
2) Нарисовать ERD для `customers`, `orders`, `products`, `order_details` в draw.io (категория Software, самый первый шаблон) или на бумаге. fileciteturn20file0turn20file1  

---

## Мини-шпаргалка
- **1:1** — одна запись ↔ одна запись  
- **1:N** — запись A ↔ много записей B (самое частое)  
- **M:N** — много ↔ много, делаем через **таблицу-связку**  
- **PK**: уникальный, не NULL, редко меняется  
- **FK**: ссылка на PK другой таблицы → целостность данных  
