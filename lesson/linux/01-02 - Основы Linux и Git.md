# Лекции 1-2: Основы Linux и Git

## История Linux

### Unix и его развитие
- **1969**: Разработка Unix в Bell Labs (Dennis Ritchie, Ken Thompson)
- **1983**: Проект GNU (Richard Stallman) - создание свободной Unix-подобной системы
- **1991**: Linus Torvalds создал ядро Linux
- Linux = ядро от Торвальдса + утилиты GNU = GNU/Linux

### Философия Unix
1. Простота - программы должны делать что-то одно, но хорошо
2. Модульность - программы работают вместе
3. Текстовые интерфейсы - универсальный формат обмена данными
4. Всё есть файл

## Дистрибутивы Linux

### Популярные семейства
- **Debian-based**: Debian, Ubuntu, Linux Mint
- **Red Hat-based**: RHEL, CentOS, Fedora
- **SUSE-based**: openSUSE, SUSE Linux Enterprise
- **Arch-based**: Arch Linux, Manjaro
- **Независимые**: Gentoo, Slackware

### Области применения
- Серверы и облачные вычисления
- Встраиваемые системы (Android)
- Суперкомпьютеры
- Десктопы и рабочие станции

## Файловая система Linux

### Структура директорий (FHS - Filesystem Hierarchy Standard)

```
/           # Корень файловой системы
├── bin/    # Основные исполняемые файлы (ls, cat, cp)
├── boot/   # Файлы загрузчика, ядро
├── dev/    # Файлы устройств
├── etc/    # Конфигурационные файлы системы
├── home/   # Домашние директории пользователей
├── lib/    # Системные библиотеки
├── media/  # Точки монтирования съёмных носителей
├── mnt/    # Временные точки монтирования
├── opt/    # Дополнительное ПО
├── proc/   # Виртуальная ФС (информация о процессах)
├── root/   # Домашняя директория root
├── sbin/   # Системные исполняемые файлы (для администрирования)
├── srv/    # Данные для сервисов
├── sys/    # Виртуальная ФС (информация об устройствах)
├── tmp/    # Временные файлы
├── usr/    # Пользовательские приложения и данные
└── var/    # Изменяемые данные (логи, кэш, спулы)
```

### Типы файлов
- `-` обычный файл
- `d` директория
- `l` символическая ссылка
- `c` символьное устройство
- `b` блочное устройство
- `p` именованный канал (pipe)
- `s` сокет

## Базовые команды Linux

### Навигация и просмотр

```bash
pwd                 # Показать текущую директорию
ls                  # Список файлов
ls -l               # Детальный список
ls -la              # Включая скрытые файлы
ls -lh              # Человекочитаемые размеры
cd /path            # Перейти в директорию
cd ~                # Перейти в домашнюю директорию
cd ..               # Перейти на уровень выше
cd -                # Вернуться в предыдущую директорию
```

### Работа с файлами и директориями

```bash
# Создание
mkdir dirname       # Создать директорию
mkdir -p a/b/c      # Создать вложенные директории
touch file.txt      # Создать пустой файл

# Копирование и перемещение
cp source dest      # Копировать файл
cp -r dir1 dir2     # Копировать директорию рекурсивно
mv source dest      # Переместить/переименовать

# Удаление
rm file             # Удалить файл
rm -r dirname       # Удалить директорию рекурсивно
rm -rf dirname      # Удалить без подтверждения (осторожно!)
rmdir dirname       # Удалить пустую директорию
```

### Просмотр содержимого файлов

```bash
cat file.txt        # Вывести весь файл
less file.txt       # Постраничный просмотр (q для выхода)
more file.txt       # Постраничный просмотр (старая версия)
head file.txt       # Первые 10 строк
head -n 20 file     # Первые 20 строк
tail file.txt       # Последние 10 строк
tail -f file.log    # Следить за изменениями в реальном времени
```

### Поиск

```bash
find /path -name "*.txt"        # Найти файлы по имени
find . -type f                  # Найти все файлы
find . -type d                  # Найти все директории
find . -size +100M              # Файлы больше 100 МБ

grep "pattern" file.txt         # Поиск строки в файле
grep -r "pattern" /path         # Рекурсивный поиск
grep -i "pattern" file          # Поиск без учёта регистра
grep -n "pattern" file          # С номерами строк
```

### Права доступа

