# Множественное наследование миксины MRO

## План занятия
- Множественное наследование (Multiple Inheritance)
- `hasattr()`
- Миксины (Mixins)
- Порядок поиска методов при наследовании
- MRO (Method Resolution Order) и `__mro__`
- `super()` в множественном наследовании
- Композиция и агрегация (+ вложенные классы как композиция)

---

## 1) Множественное наследование
**Множественное наследование** — класс наследует сразу от нескольких родителей. 

Синтаксис:
```py
class Child(Parent1, Parent2):
    pass
```

Пример:
```py
class Printable:
    def print_info(self):
        print("Печать информации...")

class Savable:
    def save(self):
        print("Сохраняем в файл...")

class Report(Printable, Savable):
    pass

r = Report()
r.print_info()  # из Printable
r.save()        # из Savable
```

Особенности:
- порядок перечисления родителей **имеет значение** (слева направо),
- если имена методов совпадают — будет выбран метод согласно порядку разрешения (MRO). 

---

## 2) `hasattr()` — проверка наличия атрибута
`hasattr(obj, "name")` → `True`, если атрибут существует, иначе `False`. 

```py
class User:
    def __init__(self, username):
        self.username = username

user = User("Alice")
print(hasattr(user, "username"))  # True
print(hasattr(user, "email"))     # False
```

Где полезно:
- в миксинах/декораторах, чтобы проверить, “поддерживает ли” объект нужное поведение,
- при динамическом добавлении полей,
- когда объекты могут иметь разную структуру. 

---

## 3) Миксины (Mixin)
**Миксин** — вспомогательный класс, дающий дополнительное поведение через множественное наследование. 

Признаки миксина:
- обычно **без состояния** (часто нет `__init__`),
- содержит 1–несколько полезных методов,
- используется только вместе с другими классами,
- имя часто заканчивается на `Mixin` (например `AuthMixin`). 

Пример (2 миксина + проверка через `hasattr`):
```py
class AuthMixin:
    def login(self):
        if not hasattr(self, "username"):
            raise AttributeError("Не задан username")
        print(f"{self.username} вошёл в систему.")

    def logout(self):
        print("Пользователь вышел из системы.")


class NotificationMixin:
    def send_email(self, message):
        if not hasattr(self, "email"):
            raise AttributeError("Не задан email")
        print(f"Отправка письма на {self.email}: {message}")


class UserProfile(AuthMixin, NotificationMixin):
    def __init__(self, username, email):
        self.username = username
        self.email = email


user = UserProfile("alice", "alice@example.com")
user.login()
user.send_email("Добро пожаловать!")
user.logout()
```

---

## 4) Порядок поиска методов + “проблема ромба”
Когда вызывается `obj.method()` Python ищет метод по цепочке наследования. В множественном наследовании появляется “**diamond problem**” (проблема ромба): два родителя могут вести к общему предку. 

Пример поиска:
```py
class A:
    def greet(self):
        print("Hello from A")

class B(A):
    pass

class C:
    def greet(self):
        print("Hello from C")

class D(B, C):
    pass

d = D()
d.greet()  # найдёт greet в A (через B), до C уже не дойдёт
```

---

## 5) MRO (Method Resolution Order)
Чтобы порядок поиска был однозначным, Python использует **MRO** — порядок разрешения методов. 

Как посмотреть MRO:
```py
print(ClassName.__mro__)  # кортеж классов в порядке поиска
``` 

Пример:
```py
class A:
    def greet(self): print("A")

class B(A):
    def greet(self): print("B")

class C(A):
    def greet(self): print("C")

class D(B, C):
    def greet(self): print("D")

print(D.__mro__)
```
Вывод покажет порядок, в котором Python будет искать методы/атрибуты.

---

## 6) `super()` в множественном наследовании
В множественном наследовании `super()` особенно важен: он вызывает **следующий метод в цепочке MRO**, а не “конкретного родителя”. 

Плохо (жёсткая привязка, MRO не учитывается):
```py
ParentClass.method(self)
```
Хорошо (учитывает MRO):
```py
super().method()
``` 

Пример “цепочки вызовов” через `super()`:
```py
class A:
    def action(self):
        print("A")

class B(A):
    def action(self):
        print("B")
        super().action()

class C(A):
    def action(self):
        print("C")
        super().action()

class D(B, C):
    def action(self):
        print("D")
        super().action()

d = D()
d.action()  # вызовы пройдут в порядке MRO
``` 

---

## 7) Композиция и агрегация
Это способы строить отношения “объект содержит другой объект”. 

### 7.1 Композиция (сильная связь)
Внутренний объект **создаётся внутри** внешнего и полностью зависит от него. 
```py
class ExitButton:
    def click(self):
        print("Выход из программы")

class Menu:
    def __init__(self):
        self.exit_button = ExitButton()  # создаётся внутри (композиция)

    def show(self):
        print("Меню открыто")
        self.exit_button.click()

menu = Menu()
menu.show()
```

