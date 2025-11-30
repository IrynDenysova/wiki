
---

````markdown
# Django · Trading Journal на WSL
## Проект `trading_journal` (журнал сделок криптофьючерсов)

Итоговая структура:

C:\Users\cp24\Documents\django\trading_journal\
    .venv/              ← виртуальное окружение (WSL)
    manage.py
    db.sqlite3
    config/             ← Django-проект
    journal/            ← приложение с журналом сделок
    templates/
        base.html       ← общий шаблон
        trades_list.html← список сделок

---

## 0. Предпосылки

- WSL + Ubuntu уже установлены.
- Django в этом проекте **устанавливаем отдельно** (свой `.venv`).

Все команды ниже — в **Ubuntu (WSL)**.

---

## 1. Создаём папку проекта на диске C:

**Где:** Ubuntu (WSL), любой каталог.

```bash
cd /mnt/c/Users/cp24/Documents

mkdir -p django
cd django

mkdir trading_journal
cd trading_journal
````

Теперь на Windows проект лежит тут:

> `C:\Users\cp24\Documents\django\trading_journal`

---

## 2. Виртуальное окружение и Django

### 2.1. Создаём venv

**Где:** WSL, папка проекта `/mnt/c/Users/cp24/Documents/django/trading_journal`:

```bash
python3 -m venv .venv
```

### 2.2. Активируем venv

```bash
source .venv/bin/activate
```

В начале строки увидишь `(.venv)`.

### 2.3. Ставим Django внутрь окружения

```bash
pip install django
python -m django --version   # просто проверка
```

---

## 3. Создаём Django-проект и приложение

### 3.1. Проект `config`

**Где:** WSL, та же папка, venv активирован.

```bash
django-admin startproject config .
```

Появятся `manage.py` и папка `config/`.

### 3.2. Приложение `journal`

```bash
python manage.py startapp journal
```

Появится папка `journal/`.

---

## 4. Регистрируем приложение `journal` в настройках

**Файл:** `config/settings.py`  
Путь на Windows: `C:\Users\cp24\Documents\django\trading_journal\config\settings.py`

Найди блок:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Замени/добавь:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'journal',  # наше приложение журнала сделок
]
```

Сохранить.

---

## 5. Настраиваем поиск шаблонов (templates)

### 5.1. Создаём папку `templates`

**Где:** WSL:

```bash
cd /mnt/c/Users/cp24/Documents/django/trading_journal
mkdir templates
```

(или создать папку через Проводник Windows внутри `trading_journal`)

### 5.2. Добавляем папку в настройки

**Файл:** `config/settings.py`

Найди блок `TEMPLATES` и поправь `'DIRS'`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← добавили нашу папку шаблонов
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

## 6. Модель сделки `Trade`

**Файл:** `journal/models.py`  
Путь: `C:\Users\cp24\Documents\django\trading_journal\journal\models.py`

Полностью замени содержимое на:

```python
from django.db import models


class Trade(models.Model):
    SIDE_CHOICES = [
        ("LONG", "Long"),
        ("SHORT", "Short"),
    ]

    STATUS_CHOICES = [
        ("OPEN", "Открыта"),
        ("CLOSED", "Закрыта"),
    ]

    exchange = models.CharField(
        max_length=50,
        default="Binance",
        verbose_name="Биржа",
    )
    symbol = models.CharField(
        max_length=20,
        verbose_name="Пара (например, BTCUSDT)",
    )
    side = models.CharField(
        max_length=5,
        choices=SIDE_CHOICES,
        verbose_name="Направление",
    )
    leverage = models.PositiveIntegerField(
        default=1,
        verbose_name="Плечо",
    )
    quantity = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        verbose_name="Объём (контракты/монеты)",
    )
    entry_price = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        verbose_name="Цена входа",
    )
    stop_loss = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name="Stop-loss",
    )
    take_profit_1 = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name="TP1",
    )
    take_profit_2 = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name="TP2",
    )
    take_profit_3 = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name="TP3",
    )

    status = models.CharField(
        max_length=6,
        choices=STATUS_CHOICES,
        default="OPEN",
        verbose_name="Статус",
    )
    realized_pnl = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name="Результат (USDT)",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано",
    )
    closed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Закрыто",
    )

    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий",
    )

    def __str__(self):
        return f"{self.symbol} {self.side} @ {self.entry_price}"

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"
        ordering = ["-created_at"]
```

