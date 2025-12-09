# Урок 10. Ветви в Git + .gitignore + clone/fork + stash

## 0) План занятия
- Что такое ветви (branches) в Git  
- Основные операции с ветками  
- Переключение на удалённую ветку  
- Откреплённый HEAD (detached HEAD)  
- Файл `.gitignore` (локальный и глобальный)  
- `git clone` и `git fork`  
- `git stash` fileciteturn8file0turn8file1

---

## 1) Что такое ветви (branches) в Git
**Ветка** — это отдельная линия разработки: набор коммитов, расположенных в хронологическом порядке. Ветки позволяют работать над задачами параллельно и **не ломать main** до момента, когда изменения готовы. fileciteturn8file0turn8file1

### Основная ветка: master vs main
Исторически основная ветка называлась `master`, но всё чаще используется `main`. fileciteturn8file0turn8file1

### Виды веток (типовой смысл)
- **Master/Main** — стабильная основная ветка (часто релизы).  
- **Feature** — под новую функциональность (временная ветка, потом merge обратно).  
- **Bugfix** — под исправление ошибок, изоляция фикса.  
- **Release** — подготовка к выпуску версии. fileciteturn8file0turn8file1

### Зачем ветки
- **Управление версиями**: разные задачи — в разных ветках.
- **Коллаборация**: разработчики не мешают друг другу.
- **Изоляция изменений**: можно тестировать/проверять, не трогая main. fileciteturn8file0turn8file1

---

## 2) Основные операции с ветками (команды)

### 2.1. Просмотр веток
```bash
git branch         # список локальных веток
git branch --list  # то же самое
git branch -a      # локальные + удалённые (remote)
```
fileciteturn8file0turn8file1

### 2.2. Создание, переключение, удаление, переименование
Создать ветку (НЕ переключаясь):
```bash
git branch feature-1
```

Переключиться на ветку:
```bash
git checkout feature-1
```

Создать и сразу переключиться:
```bash
git checkout -b feature-2
```

Переименовать текущую ветку:
```bash
git branch -m new-name
```

Удалить ветку “безопасно” (Git не даст удалить, если там есть неслитые изменения):
```bash
git branch -d feature-1
```

Принудительное удаление:
```bash
git branch -D feature-1
```
fileciteturn8file0turn8file1

---

## 3) Переключение на удалённую ветку (remote branch)

### 3.1. Сначала забрать данные с remote
```bash
git fetch --all
```
fileciteturn8file0turn8file1

### 3.2. Переключение на удалённую ветку
В современных версиях Git переключение на remote-ветки часто выглядит так же, как на локальные (Git создаст локальную tracking branch автоматически):
```bash
git checkout <remotebranch>
```
fileciteturn8file0turn8file1

В старых версиях Git нужно было явно создать локальную ветку на основе remote:
```bash
git checkout -b <remotebranch> origin/<remotebranch>
```
fileciteturn8file0turn8file1

### 3.3. Вариант: создать локальную ветку и “прижать” к origin
```bash
git checkout -b <branchname>
git reset --hard origin/<branchname>
```
fileciteturn8file0turn8file1

---

## 4) Detached HEAD (откреплённый HEAD)

### 4.1. Что это
**Detached HEAD** — состояние, когда `HEAD` указывает **на конкретный коммит**, а не на ветку. fileciteturn8file0turn8file1

### 4.2. Когда появляется
- Когда вы переключаетесь на коммит по хэшу:
  ```bash
  git checkout <commit_hash>
  ```
fileciteturn8file0turn8file1

### 4.3. Чем опасно
Если в detached HEAD вы сделаете новые коммиты, а потом уйдёте на другую ветку и забудете хэш — можно “потерять” эти коммиты (они не принадлежат ветке). fileciteturn8file0turn8file1

**Правило безопасности:** если начал что-то менять в detached HEAD — создай ветку:
```bash
git checkout -b save-my-work
```

---

## 5) Файл `.gitignore`