```bash
chmod 755 file      # Изменить права (rwxr-xr-x)
chmod u+x file      # Добавить право на выполнение владельцу
chmod -R 644 dir    # Рекурсивно изменить права

chown user file     # Изменить владельца
chown user:group    # Изменить владельца и группу
chgrp group file    # Изменить группу
```

**Права доступа в числовом формате:**
- `r` (read) = 4
- `w` (write) = 2
- `x` (execute) = 1
- Пример: `755` = `rwxr-xr-x` (4+2+1, 4+1, 4+1)

### Информация о системе

```bash
whoami              # Текущий пользователь
hostname            # Имя хоста
uname -a            # Информация о системе
df -h               # Использование дисков
du -sh dir          # Размер директории
free -h             # Использование памяти
ps aux              # Список процессов
top                 # Мониторинг процессов в реальном времени
kill PID            # Завершить процесс
```

### Работа с текстом

```bash
echo "text"         # Вывести текст
echo "text" > file  # Записать в файл (перезапись)
echo "text" >> file # Добавить в конец файла

wc file.txt         # Подсчёт строк, слов, байт
wc -l file          # Только количество строк

sort file.txt       # Сортировать строки
uniq file.txt       # Удалить дубликаты (требует сортировки)
cut -d: -f1 file    # Вырезать поля (разделитель :)
```

### Pipes и перенаправление

```bash
command1 | command2         # Передать вывод команды 1 в команду 2
command > file              # Перенаправить вывод в файл
command >> file             # Добавить вывод в файл
command 2> error.log        # Перенаправить ошибки
command &> all.log          # Перенаправить всё
command < input.txt         # Читать ввод из файла
```

### Архивы и сжатие

```bash
# tar (архивирование)
tar -cvf archive.tar files  # Создать архив
tar -xvf archive.tar        # Распаковать архив
tar -tvf archive.tar        # Просмотреть содержимое

# Со сжатием
tar -czvf archive.tar.gz files  # Создать и сжать (gzip)
tar -xzvf archive.tar.gz        # Распаковать gzip
tar -cjvf archive.tar.bz2 files # Создать и сжать (bzip2)
tar -xjvf archive.tar.bz2       # Распаковать bzip2

# Только сжатие
gzip file           # Сжать файл (создаёт file.gz)
gunzip file.gz      # Распаковать
```

## Пользователи и группы

```bash
# Управление пользователями
sudo adduser username       # Создать пользователя
sudo deluser username       # Удалить пользователя
sudo passwd username        # Изменить пароль

# Группы
groups                      # Показать группы текущего пользователя
sudo usermod -aG group user # Добавить пользователя в группу

# Переключение пользователя
su username                 # Переключиться на пользователя
sudo command                # Выполнить команду от root
sudo -i                     # Открыть root shell
```

## Сеть

```bash
ip addr                     # Показать IP-адреса
ping host                   # Проверить доступность хоста
wget url                    # Скачать файл
curl url                    # Получить содержимое URL
ssh user@host               # Подключиться по SSH
scp file user@host:/path    # Скопировать файл по SSH
```

## Управление пакетами

### Debian/Ubuntu (apt)
```bash
sudo apt update             # Обновить список пакетов
sudo apt upgrade            # Обновить пакеты
sudo apt install package    # Установить пакет
sudo apt remove package     # Удалить пакет
sudo apt search keyword     # Поиск пакета
```

### Red Hat/CentOS (yum/dnf)
```bash
sudo yum update
sudo yum install package
sudo yum remove package
```

## Системные службы (systemd)

```bash
sudo systemctl start service    # Запустить службу
sudo systemctl stop service     # Остановить службу
sudo systemctl restart service  # Перезапустить службу
sudo systemctl status service   # Статус службы
sudo systemctl enable service   # Автозапуск при загрузке
sudo systemctl disable service  # Отключить автозапуск
```

## Полезные советы

### Горячие клавиши в терминале
- `Ctrl+C` - прервать команду
- `Ctrl+D` - EOF / выход из shell
- `Ctrl+L` - очистить экран (или команда `clear`)
- `Ctrl+A` - в начало строки
- `Ctrl+E` - в конец строки
- `Ctrl+R` - поиск в истории команд
- `Tab` - автодополнение

### Специальные переменные
- `~` - домашняя директория
- `.` - текущая директория
- `..` - родительская директория
- `$HOME` - домашняя директория
- `$PATH` - пути поиска исполняемых файлов

