# Python Fundamentals — Урок 29: генераторы (`yield`), бесконечные генераторы, `close()`, `yield from`

## 0) Что повторили в начале
- Итератор: `iter()` и `next()`, StopIteration  
- Как работает цикл `for` (он вызывает `next()` до StopIteration)  
- Модуль `itertools`  
- Генераторное выражение `( ... )`

---

## 1) Генератор: что это и зачем
**Генератор** — это специальный вид итератора, который создаёт элементы **по запросу**, не загружая всю последовательность в память.

### Основные особенности генераторов
- **Ленивые вычисления**: значения появляются только когда их запрашивают.
- **Экономия памяти**: не хранит всю последовательность.
- **Сохраняет состояние**: продолжает с того места, где остановился.
- Использует **`yield` вместо `return`**.

Генераторы особенно полезны для:
- обработки больших файлов,
- потоков данных,
- бесконечных последовательностей.

---

## 2) Как создают генераторы
### 2.1 Генераторные функции
Это функции, в которых есть `yield`:
```py
def gen():
    yield 1
    yield 2
```

### 2.2 Генераторные выражения
Короткая форма в круглых скобках:
```py
squares = (x*x for x in range(10))
```

---

## 3) Функция с `yield` и как она работает
Функция с `yield` **возвращает объект генератора**.  
Важно: при создании генератора код внутри функции **ещё не выполняется** — он начинает выполняться при первом `next()` или в `for`.

### Пример (логика “паузы” на `yield`)
```py
def generate_values():
    print("Начало работы")
    yield 1
    print("Продолжение работы")
    yield 2
    print("Завершение работы")

gen = generate_values()
print(next(gen))  # Начало работы -> 1
print(next(gen))  # Продолжение работы -> 2
print(next(gen))  # Завершение работы -> StopIteration
```

**Механика `yield`:**
1) первый `next()` запускает функцию до первого `yield`, значение возвращается наружу;  
2) следующий `next()` продолжает **с того же места**;  
3) после завершения функции → `StopIteration`.

---

## 4) Генераторные функции с параметрами
Аргументы передаются **один раз** при создании генератора и используются при генерации значений.

```py
def count_up_to(n):
    count = 1
    while count <= n:
        yield count
        count += 1

gen = count_up_to(5)
for x in gen:
    print(x)
```

---

## 5) Генератор в `for`
Генератор можно перебирать в `for`, как и любой итератор: `for` сам вызывает `next()` до `StopIteration`.

---

## 6) Бесконечные генераторы
**Бесконечный генератор** никогда сам не завершится (обычно `while True`). Его обязательно останавливают вручную.

### Пример: бесконечный счётчик
```py
def infinite_counter():
    count = 1
    while True:
        yield count
        count += 1

gen = infinite_counter()

# Останавливаем вручную
for n in gen:
    if n > 5:
        break
    print(n)
```

### Пример: циклическое распределение задач
```py
def task_assigner(employees):
    while True:
        for employee in employees:
            yield employee

team = ["Alice", "Bob", "Charlie"]
assigner = task_assigner(team)

for i in range(7):
    print(f"Task {i+1} assigned to: {next(assigner)}")
```

---

## 7) Метод `close()` у генератора
`close()` **принудительно завершает** генератор. После этого следующий `next()` вызовет `StopIteration`.

```py
def sensor_data(data):
    for v in data:
        yield v

numbers = [10, 20, 30, 40, 50]
gen = sensor_data(numbers)

for x in gen:
    print("Получено:", x)
    if x >= 30:
        print("Значение найдено, закрываем генератор.")
        gen.close()
        break
```

---

## 8) `yield from` (делегирование)
`yield from iterable` передаёт элементы из другого генератора или итерируемого объекта, упрощая “вложенные” генераторы.

### Пример 1: итерируемый объект
```py
def letters():
    yield from "ABC"

gen = letters()
print(next(gen))  # A
print(next(gen))  # B
print(next(gen))  # C
```

### Пример 2: вспомогательный генератор
```py
def process_values(data):
    for value in data:
        yield value * 2

def main_generator(*sequences):
    for seq in sequences:
        yield from process_values(seq)

data1 = [1, 2, 3]
data2 = [10, 15]
for result in main_generator(data1, data2):
    print(result)
```

---

# Задания для закрепления — ответы

## Задание 1 (countdown)
```py
def countdown(n):
    while n > 0:
        yield n
        n -= 1

gen = countdown(3)
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
```
Ответ: **3, 2, 1, StopIteration** (вариант **d**).

## Задание 2 (про `yield`)
Верные утверждения: **a, c, d**
- `yield` приостанавливает выполнение и запоминает состояние ✅
- генератор можно использовать только один раз ✅ (после исчерпания он пуст)
- `yield` используется только внутри функции ✅

## Задание 3 (про `yield from`)
Верные утверждения: **a, c, d**
- делегирует управление другому генератору ✅
- может передавать элементы из списка ✅
- упрощает вложенные генераторы ✅

---

# Практическая работа — решения

## 1) Фильтр чисел: кратные 5
```py
def filter_by_five(numbers):
    for num in numbers:
        if num % 5 == 0:
            yield num

numbers = [12, 15, 33, 40, 55, 62, 75, 83, 90]
for x in filter_by_five(numbers):
    print(x)
```

## 2) Квадраты чисел от 1 до n
```py
def square_numbers(n):
    for num in range(1, n + 1):
        yield num ** 2

for s in square_numbers(10):
    print(s)
```

---

# Домашнее задание — решения

## ДЗ 1) Бесконечный генератор Фибоначчи
Фибоначчи: 0, 1, 1, 2, 3, 5, ...

```py
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

gen = fibonacci()
for _ in range(10):
    print(next(gen))
```

## ДЗ 2) Генератор уникальных элементов (с сохранением порядка)
```py
def unique_in_order(data):
    seen = set()
    for x in data:
        if x not in seen:
            seen.add(x)
            yield x

data = [3, 1, 2, 3, 4, 1, 5, 2, 6, 7, 5, 8]
for x in unique_in_order(data):
    print(x)
```

---

## Мини-шпаргалка
```text
Генератор = итератор, который “лениво” выдаёт значения по запросу.

yield:
- возвращает значение и “замораживает” выполнение функции
- следующий next() продолжает с места остановки
- после окончания -> StopIteration

Бесконечные генераторы:
- while True
- останавливать вручную (break, close)

close():
- принудительно завершает генератор
- следующий next() -> StopIteration

yield from iterable:
- передаёт элементы из iterable/другого генератора
- упрощает вложенные генераторы
```
