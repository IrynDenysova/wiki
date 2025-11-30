# Python Fundamentals — Урок 25: исключения (exceptions), обработка ошибок, `raise`, логирование (`logging`)

> Цель урока: научиться **не “ронять” программу**, а корректно обрабатывать ошибки, давать понятные сообщения пользователю и **логировать** проблемы для отладки.

---

## 1) Что такое исключения
**Исключения (Exceptions)** — события/ошибочные ситуации во время выполнения программы, которые:
- сигнализируют о проблеме,
- могут быть **обработаны**, чтобы программа продолжила работу.

Примеры типичных исключений:
- `ZeroDivisionError`: деление на ноль (`10 / 0`)
- `ValueError`: неверное значение / формат (`int("abc")`)
- `KeyError`: нет ключа в словаре (`d["missing"]`)
- `IndexError`: индекс вне диапазона (`lst[999]`)
- `TypeError`: неверный тип (`"1" + 2`)
- `FileNotFoundError`: файл не найден

### Зачем обрабатывать исключения
- **Стабильность**: программа не падает из‑за одной ошибки.
- **UX**: свои сообщения вместо traceback.
- **Отладка**: ошибки фиксируются и проще анализируются.

---

## 2) Как Python реагирует на ошибку
Когда ошибка возникает:
1) создаётся **объект исключения**, содержащий:
   - тип исключения,
   - сообщение,
   - **traceback** (где именно упало).
2) если исключение не обработано — выполнение прекращается и выводится traceback.

---

## 3) Иерархия исключений (важно понимать)
- всё наследуется от `BaseException`
- для обработки “обычных” ошибок чаще используем ветку `Exception`
- есть исключения, которые обычно **не ловят** “как обычные”: `SystemExit`, `KeyboardInterrupt`, `GeneratorExit`

Практическая мысль:
- ловите **конкретные** исключения (например `ValueError`), а не всё подряд.

---

## 4) Базовая конструкция `try-except`
```py
try:
    # код, который может вызвать исключение
except SomeError:
    # код, который выполнится при исключении
```

### Пример
```py
try:
    result = 10 / 0
    print("Не дойдём сюда при ошибке")
except ZeroDivisionError:
    print("Ошибка: деление на ноль!")
```

---

## 5) Как Python выбирает обработчик `except`
Python проверяет `except` **сверху вниз** и выполняет **первый подходящий**.

✅ Правильно (от частного к общему):
```py
try:
    x = 10 / 0
except ZeroDivisionError:
    print("Деление на ноль")
except Exception:
    print("Что-то другое")
```

❌ Неправильно (общий обработчик “съест” всё):
```py
try:
    x = 10 / 0
except Exception:
    print("Общее исключение")
except ZeroDivisionError:
    print("Этот код недостижим")
```

---

## 6) Обработка нескольких исключений в одном блоке
Можно указать кортеж типов:
```py
while True:
    try:
        user_input = input("Введите ненулевое число: ")
        result = 10 / int(user_input)
        print(f"Результат: {result}")
        break
    except (ZeroDivisionError, ValueError):
        print("Ошибка! Введите корректное ненулевое число.")
```

### Получить текст ошибки (`as e`)
```py
try:
    number = int("abc")
except ValueError as e:
    print(f"Произошла ошибка: {e}")
```

---

## 7) `try-except-else` (удобно разделяет логику)
`else` выполняется **только если в try не было исключения**.

```py
try:
    number = int(input("Введите число: "))
except ValueError:
    print("Ошибка! Введите корректное число.")
else:
    print(f"Вы ввели число: {number}")
```

**Лучшие практики:** в `try` кладём **только то**, что реально может упасть. Так проще читать и дебажить.

---

## 8) `try-except-finally`
`finally` выполняется **всегда**, была ошибка или нет. Используется для “закрытия” ресурсов.

```py
try:
    number = int(input("Введите число: "))
    result = 10 / number
except ValueError:
    print("Ошибка! Введите корректное число.")
except ZeroDivisionError:
    print("Ошибка! Деление на ноль.")
finally:
    print("Завершение программы.")
```

---

## 9) `try-except-else-finally` (всё вместе)
```py
try:
    number = int(input("Введите число: "))
    result = 10 / number
except ValueError:
    print("Ошибка: введено некорректное значение.")
except ZeroDivisionError:
    print("Ошибка: деление на ноль.")
else:
    print(f"Результат деления: {result}")
finally:
    print("Программа завершена.")
```

---

## 10) Возбуждение исключений вручную: `raise`
`raise` позволяет явно сообщить об ошибке, когда вы сами обнаружили неверное состояние.

Синтаксис:
```py
raise ExceptionType("Сообщение об ошибке")
```

Пример:
```py
number = -1
if number < 0:
    raise ValueError("Число не может быть отрицательным")
```

После `raise`:
- либо перехватываем ошибку `try-except`,
- либо даём программе завершиться с traceback (иногда это нормально).

Пример с повторным вводом:
```py
while True:
    try:
        number = int(input("Введите положительное число: "))
        if number < 0:
            raise ValueError("Число не может быть отрицательным")
        print(f"Вы ввели корректное число: {number}")
        break
    except ValueError as e:
        print(f"Ошибка: {e}. Попробуйте снова.")
```

---

## 11) Логирование (модуль `logging`)
**Логирование** — запись информации о работе программы (ошибки, предупреждения, отладка).

