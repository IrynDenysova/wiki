# MySQL — Урок 3.2. Особенности работы с датой и временем

## 1) Типы данных даты и времени в MySQL
- **DATE** — только дата `YYYY-MM-DD`  
  Диапазон: `1000-01-01` … `9999-12-31`. fileciteturn16file0turn16file1
- **DATETIME** — дата и время `YYYY-MM-DD HH:MM:SS`  
  Диапазон: `1000-01-01 00:00:00` … `9999-12-31 23:59:59`. fileciteturn16file0turn16file1
- **TIMESTAMP** — дата и время, часто используется как “время последнего обновления” (может зависеть от timezone сервера)  
  Диапазон: `1970-01-01 00:00:01` … `2038-01-19 03:14:07` (ограничение Unix time). fileciteturn16file0turn16file1
- **TIME** — только время `HH:MM:SS`  
  Диапазон: `-838:59:59` … `838:59:59`. fileciteturn16file0turn16file1
- **YEAR** — только год `YYYY`  
  Диапазон: `1901` … `2155`. fileciteturn16file0turn16file1

---

## 2) Основные функции даты/времени

### 2.1. Текущая дата и время
```sql
SELECT NOW() AS CurrentDateTime;
SELECT CURDATE() AS CurrentDate;
SELECT CURTIME() AS CurrentTime;
```
fileciteturn16file0turn16file1

### 2.2. Форматирование даты/времени: DATE_FORMAT
Формат `DATE_FORMAT(date, format)`:
```sql
SELECT DATE_FORMAT(NOW(), '%d-%m-%Y %H:%i:%s') AS FormattedDateTime;
```
fileciteturn16file0turn16file1

Частые код-символы:
- `%Y` — год (4 цифры), `%y` — год (2 цифры)
- `%m` — месяц (01-12)
- `%d` — день (01-31)
- `%H` — часы (00-23)
- `%i` — минуты (00-59)
- `%s` — секунды (00-59)

### 2.3. Разница между датами (в днях): DATEDIFF
```sql
SELECT DATEDIFF('2024-08-30', '2024-08-25') AS DaysDifference;
```
fileciteturn16file0turn16file1

### 2.4. Добавление/вычитание интервала: DATE_ADD / DATE_SUB
```sql
SELECT DATE_ADD(NOW(), INTERVAL 10 DAY) AS FutureDate;
SELECT DATE_SUB(CURDATE(), INTERVAL 90 DAY) AS PastDate;
```
fileciteturn16file0turn16file1

### 2.5. Извлечение части даты: EXTRACT / YEAR
```sql
SELECT EXTRACT(YEAR FROM NOW()) AS CurrentYear;
SELECT YEAR(order_date) AS order_year
FROM orders;
```
fileciteturn16file0turn16file1

### 2.6. Время в секунды и обратно: TIME_TO_SEC / SEC_TO_TIME
```sql
SELECT TIME_TO_SEC('02:30:00') AS Seconds;
SELECT SEC_TO_TIME(9000) AS TimeFormat;
```
fileciteturn16file0turn16file1

---

## 3) Задания с решениями (из урока)

### Задание 1 — order_date в формате ДД-ММ-ГГГГ
```sql
SELECT id,
       DATE_FORMAT(order_date, '%d-%m-%Y') AS formatted_order_date
FROM orders;
```
fileciteturn16file0turn16file1

### Задание 2 — shipped_date в формате ДД/ММ/ГГГГ ЧЧ:ММ:СС
```sql
SELECT id,
       DATE_FORMAT(shipped_date, '%d/%m/%Y %H:%i:%s') AS formatted_shipped_date
FROM orders;
```
fileciteturn16file0turn16file1

### Задание 3 — “сколько дней до отправки”
```sql
SELECT id,
       DATEDIFF(shipped_date, order_date) AS days_to_ship
FROM orders;
```
fileciteturn16file0turn16file1

