````markdown
# Django · Шпаргалка №3  
## Мультиязычность RU/EN + WSL (gettext)

> База: проект уже настроен по Шпаргалкам 
> [django_notes][django_python_windows]   
> Путь проекта: `C:\Users\cp24\Documents\django\project1`  
> Есть `venv`, приложение `main`, шаблоны `base.html` и `home.html`, модель `Note`.

---

## 0. Подготовка: установка и настройка WSL на Windows 10

### 0.1. Включаем WSL в Windows

**Действия в Windows (не в коде):**

https://learn.microsoft.com/ru-ru/windows/wsl/install

1. Открой **Панель управления → Программы → Включение или отключение компонентов Windows**.  
2. Поставь галочки:
   - **Подсистема Windows для Linux** (Windows Subsystem for Linux);
   - **Платформа виртуальной машины** (Virtual Machine Platform) — если есть.
3. Нажми **ОК**, дождись установки, **перезагрузи** компьютер.

Альтернатива через PowerShell (от имени администратора):

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
shutdown /r /t 0
````

### 0.2. Устанавливаем дистрибутив Linux

**Действия в Windows:**

1. Открой **Microsoft Store**.
    
2. Найди и установи, например, **Ubuntu**.
    
3. Запусти приложение **Ubuntu** из меню «Пуск».
    
4. При первом запуске:
    
    - дождись установки;
        
    - придумай **имя пользователя** и **пароль** (это отдельный пользователь внутри Linux).
        

После этого у тебя есть терминал Ubuntu /Debian (WSL), в котором мы будем выполнять Linux-команды.

---

## 1. Цель

Сделать на сайте поддержку языков:

- основной язык: **русский** (`ru`);
    
- дополнительный: **английский** (`en`);
    
- переключатель RU/EN в шапке;
    
- сбор/компиляция переводов через **WSL + gettext**.
    

---

## 2. Настройка i18n в `settings.py`

### 2.1. Импорт gettext

**Файл:** `config/settings.py`  
Добавь импорт вверху:

```python
from django.utils.translation import gettext_lazy as _
```

### 2.2. Базовые параметры языка

**Файл:** `config/settings.py`  
Убедись, что стоят такие значения:

```python
LANGUAGE_CODE = "ru"
USE_I18N = True
```

### 2.3. Список языков и папка локалей

**Файл:** `config/settings.py`  
Добавь/измени блок:

```python
LANGUAGES = [
    ("ru", _("Русский")),
    ("en", _("Английский")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]
```

### 2.4. Подключаем `LocaleMiddleware`

**Файл:** `config/settings.py`  
В списке `MIDDLEWARE` добавь строку **сразу после** `SessionMiddleware`:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # ← добавлено
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

---

## 3. Подготовка шаблонов к переводу

### 3.1. Базовый шаблон `base.html`

**Файл:** `templates/base.html`

В самом начале файла добавь загрузку тегов перевода:

```html
{% load i18n %}
<!DOCTYPE html>
<html lang="ru">
```

Заменяем текст на переводимые строки:

```html
<title>{% block title %}{% trans "Мой Django-сайт" %}{% endblock %}</title>
```

```html
<a class="navbar-brand" href="{% url 'home' %}">
    {% trans "Django заметки" %}
</a>
```

```html
<a class="nav-link active" aria-current="page" href="{% url 'home' %}">
    {% trans "Главная" %}
</a>
```

```html
<span>{% trans "Сайт на Django" %} · {{ request.get_host }}</span>
```

### 3.2. Главная страница `home.html`

**Файл:** `templates/home.html`

Важно: первым тегом должен быть `{% extends %}`.

```html
{% extends "base.html" %}
{% load i18n %}
```

Заголовок страницы:

```html
{% block title %}{% trans "Мои заметки · Django" %}{% endblock %}
```

Текст и кнопки:

```html
<h1 class="mb-3">{% trans "Привет, Виктор 👋" %}</h1>
```

```html
<p class="text-muted mb-0">
    {% trans "Это твой первый сайт на Django с красивым шаблоном и списком заметок из базы." %}
</p>
```

```html
<a href="/admin/" class="btn btn-outline-secondary">
    {% trans "Перейти в админку" %}
</a>
```

```html
<h2 class="h4 mb-3">{% trans "Заметки" %}</h2>
```

Блок с сообщением, когда нет заметок:

```html
<div class="alert alert-info">
    {% blocktrans %}
    Пока нет ни одной заметки. Зайди в <a href="/admin/">админ-панель</a> и создай первую 🙂
    {% endblocktrans %}
</div>
```

---

## 4. URL для смены языка и селектор RU/EN

### 4.1. View `set_language` в маршрутах

**Файл:** `config/urls.py`

Добавь импорт и путь:

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

### 4.2. Переключатель языка в `base.html`

**Файл:** `templates/base.html`

Внутри навбара, после списка ссылок (после `</ul>`), добавь форму:

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

---

## 5. Подготовка WSL для работы с переводами

### 5.1. Устанавливаем нужные пакеты

**Команды выполняются в терминале Ubuntu (WSL):**