### История команд
```bash
history             # Показать историю
!123                # Выполнить команду номер 123
!!                  # Повторить последнюю команду
!$                  # Последний аргумент предыдущей команды
```

## Основы Git

### Что такое Git?
- Распределённая система контроля версий
- Создана Linus Torvalds в 2005 году
- Отслеживает изменения в файлах
- Позволяет работать в команде
- Хранит полную историю проекта

### Основные концепции

**Working Directory** → **Staging Area** → **Repository**

- **Working Directory**: рабочая директория с файлами
- **Staging Area (Index)**: промежуточная область для подготовки коммита
- **Repository**: база данных с историей коммитов

### Первоначальная настройка

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git config --list           # Просмотр настроек
```

### Базовые команды Git

```bash
# Инициализация и клонирование
git init                    # Создать новый репозиторий
git clone url               # Клонировать репозиторий

# Статус и информация
git status                  # Статус файлов
git log                     # История коммитов
git log --oneline           # Краткая история
git log --graph --all       # Граф веток
git diff                    # Изменения в рабочей директории
git diff --staged           # Изменения в staging area

# Работа с файлами
git add file.txt            # Добавить файл в staging
git add .                   # Добавить все изменения
git commit -m "Message"     # Создать коммит
git commit -am "Message"    # Add + commit для отслеживаемых файлов

# Отмена изменений
git restore file            # Отменить изменения в файле
git restore --staged file   # Убрать из staging
git reset HEAD~1            # Отменить последний коммит (сохранить изменения)
git reset --hard HEAD~1     # Отменить коммит и изменения

# Ветки
git branch                  # Список веток
git branch name             # Создать ветку
git checkout name           # Переключиться на ветку
git checkout -b name        # Создать и переключиться
git switch name             # Переключиться (новый синтаксис)
git merge branch            # Слить ветку в текущую
git branch -d name          # Удалить ветку

# Удалённые репозитории
git remote -v               # Список удалённых репозиториев
git remote add origin url   # Добавить удалённый репозиторий
git push origin main        # Отправить изменения
git pull origin main        # Получить изменения
git fetch                   # Получить без слияния
```

### .gitignore

Файл `.gitignore` указывает, какие файлы игнорировать:

```
# Комментарий
*.log           # Все .log файлы
/temp           # Директория temp в корне
node_modules/   # Директория node_modules
*.tmp           # Все временные файлы
!important.log  # Исключение: не игнорировать
```

### Типичный рабочий процесс

```bash
# 1. Клонировать или инициализировать
git clone url
# или
git init

# 2. Создать ветку для новой функции
git checkout -b feature-name

# 3. Внести изменения в файлы
# редактировать файлы...

# 4. Добавить и зафиксировать
git add .
git status
git commit -m "Описание изменений"

# 5. Отправить в удалённый репозиторий
git push origin feature-name

# 6. Слить с основной веткой
git checkout main
git merge feature-name
git push origin main
```

### Хорошие практики

1. **Частые коммиты** - делайте коммиты часто и логически
2. **Понятные сообщения** - пишите осмысленные описания коммитов
3. **Используйте ветки** - для каждой функции/исправления
4. **Не коммитьте лишнее** - используйте .gitignore
5. **Синхронизируйте часто** - pull/push регулярно
6. **Проверяйте перед коммитом** - используйте `git status` и `git diff`

### Структура хорошего коммита

```
Краткое описание (до 50 символов)

Более подробное описание (если нужно):
- Что изменено
- Почему изменено
- Как это влияет на проект
```

---

## Справочные ресурсы

- [Linux Command Line Basics](https://ubuntu.com/tutorials/command-line-for-beginners)
- [Git Documentation](https://git-scm.com/doc)
- [Linux Journey](https://linuxjourney.com/)
- [Explain Shell](https://explainshell.com/) - объяснение команд

---

# ЧАСТЬ 2: ПРОДВИНУТЫЕ ТЕМЫ LINUX

## Shell и Bash

### Что такое Shell?
- **Shell** - интерпретатор командной строки
- Посредник между пользователем и ядром Linux
- Популярные shells: Bash, Zsh, Fish, Ksh

### Bash (Bourne Again Shell)
- Стандартный shell в большинстве дистрибутивов Linux
- Расширенная версия оригинального Bourne shell (sh)

### Переменные окружения

```bash
# Просмотр переменных
env                     # Все переменные окружения
echo $HOME              # Домашняя директория
echo $PATH              # Пути поиска программ
echo $USER              # Имя пользователя
echo $SHELL             # Текущий shell

