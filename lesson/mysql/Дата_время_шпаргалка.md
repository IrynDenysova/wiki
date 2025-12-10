# MySQL Date & Time — шпаргалка (DATE/TIME/DATETIME)

Основано на файле `datetime_queries.sql`.

---

## 1) Текущая дата и время
```sql
SELECT CURRENT_DATE;       -- текущая дата (DATE)
SELECT CURRENT_TIME;       -- текущее время (TIME)
SELECT NOW();              -- текущая дата+время (DATETIME)
SELECT CURRENT_TIMESTAMP;  -- текущая дата+время (универсально для СУБД)
```

---

## 2) Извлечение частей даты/времени
```sql
SELECT
  YEAR(NOW()), MONTH(NOW()), DAY(NOW()),
  HOUR(NOW()), MINUTE(NOW()), SECOND(NOW());
```

### День/неделя/месяц/квартал
```sql
SELECT WEEKDAY(NOW());     -- 0=Пн ... 6=Вс
SELECT DAYOFWEEK(NOW());   -- 1=Вс ... 7=Сб
SELECT DAYOFYEAR(NOW());   -- 1..366
SELECT YEARWEEK(NOW());    -- YYYYWW
SELECT WEEK(NOW());        -- номер недели (зависит от режима/начала недели)
SELECT LAST_DAY(NOW());    -- последний день месяца
SELECT MONTHNAME(NOW());   -- имя месяца
SELECT DAYNAME(NOW());     -- имя дня недели
SELECT QUARTER(NOW());     -- квартал: 1..4
```

### EXTRACT(part FROM datetime)
```sql
SELECT EXTRACT(YEAR FROM NOW());
```

---

## 3) Форматирование и парсинг

### 3.1 STR_TO_DATE(string, format) → строка → дата/время
```sql
SELECT STR_TO_DATE('20-11-2024', '%d-%m-%Y');
SELECT STR_TO_DATE('20-11-2024 15:30:00', '%d-%m-%Y %H:%i:%s');
```

### 3.2 DATE_FORMAT(datetime, format) → дата/время → строка
```sql
SELECT DATE_FORMAT(NOW(), '%d-%m-%Y %H:%i:%s');
SELECT DATE_FORMAT(NOW(), '%W, %d %M %Y %r') AS formatted_date;
```

---

## 4) Добавление/вычитание интервалов
### 4.1 DATE_ADD / DATE_SUB
```sql
SELECT DATE_ADD(NOW(), INTERVAL 7 DAY);
SELECT DATE_ADD(NOW(), INTERVAL 1 HOUR);

SELECT DATE_SUB(NOW(), INTERVAL 1 MONTH);
SELECT DATE_ADD(DATE_ADD(NOW(), INTERVAL 7 DAY), INTERVAL 2 MONTH);
```

### 4.2 Старые синонимы
```sql
SELECT ADDDATE(NOW(), INTERVAL 7 DAY);
SELECT SUBDATE('2011-01-01', INTERVAL 5 MONTH);
```

### 4.3 Синтаксис с `+ INTERVAL`
```sql
SELECT NOW() + INTERVAL 1 DAY;
SELECT NOW() + INTERVAL 1 DAY + INTERVAL 1 MONTH;
```

---

## 5) Разница между датами/временем

### 5.1 DATEDIFF(date1, date2) → разница **в днях**
> Важно: время **не учитывается**, даже если передать DATETIME.
```sql
SELECT DATEDIFF('2024-12-01', '2024-11-20');              -- 11
SELECT DATEDIFF('2024-11-19', '2024-11-20');              -- -1
SELECT DATEDIFF('2024-12-01 10:00:00', '2024-11-20 11:00:00');
```

### 5.2 TIMESTAMPDIFF(unit, datetime1, datetime2)
> Можно считать разницу в разных единицах: DAY/HOUR/MINUTE/SECOND и т.д.
```sql
SELECT TIMESTAMPDIFF(DAY,  '2024-11-10 10:00:00', NOW());
SELECT TIMESTAMPDIFF(HOUR, '2024-11-22 10:00:00', NOW());
SELECT TIMESTAMPDIFF(DAY,  '2024-11-20 11:00:00', '2024-12-01 10:00:00');
```

---

## 6) Часовые пояса (Time Zones)

### 6.1 Текущий таймзон сервера
```sql
SELECT @@global.time_zone;
```

### 6.2 CONVERT_TZ(datetime, from_tz, to_tz)
```sql
SELECT CONVERT_TZ(NOW(), '+00:00', '+04:00');
SELECT CONVERT_TZ(NOW(), 'UTC', '+04:00');
SELECT CONVERT_TZ(NOW(), 'UTC', 'Europe/Berlin');
SELECT CONVERT_TZ(NOW(), 'Europe/Berlin', '+04:00');
```

---

## 7) DATE_FORMAT — самые частые плейсхолдеры

### Дата
- `%Y` год (4 цифры), `%y` год (2 цифры)
- `%m` месяц (01–12), `%c` месяц (1–12)
- `%d` день (01–31), `%e` день (1–31)
- `%M` полное имя месяца, `%b` сокращение
- `%W` полное имя дня недели, `%a` сокращение
- `%j` день года (001–366)
- `%w` день недели (0=Вс ... 6=Сб)

### Время
- `%H` часы 24ч (00–23)
- `%h` / `%I` часы 12ч (01–12)
- `%i` минуты (00–59)
- `%s` / `%S` секунды (00–59)
- `%p` AM/PM
- `%r` время 12ч (hh:mm:ss AM/PM)
- `%T` время 24ч (hh:mm:ss)
- `%%` символ `%`

---

## 8) Мини-таблица “что чем делается”
```text
Тип: DATE          -> 'YYYY-MM-DD'
Тип: TIME          -> 'HH:MM:SS'
Тип: DATETIME      -> 'YYYY-MM-DD HH:MM:SS'

NOW(), CURRENT_TIMESTAMP()  -> текущая дата+время
CURDATE() / CURRENT_DATE    -> текущая дата
CURTIME() / CURRENT_TIME    -> текущее время

DATEDIFF(d1, d2)             -> разница в днях (время не учитывает)
TIMESTAMPDIFF(unit, d1, d2)  -> разница в нужных единицах
DATE_ADD / DATE_SUB          -> +/- интервалы
DATE_FORMAT                 -> datetime -> строка
STR_TO_DATE                 -> строка -> datetime
CONVERT_TZ                  -> перевод таймзон
```
