# Python Fundamentals — Урок 13: кортежи (`tuple`), упаковка/распаковка, `enumerate()`

## 1) Что такое кортеж (`tuple`)
**Кортеж** — упорядоченная **неизменяемая (immutable)** коллекция элементов.

Свойства:
- порядок сохраняется
- изменения “на месте” невозможны (нельзя добавить/удалить/заменить элемент)
- допускает дубликаты
- может содержать элементы разных типов
- поддерживает индексацию и срезы (как список)

---

## 2) Создание кортежей
### 2.1 Обычный кортеж
```py
my_tuple = (1, 2, 3, "apple", True)
```

### 2.2 Пустой кортеж
```py
empty_tuple = ()
```

### 2.3 Кортеж из одного элемента (ВАЖНО: запятая!)
Без запятой это **не кортеж**, а просто значение в скобках.
```py
t1 = (5,)   # tuple
t2 = (5)    # int
```

---

## 3) Доступ к элементам (индексы)
```py
my_tuple = (10, 20, 30, 40)

print(my_tuple[1])   # 20
print(my_tuple[-1])  # 40
```

---

## 4) Неизменяемость кортежей
Попытка изменения элемента даст `TypeError`:
```py
my_tuple = (10, 20, 30)
# my_tuple[1] = 40  # TypeError
```

Если нужно “изменить кортеж”:
- создаём **новый** кортеж (через конкатенацию/сборку)
- или временно переводим в список, меняем, и обратно

---

## 5) Операции с кортежами (как со списками)
```py
tuple1 = (1, 2)
tuple2 = (3, 4)

print(tuple1 + tuple2)  # (1, 2, 3, 4)  конкатенация
print(tuple1 * 3)       # (1, 2, 1, 2, 1, 2) повторение

my_tuple = (10, 20, 30)
print(20 in my_tuple)   # True  проверка элемента
print(len(my_tuple))    # 3     длина
```

Сравнение кортежей — **поэлементно** (лексикографически), как у списков:
```py
print((1, 2, 3) == (1, 2, 4))   # False
print((1, 2, 3) <  (1, 3, 0))   # True
```

---

## 6) Преобразования `tuple()` и `list()`
### 6.1 Список → кортеж
```py
my_list = [1, 2, 3]
my_tuple = tuple(my_list)
```

### 6.2 Кортеж → список
```py
my_tuple = (1, 2, 3)
my_list = list(my_tuple)
```

---

## 7) `for` с кортежами
Цикл `for` работает с кортежом так же, как со списком:
```py
my_tuple = (10, 20, 30, 40)
for item in my_tuple:
    print(item)
```

---

## 8) Упаковка и распаковка (packing / unpacking)
### 8.1 Упаковка (packing)
Если присваиваем несколько значений одной переменной — Python упакует их в кортеж:
```py
packed = 1, 2, 3
print(packed)        # (1, 2, 3)
print(type(packed))  # <class 'tuple'>
```

### 8.2 Распаковка (unpacking)
Если элементов столько же, сколько переменных:
```py
data = (1, 2, 3)
a, b, c = data
print(a, b, c)  # 1 2 3
```

⚠️ Если количество не совпадает — будет `ValueError`:
```py
data = (1, 2, 3)
# a, b = data      # ValueError: too many values to unpack
# a, b, c, d = data # ValueError: not enough values to unpack
```

### 8.3 Распаковка для `print`: оператор `*`
```py
numbers = [1, 2, 3, 4, 5]
print(numbers)     # [1, 2, 3, 4, 5]
print(*numbers)    # 1 2 3 4 5
```

### 8.4 “Звёздная” распаковка (сбор остатка в список)
Можно “собрать середину” в одну переменную:
```py
numbers = [1, 2, 3, 4, 5]
a, *other, b = numbers
print(a)      # 1
print(b)      # 5
print(other)  # [2, 3, 4]
```

### 8.5 Распаковка в цикле (очень удобно)
```py
pairs = [(1, "apple"), (2, "banana"), (3, "cherry")]
for number, fruit in pairs:
    print(f"Число: {number}, Фрукт: {fruit}")
```

---

## 9) `enumerate()` — индексы + значения
`enumerate()` добавляет счётчик при переборе коллекции.

Синтаксис:
```py
enumerate(iterable, start=0)
```

