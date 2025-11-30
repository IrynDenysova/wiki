
````markdown
# Django · RU/EN для проекта `notes` (через WSL)

Цель:  
Сделать сайт `notes` двуязычным (RU/EN) с переключателем языка в шапке,  
все команды — из WSL, проект в `C:\Users\cp24\Documents\django\notes`.

---

## 1. Настраиваем i18n в settings.py

### 1.1. Импорт gettext_lazy

**Файл:** `config/settings.py`  
(Windows-путь: `C:\Users\cp24\Documents\django\notes\config\settings.py`)

В самом верху (рядом с другими import’ами) добавь:

```python
from django.utils.translation import gettext_lazy as _
````

---

### 1.2. Базовые настройки языка

**Файл:** `config/settings.py`

Убедись, что включена интернационализация и язык по умолчанию — русский:

```python
LANGUAGE_CODE = "ru"

USE_I18N = True
```

---

### 1.3. Список языков и папка локалей

**Файл:** `config/settings.py`

Где-нибудь ниже (например, рядом с LANGUAGE_CODE) добавь:

```python
LANGUAGES = [
    ("ru", _("Русский")),
    ("en", _("Английский")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]
```

---

### 1.4. LocaleMiddleware

**Файл:** `config/settings.py`

Найди список `MIDDLEWARE` и **сразу после** `SessionMiddleware` вставь `LocaleMiddleware`:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # ← добавили
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

Сохранить файл.

---

## 2. Готовим шаблоны: base.html и home.html

### 2.1. Базовый шаблон base.html

**Файл:** `templates/base.html`  
(`C:\Users\cp24\Documents\django\notes\templates\base.html`)

1. Вверху файла добавь загрузку тегов перевода:
    

```html
{% load i18n %}
<!DOCTYPE html>
<html lang="ru">
```

2. Оберни текстовые фразы в `{% trans %}`:
    

Найди:

```html
<title>{% block title %}Мой Django-сайт{% endblock %}</title>
```

Замени:

```html
<title>{% block title %}{% trans "Мой Django-сайт" %}{% endblock %}</title>
```

Найди:

```html
<a class="navbar-brand" href="{% url 'home' %}">Django Notes</a>
```

Замени:

```html
<a class="navbar-brand" href="{% url 'home' %}">{% trans "Django заметки" %}</a>
```

Найди:

```html
<a class="nav-link active" aria-current="page" href="{% url 'home' %}">
    Главная
</a>
```

Замени:

```html
<a class="nav-link active" aria-current="page" href="{% url 'home' %}">
    {% trans "Главная" %}
</a>
```

Найди:

```html
<span>Сайт на Django · {{ request.get_host }}</span>
```

Замени:

```html
<span>{% trans "Сайт на Django" %} · {{ request.get_host }}</span>
```

Сохранить файл.

---

### 2.2. Главный шаблон home.html

**Файл:** `templates/home.html`  
(`C:\Users\cp24\Documents\django\notes\templates\home.html`)

1. Важно: **первый тег** — `{% extends %}`.  
    Убедись, что начало файла такое:
    

```html
{% extends "base.html" %}
{% load i18n %}
```

2. Оборачиваем текст в переводы.
    

Найди:

```html
{% block title %}Мои заметки · Django{% endblock %}
```

Замени:

```html
{% block title %}{% trans "Мои заметки · Django" %}{% endblock %}
```

Найди:

```html
<h1 class="mb-3">Привет, Виктор 👋</h1>
```

Замени:

```html
<h1 class="mb-3">{% trans "Привет, Виктор 👋" %}</h1>
```

Найди:

```html
<p class="text-muted mb-0">
    Это твой сайт на Django с красивым шаблоном и списком заметок из базы.
</p>
```

Замени:

```html
<p class="text-muted mb-0">
    {% trans "Это твой сайт на Django с красивым шаблоном и списком заметок из базы." %}
</p>
```

Найди кнопку:

```html
<a href="/admin/" class="btn btn-outline-secondary">
    Перейти в админку
</a>
```

Замени:

```html
<a href="/admin/" class="btn btn-outline-secondary">
    {% trans "Перейти в админку" %}
</a>
```

Найди заголовок блока:

```html
<h2 class="h4 mb-3">Заметки</h2>
```

Замени:

```html
<h2 class="h4 mb-3">{% trans "Заметки" %}</h2>
```

Найди блок «нет заметок»:

```html
<div class="alert alert-info">
    Пока нет ни одной заметки. Зайди в <a href="/admin/">админ-панель</a> и создай первую 🙂
</div>
```

Замени:

```html
<div class="alert alert-info">
    {% blocktrans %}
    Пока нет ни одной заметки. Зайди в <a href="/admin/">админ-панель</a> и создай первую 🙂
    {% endblocktrans %}
</div>
```

Сохранить файл.

---

## 3. URL для смены языка и переключатель RU/EN

### 3.1. Добавляем set_language в urls.py

**Файл:** `config/urls.py`  
(`C:\Users\cp24\Documents\django\notes\config\urls.py`)

Сделай так:

```python
from django.contrib import admin
from django.urls import path
from django.views.i18n import set_language
from main.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("set-language/", set_language, name="set_language"),
    path("", home, name="home"),
]
```

Сохранить файл.

---

### 3.2. Форма выбора языка в base.html

**Файл:** `templates/base.html`

Внутри `<nav>`, после `<ul class="navbar-nav ms-auto">...</ul>`, добавь форму:

```html
<form action="{% url 'set_language' %}" method="post" class="d-flex ms-3">
    {% csrf_token %}
    <input type="hidden" name="next" value="{{ request.path }}">
    <select name="language" class="form-select form-select-sm"
            onchange="this.form.submit()">
        <option value="ru" {% if request.LANGUAGE_CODE == 'ru' %}selected{% endif %}>RU</option>
        <option value="en" {% if request.LANGUAGE_CODE == 'en' %}selected{% endif %}>EN</option>
    </select>
