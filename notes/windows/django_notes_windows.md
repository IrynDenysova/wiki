апгрейд до: шаблоны + заметки + админка.

````markdown
# Django · Апгрейд проекта до заметок и красивого шаблона

> Проект уже установлен и настроен по базовой шпаргалке:  
> `C:\Users\cp24\Documents\django\project1` + `venv` + `config` + `main`.

---

## 1. Запуск проекта и активация venv

```bat
cd C:\Users\cp24\Documents\django\project1
venv\Scripts\activate.bat
python manage.py runserver 8001
````

Админка:  
`http://127.0.0.1:8001/admin/`

Если суперпользователь ещё не создан:

```bat
python manage.py createsuperuser
```

---

## 2. Модель заметок `Note`

**Файл:** `main/models.py`

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

### Миграции

```bat
python manage.py makemigrations
python manage.py migrate
```

---

## 3. Регистрируем заметки в админке

**Файл:** `main/admin.py`

```python
from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "text")
    list_filter = ("created_at",)
```

После этого в `/admin/` появится раздел **«Заметки»** — можно добавлять записи.

---

## 4. Шаблоны: `base.html` + `home.html`

### 4.1. Папка шаблонов

Папка уже должна быть:

```text
C:\Users\cp24\Documents\django\project1\templates
```

Если нет — создать.

---

### 4.2. Базовый шаблон `base.html`

**Файл:** `templates/base.html`

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

    {% block extra_head %}{% endblock %}
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

{% block extra_js %}{% endblock %}
</body>
</html>
```

---

### 4.3. Главная страница `home.html`

**Файл:** `templates/home.html`

```html
{% extends "base.html" %}

{% block title %}Мои заметки · Django{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col-lg-8">
        <h1 class="mb-3">Привет, Виктор 👋</h1>
        <p class="text-muted mb-0">
            Это твой первый сайт на Django с красивым шаблоном и списком заметок из базы.
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

---

### 4.4. Настройки шаблонов в `settings.py`

**Файл:** `config/settings.py`  
Блок `TEMPLATES`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # наша папка с шаблонами
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

---

## 5. View и URL для главной страницы

### 5.1. View

**Файл:** `main/views.py`

```python
from django.shortcuts import render
from .models import Note


def home(request):
    notes = Note.objects.all()
    return render(request, "home.html", {"notes": notes})
```

---

### 5.2. Маршрут

**Файл:** `config/urls.py`

```python
from django.contrib import admin
from django.urls import path
from main.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # главная страница
]
```

---

## 6. Запуск и проверка

```bat
cd C:\Users\cp24\Documents\django\project1
venv\Scripts\activate.bat
python manage.py runserver 8001
```

Открыть в браузере:

- Сайт: `http://127.0.0.1:8001/`
    
- Админка: `http://127.0.0.1:8001/admin/`
    

В админке → раздел **«Заметки»** → добавить несколько — они появятся на главной.

---

## Теги

#django #python #windows10 #venv #webdev #bootstrap #templates #notes #admin

```

Если хочешь, можем сделать ещё **третью заметку**: «как перенести этот проект на твой сервер s1.viktorplus.com (Linux + nginx + gunicorn)».
::contentReference[oaicite:0]{index=0}
```