### 9.1 Посмотреть содержимое (преобразование в list)
```py
fruits = ["apple", "banana", "cherry"]
print(list(enumerate(fruits)))  # [(0, 'apple'), (1, 'banana'), (2, 'cherry')]
```

### 9.2 Индекс и элемент
```py
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
```

### 9.3 Изменить старт индекса
```py
languages = ("Python", "Java", "C++")
for index, lang in enumerate(languages, start=1):
    print(f"{index}: {lang}")
```

### 9.4 Редактирование списка по индексу
```py
numbers = [10, 20, 30, 40]
for index, value in enumerate(numbers):
    numbers[index] = value * 10
print(numbers)  # [100, 200, 300, 400]
```

### 9.5 Сравнение соседних элементов
```py
numbers = [10, 20, 15, 30, 25, 35]
for index, value in enumerate(numbers[:-1]):
    if value > numbers[index + 1]:
        print(f"{value} больше, чем {numbers[index + 1]}")
```

---

## 10) Методы кортежа (их мало)
Кортежи неизменяемы, поэтому методов немного — основные два:

### 10.1 `count(value)` — сколько раз встречается элемент
```py
my_tuple = (1, 2, 3, 2, 4, 2)
print(my_tuple.count(2))  # 3
```

### 10.2 `index(value, start=0, end=None)` — индекс первого вхождения
Если элемента нет — `ValueError`.
```py
my_tuple = (10, 20, 30, 20, 40)
print(my_tuple.index(20))      # 1
print(my_tuple.index(20, 2))   # 3 (ищем начиная с индекса 2)
```

---

## 11) Ответы на мини-тест (из урока)
1) `my_tuple = (1, 2, 3, 4, 5); print(my_tuple[2])` → **3**  
2) кортеж с одним элементом → **(5,)** и **tuple([5])**  
3) `my_tuple = (1, 2, 3); a, b = my_tuple` → **ошибка**  
4) `end=' '` в `print` внутри `enumerate` → всё на одной строке: `0: apple 1: banana 2: cherry`

---

## 12) Практическая работа (решения)

### 12.1 Кортеж уникальных (без новых коллекций)
```py
numbers = (1, 2, 3, 2, 1, 4, 5, 3, 6)

unique_numbers = tuple()
for num in numbers:
    if num not in unique_numbers:
        unique_numbers += (num,)

print("Уникальные элементы:", unique_numbers)
# (1, 2, 3, 4, 5, 6)
```

### 12.2 Элементы больше среднего
```py
numbers = (10, 15, 20, 25, 30)

average = sum(numbers) / len(numbers)

greater_than_avg = tuple()
for num in numbers:
    if num > average:
        greater_than_avg += (num,)

print("Элементы больше среднего:", greater_than_avg)
# (25, 30)
```

---

## 13) Домашнее задание (решения)

### 13.1 “Прогрессия увеличения”
Добавить только те элементы, которые **строго больше всех предыдущих**.
```py
numbers = (3, 7, 2, 8, 5, 10, 1)

result = tuple()
max_so_far = None

for x in numbers:
    if max_so_far is None or x > max_so_far:
        result += (x,)
        max_so_far = x

print("Кортеж по возрастанию:", result)
# (3, 7, 8, 10)
```

### 13.2 Повторяющиеся элементы: вывести индексы
Найти элементы, которые встречаются больше 1 раза, и вывести их индексы.
```py
numbers = (1, 2, 3, 4, 2, 5, 3, 6, 4, 2, 9)

reported = tuple()  # чтобы не печатать один и тот же элемент дважды

for i, x in enumerate(numbers):
    if x in reported:
        continue

    # собираем индексы
    indexes = []
    for j, y in enumerate(numbers):
        if y == x:
            indexes.append(j)

    if len(indexes) > 1:
        print(f"Индексы элемента {x}:", *indexes)
        reported += (x,)
```

---

## 14) Мини-шпаргалка
```text
tuple = упорядоченная неизменяемая коллекция

создание:
(1,2,3)   ()   (5,)   1,2,3  -> тоже tuple (packing)

операции:
+  *  in  len  сравнение (поэлементно)

преобразования:
tuple(list)  list(tuple)

распаковка:
a,b,c = (1,2,3)
a,*mid,b = [1,2,3,4,5]
print(*seq)

enumerate(seq, start=0):
for idx, val in enumerate(seq): ...

методы tuple:
count(x)
index(x, start=0, end=None)  (если нет x -> ValueError)
```