### 5.1. Что это
`.gitignore` — текстовый файл, который задаёт, какие файлы/папки **не должны отслеживаться Git**. Полезно для временных файлов, локальных конфигов, бинарников и т.п. fileciteturn8file0turn8file1

### 5.2. Как создать
В корне репозитория:
```bash
touch .gitignore
```
или создать в редакторе и сохранить как `.gitignore`. fileciteturn8file0turn8file1

Можно скачать готовый пример (как в лекции):
```bash
curl -O https://raw.githubusercontent.com/aliaskov/bashscripts/master/.gitignore
```
fileciteturn8file0turn8file1

### 5.3. Синтаксис `.gitignore`
- `*` — любое количество символов
- `?` — один символ
- `[]` — символьный класс/диапазон
- `!` — исключение (НЕ игнорировать)
- `#` — комментарий fileciteturn8file0turn8file1

Примеры:
```gitignore
# игнорируем все .log
*.log

# игнорируем папку build/
build/

# но НЕ игнорируем важный лог
!important.log
```

### 5.4. Глобальный gitignore (для всех репозиториев)
Можно настроить единый файл игнорирования:
```bash
git config --global core.excludesfile .gitignore
```
fileciteturn8file0turn8file1

---

## 6) git clone и git fork

### 6.1. `git clone`
`git clone` — команда Git, которая создаёт **локальную копию удалённого репозитория** (файлы + история + ветки). По умолчанию remote называется `origin`. fileciteturn8file0turn8file1

Пример:
```bash
git clone git@github.com:user/repo.git
```

### 6.2. Fork
**Fork** — операция на платформе (GitHub/GitLab), которая создаёт **копию репозитория в вашем аккаунте**. Потом вы можете клонировать уже свой форк и работать независимо, а изменения предлагать обратно через PR (pull request). fileciteturn8file0turn8file1

---

## 7) git stash

### 7.1. Зачем нужен
Когда нужно срочно переключиться на другую ветку, но изменения ещё не готовы к коммиту — `git stash` временно “прячет” изменения в специальное хранилище (стек), возвращая рабочую копию к исходному состоянию. Потом изменения можно вернуть. fileciteturn8file0turn8file1

Мини-набор (как правило жизни):
```bash
git stash          # спрятать изменения
git stash list     # посмотреть список
git stash pop      # вернуть последние изменения и удалить их из stash
# (иногда используют git stash apply — вернуть, но оставить в stash)
```

---

## 8) Домашнее задание (из урока)
1) Создайте в GitHub новый репозиторий `git-branch`.  
2) Инициализируйте локальный репозиторий с таким же именем.  
3) Создайте и переключитесь на новую ветку `gitignore`.  
4) Добавьте в проект файл `.gitignore` (как пример из репозитория `bashscripts`).  
5) Сделайте коммит и отправьте ветку `gitignore` в репозиторий `git-branch`.  
6) Пришлите ссылку на репозиторий, где видно ветку `gitignore`. fileciteturn8file1

Подсказка-команды:
```bash
mkdir git-branch && cd git-branch
git init
git checkout -b gitignore
curl -O https://raw.githubusercontent.com/aliaskov/bashscripts/master/.gitignore
git add .gitignore
git commit -m "Add .gitignore"
git remote add origin git@github.com:<YOUR_GH>/git-branch.git
git push -u origin gitignore
```

---

## Мини-шпаргалка урока
```bash
git branch
git branch -a
git checkout -b <name>
git branch -d <name>
git branch -D <name>
git fetch --all
git checkout origin/<branch>        # (или создать локальную tracking-ветку)
git checkout <commit_hash>          # detached HEAD
git checkout -b <new_branch>        # сохранить работу из detached HEAD

# .gitignore
curl -O https://raw.githubusercontent.com/aliaskov/bashscripts/master/.gitignore
git config --global core.excludesfile .gitignore

# stash
git stash
git stash list
git stash pop
```