# Установка переменных
VARIABLE="value"        # Локальная переменная
export VARIABLE="value" # Экспортировать в окружение
unset VARIABLE          # Удалить переменную

# Добавить в PATH
export PATH=$PATH:/new/path
```

### Конфигурационные файлы Bash

```bash
~/.bashrc               # Выполняется при запуске интерактивного shell
~/.bash_profile         # Выполняется при логине
~/.bash_logout          # Выполняется при выходе
/etc/profile            # Глобальный профиль системы
/etc/bash.bashrc        # Глобальный bashrc
```

### Алиасы (Aliases)

```bash
# Создание алиаса
alias ll='ls -la'
alias update='sudo apt update && sudo apt upgrade'
alias ..='cd ..'
alias ...='cd ../..'

# Просмотр алиасов
alias

# Удаление алиаса
unalias ll

# Постоянные алиасы - добавить в ~/.bashrc
echo "alias ll='ls -la'" >> ~/.bashrc
source ~/.bashrc        # Применить изменения
```

## Перенаправление и Pipes

### Перенаправление ввода/вывода

```bash
# Стандартные потоки
# 0 = stdin (стандартный ввод)
# 1 = stdout (стандартный вывод)
# 2 = stderr (стандартный вывод ошибок)

command > file          # Перенаправить stdout в файл (перезапись)
command >> file         # Добавить stdout в файл
command 2> error.log    # Перенаправить stderr
command &> all.log      # Перенаправить stdout и stderr
command 2>&1            # Перенаправить stderr в stdout
command < file          # Читать stdin из файла
command > /dev/null     # Игнорировать вывод

# Примеры
ls -la > listing.txt
cat file.txt | grep "error" > errors.txt
find / -name "*.conf" 2> /dev/null
```

### Pipes (Конвейеры)

```bash
command1 | command2     # Вывод команды1 → ввод команды2

# Примеры
ls -la | grep "txt"                      # Найти .txt файлы
cat /var/log/syslog | grep error | wc -l # Подсчитать ошибки
ps aux | sort -k 3 -nr | head -5        # Топ-5 процессов по CPU
history | grep ssh                       # Поиск в истории
```

### Команда tee

```bash
# Вывод одновременно на экран и в файл
command | tee file.txt
command | tee -a file.txt   # С добавлением

# Пример
ls -la | tee listing.txt | grep "txt"
```

## Обработка текста

### grep - поиск по шаблону

```bash
grep "pattern" file             # Базовый поиск
grep -i "pattern" file          # Без учёта регистра
grep -r "pattern" /path         # Рекурсивный поиск
grep -n "pattern" file          # С номерами строк
grep -v "pattern" file          # Инвертировать (исключить)
grep -c "pattern" file          # Подсчитать совпадения
grep -A 3 "pattern" file        # 3 строки после
grep -B 3 "pattern" file        # 3 строки до
grep -C 3 "pattern" file        # 3 строки до и после
grep -E "regex" file            # Расширенные регулярные выражения
grep -w "word" file             # Только целые слова

# Примеры
grep -r "error" /var/log
grep -i "failed" /var/log/auth.log
ps aux | grep apache
```

### sed - потоковый редактор

```bash
# Замена текста
sed 's/old/new/' file           # Заменить первое вхождение в каждой строке
sed 's/old/new/g' file          # Заменить все вхождения
sed 's/old/new/gi' file         # Без учёта регистра
sed -i 's/old/new/g' file       # Изменить файл на месте

# Удаление строк
sed '5d' file                   # Удалить 5-ю строку
sed '1,3d' file                 # Удалить строки 1-3
sed '/pattern/d' file           # Удалить строки с pattern

# Вывод строк
sed -n '5p' file                # Вывести только 5-ю строку
sed -n '10,20p' file            # Вывести строки 10-20

# Примеры
sed 's/foo/bar/g' input.txt > output.txt
sed -i 's/127.0.0.1/localhost/g' /etc/hosts
```

### awk - обработка текста и данных

```bash
# Базовый синтаксис: awk 'pattern {action}' file