Сохранить.

---

## 7. Миграции (создаём таблицу в БД)

**Где:** WSL, в папке проекта, venv активирован.

```bash
cd /mnt/c/Users/cp24/Documents/django/trading_journal
source .venv/bin/activate

python manage.py makemigrations
python manage.py migrate
```

---

## 8. Регистрируем `Trade` в админке

**Файл:** `journal/admin.py`  
Путь: `C:\Users\cp24\Documents\django\trading_journal\journal\admin.py`

Замени содержимое на:

```python
from django.contrib import admin
from .models import Trade


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "exchange",
        "symbol",
        "side",
        "leverage",
        "entry_price",
        "status",
        "realized_pnl",
    )
    list_filter = ("exchange", "side", "status", "created_at")
    search_fields = ("symbol", "comment")
    date_hierarchy = "created_at"
```

Сохранить.

---

## 9. Создаём суперпользователя (чтобы вносить сделки)

**Где:** WSL.

```bash
cd /mnt/c/Users/cp24/Documents/django/trading_journal
source .venv/bin/activate

python manage.py createsuperuser
```

Дальше ввести логин/почту/пароль.

---

## 10. Базовый шаблон `base.html`

**Файл:** `templates/base.html`  
Путь: `C:\Users\cp24\Documents\django\trading_journal\templates\base.html`

