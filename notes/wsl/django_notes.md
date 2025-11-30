 у тебя есть Windows 10.

Ниже — **НОВАЯ версия** «сайт `notes` на WSL», с нуля до работающего сайта с шаблоном и заметками.

---

````markdown
# Django · Шпаргалка: сайт `notes` с шаблоном, полностью на WSL

Цель:  
1. Включить WSL и поставить Ubuntu.  
2. Создать Django-проект `notes` на WSL.  
3. Сделать приложение заметок с красивым Bootstrap-шаблоном.  
4. Запускать сайт из WSL, открывать в браузере Windows.

Итоговая структура:

```text
C:\Users\cp24\Documents\django\notes\
    .venv/              ← виртуальное окружение (WSL)
    manage.py
    db.sqlite3
    config/             ← Django-проект (settings, urls, wsgi)
    main/               ← приложение
    templates/
        base.html       ← базовый шаблон
        home.html       ← главная с заметками
````

---

## 0. Включаем WSL и ставим Ubuntu (делается один раз)

### 0.1. Включаем WSL в Windows

**Где:** PowerShell от имени администратора.

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
shutdown /r /t 0
```

> После этих команд компьютер перезагрузится.

Альтернатива:  
«Панель управления → Программы → Включение или отключение компонентов Windows» →  
поставить галочки:

- **Подсистема Windows для Linux**
    
- **Платформа виртуальной машины**
    

и перегрузить.

### 0.2. Устанавливаем Ubuntu из Microsoft Store

1. Открыть **Microsoft Store**.
    
2. Найти и установить **Ubuntu** (обычно «Ubuntu 22.04 LTS» или подобное).
    
3. Запустить Ubuntu через меню «Пуск».
    
4. Первый запуск:
    
    - подождать, пока всё развернётся;
        
    - придумать **username** и **password** для Linux (не влияет на Windows).
        

После этого у тебя есть терминал Ubuntu (WSL).

---

## 1. Создаём папку проекта на диске C: (через WSL)

**Где:** Ubuntu (WSL).

```bash
# Переходим в Documents на диске C:
cd /mnt/c/Users/cp24/Documents

# Папка для всех Django-проектов
mkdir -p django
cd django

# Папка конкретно под сайт notes
mkdir notes
cd notes
```

Теперь путь к проекту в Windows:

```text
C:\Users\cp24\Documents\django\notes
```

---

## 2. Виртуальное окружение и Django (всё в WSL)

### 2.1. Создаём виртуальное окружение `.venv`

**Где:** Ubuntu в папке проекта (`/mnt/c/Users/cp24/Documents/django/notes`):

```bash
python3 -m venv .venv
```

### 2.2. Активируем окружение

```bash
source .venv/bin/activate
```

> В начале строки появится `(.venv)`.

### 2.3. Ставим Django внутрь этого окружения

```bash
pip install django
python -m django --version   # проверка
```

---

## 3. Создаём Django-проект и приложение

### 3.1. Проект `config`

**Где:** Ubuntu, папка проекта + активный `.venv`.

```bash
django-admin startproject config .
```

Появятся файлы:

```text
notes/
    manage.py
    config/
```

### 3.2. Приложение `main`

```bash
python manage.py startapp main
```

Появится папка `main/`.

---

## 4. Регистрируем приложение `main` в настройках

**Файл:**  
`config/settings.py`  
(в Windows: `C:\Users\cp24\Documents\django\notes\config\settings.py`)

Найди список `INSTALLED_APPS` и добавь `'main',`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main',  # наше приложение заметок
]
```

Сохранить файл.

---

## 5. Модель заметки `Note`

**Файл:**  
`main/models.py`  
(`C:\Users\cp24\Documents\django\notes\main\models.py`)

Замени содержимое на:

```python
from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
        ordering = ["-created_at"]
```

Сохранить.

---

## 6. Миграции и база данных

**Где:** Ubuntu (WSL), в папке проекта.

```bash
cd /mnt/c/Users/cp24/Documents/django/notes
source .venv/bin/activate

python manage.py makemigrations
python manage.py migrate
```

После этого рядом с `manage.py` появится `db.sqlite3`.

---

## 7. Регистрируем `Note` в админке

**Файл:**  
`main/admin.py`  
(`C:\Users\cp24\Documents\django\notes\main\admin.py`)

Замени содержимое на:

```python
from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "text")
    list_filter = ("created_at",)
```

Сохранить.

---

## 8. Создаём суперпользователя

**Где:** Ubuntu (WSL).

```bash
cd /mnt/c/Users/cp24/Documents/django/notes
source .venv/bin/activate