# Вывод колонок
awk '{print $1}' file           # Первая колонка
awk '{print $1, $3}' file       # 1-я и 3-я колонки
awk '{print $NF}' file          # Последняя колонка

# С разделителем
awk -F: '{print $1}' /etc/passwd    # Разделитель :

# Условия
awk '$3 > 1000' file                # Строки где 3-я колонка > 1000
awk '/pattern/ {print $1}' file     # Вывести 1-ю колонку если есть pattern

# Суммирование
awk '{sum += $1} END {print sum}' file

# Примеры
awk '{print $1, $4}' access.log
df -h | awk '{print $1, $5}'
ps aux | awk '{print $1, $11}'
awk -F: '{print $1}' /etc/passwd    # Список пользователей
```

### cut - вырезание частей строк

```bash
cut -d':' -f1 /etc/passwd       # 1-е поле с разделителем :
cut -d',' -f1,3 file.csv        # 1-е и 3-е поля
cut -c1-10 file                 # Символы 1-10
```

### sort - сортировка

```bash
sort file                       # Алфавитная сортировка
sort -r file                    # Обратная сортировка
sort -n file                    # Числовая сортировка
sort -k2 file                   # Сортировка по 2-й колонке
sort -u file                    # Уникальные строки
sort -t: -k3 -n /etc/passwd     # По 3-му полю, разделитель :
```

### uniq - удаление дубликатов

```bash
uniq file                       # Удалить последовательные дубликаты
uniq -c file                    # С подсчётом
uniq -d file                    # Только дубликаты
uniq -u file                    # Только уникальные

# Пример: подсчёт уникальных IP
cat access.log | awk '{print $1}' | sort | uniq -c | sort -rn
```

### tr - замена символов

```bash
tr 'a-z' 'A-Z' < file           # Перевести в верхний регистр
tr -d '0-9' < file              # Удалить цифры
tr -s ' ' < file                # Сжать пробелы
echo "hello" | tr 'a-z' 'A-Z'   # HELLO
```

## Процессы

### Просмотр процессов

```bash
ps                              # Процессы текущего пользователя
ps aux                          # Все процессы
ps aux | grep process_name      # Найти процесс
ps -ef                          # Полный формат
ps -u username                  # Процессы пользователя

top                             # Интерактивный мониторинг
htop                            # Улучшенная версия top (требует установки)

pgrep process_name              # Найти PID по имени
pidof process_name              # PID процесса
```

### Управление процессами

```bash
# Запуск процессов
command &                       # Запустить в фоне
nohup command &                 # Запустить с отключением от терминала

# Управление заданиями
jobs                            # Список фоновых заданий
fg %1                           # Перевести задание 1 на передний план
bg %1                           # Продолжить задание в фоне
Ctrl+Z                          # Приостановить текущий процесс

# Завершение процессов
kill PID                        # Послать SIGTERM (мягкое завершение)
kill -9 PID                     # Послать SIGKILL (принудительное)
kill -15 PID                    # SIGTERM (по умолчанию)
killall process_name            # Завершить все процессы с именем
pkill process_name              # То же самое

# Приоритеты
nice -n 10 command              # Запустить с приоритетом 10
renice -n 5 -p PID              # Изменить приоритет процесса
```

### Мониторинг системы

```bash
top                             # Мониторинг процессов
uptime                          # Время работы системы и нагрузка
free -h                         # Использование памяти
df -h                           # Использование дисков
du -sh /path                    # Размер директории
iostat                          # Статистика I/O
vmstat                          # Статистика виртуальной памяти
netstat -tuln                   # Сетевые соединения
ss -tuln                        # Сокеты (замена netstat)
lsof                            # Открытые файлы
```

## Скрипты Bash

### Создание скрипта

```bash
#!/bin/bash
# Это комментарий

echo "Hello, World!"
```

### Переменные

```bash
#!/bin/bash

# Объявление переменных
NAME="John"
AGE=30

# Использование переменных
echo "Name: $NAME"
echo "Age: ${AGE}"

# Ввод от пользователя
read -p "Enter your name: " USERNAME
echo "Hello, $USERNAME"

# Аргументы командной строки
echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "All arguments: $@"
echo "Number of arguments: $#"
```

### Условные операторы

```bash
#!/bin/bash

# If-else
if [ "$1" -gt 10 ]; then
    echo "Больше 10"