</form>
```

Сохранить.

Теперь в шапке появится селект RU/EN.

---

## 4. gettext и сбор переводов через WSL

### 4.1. Устанавливаем gettext в Ubuntu (если ещё нет)

**Где:** Ubuntu (WSL).

```bash
sudo apt update
sudo apt install -y gettext
```

(Если уже ставил по прошлой шпаргалке — этот шаг уже сделан.)

---

### 4.2. Переходим в проект и активируем venv

**Где:** Ubuntu (WSL).

```bash
cd /mnt/c/Users/cp24/Documents/django/notes
source .venv/bin/activate
```

---

### 4.3. Собираем сообщения для английского

**Где:** Ubuntu (WSL), активное `.venv`:

```bash
python manage.py makemessages -l en
```

Django создаст:

```text
locale/
    en/
        LC_MESSAGES/
            django.po
```

---

## 5. Редактируем django.po (руские строки → английский)

**Файл:** `locale/en/LC_MESSAGES/django.po`  
(Windows-путь: `C:\Users\cp24\Documents\django\notes\locale\en\LC_MESSAGES\django.po`)

Открыть любым редактором (VS Code, Notepad++).

### 5.1. Шапка файла (можно слегка поправить)

В начале будет блок `msgid "" / msgstr ""`. Можно привести к такому виду:

```po
msgid ""
msgstr ""
"Project-Id-Version: notes project\n"
"POT-Creation-Date: 2025-11-23 22:03+0000\n"
"PO-Revision-Date: 2025-11-23 23:30+0000\n"
"Last-Translator: Viktor Khomenko <EMAIL@ADDRESS>\n"
"Language-Team: English <LL@li.org>\n"
"Language: en\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"
```

(Точные даты/почту можно не заморачиваться — главное `Language: en`.)

---

### 5.2. Прописываем переводы для наших строк

Найди строки с нашими `msgid` и заполни `msgstr`. Например:

```po
#: config/settings.py:XXX
msgid "Русский"
msgstr "Russian"

