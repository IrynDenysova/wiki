# Bash обработка ошибок — шпаргалка

Коротко: настройте скрипт на немедленное завершение при ошибках, дополните `trap`-ами и логикой проверки команд.
#bash, #error-handling, #shell
---

## Настройки на уровне скрипта

```bash
set -euo pipefail
IFS=$'\n\t'
```

- `-e` (errexit) — выход, если команда возвращает ненулевой код.
- `-u` — ошибка при чтении unset переменной.
- `-o pipefail` — код конвейера = код последней команды, которая завершилась с ошибкой.

## Проверка команд

```bash
if ! command -v curl &>/dev/null; then
  echo "curl missing" >&2
  exit 1
fi
```

Используйте `||` и `&&` для inline-логики: `cmd || exit 1`.

## Трапы и cleanup

```bash
cleanup() {
  rm -f "$tmp"
}
trap cleanup EXIT
```

Можно ловить сигналы: `trap 'echo interrupted; exit 1' INT TERM`.

## Логирование ошибок

```bash
warn() { echo "WARN: $*" >&2; }
fail() {
  echo "ERROR: $*" >&2
  exit 1
}
```

Выводите ошибки в stderr и используйте `fail` в точках отказа.

## Контроль кода возврата

- После `cmd` можно взять `$?` или использовать `|| fail`.
- Для `for`/`while` циклов аккуратно проверяйте каждые команды.
- Добавьте `return 1` в helper-функциях при ошибке.

## Советы

- `set -x` включайте локально в блоках, чтобы выводить только нужные команды (см. debugging).
- Всегда проверяйте результат `trap` и возвращаемый код.
- В `CI` лучше выводить `set -x` + `date` + `env` для диагностики.

## Ресурсы

- https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
- `help set`, `man bash`

---

Вернуться к [главной странице](../README.md).