### Задание 4 — дата 90 дней назад
```sql
SELECT DATE_SUB(CURDATE(), INTERVAL 90 DAY) AS PastDate;
```
fileciteturn16file0turn16file1

### Задание 5 — скрытые преобразования (помним из урока 3.1)
```sql
SELECT '2024-08-25' + 5 AS Result;
SELECT CONCAT('Total sales: $', 12345.67) AS SalesReport;
```
fileciteturn16file0turn16file1

### Задание 6 — извлечь год из order_date
```sql
SELECT id,
       YEAR(order_date) AS order_year
FROM orders;
```
fileciteturn16file0turn16file1

### Задание 7 — текст → DATE (CAST)
```sql
SELECT CAST('2024-08-25' AS DATE) AS ConvertedDate;
```
fileciteturn16file0turn16file1

---

## 4) Различия MySQL и PostgreSQL (по датам)
Идея: в разных СУБД — разные функции/операторы. fileciteturn16file0turn16file1

Короткая памятка:
- Текущая дата/время:  
  MySQL: `NOW()` / `CURDATE()` / `CURTIME()`  
  PostgreSQL: `CURRENT_TIMESTAMP` / `CURRENT_DATE` / `CURRENT_TIME`
- Разница в днях:  
  MySQL: `DATEDIFF(d1, d2)`  
  PostgreSQL: `DATE_PART('day', d1 - d2)`
- Прибавить/вычесть интервал:  
  MySQL: `DATE_ADD(date, INTERVAL 10 DAY)` / `DATE_SUB(...)`  
  PostgreSQL: `date + INTERVAL '10 day'` / `date - INTERVAL '10 day'`
- Время в секунды:  
  MySQL: `TIME_TO_SEC(time)`  
  PostgreSQL: `EXTRACT(EPOCH FROM time)`
- Секунды → время:  
  MySQL: `SEC_TO_TIME(seconds)`  
  PostgreSQL: обычно `TO_TIMESTAMP(seconds)` (в зависимости от задачи)

---

## 5) Домашнее задание (что требуется)
1) Вывести ваш возраст на текущий день **в секундах**. fileciteturn16file0turn16file1  
   Вариант в MySQL (если есть дата рождения):
   ```sql
   SELECT TIMESTAMPDIFF(SECOND, '1990-01-01', NOW()) AS age_seconds;
   ```
2) Какая дата будет через **51 день**. fileciteturn16file0turn16file1  
   ```sql
   SELECT DATE_ADD(CURDATE(), INTERVAL 51 DAY) AS plus_51_days;
   ```
3) Отформатировать предыдущий запрос: вывести **день недели** для этой даты (использовать документацию MySQL). fileciteturn16file0turn16file1  
4) Подключиться к `northwind`: вывести `transaction_created_date` из `inventory_transactions` и столбец `+3 часа`. fileciteturn16file0turn16file1  
   ```sql
   SELECT transaction_created_date,
          DATE_ADD(transaction_created_date, INTERVAL 3 HOUR) AS plus_3_hours
   FROM inventory_transactions;
   ```
5) Вывести текст: `Клиент с id <customer_id> сделал заказ <order_date>` из `orders`  
   – двумя способами: **неявное преобразование** и **явное CAST** (для customer_id использовать `CHAR`, не `VARCHAR`). fileciteturn16file0turn16file1

---

## 6) Мини-шпаргалка урока
```sql
-- now/date/time
NOW(); CURDATE(); CURTIME();

-- format
DATE_FORMAT(dt, '%d-%m-%Y %H:%i:%s');

-- difference days
DATEDIFF(date1, date2);

-- +/- intervals
DATE_ADD(dt, INTERVAL 10 DAY);
DATE_SUB(dt, INTERVAL 3 HOUR);

-- extract
EXTRACT(YEAR FROM dt);
YEAR(dt);

-- time <-> seconds
TIME_TO_SEC('02:30:00');
SEC_TO_TIME(9000);

-- cast string -> date
CAST('2024-08-25' AS DATE);
```
