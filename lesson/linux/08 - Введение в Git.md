# Урок 8. Введение в Git (Git vs GitHub, SSH key, первые команды)

## 1) Что такое система контроля версий (VCS)
**Система контроля версий** — инструмент, который помогает отслеживать изменения в коде/файлах во времени, работать в команде, возвращаться к прошлым версиям и безопасно объединять изменения.

---

## 2) Виды систем контроля версий

### 2.1. Централизованные (CVCS)
**Идея:** один центральный сервер хранит все версии, разработчики синхронизируют свои рабочие копии с сервером.  
**Примеры:** CVS, SVN, Perforce.  
**Минусы:** зависимость от сервера, медленнее некоторые операции, уязвимость при отказе сервера.

### 2.2. Распределённые (DVCS)
**Идея:** у каждого разработчика *полная копия репозитория* со всей историей.  
**Примеры:** Git, Mercurial, Bazaar.  
**Плюсы:** автономная работа, устойчивость к отказам, высокая скорость операций.

### 2.3. Локальные (Local VCS)
Работают с отдельными файлами на одном компьютере (базовый контроль версий, плохо подходит для командной работы).

---

## 3) Создание Git (краткая история)
- Git появился в **2005** году: Линус Торвальдс создавал инструмент для эффективного управления версиями в разработке Linux.
- Git быстро стал стандартом из‑за скорости, гибкости и распределённой модели.

---

## 4) Основные принципы и функции Git

### Принципы
- **Распределённость**: у каждого есть полная история.
- **Снимки (snapshots)**: Git фиксирует состояния проекта.
- **Скорость и эффективность**: оптимизация под большие проекты.

### Функции
- Контроль версий и откат к прошлым состояниям.
- Ветвление и слияние (branching/merging).
- Работа с удалёнными репозиториями (HTTP/SSH и др.).
- Отслеживание авторства и контроля доступа.

---

## 5) Git vs GitHub
- **Git** — система контроля версий (работает локально, командная строка/GUI).
- **GitHub** — веб‑платформа для хостинга Git‑репозиториев + инструменты совместной разработки (PR, обсуждения, социальные функции, интеграции).

---

## 6) Подготовка: установка Git и базовая настройка

### Проверка, что Git установлен
```bash
git --version
```

- Windows: удобно использовать **Git Bash**
- macOS: обычно ставят через **Xcode** (если не стоит — система предложит поставить)

### Представиться Git (нужно один раз)
```bash
git config --global user.name "Ваше имя"
git config --global user.email "ваш@адрес.почты"
```

Проверить настройки:
```bash
git config --global --list
```

---

## 7) GitHub: добавление SSH‑ключа

### 7.1. Посмотреть публичный ключ (если нет — сначала сгенерировать)
```bash
cat ~/.ssh/id_ed25519.pub
# или
cat ~/.ssh/id_rsa.pub
```

### 7.2. Проверка подключения к GitHub по SSH
```bash
ssh -T git@github.com
```

### 7.3. Добавление ключа в GitHub (через сайт)
Путь в интерфейсе:
- Профиль (иконка справа сверху) → **Settings**
- **SSH and GPG keys**
- **New SSH key**
- Вставить публичный ключ, задать **Title**
- **Add SSH key**

---

## 8) Создание репозитория на GitHub
- Нажать **+** (справа сверху) → **New repository**
- Ввести название, оставить остальное по умолчанию
- Нажать **Create repository**

---

## 9) Основные стадии работы с Git (workflow)

### Главное правило
Есть 4 “зоны”, через которые проходит ваш код:
1) **Working Directory** (рабочая папка)
2) **Staging Area / Index** (подготовка к коммиту)
3) **Local Repository** (локальная история)
4) **Remote Repository** (удалённый репозиторий, например GitHub)