elif [ "$1" -eq 10 ]; then
    echo "Равно 10"
else
    echo "Меньше 10"
fi

# Операторы сравнения чисел
# -eq (равно), -ne (не равно)
# -gt (больше), -ge (больше или равно)
# -lt (меньше), -le (меньше или равно)

# Операторы для строк
if [ "$STRING" = "hello" ]; then
    echo "Привет"
fi
# = (равно), != (не равно)
# -z (пустая строка), -n (непустая строка)

# Проверка файлов
if [ -f "/path/to/file" ]; then
    echo "Файл существует"
fi
# -f (файл), -d (директория)
# -e (существует), -r (читаемый)
# -w (записываемый), -x (исполняемый)

# Логические операторы
if [ "$A" -gt 5 ] && [ "$B" -lt 10 ]; then
    echo "Оба условия верны"
fi
# && (И), || (ИЛИ), ! (НЕ)
```

### Циклы

```bash
#!/bin/bash

# For loop
for i in 1 2 3 4 5; do
    echo "Number: $i"
done

# For loop с диапазоном
for i in {1..10}; do
    echo $i
done

# For loop по файлам
for file in *.txt; do
    echo "Processing $file"
done

# While loop
counter=1
while [ $counter -le 5 ]; do
    echo "Counter: $counter"
    ((counter++))
done

# Until loop
counter=1
until [ $counter -gt 5 ]; do
    echo "Counter: $counter"
    ((counter++))
done

# Чтение файла построчно
while IFS= read -r line; do
    echo "Line: $line"
done < file.txt
```

### Функции

```bash
#!/bin/bash

# Объявление функции
function greet() {
    echo "Hello, $1!"
}

# Или так
say_goodbye() {
    echo "Goodbye, $1!"
}

# Вызов функций
greet "World"
say_goodbye "Friend"

# Возврат значения
add_numbers() {
    result=$(($1 + $2))
    echo $result
}

sum=$(add_numbers 5 3)
echo "Sum: $sum"
```

### Примеры скриптов

#### Резервное копирование

```bash
#!/bin/bash
# backup.sh - Скрипт резервного копирования

SOURCE_DIR="/home/user/documents"
BACKUP_DIR="/backup"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_FILE="backup_$DATE.tar.gz"

echo "Создание резервной копии..."
tar -czf "$BACKUP_DIR/$BACKUP_FILE" "$SOURCE_DIR"

if [ $? -eq 0 ]; then
    echo "Резервная копия создана: $BACKUP_FILE"
else
    echo "Ошибка при создании резервной копии"
    exit 1
fi
```

#### Проверка доступности сервера

```bash
#!/bin/bash
# check_server.sh - Проверка доступности сервера

HOST="example.com"
PING_COUNT=4

if ping -c $PING_COUNT $HOST > /dev/null 2>&1; then
    echo "$HOST доступен"
    exit 0
else
    echo "$HOST недоступен"
    exit 1
fi
```

#### Мониторинг использования диска

```bash
#!/bin/bash
# disk_check.sh - Проверка использования диска

THRESHOLD=80
USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')

if [ $USAGE -gt $THRESHOLD ]; then
    echo "ВНИМАНИЕ: Использование диска $USAGE% превышает порог $THRESHOLD%"
    # Отправить уведомление
    # mail -s "Disk Usage Alert" admin@example.com
else
    echo "Использование диска: $USAGE% - OK"
fi
```

## Права доступа и безопасность

### Расширенные права

```bash
# SUID (Set User ID) - выполнение от имени владельца
chmod u+s file              # Установить SUID
chmod 4755 file             # То же самое числом

# SGID (Set Group ID) - выполнение от имени группы
chmod g+s directory         # Установить SGID
chmod 2755 directory        # То же самое числом

# Sticky bit - только владелец может удалять файлы
chmod +t directory          # Установить sticky bit
chmod 1755 directory        # То же самое числом

# Примеры
ls -l /usr/bin/passwd       # -rwsr-xr-x (SUID установлен)
ls -ld /tmp                 # drwxrwxrwt (sticky bit)
```

### ACL (Access Control Lists)

```bash
# Установить ACL
setfacl -m u:username:rwx file      # Права для пользователя
setfacl -m g:groupname:rx file      # Права для группы

# Просмотр ACL
getfacl file

