# Урок 11. Работа со скриптами — практическая работа (часть 2)

## Ключевая идея
**Скрипт** — небольшая программа (файл с командами), которая выполняет последовательность действий автоматически.

---

## Задание 1 — скрипт `script_ВАШЕИМЯ.sh`

### Требования
Скрипт должен:
- вывести приветствие
- показать текущий каталог
- вывести список всех процессов
- показать текущую дату и время
- проверить наличие файлов/строк с ключевым словом `error` в `/var/log/`
- вывести содержимое `/etc/os-release`
- посчитать количество строк в `/etc/os-release`
- вывести последние 5 строк `/etc/os-release`
- вывести информацию о пользователях из `/etc/passwd` через `awk` в формате  
  `Имя пользователя: ..., Домашний каталог: ...`
- вывести сообщение о завершении

Потом:
- дать права на исполнение
- скопировать скрипт в `/tmp/`

### Пример решения
```bash
#!/bin/bash

echo "Привет! Этот скрипт покажет текущий каталог и список процессов."

echo "Текущий каталог:"
pwd

echo "Список всех процессов:"
ps -ef

echo "Текущая дата и время:"
date

echo "Файлы/строки, содержащие ключевое слово 'error' в /var/log/:"
grep -rn "error" /var/log/ 2>/dev/null

echo "Содержимое файла /etc/os-release:"
cat /etc/os-release

echo "Количество строк в /etc/os-release:"
wc -l /etc/os-release

echo "Последние 5 строк /etc/os-release:"
tail -n 5 /etc/os-release

echo "Информация о пользователях:"
awk -F ':' '{print "Имя пользователя: " $1 ", Домашний каталог: " $6}' /etc/passwd

echo "Скрипт успешно выполнен!"
```

### Команды после создания
```bash
chmod +x script_ВАШЕИМЯ.sh
cp script_ВАШЕИМЯ.sh /tmp/script_ВАШЕИМЯ.sh
```

---

## Задание 2 — разобрать скрипт (дата → файлы → папка → вывод)

### Скрипт (пример)
```bash
#!/bin/bash
#
DATE=`date '+%d-%m-%y'`

for i in {1..5}
do
  date +'%H-%M-%S' > File-$i.txt
  sleep 5
done

mkdir -p $DATE
cp File*.txt $DATE

for FILE in $DATE/*
do
  cat $FILE
done
```

### Что делает (по шагам)
1) `DATE=...` сохраняет текущую дату (день-месяц-год).  
2) Цикл `for` создаёт 5 файлов `File-1.txt ... File-5.txt`, в каждом — текущее время.  
3) `sleep 5` — пауза 5 секунд между созданием файлов.  
4) `mkdir -p $DATE` — создаёт папку с именем даты.  
5) `cp File*.txt $DATE` — копирует файлы в папку даты.  
6) Второй цикл выводит содержимое каждого файла.

### Улучшенная версия (современнее и безопаснее — с кавычками)
```bash
#!/bin/bash
DATE="$(date '+%d-%m-%y')"

for i in {1..5}; do
  date +'%H-%M-%S' > "File-$i.txt"
  sleep 5
done

mkdir -p "$DATE"
cp File*.txt "$DATE"

for FILE in "$DATE"/*; do
  cat "$FILE"
done
```

---

## Задание 2 (варианты) — циклы `for` и `while`

### Вариант с `for`
```bash
#!/bin/bash

for i in {1..5}
do
  echo "Iteration $i"
  touch "file_$i.txt"
  sleep 2
done

echo "All files created:"
ls -l file_*.txt
```

### Вариант с `while`
```bash
#!/bin/bash

COUNT=1
while [ $COUNT -le 5 ]
do
  echo "Iteration $COUNT"
  touch "file_$COUNT.txt"
  sleep 2
  ((COUNT++))
done

echo "All files created:"
ls -l file_*.txt
```

---

## Задание 3 — для каждого объекта определить: директория или файл

```bash
#!/bin/bash

CURRENT_DIR="$(pwd)"
echo "Привет! Этот скрипт покажет информацию о каждом файле в текущем каталоге."
cd "$CURRENT_DIR" || exit 1

for FILE in *
do
  if [ -d "$FILE" ]; then
    echo "$FILE - это директория"
  else
    echo "$FILE - это файл"
  fi
done

echo "Скрипт успешно выполнен!"
```

---

## Задание 4 — генерация случайных файлов (количество = аргумент)

### Идея
Скрипт принимает число `N` и создаёт `N` файлов со случайными именами/расширениями и случайным содержимым.

### Пример решения
```bash
#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Ошибка: не указано количество файлов. Используйте: $0 <количество_файлов>"
  exit 1
fi

NUM_FILES="$1"
mkdir -p generated_files

for ((i=1; i<=NUM_FILES; i++))
do
  FILE_NAME="generated_files/file_${i}-$(date '+%Y-%m-%d').$RANDOM"
  RANDOM_TEXT="$(head -c 100 /dev/urandom | base64 2>/dev/null | head -c 100)"
  echo "$RANDOM_TEXT" > "$FILE_NAME"
done

echo "Файлы успешно созданы!"
```

---

## Экспресс-опрос (ответы)
1) **Какая первая строка в скрипте и для чего?**  
   Обычно это **shebang**, например `#!/bin/bash` — показывает системе, каким интерпретатором выполнять скрипт.

2) **Что будет, если команда написана с ошибкой?**  
   По умолчанию bash **попробует выполнить дальше** (скрипт не обязан остановиться).  
   Чтобы “падать” при ошибках, часто добавляют режим:
   ```bash
   set -e
   ```
   (или `set -euo pipefail` в более строгих сценариях).

---

## Домашнее задание — `permission_checker.sh`
**Задача:** получить список прав на файлы внутри директории `/opt/ВАШАГРУППА` и если есть файлы `.sh`, добавить им право на исполнение.

### Рабочий вариант (наиболее простой)
```bash
#!/bin/bash

DIR="/opt/ВАШАГРУППА"

echo "Проверяю директорию: $DIR"
ls -la "$DIR"

# Добавляем право на исполнение для всех .sh файлов
find "$DIR" -type f -name "*.sh" -exec chmod +x {} \;

echo "Done."
```

### Чуть аккуратнее: выводить, что изменили
```bash
#!/bin/bash
DIR="/opt/ВАШАГРУППА"

echo "Список .sh перед изменениями:"
find "$DIR" -type f -name "*.sh" -exec ls -l {} \;

find "$DIR" -type f -name "*.sh" -exec chmod +x {} \;

echo "Список .sh после изменений:"
find "$DIR" -type f -name "*.sh" -exec ls -l {} \;
```

---

## Мини-шпаргалка по уроку
```bash
chmod +x script.sh
./script.sh
cp script.sh /tmp/

ps -ef
grep -rn "error" /var/log/ 2>/dev/null
cat /etc/os-release
wc -l /etc/os-release
tail -n 5 /etc/os-release
awk -F ':' '{print $1, $6}' /etc/passwd

find /opt/ВАШАГРУППА -type f -name "*.sh" -exec chmod +x {} \;
```
