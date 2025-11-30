# MySQL — Урок 11.1. Оптимизация запросов. Индексация. EXPLAIN

## 0) Доступ к БД (на запись) для практики
- `hostname`: `ich-edit.edu.itcareerhub.de`
- `MYSQL_USER`: `ich1`
- `MYSQL_PASSWORD`: `ich1_password_ilovedbs` fileciteturn28file0 fileciteturn28file1

---

## 1) Что такое оптимизация запросов
Оптимизация запросов в MySQL нужна, чтобы:
- уменьшить время выполнения запросов;
- уменьшить использование ресурсов (CPU/память);
- повысить общую эффективность работы БД. fileciteturn28file0 fileciteturn28file1

Один из ключевых инструментов оптимизации — **индексация**. fileciteturn28file0 fileciteturn28file1

---

## 2) Индексация и индекс — определения
**Индексация** — способ организации данных, который ускоряет выполнение запросов. fileciteturn28file0 fileciteturn28file1

**Индекс** — структура данных (чаще всего дерево), которая помогает быстрее находить нужные записи без полного сканирования таблицы. fileciteturn28file0 fileciteturn28file1

---

## 3) Типы индексов в MySQL

### 3.1. PRIMARY KEY
Индекс создаётся автоматически для столбца, объявленного первичным ключом. Гарантирует **уникальность** и быстрый поиск по ключу. fileciteturn28file0 fileciteturn28file1

```sql
CREATE TABLE employees (
  id   INT PRIMARY KEY,
  name VARCHAR(100),
  age  INT
);
```
fileciteturn28file0 fileciteturn28file1

### 3.2. UNIQUE INDEX
Гарантирует уникальность значений в одном или нескольких столбцах. fileciteturn28file0 fileciteturn28file1
```sql
CREATE UNIQUE INDEX idx_employee_email ON employees (email);
```
fileciteturn28file0 fileciteturn28file1

### 3.3. INDEX (обычный индекс)
Ускоряет поиск по одному или нескольким полям, **не** накладывает ограничений на уникальность. fileciteturn28file0 fileciteturn28file1
```sql
CREATE INDEX idx_employee_name ON employees (name);
```
fileciteturn28file0 fileciteturn28file1

### 3.4. FULLTEXT INDEX
Используется для полнотекстового поиска по текстовым полям. fileciteturn28file0 fileciteturn28file1
```sql
CREATE FULLTEXT INDEX idx_article_text ON articles (content);
```
fileciteturn28file0 fileciteturn28file1

### 3.5. COMPOSITE INDEX (составной индекс)
Индекс на **несколько** столбцов одновременно. Полезен, когда запросы используют сразу несколько условий по разным полям. fileciteturn28file0 fileciteturn28file1
```sql
CREATE INDEX idx_employee_name_age ON employees (name, age);
```
fileciteturn28file0 fileciteturn28file1

---

## 4) Как индексы ускоряют запросы (идея)
Без индекса MySQL обычно делает **полный обход таблицы** (просматривает каждую строку).

Пример без индекса: fileciteturn28file0 fileciteturn28file1
```sql
SELECT * FROM employees WHERE age = 30;
```

С индексом MySQL может использовать структуру индекса и быстрее найти нужные строки. fileciteturn28file0 fileciteturn28file1
```sql
CREATE INDEX idx_employee_age ON employees (age);
SELECT * FROM employees WHERE age = 30;
```

---

## 5) Минусы индексации (почему нельзя индексировать всё подряд)
Индексация — это не “бесплатное ускорение”. Ограничения: fileciteturn28file0 fileciteturn28file1
- индексы занимают **дисковое пространство**;
- замедляют операции **INSERT/UPDATE/DELETE**, потому что индексы нужно обновлять;
- на **очень маленьких таблицах** может не дать заметного эффекта.

**Правило из урока:** не индексируйте все столбцы подряд — создавайте индексы только там, где они реально нужны для частых поисковых запросов. fileciteturn28file0 fileciteturn28file1

---

## 6) Индексы для ORDER BY и GROUP BY
Индексы могут ускорить запросы с `ORDER BY` и `GROUP BY`, если индекс включает столбцы, по которым идёт сортировка или группировка. fileciteturn28file0 fileciteturn28file1

Пример: fileciteturn28file0 fileciteturn28file1
```sql
CREATE INDEX idx_name_age ON employees (name, age);
SELECT * FROM employees ORDER BY name, age;
```

---

## 7) EXPLAIN — анализ плана выполнения запроса
**EXPLAIN** показывает, как MySQL собирается выполнять запрос. fileciteturn28file0 fileciteturn28file1

Пример:
```sql
EXPLAIN SELECT * FROM employees WHERE age = 30;
```
Что можно понять по EXPLAIN (на уровне идеи): fileciteturn28file0 fileciteturn28file1
- будет ли полный скан таблицы или использование индекса,
- оценка количества строк, которые будут прочитаны,
- какой индекс будет использован (если применимо).

---

## 8) Практическая работа: таблица students (решение из урока)

### 8.1. Создать таблицу
```sql
CREATE TABLE students (
  id    INT PRIMARY KEY AUTO_INCREMENT,
  name  VARCHAR(100),
  age   INT,
  grade DECIMAL(4, 2)
);
```
fileciteturn28file1

### 8.2. Заполнить таблицу (пример — можно своими значениями)
```sql
INSERT INTO students (name, age, grade) VALUES
  ('Alice', 20, 4.50),
  ('Bob',   20, 3.80),
  ('Diana', 22, 4.10);
```

### 8.3. Индекс по age
```sql
CREATE INDEX idx_age ON students(age);
```
fileciteturn28file1

### 8.4. Запрос на выборку студентов конкретного возраста
```sql
SELECT * FROM students WHERE age = 20;
```
fileciteturn28file1

### 8.5. План выполнения
```sql
EXPLAIN SELECT * FROM students WHERE age = 20;
```
fileciteturn28file1

---

## 9) Мини-шпаргалка
```sql
-- обычный индекс
CREATE INDEX idx_col ON t(col);

-- уникальный индекс
CREATE UNIQUE INDEX idx_u ON t(col);

-- составной индекс
CREATE INDEX idx_a_b ON t(a, b);

-- план запроса
EXPLAIN SELECT * FROM t WHERE col = 123;
```