# Удалить ACL
setfacl -x u:username file
setfacl -b file                     # Удалить все ACL

# Рекурсивно
setfacl -R -m u:username:rwx directory
```

### sudo и привилегии

```bash
# Выполнить команду от root
sudo command

# Переключиться на root
sudo -i
sudo su

# Выполнить от имени другого пользователя
sudo -u username command

# Редактировать sudoers
sudo visudo

# Проверить права sudo
sudo -l
```

### Конфигурация sudoers

```bash
# /etc/sudoers

# Разрешить пользователю все команды
username ALL=(ALL:ALL) ALL

# Без запроса пароля
username ALL=(ALL) NOPASSWD: ALL

# Только определённые команды
username ALL=(ALL) /usr/bin/apt, /usr/bin/systemctl

# Группа
%groupname ALL=(ALL:ALL) ALL
```

## Сеть

### Сетевые команды

```bash
# Информация о сети
ip addr show                # IP-адреса интерфейсов
ip link show                # Сетевые интерфейсы
ip route show               # Таблица маршрутизации
ifconfig                    # Устаревшая команда (если установлена)

# Проверка соединения
ping host                   # ICMP ping
ping -c 4 host              # 4 пакета
traceroute host             # Маршрут до хоста
mtr host                    # Комбинация ping и traceroute

# DNS
nslookup domain             # DNS запрос
dig domain                  # Детальная DNS информация
host domain                 # Простой DNS запрос

# Сокеты и соединения
netstat -tuln               # Прослушиваемые порты
netstat -tulnp              # С именами программ
ss -tuln                    # Современная замена netstat
ss -tulnp                   # С процессами
lsof -i :80                 # Что использует порт 80

# Скачивание
wget url                    # Скачать файл
wget -c url                 # Продолжить прерванную загрузку
curl url                    # Получить содержимое
curl -O url                 # Скачать файл
curl -I url                 # Только заголовки
```

### Настройка сети

```bash
# Включить/выключить интерфейс
sudo ip link set eth0 up
sudo ip link set eth0 down

# Установить IP-адрес
sudo ip addr add 192.168.1.100/24 dev eth0
sudo ip addr del 192.168.1.100/24 dev eth0

# Добавить маршрут
sudo ip route add 10.0.0.0/24 via 192.168.1.1
sudo ip route del 10.0.0.0/24

# Перезапуск сети (зависит от системы)
sudo systemctl restart networking
sudo systemctl restart NetworkManager
```

### SSH

```bash
# Подключение
ssh user@host
ssh -p 2222 user@host           # Нестандартный порт

# Копирование файлов
scp file.txt user@host:/path    # На удалённый хост
scp user@host:/path/file.txt .  # С удалённого хоста
scp -r directory user@host:~    # Рекурсивно

# SSH ключи
ssh-keygen                      # Создать ключ
ssh-keygen -t rsa -b 4096       # RSA 4096 бит
ssh-copy-id user@host           # Скопировать публичный ключ

# SSH туннели
ssh -L 8080:localhost:80 user@host  # Локальный порт-форвардинг
ssh -R 8080:localhost:80 user@host  # Удалённый порт-форвардинг
ssh -D 1080 user@host               # SOCKS прокси

# SSH конфигурация (~/.ssh/config)
Host myserver
    HostName server.example.com
    User username
    Port 2222
    IdentityFile ~/.ssh/id_rsa
```

### Firewall (ufw)

```bash
# Управление ufw
sudo ufw status                 # Статус
sudo ufw enable                 # Включить
sudo ufw disable                # Выключить

# Правила
sudo ufw allow 22               # Разрешить порт 22
sudo ufw allow ssh              # То же самое
sudo ufw allow 80/tcp           # Разрешить TCP/80
sudo ufw allow from 192.168.1.0/24  # Разрешить подсеть
sudo ufw deny 25                # Запретить порт

# Удаление правил
sudo ufw delete allow 80
sudo ufw status numbered        # Показать номера правил
sudo ufw delete 2               # Удалить правило номер 2

# Сброс
sudo ufw reset                  # Сбросить все правила
```

## Планировщики задач

### cron

```bash
# Редактировать crontab текущего пользователя
crontab -e

# Просмотр crontab
crontab -l

# Удалить crontab
crontab -r