```bash
sudo apt update
sudo apt install -y gettext python3-venv
```

### 5.2. Переходим в папку проекта через WSL

**Команда в WSL:**

```bash
cd /mnt/c/Users/cp24/Documents/django/project1
```

### 5.3. Создаём отдельный venv только для переводов

**Команды в WSL:**

```bash
python3 -m venv .venv_wsl
source .venv_wsl/bin/activate

pip install django
python -m django --version   # проверка
```

---

## 6. Создание и редактирование английских переводов

### 6.1. Сбор строк для языка `en`

**Команда в WSL (в папке проекта, venv `.venv_wsl` активирован):**

```bash
python manage.py makemessages -l en
```

Django создаст файл:

```text
locale/en/LC_MESSAGES/django.po
```

### 6.2. Редактирование `django.po`

**Файл:** `locale/en/LC_MESSAGES/django.po`

В шапке файла замени первый блок на:

```po
msgid ""
msgstr ""
"Project-Id-Version: Django Notes\n"
"POT-Creation-Date: 2025-11-23 22:03+0000\n"
"PO-Revision-Date: 2025-11-23 23:00+0000\n"
"Last-Translator: Viktor Khomenko <EMAIL@ADDRESS>\n"
"Language-Team: English <LL@li.org>\n"
"Language: en\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"
```

И пропиши переводы для строк проекта:

```po
#: config/settings.py:129
msgid "Русский"
msgstr "Russian"

#: config/settings.py:130
msgid "Английский"
msgstr "English"

#: templates/base.html:6
msgid "Мой Django-сайт"
msgstr "My Django site"

#: templates/base.html:48
msgid "Django заметки"
msgstr "Django notes"

#: templates/base.html:60
msgid "Главная"
msgstr "Home"

#: templates/base.html:76
msgid "Сайт на Django"
msgstr "Site powered by Django"

#: templates/home.html:5
msgid "Мои заметки · Django"
msgstr "My notes · Django"

#: templates/home.html:10
msgid "Привет, Виктор 👋"
msgstr "Hi, Viktor 👋"

#: templates/home.html:12
msgid ""
"Это твой первый сайт на Django с красивым шаблоном и списком заметок из базы."
msgstr ""
"This is your first Django site with a nice template and a list of notes from "
"the database."

#: templates/home.html:17
msgid "Перейти в админку"
msgstr "Go to admin"

#: templates/home.html:24
msgid "Заметки"
msgstr "Notes"

#: templates/home.html:46
msgid ""
"Пока нет ни одной заметки. Зайди в <a href=\"/admin/\">админ-панель</a> и "
"создай первую 🙂"
msgstr ""
"There are no notes yet. Go to the <a href=\"/admin/\">admin panel</a> and "
"create the first one 🙂"
```

> Все английские `msgid` из самого Django (`Messages`, `Enter a valid value.` и т.д.) можно оставить как есть с `msgstr ""`.

---

## 7. Компиляция переводов

### 7.1. Превращаем `.po` в `.mo`

**Команда в WSL (всё ещё в `.venv_wsl`):**

```bash
cd /mnt/c/Users/cp24/Documents/django/project1
python manage.py compilemessages
```

Django создаст/обновит `locale/en/LC_MESSAGES/django.mo`.

---

## 8. Запуск сайта и проверка

### 8.1. Запуск сервера (как обычно)

**Команды в Windows (cmd):**

```bat
cd C:\Users\cp24\Documents\django\project1
venv\Scripts\activate.bat
python manage.py runserver 8001
```

Открыть в браузере:

- `http://127.0.0.1:8001/` — сайт;
    
- выбрать в селекте **RU** или **EN** в шапке:
    
    - RU → интерфейс по-русски,
        
    - EN → тексты, описанные в `django.po`, на английском.
        

---

## 9. Добавление нового языка (пример: немецкий)

### 9.1. Добавляем язык в настройки

**Файл:** `config/settings.py`

```python
LANGUAGES = [
    ("ru", _("Русский")),
    ("en", _("Английский")),
    ("de", _("Немецкий")),
]
```

### 9.2. Создаём файл переводов

**Команда в WSL:**

```bash
cd /mnt/c/Users/cp24/Documents/django/project1
source .venv_wsl/bin/activate
python manage.py makemessages -l de
# редактируем locale/de/LC_MESSAGES/django.po
python manage.py compilemessages
```

### 9.3. Добавляем DE в селектор

**Файл:** `templates/base.html`

```html
<select name="language" class="form-select form-select-sm"
        onchange="this.form.submit()">
    <option value="ru" {% if request.LANGUAGE_CODE == 'ru' %}selected{% endif %}>RU</option>
    <option value="en" {% if request.LANGUAGE_CODE == 'en' %}selected{% endif %}>EN</option>
    <option value="de" {% if request.LANGUAGE_CODE == 'de' %}selected{% endif %}>DE</option>
</select>
```

---

## Теги

#django #python #windows10 #wsl #gettext #i18n #localization #ru #en #de #venv

```
::contentReference[oaicite:0]{index=0}
```