python manage.py createsuperuser
```

Следовать вопросам в терминале (логин, почта, пароль).

---

## 9. Настраиваем папку `templates`

### 9.1. Создаём папку шаблонов

**Где:** Ubuntu:

```bash
cd /mnt/c/Users/cp24/Documents/django/notes
mkdir templates
```

(или создать папку `templates` через Проводник в Windows)

### 9.2. Говорим Django, где искать шаблоны

**Файл:**  
`config/settings.py`

Найди блок `TEMPLATES` и поменяй `DIRS`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← наша общая папка шаблонов
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Сохранить.

---

## 10. Базовый шаблон `base.html` (Bootstrap)

**Файл:**  
`templates/base.html`  
(`C:\Users\cp24\Documents\django\notes\templates\base.html`)

Создай файл и вставь:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Мой Django-сайт{% endblock %}</title>

    <!-- Bootstrap 5 по CDN -->
    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
        integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
        crossorigin="anonymous"
    >

    <style>
        body {
            background-color: #f5f5f7;
        }
        .navbar-brand {
            font-weight: 700;
            letter-spacing: 0.03em;
        }
        .main-wrapper {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .note-card {
            border-radius: 1rem;
            border: none;
            box-shadow: 0 8px 20px rgba(0,0,0,0.06);
        }
        .note-card .card-title {
            font-weight: 600;
        }
        .footer {
            font-size: 0.85rem;
            color: #777;
            padding: 1.5rem 0;
        }
    </style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
    <div class="container">
        <a class="navbar-brand" href="{% url 'home' %}">Django Notes</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbarNav" aria-controls="navbarNav"
                aria-expanded="false" aria-label="Переключить навигацию">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="{% url 'home' %}">
                        Главная
                    </a>
                </li>
            </ul>
        </div>
    </div>
</nav>

<main class="main-wrapper">
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</main>

<footer class="footer">
    <div class="container text-center">
        <span>Сайт на Django · {{ request.get_host }}</span>
    </div>
</footer>

<script
    src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
    crossorigin="anonymous"
></script>
</body>
</html>
```

Сохранить.

---

## 11. Главный шаблон `home.html` (список заметок)

**Файл:**  
`templates/home.html`  
(`C:\Users\cp24\Documents\django\notes\templates\home.html`)

Создай файл и вставь:

```html
{% extends "base.html" %}

{% block title %}Мои заметки · Django{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col-lg-8">
        <h1 class="mb-3">Привет, Виктор 👋</h1>
        <p class="text-muted mb-0">
            Это твой сайт на Django с красивым шаблоном и списком заметок из базы.
        </p>
    </div>
    <div class="col-lg-4 text-lg-end mt-3 mt-lg-0">
        <a href="/admin/" class="btn btn-outline-secondary">
            Перейти в админку
        </a>
    </div>
</div>

<hr class="mb-4">

<h2 class="h4 mb-3">Заметки</h2>

{% if notes %}
    <div class="row g-3">
        {% for note in notes %}
            <div class="col-md-6 col-lg-4">
                <div class="card note-card h-100">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title mb-2">{{ note.title }}</h5>
                        <p class="card-text text-muted small mb-2">
                            {{ note.created_at|date:"d.m.Y H:i" }}
                        </p>
                        <p class="card-text flex-grow-1">
                            {{ note.text|linebreaksbr }}
                        </p>
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
{% else %}
    <div class="alert alert-info">
        Пока нет ни одной заметки. Зайди в <a href="/admin/">админ-панель</a> и создай первую 🙂
    </div>
{% endif %}
{% endblock %}
```

Сохранить.

---

## 12. View для главной страницы

**Файл:**  
`main/views.py`  
(`C:\Users\cp24\Documents\django\notes\main\views.py`)

Замени содержимое на:

```python
from django.shortcuts import render
from .models import Note


def home(request):
    notes = Note.objects.all()
    return render(request, "home.html", {"notes": notes})
```

Сохранить.

---

## 13. Маршруты (`urls.py`)

**Файл:**  
`config/urls.py`  
(`C:\Users\cp24\Documents\django\notes\config\urls.py`)

Сделай так:

```python
from django.contrib import admin
from django.urls import path
from main.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),  # главная страница
]
```

Сохранить.

---

## 14. Запуск сервера полностью через WSL

**Где:** Ubuntu (WSL).

```bash
cd /mnt/c/Users/cp24/Documents/django/notes
source .venv/bin/activate

python manage.py runserver 0.0.0.0:8001
```

Теперь в **браузере Windows**:

- сайт: `http://localhost:8001/`
    
- админка: `http://localhost:8001/admin/`
    

В админке зайди под суперпользователем → раздел **«Заметки»** → добавь пару записей — они появятся на главной.

---

## 15. Краткая версия «как запускать потом»

Каждый раз, когда хочешь поработать с проектом:

```text
1) Открыть Ubuntu (WSL).

2) В терминале:
   cd /mnt/c/Users/cp24/Documents/django/notes
   source .venv/bin/activate

3) Запустить:
   python manage.py runserver 0.0.0.0:8001

4) Открыть в браузере:
   http://localhost:8001/
```

---

## Теги

#django #python #wsl #ubuntu #windows10 #notes #venv #bootstrap #шпаргалка

```

Если хочешь, следующим шагом можем сделать **отдельную шпаргалку именно под i18n (RU/EN)**, но уже тоже в контексте этого нового проекта `notes` на WSL.
::contentReference[oaicite:0]{index=0}
```