### 7.2 Агрегация (слабее связь)
Вложенный объект **создаётся снаружи** и передаётся внешнему, может жить отдельно. 
```py
class University:
    def __init__(self, name):
        self.name = name

    def get_info(self):
        print(f"Обучение проходит в университете: {self.name}")

class Teacher:
    def __init__(self, name, university):
        self.name = name
        self.university = university  # пришёл извне (агрегация)

    def introduce(self):
        print(f"Преподаватель: {self.name}")
        self.university.get_info()

uni = University("Tech University")
t1 = Teacher("Anna", uni)
t2 = Teacher("Dmitry", uni)
t1.introduce()
t2.introduce()
```

### 7.3 Вложенные классы как композиция
Иногда класс логически “часть” другого — удобно определить его внутри. Это тоже композиция (внешний класс создаёт и контролирует внутренний). 
```py
class Smartphone:
    class Battery:
        def __init__(self, capacity):
            self.capacity = capacity
            self.charge = capacity

        def use(self, amount):
            self.charge = max(self.charge - amount, 0)
            print(f"Батарея: {self.charge}/{self.capacity} мАч")

    def __init__(self, model, battery_capacity):
        self.model = model
        self.battery = self.Battery(battery_capacity)

    def play_video(self):
        print(f"{self.model} воспроизводит видео...")
        self.battery.use(300)

phone = Smartphone("Pixel 9", 4000)
phone.play_video()
```

---

# Ответы на задания (из урока)

## Закрепление 1: порядок поиска метода
Код (D(B, C), а B и C наследуют от A, при этом greet определён в C):
Порядок: **D → B → C → A → object**. 

## Закрепление 2
1) Для чего `super()` в наследовании? → **b** (гибко переходить к следующему методу в MRO).   
2) Что выведет:
```py
class SaveMixin:
    def process(self): print("Saving...")
class PrintMixin:
    def process(self): print("Printing...")
class Document(SaveMixin, PrintMixin):
    pass
Document().process()
```
Ответ: **Saving...** (левый родитель первый по MRO). 

## Закрепление 3
1) Композиция/Агрегация/Вложенный класс → **1-b, 2-c, 3-a**.   
2) Какая связь?
```py
class Course:
    def __init__(self, teacher):
        self.teacher = teacher
```
Ответ: **агрегация (b)** — `teacher` приходит извне. 

---

# Практическая работа — решения

## 1) `Student`
Требования: имя+email, `__str__` (например имя), `notify(message)` печатает: `Email to <email>: <message>` 
```py
class Student:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return self.name

    def notify(self, message):
        print(f"Email to {self.email}: {message}")


s = Student("Alice", "alice@example.com")
print(s)
s.notify("You have been enrolled.")
```

## 2) `Course`
Требования: title, список `students`, методы `add_student`, `show_students`, `notify_all`. 
```py
class Course:
    def __init__(self, title):
        self.title = title
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def show_students(self):
        print(f"Students enrolled in {self.title}:")
        for student in self.students:
            print("-", student)

    def notify_all(self, message):
        for student in self.students:
            student.notify(message)


s1 = Student("Alice", "alice@example.com")
s2 = Student("Bob", "bob@example.com")

course = Course("Python OOP")
course.add_student(s1)
course.add_student(s2)
course.show_students()
course.notify_all("Welcome to the course!")
```

---

# Домашнее задание — решения

## ДЗ 1) `AudioFileMixin` и `VideoFileMixin`
Требования:
- `AudioFileMixin` требует поле `audio_tracks` (список), метод `play_audio()`
- `VideoFileMixin` требует поле `video_files` (список), метод `play_video()`
- если нужного поля нет → `AttributeError`. 

```py
class AudioFileMixin:
    def play_audio(self):
        if not hasattr(self, "audio_tracks"):
            raise AttributeError("Не задан audio_tracks")
        print(f"Воспроизведение аудио для {self.__class__.__name__}:")
        for track in self.audio_tracks:
            print(track)


class VideoFileMixin:
    def play_video(self):
        if not hasattr(self, "video_files"):
            raise AttributeError("Не задан video_files")
        print(f"Воспроизведение видео для {self.__class__.__name__}:")
        for video in self.video_files:
            print(video)
```

## ДЗ 2) Устройства: `MediaPlayer` и `Laptop`
Требования:
- `MediaPlayer` поддерживает только аудио (принимает список треков),
- `Laptop` поддерживает аудио и видео (два списка). 

```py
class MediaPlayer(AudioFileMixin):
    def __init__(self, audio_tracks):
        self.audio_tracks = audio_tracks


class Laptop(AudioFileMixin, VideoFileMixin):
    def __init__(self, audio_tracks, video_files):
        self.audio_tracks = audio_tracks
        self.video_files = video_files


mp = MediaPlayer(["track1.mp3", "track2.mp3"])
mp.play_audio()

lap = Laptop(["song.mp3"], ["movie.mp4", "clip.mov"])
lap.play_audio()
lap.play_video()
```

---

## Мини-шпаргалка урока
```text
Multiple inheritance:
class X(A, B): ...

hasattr(obj, "attr") -> True/False

Mixins:
- без состояния (часто без __init__)
- добавляют поведение
- имя *Mixin

MRO:
Class.__mro__ -> порядок поиска методов

super() в MI:
super().method() -> следующий метод по MRO

Композиция:
внешний объект создаёт и “владеет” внутренним

Агрегация:
внешний объект получает готовый внутренний извне
```