### Команды по стадиям
- `git clone` — скачать репозиторий с удалённого сервера (удалённый → локально)
- `git add` — добавить изменения в staging
- `git commit` — зафиксировать изменения в локальной истории
- `git push` — отправить коммиты в удалённый репозиторий
- `git pull` — забрать изменения и объединить с локальными

---

## 10) git init и директория .git

### 10.1. git init
Инициализирует новый репозиторий Git:
- создаёт скрытую папку **.git**
- инициализирует пустой репозиторий
- создаёт базовую конфигурацию и индекс (staging area)

```bash
git init
```

### 10.2. Что внутри .git (кратко)
- `config` — настройки репозитория
- `objects/` — хранилище объектов (коммиты/файлы)
- `index` — staging area
- `refs/` — ссылки на ветки/теги
- `hooks/` — скрипты на события (pre-commit и др.)

---

## 11) Практика: создать локальный репозиторий и запушить на GitHub

```bash
git init
echo "# test" >> README.md
git status
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:USERNAME/REPO_NAME.git
git push -u origin main
git log
```

---

## 12) Домашнее задание (по уроку)
1) Создать на GitHub новый репозиторий **git_intro**  
2) На компьютере создать папку `git_intro` и инициализировать репозиторий  
3) Скопировать в папку любую картинку/фото  
4) Отправить изменения в GitHub:

```bash
git init
git add ИМЯ_ФАЙЛА
git commit -m "Added photo"
git branch -M main
git remote add origin git@github.com:ВАШЕ_ИМЯ_НА_GITHUB/git_intro.git
git push -u origin main
```

5) Прислать ссылку на репозиторий.

---

## 13) Мини-шпаргалка команд (самое частое)
```bash
git status
git add <file>        # или: git add .
git commit -m "msg"
git log --oneline
git push
git pull
```

Дополнительно (часто пригождается позже):
- ветки: `git branch`, `git checkout -b name`, `git merge name`
- откат: `git revert`, `git reset`
- очистка: `git clean -xdf -n` (сначала посмотреть)


---

## Дополнительные материалы

### Настройка Git

```bash
# Основные настройки
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git config --global init.defaultBranch main

# Редактор по умолчанию
git config --global core.editor "vim"

# Цветной вывод
git config --global color.ui auto

# Просмотр настроек
git config --list
git config --global --list
```

### Полезные алиасы

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.lg "log --oneline --graph --all --decorate"
```

### Работа с .gitignore

```bash
# Примеры .gitignore
*.log              # Все лог-файлы
node_modules/      # Директория
!important.log     # Исключение из правила
temp*              # Файлы начинающиеся с temp
/config.local      # Только в корне репозитория
```

**Шаблоны для разных языков:** [gitignore.io](https://www.toptal.com/developers/gitignore)

### Просмотр истории

```bash
git log --oneline --graph --all --decorate    # Красивый граф
git log --author="Name"                        # Коммиты автора
git log --since="2 weeks ago"                  # За период
git log --grep="keyword"                       # Поиск по сообщениям
git log file.txt                               # История файла
git show commit_hash                           # Детали коммита
git diff                                       # Изменения не в stage
git diff --staged                              # Изменения в stage
```

### Отмена изменений

```bash
git checkout -- file.txt       # Отменить изменения в файле
git restore file.txt           # То же (новый синтаксис)
git reset HEAD file.txt        # Убрать файл из stage
git restore --staged file.txt  # То же (новый синтаксис)
git revert commit_hash         # Отменить коммит (создать новый)
git reset --soft HEAD~1        # Отменить последний коммит (изменения остаются)
git reset --hard HEAD~1        # Отменить коммит и изменения (опасно!)
```

### Ресурсы

- [Pro Git Book](https://git-scm.com/book/ru/v2) — бесплатная книга на русском
- [Learn Git Branching](https://learngitbranching.js.org/?locale=ru_RU) — интерактивное обучение
- [Oh My Git!](https://ohmygit.org/) — игра для изучения Git
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