Создай файл и вставь:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Trading Journal{% endblock %}</title>

    <!-- Bootstrap 5 по CDN -->
    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
        integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
        crossorigin="anonymous"
    >

    <style>
        body {
            background-color: #0b1120;
            color: #e5e7eb;
        }
        .navbar {
            background: #020617;
        }
        .navbar-brand {
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        .main-wrapper {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .card-dark {
            background: #020617;
            border-radius: 1rem;
            border: 1px solid #1f2937;
            box-shadow: 0 8px 30px rgba(0,0,0,0.5);
        }
        .badge-long {
            background: #166534;
        }
        .badge-short {
            background: #b91c1c;
        }
        .pnl-positive {
            color: #22c55e;
        }
        .pnl-negative {
            color: #ef4444;
        }
        .footer {
            font-size: 0.85rem;
            color: #6b7280;
            padding: 1.5rem 0;
        }
        a {
            color: #60a5fa;
        }
        a:hover {
            color: #93c5fd;
        }
        table thead {
            background: #020617;
        }
        table tbody tr:hover {
            background: rgba(55,65,81,0.3);
        }
    </style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark shadow-sm">
    <div class="container">
        <a class="navbar-brand" href="{% url 'trades_list' %}">
            Trading Journal
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbarNav" aria-controls="navbarNav"
                aria-expanded="false" aria-label="Переключить навигацию">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a class="nav-link active" href="{% url 'trades_list' %}">
                        Журнал сделок
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/admin/">
                        Админка
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
        <span>Trading Journal · {{ request.get_host }}</span>
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

## 11. Шаблон списка сделок `trades_list.html`

**Файл:** `templates/trades_list.html`  
Путь: `C:\Users\cp24\Documents\django\trading_journal\templates\trades_list.html`

Создай файл и вставь:

```html
{% extends "base.html" %}

{% block title %}Журнал сделок · Trading Journal{% endblock %}

{% block content %}
<div class="card card-dark mb-4">
    <div class="card-body">
        <h1 class="h4 mb-2">Журнал сделок</h1>
        <p class="text-secondary mb-0">
            Все сделки из базы данных Django. Новые сделки добавляются через <a href="/admin/">админ-панель</a>.
        </p>
    </div>
</div>

{% if trades %}
<div class="card card-dark">
    <div class="card-body p-0">
        <div class="table-responsive">
            <table class="table table-dark table-hover mb-0 align-middle">
                <thead>
                <tr>
                    <th scope="col">Дата</th>
                    <th scope="col">Биржа</th>
                    <th scope="col">Пара</th>
                    <th scope="col">Напр.</th>
                    <th scope="col">Плечо</th>
                    <th scope="col">Объём</th>
                    <th scope="col">Вход</th>
                    <th scope="col">SL</th>
                    <th scope="col">TP1/TP2/TP3</th>
                    <th scope="col">Статус</th>
                    <th scope="col">P&L (USDT)</th>
                    <th scope="col">Комментарий</th>
                </tr>
                </thead>
                <tbody>
                {% for trade in trades %}
                    <tr>
                        <td>{{ trade.created_at|date:"d.m.Y H:i" }}</td>
                        <td>{{ trade.exchange }}</td>
                        <td>{{ trade.symbol }}</td>
                        <td>
                            {% if trade.side == "LONG" %}
                                <span class="badge badge-long">LONG</span>
                            {% else %}
                                <span class="badge badge-short">SHORT</span>
                            {% endif %}
                        </td>
                        <td>{{ trade.leverage }}x</td>
                        <td>{{ trade.quantity }}</td>
                        <td>{{ trade.entry_price }}</td>
                        <td>
                            {% if trade.stop_loss %}
                                {{ trade.stop_loss }}
                            {% else %}
                                —
                            {% endif %}
                        </td>
                        <td>
                            {% if trade.take_profit_1 %}TP1: {{ trade.take_profit_1 }}{% endif %}
                            {% if trade.take_profit_2 %}<br>TP2: {{ trade.take_profit_2 }}{% endif %}
                            {% if trade.take_profit_3 %}<br>TP3: {{ trade.take_profit_3 }}{% endif %}
                            {% if not trade.take_profit_1 and not trade.take_profit_2 and not trade.take_profit_3 %}
                                —
                            {% endif %}
                        </td>
                        <td>{{ trade.get_status_display }}</td>
                        <td>
                            {% if trade.realized_pnl %}
                                {% if trade.realized_pnl > 0 %}
                                    <span class="pnl-positive">+{{ trade.realized_pnl }}</span>
                                {% elif trade.realized_pnl < 0 %}
                                    <span class="pnl-negative">{{ trade.realized_pnl }}</span>
                                {% else %}
                                    {{ trade.realized_pnl }}
                                {% endif %}
                            {% else %}
                                {% if trade.status == "OPEN" %}
                                    <span class="text-secondary">Открыта</span>
                                {% else %}
                                    —
                                {% endif %}
                            {% endif %}
                        </td>
                        <td style="max-width: 220px; white-space: pre-wrap;">
                            {{ trade.comment|default:"" }}
                        </td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% else %}
<div class="card card-dark">
    <div class="card-body">
        <p class="mb-0">
            Пока нет ни одной сделки. Зайди в <a href="/admin/">админку</a> и создай первую.
        </p>
    </div>
</div>
{% endif %}
{% endblock %}
```

Сохранить.

---

## 12. View для списка сделок

**Файл:** `journal/views.py`  
Путь: `C:\Users\cp24\Documents\django\trading_journal\journal\views.py`

Полностью замени на:

```python
from django.shortcuts import render
from .models import Trade


def trades_list(request):
    trades = Trade.objects.all()
    return render(request, "trades_list.html", {"trades": trades})
```

Сохранить.

---

## 13. Маршруты (urls.py)

**Файл:** `config/urls.py`  
Путь: `C:\Users\cp24\Documents\django\trading_journal\config\urls.py`

Сделай таким:

```python
from django.contrib import admin
from django.urls import path
from journal.views import trades_list

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", trades_list, name="trades_list"),
]
```

Сохранить.

---

## 14. Запуск сервера (через WSL)

**Где:** WSL.

```bash
cd /mnt/c/Users/cp24/Documents/django/trading_journal
source .venv/bin/activate

python manage.py runserver 0.0.0.0:8002
```

Теперь в браузере Windows:

- Журнал: [http://localhost:8002/](http://localhost:8002/)
    
- Админка: [http://localhost:8002/admin/](http://localhost:8002/admin/)
    

В админке → твоим суперпользователем → раздел **«Сделки»** → создаёшь сделки,  
они появляются в таблице на главной.

---

## 15. Краткая памятка по проекту `trading_journal`

```text
Запуск:
  1) Открыть Ubuntu (WSL)
  2) cd /mnt/c/Users/cp24/Documents/django/trading_journal
  3) source .venv/bin/activate
  4) python manage.py runserver 0.0.0.0:8002
  5) http://localhost:8002/ в браузере Windows
```

---

## Теги

#django #wsl #trading #journal #crypto #futures #python #bootstrap #venv #шпаргалка

```

Если хочешь, дальше можем:
- добавить **форму добавления сделки** прямо с сайта (без админки),
- или прикрутить простую статистику: суммарный PnL, винрейт, средний R:R и т.п.
::contentReference[oaicite:0]{index=0}
```