### 11.1 Уровни логирования
- `DEBUG` — отладка
- `INFO` — общая информация
- `WARNING` — предупреждения
- `ERROR` — ошибки (программа может продолжать)
- `CRITICAL` — критические ошибки

> По умолчанию выводятся сообщения уровня `WARNING` и выше.

Пример:
```py
import logging

logging.basicConfig()  # по умолчанию WARNING+
logging.debug("debug")     # не видно
logging.info("info")       # не видно
logging.warning("warn")    # видно
logging.error("error")     # видно
logging.critical("crit")   # видно
```

Чтобы видеть `DEBUG` и `INFO`:
```py
logging.basicConfig(level=logging.DEBUG)
```

### 11.2 Запись логов в файл
```py
import logging

logging.basicConfig(filename="app.log", level=logging.INFO)
logging.info("Программа запущена")
logging.warning("Низкий уровень памяти")
logging.error("Ошибка подключения к базе данных")
```

### 11.3 Логи внутри обработки исключений
```py
import logging

logging.basicConfig(filename="app.log", level=logging.ERROR)

try:
    result = 10 / 0
except ZeroDivisionError as e:
    logging.error(f"Ошибка: {e}")
```

### 11.4 Формат логов (`format=...`)
Полезные плейсхолдеры:
- `%(asctime)s` — время
- `%(levelname)s` — уровень
- `%(filename)s` — имя файла
- `%(lineno)d` — номер строки
- `%(message)s` — сообщение

Пример формата:
```py
import logging

logging.basicConfig(
    filename="app.log",
    format="%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s",
    level=logging.DEBUG
)

logging.debug("debug")
logging.info("info")
logging.warning("warning")
logging.error("error")
logging.critical("critical")
```

---

## 12) Лучшие практики обработки исключений
1) **Обрабатывайте только ожидаемые исключения** (конкретные типы).
2) **Минимизируйте код в `try`** — только то, что может упасть.
3) Используйте `finally` для освобождения ресурсов (файлы, соединения).
4) **Логируйте ошибки**, а не просто `print()`.

---

# Задания для закрепления (ответы)

### Задание 1
```py
try:
    x = 1 / 0
except Exception:
    print("Общее исключение")
except ZeroDivisionError:
    print("Ошибка деления на ноль")
```
Ответ: выведется **«Общее исключение»**, потому что `Exception` стоит раньше и перехватывает всё.

### Задание 2.1
Что делает `raise`?  
Ответ: **создаёт/возбуждает исключение**.

### Задание 2.2
```py
try:
    print("До исключения", end=" | ")
    raise ValueError("Ошибка!")
    print("После исключения", end=" | ")
except ValueError as e:
    print(f"Перехвачено исключение: {e}")
```
Ответ:  
`До исключения | Перехвачено исключение: Ошибка!`

### Задание 3
Что делает `filename="app.log"` в `logging.basicConfig()`?  
Ответ: **указывает файл**, в который записывать логи.

---

# Практическая работа (решения)

## 1) Ввод числа до тех пор, пока пользователь не введёт корректное
```py
def get_valid_number() -> float:
    while True:
        try:
            return float(input("Введите число: "))
        except ValueError:
            print("Ошибка: Введите корректное число.")

num = get_valid_number()
print(f"Вы ввели число: {num}")
```

## 2) Проверка возраста (>= 18) через `raise`
```py
def check_age() -> None:
    age = int(input("Введите возраст: "))
    if age < 18:
        raise ValueError("Ошибка: Возраст должен быть 18 лет и старше.")
    print("Возраст принят.")

try:
    check_age()
except ValueError as e:
    print(e)
```

---

# Домашнее задание (решения)

## ДЗ 1) Деление без ошибок (ввод пользователем)
Требования: обработать:
- некорректные числа (`ValueError`)
- деление на ноль (`ZeroDivisionError`)

```py
def safe_division() -> float:
    while True:
        try:
            a = float(input("Введите делимое: "))
            b = float(input("Введите делитель: "))
            return a / b
        except ValueError:
            print("Ошибка: Введено некорректное число.")
        except ZeroDivisionError:
            print("Ошибка: Деление на ноль запрещено.")

result = safe_division()
print(f"Результат: {result}")
```

## ДЗ 2) Логирование ошибок в `errors.log` (формат как в примере)
Пример ожидаемой строки:
`2025-02-23 22:38:53,686 - ERROR - test.py - 16 - Ошибка: ...`

Решение:
```py
import logging

logging.basicConfig(
    filename="errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
)

def safe_division_with_logging() -> float:
    while True:
        try:
            a = float(input("Введите делимое: "))
            b = float(input("Введите делитель: "))
            return a / b
        except ValueError as e:
            msg = f"Ошибка: Введено некорректное число. ({e})"
            print(msg)
            logging.error(msg)
        except ZeroDivisionError as e:
            msg = f"Ошибка: Деление на ноль запрещено. ({e})"
            print(msg)
            logging.error(msg)

print("Результат:", safe_division_with_logging())
```

---

## Мини-шпаргалка
```text
try:
    ...
except SpecificError as e:
    ...
except (E1, E2):
    ...
else:
    ...   # если ошибок не было
finally:
    ...   # всегда

raise ValueError("...")  # вызвать исключение вручную

logging.basicConfig(
  filename="app.log",
  level=logging.DEBUG,
  format="%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s"
)
logging.error("...")
```
