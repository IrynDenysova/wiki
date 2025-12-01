Вот компактная шпаргалка в `markdown`, которую можно сохранить как `django_s1_setup.md`.

````md
# Django + #Gunicorn + #Nginx на #s1.viktorplus.com #linux #ubuntu #debian

Система: Debian/Ubuntu  
Пользователь: `viktor`  
Проект: `/home/viktor/sites/mysite`  
Docker-nginx уже крутится на `8081`, порт `80` свободен.

---

## 0. Проверки перед стартом

```bash
# Кто слушает 80/8081
sudo ss -tulpn | egrep ':80 |:8081 '

# Статусы nginx/apache
sudo systemctl status nginx apache2 --no-pager
````

Ожидаем:

* на `8081` — `docker-proxy` (контейнер nginx),
* на `80` — свободно, nginx не установлен.

---

## 1. Установка базовых пакетов

> Была проблема: venv не создавался (`ensurepip is not available`) и не было `pip`.

Решение:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip nginx git
```

---

## 2. Создание структуры проекта и виртуального окружения

```bash
mkdir -p /home/viktor/sites/mysite
cd /home/viktor/sites/mysite

# создаём venv
python3 -m venv venv

# активируем
source venv/bin/activate

# ставим зависимости
pip install --upgrade pip
pip install django gunicorn
```

---

## 3. Создание Django-проекта

```bash
cd /home/viktor/sites/mysite
django-admin startproject config .

python manage.py migrate
python manage.py createsuperuser
```

---

## 4. Настройка `settings.py`

Файл: `config/settings.py`

```python
DEBUG = False

ALLOWED_HOSTS = [
    "s1.viktorplus.com",
    "viktorplus.com",
    "127.0.0.1",
    "localhost",
    "ТВОЙ_IP_СЕРВЕРА",
]
```

Статика:

```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
```

Сбор статики:

```bash
source venv/bin/activate
python manage.py collectstatic
```

---

## 5. Настройка Gunicorn через systemd

Файл: `/etc/systemd/system/gunicorn-mysite.service`

```ini
[Unit]
Description=Gunicorn for Django project mysite
After=network.target

[Service]
User=viktor
Group=www-data
WorkingDirectory=/home/viktor/sites/mysite
Environment="PATH=/home/viktor/sites/mysite/venv/bin"
ExecStart=/home/viktor/sites/mysite/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/viktor/sites/mysite/gunicorn.sock \
          config.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

Активировать:

```bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn-mysite
sudo systemctl start gunicorn-mysite
sudo systemctl status gunicorn-mysite --no-pager
ls -lah /home/viktor/sites/mysite/gunicorn.sock
```

---

## 6. Настройка Nginx (виртуальный хост)

Файл: `/etc/nginx/sites-available/mysite`

```nginx
server {
    listen 80;
    server_name s1.viktorplus.com viktorplus.com;

    root /home/viktor/sites/mysite;

    location /static/ {
        alias /home/viktor/sites/mysite/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/viktor/sites/mysite/gunicorn.sock;
    }
}
```

Подключить сайт и перезагрузить nginx:

```bash
sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/mysite
sudo rm /etc/nginx/sites-enabled/default 2>/dev/null || true

sudo nginx -t
sudo systemctl reload nginx
```

---

## 7. Firewall и доступ снаружи

### 7.1. UFW на сервере

```bash
sudo ufw status
sudo ufw allow 'Nginx Full'
sudo ufw reload
sudo ufw status
```

### 7.2. Внешний фаервол у хостера

* В панели провайдера открыть входящий TCP `80` (и `443` на будущее).

### 7.3. DNS

Проверка:

```bash
hostname -I
host s1.viktorplus.com
```

* A-запись `s1.viktorplus.com` должна указывать на IP из `hostname -I`.

---

## 8. Типовые проблемы и как мы их чинили

### 8.1. `ERR_CONNECTION_TIMED_OUT` в браузере

Причины:

* Порт 80 закрыт во внешнем firewall.
* DNS смотрит не на тот IP.

Решения:

* Открыть порт 80 у провайдера.
* Поправить A-запись домена на правильный IP.

### 8.2. `502 Bad Gateway` от nginx

Проверка:

```bash
sudo systemctl status gunicorn-mysite --no-pager
ls -lah /home/viktor/sites/mysite/gunicorn.sock
sudo tail -n 50 /var/log/nginx/error.log
```

У нас была ошибка:

```text
connect() to unix:/home/viktor/sites/mysite/gunicorn.sock failed (13: Permission denied)
```

Решение — дать право прохода по каталогам к сокету:

```bash
sudo chmod o+x /home
sudo chmod o+x /home/viktor
sudo chmod o+x /home/viktor/sites
sudo chmod o+x /home/viktor/sites/mysite

sudo systemctl restart gunicorn-mysite
sudo systemctl reload nginx
```

После этого `curl -I http://127.0.0.1` → `HTTP/1.1 200 OK`, и сайт стал открываться.

---

## 9. Простая главная страница

### 9.1. Создание приложения `main`

```bash
cd /home/viktor/sites/mysite
source venv/bin/activate
python manage.py startapp main
```

`config/settings.py`:

```python
INSTALLED_APPS = [
    # стандартные приложения Django ...
    'main',
]
```

### 9.2. View

`main/views.py`:

```python
from django.shortcuts import render

def index(request):
    return render(request, "main/index.html")
```

### 9.3. URL-маршрут

`config/urls.py`:

```python
from django.contrib import admin
from django.urls import path
from main.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="home"),
]
```

### 9.4. Шаблон

```bash
mkdir -p main/templates/main
nano main/templates/main/index.html
```

Пример содержимого:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>s1.viktorplus.com – Django</title>
</head>
<body>
    <h1>Привет с s1.viktorplus.com!</h1>
    <p>Django работает 🚀</p>
</body>
</html>
```

### 9.5. Перезапуск Gunicorn

```bash
sudo systemctl restart gunicorn-mysite
```

Теперь:

* `http://s1.viktorplus.com/` → ваша главная страница,
* `http://s1.viktorplus.com/admin` → админка.

---

## 10. Быстрый чек-лист «жив ли сайт»

```bash
# nginx слушает 80?
sudo ss -tulpn | grep ':80 '

# локальный запрос
curl -I http://127.0.0.1

# статус gunicorn
sudo systemctl status gunicorn-mysite --no-pager

# ошибки nginx
sudo tail -n 50 /var/log/nginx/error.log
```

```

Если хочешь, можем к этой шпаргалке потом добавить разделы про HTTPS (Let’s Encrypt), PostgreSQL и вариант той же схемы в Docker.
```
