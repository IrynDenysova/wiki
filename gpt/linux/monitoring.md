# Мониторинг / Процессы / Переменные среды — шпаргалка

Коротко: команда `monitoring` в Linux — это набор утилит для проверки загрузки CPU/памяти/дисков, аудита процессов и состояния окружения. Эта шпаргалка собирает базовые проверки ресурсов и полезные переменные среды.
#monitoring, #linux, #processes, #env
---

## Базовые проверки ресурсов

Вставьте эти команды в терминал, чтобы получить мгновенную картину системы:

- `free -h` — использование RAM и swap в удобных единицах, `-m` для мегабайт
- `free -m` — тот же вывод в мегабайтах
- `df -h` — занятость файловых систем по точкам монтирования
- `df -h /var` — показать только `/var`
- `cat /proc/cpuinfo` — подробности по ядрам, потокам, частотам
- `lscpu` — сводная таблица процессора
- `uptime` — аптайм и load average (1/5/15 минут)
- `vmstat 1 5` — каждые 1 сек 5 выборок по памяти, процессам и IO
- `iostat -xz 1` *(sysstat)* — загрузка дисков, очереди, проценты CPU
- `watch -n 1 'free -h'` — смотреть обновления каждые секунды
- `env` - Показать все переменные окружения текущего процесса

## Процессы и их аудит

- `top` / `htop` — интерактивные мониторы CPU/памяти
- `ps -eo pid,user,%cpu,%mem,stat,cmd --sort=-%cpu | head` — самые ресурсоёмкие
- `ps -ef --forest | head` — дерево процессов
- `pidstat -urd 1` *(sysstat)* — разбивка по PID, нагрузка на CPU/IO
- `pgrep nginx` / `pgrep -fl sshd` — найти PID по имени
- `pkill -HUP sshd` — послать сигнал процессам по шаблону
- `pstree -p` — визуальное дерево с PID
- `strace -p PID -s 80 -e trace=open` — трассировка системных вызовов (для дебага процессов)

## Журналирование и контекст

- `journalctl -b -p err` — ошибки текущего запуска (systemd)
- `dmesg | tail` — ядровые сообщения (память/драйверы)
- `sudo tail -f /var/log/syslog` — лог системы в реальном времени
- `watch -n 5 'ps -eo pid,cmd,%cpu,%mem --sort=-%mem | head'` — следить за ростом потребления

## Переменные среды (environment variables)

| Переменная | Что хранит | Как посмотреть |
|------------|------------|----------------|
| `PATH` | пути для поиска команд | `echo $PATH` или `printenv PATH` |
| `HOME` | домашняя директория пользователя | `echo $HOME` |
| `SHELL` | текущая шелл-программа (bash/zsh) | `echo $SHELL` |
| `USER`, `LOGNAME` | имя пользователя | `echo $USER` |
| `LANG`, `LC_ALL` | локаль/кодировка | `locale` или `echo $LANG` |
| `TERM` | тип терминала (например `xterm-256color`) | `echo $TERM` |
| `LD_LIBRARY_PATH` | каталоги для поиска shared libs | `echo $LD_LIBRARY_PATH` |
| `PS1` | приглашение (prompt) | `echo $PS1` |
| `EDITOR` | редактор по умолчанию для git/visudo | `echo $EDITOR` |
| `UMASK` | маска прав для new файлов | `umask` |

### Работа с переменными

```
export MYAPP_ENV=production    # задать переменную для сессии
env | grep MYAPP               # найти все settings по префиксу
set | grep -i path             # показать все переменные/функции с Path
unset MYAPP_ENV                # удалить
```

Для постоянных переменных добавьте строки в `~/.bashrc`, `~/.profile` или соответствующий конфиг shell.

## Советы по мониторингу

- Используйте `sar` (sysstat) для долгосрочного мониторинга и графиков (если установлен)
- Объединяйте вывод `vmstat`, `iostat` и `free` в скрипт `/usr/local/bin/check-resources` для быстрой диагностики
- При подозрении на утечку памяти проверяйте `smem`, `pmap` и `cat /proc/<PID>/status`
- Храните alias в `~/.bash_aliases`, например `alias mem='ps -eo pid,user,%mem,cmd --sort=-%mem | head'`
- Программируйте health-check через `watch`, `cron` + `systemd` таймеры, чтобы логировать скачки нагрузки

## Источники и справка

- `man free`, `man df`, `man ps`, `man journalctl`, `man env`
- Документация `procps-ng`: https://gitlab.com/procps-ng/procps
- `sysstat`: https://github.com/sysstat/sysstat

---

Вернуться к [главной странице](./README.md).
