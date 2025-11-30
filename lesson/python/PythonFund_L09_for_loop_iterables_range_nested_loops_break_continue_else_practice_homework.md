# Python Fundamentals — Урок 9: цикл `for`, `range()`, `break/continue/else`, вложенные циклы

## 1) Повторение (из прошлого урока)
- строки неизменяемы (immutable)
- кодировки, `ord()` / `chr()`
- сравнение строк, `len()`
- индексация и срезы
- оператор принадлежности `in`

---

## 2) Итерируемый объект (iterable)
**Итерируемый объект** — это объект, который содержит множество элементов и может отдавать их **по одному**.

Примеры итерируемых объектов:
- строка (`"Python"`) — можно перебирать символы
- список, кортеж, множество, словарь
- `range(...)`

---

## 3) Цикл `for`: идея и синтаксис
`for` выполняет блок кода **для каждого элемента** последовательности/итерируемого объекта.

Синтаксис:
```py
for variable in sequence:
    # тело цикла
```

Что означает:
- `sequence` — итерируемый объект
- `variable` — переменная, которая **на каждой итерации** получает следующий элемент
- цикл заканчивается сам, когда элементы закончились

Пример (перебор строки):
```py
text = "Python"
for letter in text:
    print(letter)
```

### Пример с `end`
```py
text = "Hello"
for letter in text:
    print(letter, end="")
# вывод: Hello
```

---

## 4) `range()` — генератор диапазона чисел для `for`
`range()` создаёт последовательность чисел, по которой удобно идти в цикле.

Синтаксис:
```py
range(start, stop, step)
```

- `stop` (обязательный) — конечная граница (**не включается**)
- `start` (необязательный) — начальное значение (**включается**), по умолчанию `0`
- `step` (необязательный) — шаг, по умолчанию `1`

### 4.1 `range(stop)`
```py
for i in range(5):
    print(i)
# 0 1 2 3 4
```

### 4.2 `range(start, stop)`
```py
for i in range(2, 6):
    print(i)
# 2 3 4 5
```

### 4.3 `range(start, stop, step)`
```py
for i in range(1, 10, 2):
    print(i)
# 1 3 5 7 9
```

### 4.4 Отрицательный шаг
Если `step` отрицательный, обычно `start > stop`.
```py
for i in range(10, 0, -2):
    print(i)
# 10 8 6 4 2
```

---

## 5) `break`, `continue`, `else` в цикле `for`
В `for` эти операторы работают так же, как в `while`.

### 5.1 `break` — досрочно завершить цикл
```py
for letter in "Python":
    if letter == "h":
        break
    print(letter, end=" ")
# вывод: P y t
```

### 5.2 `continue` — пропустить текущую итерацию
```py
for letter in "Python":
    if letter == "h":
        continue
    print(letter, end=" ")
# вывод: P y t o n
```

### 5.3 `else` в `for`
`else` выполнится **только если цикл завершился нормально**, то есть **без `break`**.

```py
for letter in "Python":
    if letter == "a":
        break
    print(letter, end=" ")
else:
    print("Цикл завершён нормально.")
# вывода с break не будет, потому что "a" в строке нет → break не сработает
# значит будет: P y t h o n Цикл завершён нормально.
```

---

## 6) Вложенные циклы (nested loops)
**Вложенный цикл** — цикл внутри цикла.  
Внутренний цикл выполняется **полностью** для каждой итерации внешнего.

Синтаксис:
```py
for outer in outer_seq:
    for inner in inner_seq:
        ...
```

Пример:
```py
for i in "AB":
    for j in "12":
        print(i, j)
# A 1
# A 2
# B 1
# B 2
```

### Пример “часы:минуты”
```py
for hour in range(24):
    for minute in range(60):
        print("Время (часов:минут): ", hour, ":", minute, sep="")
```

---

## 7) Вложенные циклы `while + for` (комбинация)
Пример: вывести время на 3 часа вперёд, но не выходя за пределы суток.
```py
current_hours = int(input("Введите текущий час: "))
end_time = current_hours + 3

while current_hours < 24 and current_hours < end_time:
    for minutes in range(60):
        print("Время (часов:минут): ", current_hours, ":", minutes, sep="")
    current_hours += 1
```

---

## 8) Контрольные мини-вопросы (быстрые ответы)
### 8.1
```py
for i in range(5):
    print(i)
```
Ответ: `0 1 2 3 4` (каждое на новой строке)

### 8.2
```py
for i in range(1, 10, 2):
    print(i)
```
Ответ: `1 3 5 7 9`

### 8.3
```py
for i in range(10, 0, -2):
    print(i)
```
Ответ: `10 8 6 4 2`

### 8.4
```py
for i in range(3):
    for j in range(3):
        print(i + j, end=" ")
```
Ответ: `0 1 2 1 2 3 2 3 4`

---

## 9) Практическая работа (готовые решения)

### 9.1 Факториал (без `math`)
Факториал: `n! = 1 * 2 * ... * n`
```py
num = int(input("Введите число: "))
factorial = 1
for i in range(1, num + 1):
    factorial *= i
print("Факториал числа", num, "равен", factorial)
```

### 9.2 “Звёздный прямоугольник”
```py
width = int(input("Введите ширину: "))
height = int(input("Введите высоту: "))

for _ in range(height):
    for _ in range(width):
        print("*", end="")
    print()  # новая строка
```

### 9.3 Простое число (2 варианта)
**Базовый вариант** (проверка делителей от 2 до n-1):
```py
num = int(input("Введите число: "))
if num > 1:
    for i in range(2, num):
        if num % i == 0:
            print("Не является простым")
            break
    else:
        print("Является простым")
else:
    print("Не является простым")
```

**Оптимизированный** (проверка до `sqrt(n)`):
```py
num = int(input("Введите число: "))
if num > 1:
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            print("Не является простым")
            break
    else:
        print("Является простым")
else:
    print("Не является простым")
```

---

## 10) Домашнее задание (решения/шаблоны)

### 10.1 Таблица умножения 1..n (ровные столбцы)
Идея: использовать форматирование ширины, например `:4` (подстрой под своё n).

```py
n = int(input("Введите число: "))

for i in range(1, n + 1):
    for j in range(1, n + 1):
        print(f"{i*j:4}", end="")
    print()
```

### 10.2 “Лестница чисел”
```py
n = int(input("Введите число: "))

for i in range(1, n + 1):
    for j in range(1, i + 1):
        print(j, end=" ")
    print()
```

### 10.3 Удалить повторяющиеся символы (оставить первые вхождения)
Вариант 1 (через множество `seen`):
```py
s = input("Введите строку: ")

seen = set()
result = []

for ch in s:
    if ch not in seen:
        seen.add(ch)
        result.append(ch)

print("Результат:", "".join(result))
```

Вариант 2 (без set, но медленнее на длинных строках):
```py
s = input("Введите строку: ")
result = ""

for ch in s:
    if ch not in result:
        result += ch

print("Результат:", result)
```

---

## 11) Мини-шпаргалка
```text
for x in iterable:
    ...

range(stop) -> 0..stop-1
range(start, stop) -> start..stop-1
range(start, stop, step) -> с шагом step
отрицательный step -> идём назад, start обычно > stop

break    -> выйти из цикла
continue -> пропустить итерацию
else     -> выполнится, если не было break

вложенные циклы: внутренний выполняется полностью для каждого шага внешнего
```