# Формат crontab:
# * * * * * command
# │ │ │ │ │
# │ │ │ │ └─ День недели (0-7, 0 и 7 = воскресенье)
# │ │ │ └─── Месяц (1-12)
# │ │ └───── День месяца (1-31)
# │ └─────── Час (0-23)
# └───────── Минута (0-59)

# Примеры
0 2 * * * /path/to/backup.sh        # Каждый день в 2:00
*/15 * * * * /path/to/check.sh      # Каждые 15 минут
0 0 * * 0 /path/to/weekly.sh        # Каждое воскресенье в полночь
0 9 1 * * /path/to/monthly.sh       # 1-го числа каждого месяца в 9:00
@reboot /path/to/startup.sh         # При загрузке системы
@daily /path/to/daily.sh            # Один раз в день
```

### systemd timers

```bash
# Список таймеров
systemctl list-timers

# Создать timer unit (/etc/systemd/system/mytask.timer)
[Unit]
Description=My Task Timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target

# Создать service unit (/etc/systemd/system/mytask.service)
[Unit]
Description=My Task Service

[Service]
ExecStart=/path/to/script.sh

# Включить таймер
sudo systemctl enable mytask.timer
sudo systemctl start mytask.timer
```

## Логи

### Системные логи

```bash
# Основные логи
/var/log/syslog             # Системный лог (Debian/Ubuntu)
/var/log/messages           # Системный лог (RHEL/CentOS)
/var/log/auth.log           # Аутентификация (Debian/Ubuntu)
/var/log/secure             # Аутентификация (RHEL/CentOS)
/var/log/kern.log           # Ядро
/var/log/dmesg              # Загрузка системы
/var/log/apache2/           # Apache
/var/log/nginx/             # Nginx

# Просмотр логов
tail -f /var/log/syslog     # Следить за логом
tail -n 50 /var/log/syslog  # Последние 50 строк
grep "error" /var/log/syslog
```

### journalctl (systemd)

```bash
# Просмотр журнала
journalctl                      # Весь журнал
journalctl -f                   # Следить в реальном времени
journalctl -n 50                # Последние 50 строк
journalctl -p err               # Только ошибки
journalctl -u service.service   # Логи службы
journalctl --since "1 hour ago" # За последний час
journalctl --since today        # За сегодня
journalctl -k                   # Логи ядра
journalctl --disk-usage         # Использование диска
journalctl --vacuum-time=2d     # Удалить старше 2 дней
```

## Полезные советы

### Поиск команд в истории

```bash
history                     # Показать историю
history | grep ssh          # Поиск в истории
!123                        # Выполнить команду 123
!!                          # Повторить последнюю команду
sudo !!                     # Повторить с sudo
!$                          # Последний аргумент
Ctrl+R                      # Интерактивный поиск
```

### Работа с несколькими командами

```bash
command1 ; command2         # Выполнить последовательно
command1 && command2        # Выполнить 2, если 1 успешна
command1 || command2        # Выполнить 2, если 1 неуспешна
(command1 ; command2)       # Выполнить в подоболочке
```

### Расширения имён файлов

```bash
ls *.txt                    # Все .txt файлы
ls file?.txt                # file1.txt, fileA.txt
ls file[123].txt            # file1.txt, file2.txt, file3.txt
ls {a,b,c}.txt              # a.txt, b.txt, c.txt
ls file{1..5}.txt           # file1.txt до file5.txt
```

### Быстрое редактирование

```bash
# Горячие клавиши в терминале
Ctrl+A                      # В начало строки
Ctrl+E                      # В конец строки
Ctrl+K                      # Удалить до конца строки
Ctrl+U                      # Удалить до начала строки
Ctrl+W                      # Удалить слово
Ctrl+Y                      # Вставить удалённое
Alt+F                       # Слово вперёд
Alt+B                       # Слово назад
```

## Практические задания

1. **Создайте скрипт резервного копирования** домашней директории
2. **Настройте cron** для автоматического выполнения скрипта
3. **Создайте алиасы** для часто используемых команд
4. **Напишите скрипт** для мониторинга доступности сервера
5. **Настройте SSH** с ключевой аутентификацией
6. **Изучите логи** системы и найдите ошибки за последний час

## Дополнительные ресурсы

- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
- [Bash Hackers Wiki](https://wiki.bash-hackers.org/)
- [Greg's Wiki - Bash Guide](https://mywiki.wooledge.org/BashGuide)
