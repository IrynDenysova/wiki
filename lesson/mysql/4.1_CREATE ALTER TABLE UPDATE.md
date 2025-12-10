# MySQL — Урок 4.1. Создание и изменение таблиц. Ограничения (constraints) + UPDATE

## 0) О чём урок (самое важное)
- **CREATE TABLE**: создаём таблицу “с нуля”
- **Constraints (ограничения)**: правила целостности данных
- **INSERT**: наполнение таблицы
- **CREATE TABLE ... AS SELECT**: создать таблицу на основе существующей выборки
- **UPDATE**: исправление/изменение данных
- Почему данные обычно **не вносятся вручную** (источники данных)

---

## 1) Constraints (ограничения): зачем они
Ограничения защищают БД от “плохих” данных: пустых значений там, где они недопустимы, дублей, отрицательных зарплат и т.д.

### Основные ограничения
- **PRIMARY KEY** — уникально идентифицирует строку; не может быть `NULL`.
- **AUTO_INCREMENT** — автоматически увеличивает значение (часто вместе с PRIMARY KEY).
- **UNIQUE** — запрещает дубликаты в столбце/комбинации столбцов.
- **NOT NULL** — значение обязательно (NULL запрещён).
- **DEFAULT** — значение по умолчанию при вставке (если не указали явно).
- **CHECK** — логическое условие на значение (например, `Salary > 0`).

> Запомни: ограничения — это “охранники на входе” в таблицу.

---

## 2) CREATE TABLE — общий шаблон
```sql
CREATE TABLE TableName (
  Column1 DataType [Constraints],
  Column2 DataType [Constraints],
  ...
);
```

Перед созданием таблицы продумай:
- какие столбцы нужны,
- какой **тип** у каждого,
- какие **ограничения** должны защищать данные.

---

## 3) Практика: таблица Employees (пример из урока)

### 3.1. Создание таблицы
```sql
CREATE TABLE Employees (
  EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
  FirstName  VARCHAR(50) NOT NULL,
  LastName   VARCHAR(50) NOT NULL,
  BirthDate  DATE,
  HireDate   DATE DEFAULT CURRENT_DATE,
  Salary     DECIMAL(10, 2) CHECK (Salary > 0),
  Email      VARCHAR(100) UNIQUE
);
```

Что здесь важно:
- `EmployeeID` сам увеличивается и уникален — удобно для идентификаторов
- имена не могут быть пустыми (`NOT NULL`)
- `HireDate` автоматически ставится как текущая дата, если не указали
- `Salary` обязана быть > 0 (`CHECK`)
- `Email` не может повторяться (`UNIQUE`)

### 3.2. INSERT — вставка данных (5 строк одним запросом)
```sql
INSERT INTO Employees (FirstName, LastName, BirthDate, Salary, Email)
VALUES
  ('Alice',   'Green',    '1985-05-15', 55000.00, 'alice.green@example.com'),
  ('Bob',     'Smith',    '1990-08-22', 60000.00, 'bob.smith@example.com'),
  ('Charlie', 'Johnson',  '1988-02-10', 52000.00, 'charlie.johnson@example.com'),
  ('Diana',   'Williams', '1992-11-01', 58000.00, 'diana.williams@example.com'),
  ('Edward',  'Brown',    '1987-09-30', 61000.00, 'edward.brown@example.com');
```

### 3.3. Проверка
```sql
SELECT *
FROM Employees;
```

### 3.4. Ошибки при вставке (полезно проверить)
Попробуй вставить записи, которые нарушают ограничения:
- пустое имя (`NULL` в `FirstName`)
- отрицательная зарплата
- дублирующийся email  
→ MySQL должен вернуть ошибку.

---

## 4) Создать таблицу на основе другой: CREATE TABLE ... AS SELECT
Частая практика — не создавать “с нуля”, а брать существующую таблицу как основу.

Шаблон:
```sql
CREATE TABLE NewTable AS
SELECT *
FROM ExistingTable
WHERE <условие>;
```

### Пример: “короткая” таблица из первых 2 строк Employees
```sql
CREATE TABLE Employees_short AS
SELECT *
FROM Employees
LIMIT 2;
```

---

## 5) UPDATE — изменение существующих записей
`UPDATE` используется, когда данные уже есть, но их нужно исправить/обновить.

### 5.1. Шаблон
```sql
UPDATE TableName
SET col1 = new_value1,
    col2 = new_value2
WHERE condition;
```

### 5.2. Важнейшее правило безопасности
**Всегда проверяй WHERE.**  
`UPDATE` без `WHERE` обновит **все строки**.

### 5.3. Примеры из урока

Изменить зарплату сотрудника с `EmployeeID = 1`:
```sql
UPDATE Employees
SET Salary = 65000
WHERE EmployeeID = 1;
```

Увеличить зарплату всем, кто работает с 2024 года, на 10%:
```sql
UPDATE Employees
SET Salary = Salary * 1.10
WHERE HireDate >= '2024-01-01';
```

---

## 6) Откуда обычно берутся данные в БД (почему не вручную)
### Основные источники/методы
- **Импорт файлов**: CSV / Excel / XML / JSON
- **Формы и интерфейсы**: сайты/приложения, где пользователь вводит данные
- **API**: автоматическая передача между системами
- **Копирование из других БД / ETL**: миграции, синхронизация, выгрузки

### Почему вручную не вносят
- **Низкая масштабируемость** (много данных — вручную долго)
- **Ошибки человеческого фактора**
- **Интеграции** требуют автоматического обмена
- **Поддержка актуальности** проще через автоматические процессы

---

## 7) Мини-шпаргалка (самое нужное)
```sql
-- создать таблицу
CREATE TABLE t (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  email VARCHAR(100) UNIQUE,
  created_at DATE DEFAULT CURRENT_DATE,
  salary DECIMAL(10,2) CHECK (salary > 0)
);

-- вставить данные
INSERT INTO t (name, email, salary)
VALUES ('A', 'a@x.com', 1000.00);

-- создать таблицу из выборки
CREATE TABLE t2 AS
SELECT * FROM t
LIMIT 10;

-- обновить данные (ВСЕГДА С WHERE!)
UPDATE t
SET salary = salary * 1.10
WHERE id = 1;
```
