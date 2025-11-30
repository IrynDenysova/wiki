````markdown
# Django на Windows 10 с готовым HTML-шаблоном  
(вариант с активацией `venv` как у нас сейчас)

Итоговая структура:

```text
C:\Users\cp24\Documents\django\project1\
    venv\               ← виртуальная среда
    manage.py
    db.sqlite3
    config\             ← настройки проекта
    main\               ← приложение
    templates\
        home.html       ← шаблон главной страницы
````

---

## 0. Подготовка

1. Установить **Python 3.x** (с галочкой **“Add python.exe to PATH”**).
    
2. Открыть **Командную строку (cmd)**.
    

Проверка:

```bat
python --version
pip --version
```

---

## 1. Папка для проектов и проекта

```bat
cd %USERPROFILE%\Documents
mkdir django
cd django
mkdir project1
cd project1
```

---

## 2. Создаём и активируем виртуальную среду `venv`, ставим Django

### 2.1. Создаём venv

```bat
py -m venv venv
```

### 2.2. Активируем venv

```bat
venv\Scripts\activate.bat
```

> Если всё ок — в начале строки появится префикс:  
> `(venv) C:\Users\...\project1>`

### 2.3. Ставим Django внутри активированного venv

```bat
pip install --upgrade pip
pip install django
python -m django --version   :: проверка
```

---

## 3. Создаём Django-проект

```bat
python -m django startproject config .
```

Получится:

```text
project1\
    venv\
    manage.py
    config\
```

---

## 4. Создаём приложение `main`

```bat
python manage.py startapp main
```

---

## 5. Регистрируем приложение `main`

Открыть файл:

```text
C:\Users\cp24\Documents\django\project1\config\settings.py
```

Найти `INSTALLED_APPS` и добавить `'main',`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main',  # наше приложение
]
```

Сохранить.

---

## 6. Подключаем папку `templates` и создаём `home.html`

### 6.1. Создаём папку `templates` и файл шаблона

В `C:\Users\cp24\Documents\django\project1` создать папку:

```text
templates
```

Внутри — файл:

```text
C:\Users\cp24\Documents\django\project1\templates\home.html
```

Содержимое `home.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Мой первый сайт на Django</title>
</head>
<body>
    <h1>Привет, Виктор!</h1>
    <p>Эта страница отдается через шаблон <code>home.html</code>.</p>
</body>
</html>
```

### 6.2. Настраиваем поиск шаблонов в `settings.py`

В `config\settings.py` найти блок `TEMPLATES` и указать папку `templates`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← наша папка с шаблонами
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

Сохранить.

---

## 7. View, которая рендерит шаблон

Открыть:

```text
C:\Users\cp24\Documents\django\project1\main\views.py
```

Сделать так:

```python
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')
```

Сохранить.

---

## 8. Маршрут для главной страницы

Открыть:

```text
C:\Users\cp24\Documents\django\project1\config\urls.py
```

Содержимое:

```python
from django.contrib import admin
from django.urls import path
from main.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # главная страница
]
```

Сохранить.

---

## 9. Миграции и запуск сервера

Всё ещё в активном venv `(venv)`:

```bat
python manage.py migrate
python manage.py runserver 8001
```

Открыть в браузере:

```text
http://127.0.0.1:8001/
```

Появится страница из `home.html`.

---

## 10. Как запускать проект потом (краткая версия)

Каждый раз:

```bat
cd %USERPROFILE%\Documents\django\project1
venv\Scripts\activate.bat
python manage.py runserver 8001
```

---

## Теги

#django #python #windows10 #venv #webdev 

```
::contentReference[oaicite:0]{index=0}
```