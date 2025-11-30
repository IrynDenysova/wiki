# Bash и cron

Описание: шаблон для разворачивания cron-заданий, которые запускаются через `/usr/bin/env bash`, пишут лог и безопасно работают в строгом режиме.
#bash, #cron, #automation
---

## Входные предпосылки

1. `#!/usr/bin/env bash` + `set -euo pipefail` + `IFS=$'\n\t'` защищают от неожиданных значений.
2. Пропишите `PATH`, `HOME`, `LOG_DIR`, чтобы cron-окружение не зависело от переменных пользователя.
3. Логирование через `exec > >(tee -a "$LOG_FILE") 2>&1` сохраняет вывод команды и stderr.
4. Захват `flock`/`lockfile` предотвращает одновременное выполнение `cron`-задачи.
5. `trap 'rm -f /tmp/myjob.pid' EXIT` очищает временные файлы.

## Пример записи в crontab

```cron
0 2 * * * /usr/bin/env bash /opt/scripts/backup.sh
```

Добавьте `source /etc/default/myjob`, если требуются глобальные переменные. Помните, что `cron` не читает `~/.bashrc`, поэтому объявляйте все нужные переменные и `PATH` явно.

## Пример шаблона

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

LOCKFILE=/var/run/backup.lock
LOG_DIR=/var/log/backup
LOG_FILE="$LOG_DIR/$(date +%F).log"

mkdir -p "$LOG_DIR"
exec > >(tee -a "$LOG_FILE") 2>&1
exec 200>"$LOCKFILE"
flock -n 200 || exit 0

log() {
   printf '[%s] %s\n' "$(date +'%F %T')" "$*"
}

main() {
   log "Старт"
   # TODO: основной сценарий
   log "Финиш"
}

main "${@}"
```

## Рекомендации

- Вызывайте `command || fail` внутри функции `main`, чтобы ошибки фиксировались и записывались в лог.
- Используйте `flock`, чтобы избежать параллельного запуска, особенно если cron запускается чаще, чем выполняется задача.
- Делайте `crontab -l > /etc/cron.d/myjob` для сохранения версии задания в контролируемом файле.
- Включите `set -x` только при необходимости; лучше временно включать `bash -x` в отдельной копии скрипта, а затем отключать `set -x` перед деплоем.

## Полезные ссылки

- `man cron`
- `man 5 crontab`
- `man flock`

---


Вернуться к [главной странице](../README.md).
