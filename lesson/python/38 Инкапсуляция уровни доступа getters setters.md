# Инкапсуляция уровни доступа getters setters

## 📖 Быстрая навигация по операторам и функциям

- [Инкапсуляция — что это и зачем](#1-инкапсуляция-что-это-и-зачем)
- [Уровни доступа в Python (это соглашения, а не “запрет”)](#2-уровни-доступа-в-python-это-соглашения-а-не-запрет)
- [Манглирование имён (name mangling)](#3-манглирование-имён-name-mangling)
- [Защищённые и приватные методы](#4-защищённые-и-приватные-методы)
- [Геттеры и сеттеры (ручной стиль)](#5-геттеры-и-сеттеры-ручной-стиль)
- [`@property`: “красивый” интерфейс без get/set в названии](#6-property-красивый-интерфейс-без-getset-в-названии)

**[📚 Дополнительная информация и примеры](#дополнительная-информация)**


## План урока
- Инкапсуляция
- Уровни доступа в Python: public / protected / private
- Защищённые и приватные **методы**
- Манглирование имён (name mangling)
- Геттеры и сеттеры (ручной стиль)
- Декоратор `@property` (свойства), read-only свойства
- Практика: SecureUSB
- ДЗ: BankAccount + история операций

---

## 1) Инкапсуляция — что это и зачем
**Инкапсуляция** — подход, при котором внутреннее устройство объекта скрывается, а взаимодействие происходит через понятный и контролируемый интерфейс.

Что даёт:
- защита данных от случайных изменений,
- контроль поведения через ограниченные “точки входа”,
- удобное использование объекта без знания внутренней структуры.

---

## 2) Уровни доступа в Python (это соглашения, а не “запрет”)
В Python нет жёстких модификаторов доступа как в Java/C#, поэтому используются **соглашения по именованию**:

### 2.1 Public (публичные) — без подчёркиваний
- доступны везде (чтение/запись),
- это часть “официального” интерфейса класса.

```py
class Book:
    def __init__(self, title, author):
        self.title = title     # public
        self.author = author   # public

book = Book("1984", "George Orwell")
print(book.title)
book.title = "Animal Farm"
```

### 2.2 Protected (защищённые) — одно подчёркивание `_name`
- **можно** обратиться извне, но это сигнал: “внутренняя деталь реализации”,
- корректно использовать внутри класса и в наследниках.

```py
class Book:
    def __init__(self, title):
        self._title = title  # protected

class SpecialBook(Book):
    def loud_title(self):
        return self._title.upper()
```

### 2.3 Private (приватные) — два подчёркивания `__name`
- предназначены только для использования **внутри класса**,
- “скрытие” реализовано через **механизм mangling**, а не реальный запрет.

```py
class Book:
    def __init__(self, title):
        self.__title = title  # private

    def show_title(self):
        print(self.__title)
```

---

## 3) Манглирование имён (name mangling)
Если атрибут начинается с `__` и **не заканчивается** `__`, Python преобразует имя:
- `__value` → `_ClassName__value`

Пример:
```py
class Book:
    def __init__(self, title):
        self.__title = title

book = Book("Brave New World")
# print(book.__title)          # AttributeError
print(book._Book__title)       # технически возможно, но делать так НЕ рекомендуется
```

Идея mangling:
- уменьшить шанс случайных конфликтов имён в наследниках,
- затруднить “случайный” доступ извне,
- при этом оставляя возможность для отладки (в крайних случаях).

---

## 4) Защищённые и приватные методы
### 4.1 Protected methods: `_method()`
Используются, когда:
- часть логики нужно вынести в отдельный метод,
- метод не предназначен для внешнего вызова,
- но может быть расширен в наследниках.

Пример (подготовка данных):
```py
class Report:
    def __init__(self, data):
        self.data = data

    def generate(self):
        cleaned = self._prepare_data()
        print("Отчёт:")
        print("\n".join(cleaned))

    def _prepare_data(self):
        return [line.strip() for line in self.data if line.strip()]


class SalesReport(Report):
    def _prepare_data(self):
        raw = super()._prepare_data()
        return [line for line in raw if not line.startswith("#")]
```

### 4.2 Private methods: `__method()`
Используются, когда:
- логику нужно строго спрятать,
- не хотите, чтобы метод вызывали извне,
- и не хотите, чтобы наследники переопределяли его случайно.

```py
class User:
    def __init__(self, name):
        self.name = name
        self.__id = self.__generate_id()

    def show_info(self):
        print(f"{self.name} — ID: {self.__id}")

    def __generate_id(self):
        from random import randint
        return f"user-{randint(1000, 9999)}"
```

---

## 5) Геттеры и сеттеры (ручной стиль)
Когда поле приватное, доступ обычно делают через методы:
- **getter** — прочитать значение,
- **setter** — изменить значение (часто с валидацией).

Пример:
```py
class Temperature:
    def __init__(self):
        self.__celsius = 0

    def get_celsius(self):
        return self.__celsius

    def set_celsius(self, value):
        if value < -273.15:
            raise ValueError("Температура не может быть ниже абсолютного нуля")
        self.__celsius = value

temp = Temperature()
temp.set_celsius(25)
print(temp.get_celsius())
```

Чтобы не дублировать валидацию, её удобно вынести в отдельный приватный метод:
```py
class Temperature:
    def __init__(self, value):
        self.__validate_celsius(value)
        self.__celsius = value

    def get_celsius(self):
        return self.__celsius

    def set_celsius(self, value):
        self.__validate_celsius(value)
        self.__celsius = value

    @staticmethod
    def __validate_celsius(value):
        if value < -273.15:
            raise ValueError("Температура не может быть ниже абсолютного нуля")
```

---

## 6) `@property`: “красивый” интерфейс без get/set в названии
`@property` позволяет обращаться к методам как к обычным атрибутам:
- `obj.value` вместо `obj.get_value()`,
но при этом сохраняет контроль (валидация/логика).

Шаблон:
```py
class MyClass:
    def __init__(self, value):
        self.__attr = value

    @property
    def attr(self):          # getter
        return self.__attr

    @attr.setter
    def attr(self, value):   # setter
        self.__attr = value
```

Пример с валидацией:
```py
class Temperature:
    def __init__(self, value):
        self.__celsius = 0
        self.celsius = value  # вызов setter

    @property
    def celsius(self):
        return self.__celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Температура не может быть ниже абсолютного нуля")
        self.__celsius = value
```

### Read-only свойства (только чтение)
Если нужен атрибут “только для чтения” — создаём только getter:
```py
class Temperature:
    def __init__(self, celsius):
        self.__celsius = celsius

    @property
    def celsius(self):
        return self.__celsius

    @property
    def fahrenheit(self):
        return self.__celsius * 9 / 5 + 32
```

---

# Задания для закрепления — ответы

## Задание 1: ошибка в `Book.show_title`
Было:
```py
def show_title(self):
    print(__title)
```
Правильно:
```py
def show_title(self):
    print(self.__title)
```

## Задание 1: верные утверждения про уровни доступа
Верные: **a, d**
- a) публичные атрибуты доступны везде ✅
- d) защищённые атрибуты могут использоваться в дочерних классах ✅

## Задание 2: ошибка в `@property`
Было (ошибка в названии getter):
```py
@property
def __celsius(self):
    return self.__celsius
```
Правильно:
```py
@property
def celsius(self):
    return self.__celsius
```

---

# Практическая работа — решения

## 1) SecureUSB: безопасная флешка (read + lock/unlock)
Требования:
- передаётся секретное содержимое и пароль,
- `unlock(password)` → True/False и разблокировка при успехе,
- `lock()` блокирует,
- `read()` возвращает данные только если разблокировано, иначе `PermissionError`.

```py
class SecureUSB:
    def __init__(self, secure_data, password):
        self.__secure_data = secure_data
        self.__password = password
        self.__locked = True

    def unlock(self, password):
        if password == self.__password:
            self.__locked = False
            return True
        return False

    def lock(self):
        self.__locked = True

    def read(self):
        if self.__locked:
            raise PermissionError("Device is locked. Access denied.")
        return self.__secure_data


usb = SecureUSB("Secret plans", "qwerty")

try:
    print(usb.read())
except PermissionError as e:
    print(e)

if not usb.unlock("1234"):
    print("Access denied.")

if usb.unlock("qwerty"):
    print("Access granted.")

print("Data:", usb.read())
```

## 2) SecureUSB: доступ через свойство `data` (`@property`)
Требования: вместо `read()` используем `usb.data`.

```py
class SecureUSB:
    def __init__(self, secure_data, password):
        self.__secure_data = secure_data
        self.__password = password
        self.__locked = True

    def unlock(self, password):
        if password == self.__password:
            self.__locked = False
            return True
        return False

    def lock(self):
        self.__locked = True

    @property
    def data(self):
        if self.__locked:
            raise PermissionError("Device is locked. Access denied.")
        return self.__secure_data


usb = SecureUSB("Secret plans", "qwerty")
try:
    print(usb.data)
except PermissionError as e:
    print(e)

if usb.unlock("qwerty"):
    print("Access granted.")
print("Data:", usb.data)
```

---

# Домашнее задание — решения

## ДЗ 1) BankAccount: владелец, баланс, пополнение/снятие/показ баланса
Идея инкапсуляции:
- имя владельца можно оставить публичным (`owner`),
- баланс и историю операций лучше скрыть (`__balance`, `__history`),
- изменение баланса только через методы.

```py
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount <= 0:
            print("Error: Amount must be positive.")
            return
        self.__balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            print("Error: Amount must be positive.")
            return
        if amount > self.__balance:
            print("Error: Not enough funds.")
            return
        self.__balance -= amount

    def show_balance(self):
        print(f"Current balance: {self.__balance}")


acc = BankAccount("Viktor", 0)
acc.deposit(150)
acc.show_balance()
acc.withdraw(-10)
acc.show_balance()
acc.withdraw(1000)
acc.show_balance()
```

## ДЗ 2) История операций (read-only `history` через property)
Требования:
- каждое пополнение/снятие пишет запись в историю,
- `history` доступна только для чтения,
- формат: `"Deposit: 150"`, `"Withdraw: 100"`.

```py
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance
        self.__history = []

    def deposit(self, amount):
        if amount <= 0:
            print("Error: Amount must be positive.")
            return
        self.__balance += amount
        self.__history.append(f"Deposit: {amount}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Error: Amount must be positive.")
            return
        if amount > self.__balance:
            print("Error: Not enough funds.")
            return
        self.__balance -= amount
        self.__history.append(f"Withdraw: {amount}")

    def show_balance(self):
        print(f"Current balance: {self.__balance}")

    @property
    def history(self):
        # возвращаем копию, чтобы снаружи нельзя было “испортить” список
        return list(self.__history)


acc = BankAccount("Viktor")
acc.deposit(150)
acc.withdraw(100)
acc.show_balance()

print("Operation history:")
for item in acc.history:
    print(item)
```

---

## Мини-шпаргалка урока
```text
public:    name
protected: _name        # “не трогать снаружи” (соглашение)
private:   __name       # name mangling -> _ClassName__name

getter/setter (старый стиль):
get_x(), set_x(value)

property стиль:
@property
def x(self): ...
@x.setter
def x(self, value): ...

read-only property:
@property
def x(self): ...   # без setter
```


---

## 📚 Дополнительная информация

_Этот раздел будет дополнен практическими примерами и дополнительной информацией._
