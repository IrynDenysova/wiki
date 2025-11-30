# MySQL — Урок 12.2. Параметры в хранимых процедурах (IN / OUT / INOUT)

## 0) Доступ к учебной БД (на запись)
- `hostname`: `ich-edit.edu.itcareerhub.de`
- `MYSQL_USER`: `ich1`
- `MYSQL_PASSWORD`: `ich1_password_ilovedbs` fileciteturn31file0turn31file1

---

## 1) Зачем параметры в процедурах
В MySQL хранимые процедуры могут принимать параметры, чтобы:
- получать входные значения при вызове,
- возвращать результаты наружу,
- делать процедуру **гибкой** (одна процедура работает для разных входных данных). fileciteturn31file1

Есть 3 типа параметров:
- `IN` — входной (только чтение),
- `OUT` — выходной (вернуть значение),
- `INOUT` — вход + выход (принять значение, изменить, вернуть). fileciteturn31file0turn31file1

---

## 2) IN-параметры (входные)

### 2.1. Что это
`IN` — входные параметры, которые передаются в процедуру при вызове, и используются в процессе выполнения процедуры. fileciteturn31file0turn31file1

### 2.2. Характеристики IN
- значение **передаётся** в процедуру;
- параметр можно использовать, но его **нельзя менять** (только чтение);
- даже если попытаться изменить, изменение **не возвращается** вызывающей программе. fileciteturn31file0turn31file1

### 2.3. Пример: получить имя сотрудника по его id
```sql
DELIMITER $$
CREATE PROCEDURE get_employee_name(IN emp_id INT)
BEGIN
  SELECT name FROM employees WHERE id = emp_id;
END $$
DELIMITER ;
```
fileciteturn31file0turn31file1

Вызов:
```sql
CALL get_employee_name(1);
```
fileciteturn31file0turn31file1

---

## 3) OUT-параметры (выходные)

### 3.1. Что это
`OUT` — выходные параметры, которые используются, чтобы **вернуть значение из процедуры**. fileciteturn31file0turn31file1

### 3.2. Характеристики OUT
- значение назначается **внутри** процедуры и возвращается после выполнения;
- OUT не используется как входной параметр;
- вызывающая программа/сессия получает значение OUT после завершения процедуры. fileciteturn31file0turn31file1

### 3.3. Пример: вернуть зарплату сотрудника через OUT
```sql
DELIMITER $$
CREATE PROCEDURE get_employee_salary(IN emp_id INT, OUT emp_salary INT)
BEGIN
  SELECT salary INTO emp_salary
  FROM employees
  WHERE id = emp_id;
END $$
DELIMITER ;
```
fileciteturn31file0turn31file1

Вызов (через пользовательскую переменную):
```sql
SET @salary = 0;
CALL get_employee_salary(1, @salary);
SELECT @salary;
```
fileciteturn31file0turn31file1

---

## 4) INOUT-параметры (двунаправленные)

### 4.1. Что это
`INOUT` — двунаправленные параметры: можно **передать значение в процедуру**, изменить его внутри и **вернуть обратно**. fileciteturn31file0turn31file1

### 4.2. Характеристики INOUT
- работает и как вход, и как выход;
- начальное значение передаётся в процедуру;
- внутри процедуры параметр можно менять, и новое значение возвращается вызывающей стороне. fileciteturn31file0turn31file1

### 4.3. Пример: увеличить зарплату на 20% (через INOUT)
```sql
DELIMITER $$
CREATE PROCEDURE update_employee_salary(INOUT emp_salary INT)
BEGIN
  SET emp_salary = emp_salary * 1.2;
END $$
DELIMITER ;
```
fileciteturn31file0turn31file1

Вызов:
```sql
SET @salary = 5000;
CALL update_employee_salary(@salary);
SELECT @salary;
```
fileciteturn31file0turn31file1

---

## 5) Сравнение типов параметров (таблица)
| Тип | Передаёт в процедуру | Возвращает из процедуры | Можно менять внутри |
|---|---|---|---|
| IN | Да | Нет | Нет |
| OUT | Нет | Да | Да |
| INOUT | Да | Да | Да |

fileciteturn31file0turn31file1

---

## 6) Практическая работа (из урока) — решения

### 6.1. IN: найти имя товара по id
1) Создать таблицу `products (id, product_name, price)` и вставить данные.  
2) Процедура:
```sql
CREATE PROCEDURE get_product_name(IN product_id INT)
BEGIN
  SELECT product_name FROM products WHERE id = product_id;
END;
```
fileciteturn31file1

### 6.2. OUT: вернуть годовую зарплату (monthly_salary * 12)
```sql
CREATE PROCEDURE get_annual_salary(IN emp_id INT, OUT annual_salary INT)
BEGIN
  SELECT monthly_salary * 12 INTO annual_salary
  FROM employees
  WHERE id = emp_id;
END;
```
fileciteturn31file1

Вызов:
```sql
SET @annual = 0;
CALL get_annual_salary(1, @annual);
SELECT @annual;
```

### 6.3. INOUT: увеличить бонус на 15%
```sql
CREATE PROCEDURE increase_bonus(INOUT bonus_amount DECIMAL(10, 2))
BEGIN
  SET bonus_amount = bonus_amount * 1.15;
END;
```
fileciteturn31file1

Вызов:
```sql
SET @bonus = 1000;
CALL increase_bonus(@bonus);
SELECT @bonus;   -- ожидаемо: 1150
```
fileciteturn31file1

---

## 7) Домашнее задание (как в материалах)
1) Вывести `department_id`, где работает сотрудник, по `id` сотрудника. fileciteturn31file0turn31file1  
2) Создать процедуру `get_employee_age`: принимает `id` (IN) и возвращает возраст (OUT). fileciteturn31file0turn31file1  
3) Создать процедуру `decrease_salary`: принимает зарплату (INOUT) и уменьшает её на 10%. fileciteturn31file0turn31file1  

---

## 8) Мини-шпаргалка вызова
- `IN` → просто значение: `CALL p(123);`
- `OUT` → нужна переменная: `CALL p(123, @out); SELECT @out;`
- `INOUT` → нужна переменная: `SET @x=...; CALL p(@x); SELECT @x;`