#: config/settings.py:YYY
msgid "Английский"
msgstr "English"

#: templates/base.html:XX
msgid "Мой Django-сайт"
msgstr "My Django site"

#: templates/base.html:XX
msgid "Django заметки"
msgstr "Django notes"

#: templates/base.html:XX
msgid "Главная"
msgstr "Home"

#: templates/base.html:XX
msgid "Сайт на Django"
msgstr "Site powered by Django"

#: templates/home.html:XX
msgid "Мои заметки · Django"
msgstr "My notes · Django"

#: templates/home.html:XX
msgid "Привет, Виктор 👋"
msgstr "Hi, Viktor 👋"

#: templates/home.html:XX
msgid ""
"Это твой сайт на Django с красивым шаблоном и списком заметок из базы."
msgstr ""
"This is your Django site with a nice template and a list of notes from the "
"database."

#: templates/home.html:XX
msgid "Перейти в админку"
msgstr "Go to admin"

#: templates/home.html:XX
msgid "Заметки"
msgstr "Notes"

#: templates/home.html:XX
msgid ""
"Пока нет ни одной заметки. Зайди в <a href=\"/admin/\">админ-панель</a> и "
"создай первую 🙂"
msgstr ""
"There are no notes yet. Go to the <a href=\"/admin/\">admin panel</a> and "
"create the first one 🙂"
```

> Номера строк (`:XX`) могут отличаться — не страшно, главное, чтобы `msgid` совпадал.

Все английские `msgid` из самого Django (`Messages`, `Enter a valid value.` и т.п.) можно оставить с `msgstr ""` — они и так уже на английском.

Сохранить `django.po`.

---

## 6. Компилируем переводы

**Где:** Ubuntu (WSL), в проекте, с активным `.venv`:

```bash
cd /mnt/c/Users/cp24/Documents/django/notes
source .venv/bin/activate

python manage.py compilemessages
```

После этого в `locale/en/LC_MESSAGES/` появится (или обновится) `django.mo`.

---

## 7. Запуск и проверка

**Где:** Ubuntu (WSL).

```bash
cd /mnt/c/Users/cp24/Documents/django/notes
source .venv/bin/activate

python manage.py runserver 0.0.0.0:8001
```

В браузере Windows:

- Открыть: `http://localhost:8001/`
    
- В правом верхнем углу, в селекте, выбрать:
    
    - `RU` → интерфейс на русском
        
    - `EN` → строки, которые мы перевели в `django.po`, станут на английском
        

---

## 8. Краткий чек-лист RU/EN через WSL

```text
1) Настроить settings.py:
   - LANGUAGE_CODE="ru", USE_I18N=True
   - LANGUAGES = [("ru","Русский"), ("en","Английский")]
   - LOCALE_PATHS = [BASE_DIR / "locale"]
   - добавить LocaleMiddleware

2) В шаблонах base.html и home.html использовать {% load i18n %}, {% trans %}, {% blocktrans %}.

3) В urls.py добавить set_language и путь "set-language/".

4) В base.html добавить форму <select name="language"> RU/EN.

5) В WSL:
   cd /mnt/c/Users/cp24/Documents/django/notes
   source .venv/bin/activate
   sudo apt install gettext    # если не установлен
   python manage.py makemessages -l en

6) Заполнить locale/en/LC_MESSAGES/django.po (msgstr).

7) В WSL:
   python manage.py compilemessages

8) Запуск:
   python manage.py runserver 0.0.0.0:8001
   -> http://localhost:8001/
```

---

# Теги

#django #wsl #i18n #gettext #ru #en #python #notes #шпаргалка

```
::contentReference[oaicite:0]{index=0}
```