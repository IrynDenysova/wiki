# Конспект Linux + Git (занятия 3–12) — кратко и по делу

## Содержание
- [Linux](#linux)
  - [Потоки, перенаправления, пайпы](#потоки-перенаправления-пайпы)
  - [Редакторы: vi/vim и nano](#редакторы-vivim-и-nano)
  - [SSH и SCP](#ssh-и-scp)
  - [Переменные окружения и PATH](#переменные-окружения-и-path)
  - [Процессы и ресурсы](#процессы-и-ресурсы)
  - [Права на файлы и chmod](#права-на-файлы-и-chmod)
  - [Поиск файлов: find и locate](#поиск-файлов-find-и-locate)
  - [Bash-скрипты и циклы](#bash-скрипты-и-циклы)
- [Git](#git)
  - [База: репозиторий, staging, commit, remote](#база-репозиторий-staging-commit-remote)
  - [Ветки, remote-ветки, detached HEAD](#ветки-remote-ветки-detached-head)
  - [.gitignore (локальный и глобальный)](#gitignore-локальный-и-глобальный)
  - [stash](#stash)
  - [merge vs rebase](#merge-vs-rebase)
  - [amend / reset / checkout / revert](#amend--reset--checkout--revert)
  - [Мини-шпаргалка Git (must-have)](#мини-шпаргалка-git-must-have)

---

# Linux

## Потоки, перенаправления, пайпы

### 3 стандартных потока (FD)
- **stdin (0)** — ввод
- **stdout (1)** — обычный вывод
- **stderr (2)** — ошибки

### Перенаправления
Записать (перезаписать):
```bash
command > out.txt
```

Дописать в конец:
```bash
command >> out.txt
```

Ввод из файла:
```bash
command < in.txt
```

Ошибки отдельно:
```bash
command 2> err.txt
```

stdout + stderr в один файл:
```bash
command > all.txt 2>&1
```

Игнорировать ошибки:
```bash
command 2>/dev/null
```

### Pipe `|`
stdout одной команды становится stdin следующей:
```bash
command1 | command2 | command3
```

Полезные связки:
```bash
history | tail -3
df -h | grep -w / | awk '{print $5}' | sed 's/%//g'
cat /etc/group | wc -l
```

---

## Редакторы: vi/vim и nano

### vi/vim: режимы и минимум команд
- `i` — вставка (Insert)
- `Esc` — командный режим
- `:w` сохранить, `:q` выйти, `:wq` сохранить+выйти, `:q!` выйти без сохранения
- `ZZ` — сохранить+выйти (быстро)
- `dd` удалить строку, `yy` копировать строку, `p` вставить, `u` undo
- `/text` поиск, `n` следующее совпадение
- `G` — в конец файла

### nano: просто
- редактирование сразу
- выход: `Ctrl + X`

---

## SSH и SCP

### Ключи
Генерация (типично один раз):
```bash
ssh-keygen
```

Файлы по умолчанию:
- приватный: `~/.ssh/id_rsa` (или `id_ed25519`)
- публичный: `~/.ssh/id_rsa.pub` (или `id_ed25519.pub`)

Показать публичный ключ:
```bash
cat ~/.ssh/id_ed25519.pub
```

### Подключение по SSH
```bash
ssh user@host
ssh -i ~/.ssh/id_ed25519 user@host
```

### SCP (копирование поверх SSH)
Скачать файл с сервера в текущую папку:
```bash
scp -i ~/.ssh/id_ed25519 user@host:/path/to/file .
```

Загрузить файл на сервер:
```bash
scp file.txt user@host:/path/to/dir/
```

---

## Переменные окружения и PATH

Показать все переменные:
```bash
env
```

Установить переменную в текущей сессии:
```bash
export MY_VAR=hello
echo $MY_VAR
```

Удалить:
```bash
unset MY_VAR
```

### PATH
Показать:
```bash
echo $PATH
```

Добавить каталог в начало PATH (на сессию):
```bash
export PATH=/my/bin:$PATH
```

---

## Процессы и ресурсы

### top — интерактивно
```bash
top
```

### ps — снимок процессов
```bash
ps -ef
ps aux
```

Найти процесс:
```bash
ps -ef | grep sshd
```

### kill — сигналы
Мягко завершить (по умолчанию SIGTERM 15):
```bash
kill PID
```

Жёстко (SIGKILL 9 — без шанса “сохраниться”):
```bash
kill -9 PID
```

По имени процесса:
```bash
killall nginx
```

---

## Права на файлы и chmod

Вид прав:
```bash
ls -la
# -rwxr-xr--
```

Схема: `type | u(rwx) | g(rwx) | o(rwx)`

### chmod (цифрами)
- `7=rwx`, `6=rw-`, `5=r-x`, `4=r--`, `0=---`

Примеры:
```bash
chmod 755 script.sh   # rwx r-x r-x
chmod 644 file.txt    # rw- r-- r--
```

### chmod (символами)
```bash
chmod +x script.sh        # добавить execute всем
chmod u+x script.sh       # execute владельцу
chmod go-w file.txt       # убрать write у группы и остальных
chmod -R 755 dir/         # рекурсивно
```

---

## Поиск файлов: find и locate

### find (ищет “по факту” на диске)
```bash
find /path -name "*.txt"
find /path -iname "*.JPG"      # без регистра
find /path -type f             # только файлы
find /path -type d             # только директории
find /path -size +1M           # больше 1MB
find /path -mtime -5           # изменены < 5 дней назад
```

Действие для каждого:
```bash
find /path -type f -name "*.sh" -exec chmod +x {} \;
```

Удаление (осторожно):
```bash
find /path -type f -name "*.old" -delete
```

Ошибки в /dev/null:
```bash
find /home -name "*.log" 2>/dev/null
```

### locate (быстро, по базе)
```bash
sudo updatedb
locate passwd
```

---

## Bash-скрипты и циклы

### Минимальный скрипт
```bash
#!/bin/bash
echo "Hello"
date
```

Сделать исполняемым и запустить:
```bash
chmod +x script.sh
./script.sh
```

### Переменные (без пробелов!)
```bash
NAME="Viktor"
echo "Hello $NAME"
```

### Текущая директория
```bash
pwd
```

### Цикл for
```bash
for i in {1..5}; do
  echo "$i"
done
```

### Цикл while
```bash
i=1
while [ $i -le 5 ]; do
  echo "$i"
  ((i++))
done
```

### Практичные куски
Поиск слова в логах:
```bash
grep -rn "error" /var/log 2>/dev/null
```

Вывести права файла “чисто”:
```bash
ls -l /etc/passwd | awk '{print $1}'
```

---

# Git

## База: репозиторий, staging, commit, remote

### 4 зоны Git
1) Working directory  
2) Staging (index)  
3) Local repo  
4) Remote repo (origin)

### Старт
Инициализация нового репозитория:
```bash
git init
```

Клонирование существующего:
```bash
git clone git@github.com:user/repo.git
```

Проверить состояние:
```bash
git status
```

Добавить в staging:
```bash
git add file.txt
git add .
```

Коммит:
```bash
git commit -m "message"
```

Лог:
```bash
git log --oneline --decorate
```

Отправить/забрать:
```bash
git push
git pull
```

Remote:
```bash
git remote -v
git remote add origin git@github.com:user/repo.git
```

---

## Ветки, remote-ветки, detached HEAD

Список веток:
```bash
git branch
git branch -a
```

Создать:
```bash
git branch feature
```

Переключиться:
```bash
git checkout feature
```

Создать и переключиться:
```bash
git checkout -b feature
```

Удалить:
```bash
git branch -d feature
git branch -D feature
```

### Remote-ветки
Обновить сведения:
```bash
git fetch --all
```

Создать локальную ветку, отслеживающую remote:
```bash
git checkout -b feature origin/feature
```

### Detached HEAD
Переход на конкретный коммит:
```bash
git checkout <commit_hash>
```

Если начал работу в detached HEAD — **сохранись в ветку**:
```bash
git checkout -b save-my-work
```

---

## .gitignore (локальный и глобальный)

Создать:
```bash
touch .gitignore
```

Типовые правила:
```gitignore
*.log
__pycache__/
.env
build/
```

Исключение (НЕ игнорировать):
```gitignore
!important.log
```

Глобальный ignore (для всех репозиториев — если нужно):
```bash
git config --global core.excludesfile ~/.gitignore_global
```

---

## stash
Спрятать незакоммиченные изменения:
```bash
git stash
```

Список:
```bash
git stash list
```

Вернуть и удалить из stash:
```bash
git stash pop
```

Вернуть, но оставить в stash:
```bash
git stash apply
```

---

## merge vs rebase

### merge
Сливает ветки, обычно создаёт merge-коммит:
```bash
git checkout main
git merge feature
```

### rebase
Переносит коммиты feature поверх main, делает историю линейной:
```bash
git checkout feature
git rebase main
```

### Золотое правило rebase
**Не делай rebase веток, которые уже используют другие люди (публичных).**  
Иначе придётся делать `push --force` и можно сломать историю коллегам.

---

## amend / reset / checkout / revert

### amend — поправить последний коммит
- поменять сообщение
- добавить забытые файлы

```bash
git add forgotten.txt
git commit --amend
```

### reset — сдвинуть HEAD назад (осторожно)
- `--soft` — оставить изменения staged
- `--mixed` (по умолчанию) — оставить изменения unstaged
- `--hard` — выкинуть изменения полностью

```bash
git reset --soft <commit>
git reset <commit>
git reset --hard <commit>
```

### checkout — переключения + восстановление файла
Восстановить файл из коммита:
```bash
git checkout <commit_hash> -- path/to/file
```

### revert — безопасно отменить коммит (новым коммитом)
```bash
git revert <commit_hash>
```

**Revert vs Reset:**  
- `revert` — безопасно для shared/main (история не переписывается)  
- `reset` — переписывает историю/указатели (опасно на общих ветках)

---

## Мини-шпаргалка Git (must-have)
```bash
git status
git add .
git commit -m "msg"
git log --oneline --decorate
git branch -a
git checkout -b feature
git fetch --all
git pull
git push -u origin <branch>

# игнор
touch .gitignore

# stash
git stash
git stash pop

# слияния
git merge feature
git rebase main

# исправить последний коммит
git commit --amend

# безопасная отмена
git revert <commit>
```
