# MySQL — Урок 11.2. Пользовательские функции (CREATE FUNCTION)

## 0) Доступ к БД (на запись) для практики
- `hostname`: `ich-edit.edu.itcareerhub.de`
- `MYSQL_USER`: `ich1`
- `MYSQL_PASSWORD`: `ich1_password_ilovedbs`

fileciteturn29file0 fileciteturn29file1

---

## 1) Что такое пользовательская функция (UDF)
**Пользовательская функция** — это функция, которую вы создаёте сами командой `CREATE FUNCTION`.  
После создания её можно использовать в запросах так же, как встроенные функции MySQL.

fileciteturn29file0 fileciteturn29file1

---

## 2) Синтаксис создания функции
Базовый шаблон:

```sql
CREATE FUNCTION function_name (parameter1 datatype, parameter2 datatype, ...)
RETURNS return_datatype
DETERMINISTIC
BEGIN
  -- Function body
  RETURN return_value;
END;
```

fileciteturn29file0 fileciteturn29file1

### Зачем нужен `DELIMITER`
Внутри тела функции используются `;`, поэтому перед созданием функции обычно меняют разделитель команд:

```sql
DELIMITER //
-- CREATE FUNCTION ... END //
DELIMITER ;
```

fileciteturn29file0 fileciteturn29file1

---

## 3) Важное свойство: DETERMINISTIC / NON-DETERMINISTIC
- **DETERMINISTIC** — функция для одинаковых входных данных всегда возвращает одинаковый результат.
- **NON-DETERMINISTIC** — функция может возвращать разные результаты при одинаковых входных данных (например, если внутри используется `NOW()`).

fileciteturn29file0 fileciteturn29file1

---

## 4) Примеры пользовательских функций (из урока)

### 4.1. Квадратный корень
```sql
DELIMITER //
CREATE FUNCTION square_root(x DOUBLE)
RETURNS DOUBLE
DETERMINISTIC
BEGIN
  RETURN SQRT(x);
END //
DELIMITER ;
```

fileciteturn29file0 fileciteturn29file1

### 4.2. Возраст по дате рождения
```sql
DELIMITER //
CREATE FUNCTION calculate_age(birthdate DATE)
RETURNS INT
DETERMINISTIC
BEGIN
  RETURN TIMESTAMPDIFF(YEAR, birthdate, CURDATE());
END //
DELIMITER ;
```

fileciteturn29file0 fileciteturn29file1

### 4.3. Приветствие
```sql
DELIMITER //
CREATE FUNCTION greet_user(name VARCHAR(100))
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
  RETURN CONCAT('Hello, ', name, '!');
END //
DELIMITER ;
```

fileciteturn29file0 fileciteturn29file1

---

## 5) Использование пользовательских функций
После создания вызываем как обычную функцию:

```sql
SELECT square_root(25);
SELECT calculate_age('1990-01-01');
SELECT greet_user('Alice');
```

fileciteturn29file0 fileciteturn29file1

---

## 6) Практическая работа (из урока) + решения

### 6.1. Функция: перевести текст в верхний регистр
Задание: функция принимает строку и возвращает её в верхнем регистре.

Решение:
```sql
DELIMITER //
CREATE FUNCTION to_uppercase(input_text VARCHAR(255))
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
  RETURN UPPER(input_text);
END //
DELIMITER ;
```

fileciteturn29file1

### 6.2. Функция: проверка чётности
Задание: вернуть `1`, если число чётное, и `0` — если нечётное.

Решение:
```sql
DELIMITER //
CREATE FUNCTION is_even(number INT)
RETURNS BOOLEAN
DETERMINISTIC
BEGIN
  RETURN number % 2 = 0;
END //
DELIMITER ;
```

fileciteturn29file1

---

## 7) Домашнее задание (из материалов)
1) **Площадь круга**: функция по радиусу `r` (π через `PI()`).
2) **Гипотенуза** прямоугольного треугольника по катетам `a` и `b`.

fileciteturn29file0

---

## 8) Мини-шпаргалка
```sql
-- создать функцию
DELIMITER //
CREATE FUNCTION f(x INT)
RETURNS INT
DETERMINISTIC
BEGIN
  RETURN x + 1;
END //
DELIMITER ;

-- использовать
SELECT f(10);
```
