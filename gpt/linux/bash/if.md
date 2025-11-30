# Bash `if` — шпаргалка

Коротко: `if` — основной способ ветвления: используйте `[[` для сложных проверок, `-f/-d` для файлов и `case` для шаблонов.
#bash, #if, #conditionals
---

## Стандартный синтаксис

```bash
if CONDITION; then
  commands
elif OTHER_CONDITION; then
  other
else
  fallback
fi
```

`CONDITION` может быть командой (код возврата 0 = успех) или выражением `[[ ]]`/`[ ]`.

## Различия `[[ ]]` vs `[ ]` vs `test`

- `[[ ... ]]` — встроенное, безопаснее с пробелами и glob-ами, позволяет `&&`, `||`, `=~`.
- `[ ... ]` / `test ...` — POSIX-совместно, требует пробелов вокруг `[`.
- Примеры:
  ```bash
  if [[ -f $file && $file == *.sh ]]; then
    echo shell
  fi
  ```
  ```bash
  if [ "$value" -gt 10 ]; then
    echo big
  fi
  ```
  ```bash
  if grep -q foo bar; then
    echo match
  fi
  ```

## Операторы сравнения

| Тип | Операции |
|-----|----------|
| Строки | `==`, `!=`, `=~` (regexp), `<`, `>` (в `[[ ]]`) |
| Целые | `-eq`, `-ne`, `-lt`, `-le`, `-gt`, `-ge` |
| Файлы | `-f`, `-d`, `-e`, `-r`, `-w`, `-x`, `-s`, `-L` |

## Комбинации и логика

- `&&` и `||` внутри `[[ ]]`:
  ```bash
  if [[ $a -gt 0 && $b -gt 0 ]]; then ...
  ```
- Внешние `&&`/`||` для коротких условий:
  ```bash
  [[ -z $var ]] && fail "require var"
  ```
- `!` — отрицание:
  ```bash
  if ! command -v git >/dev/null; then
    echo "git missing"
  fi
  ```

## case как альтернатива

```
case $target in
  start) start_service ;; 
  stop) stop_service ;; 
  *) usage ;; 
 esac
```

## Советы

- Пользуйтесь `set -euo pipefail`, тогда `if` с командой автоматически прекратит скрипт при ошибке.
- Всегда кавычьте переменные: `[[ -n $var ]]` и `[[ $var == "" ]]`.
- Используйте `command -v` вместо `which`.
- Для чисел используйте `(( ))`: `if (( count > 5 )); then ...
- Логируйте, почему условие не прошло: `[[ -f $file ]] || { echo "missing" >&2; exit 1; }`
- Для сложных условий вынесите в функцию с понятным именем.

## Примеры

```
if [[ $# -lt 1 ]]; then
  echo "usage: $0 file" >&2
  exit 1
fi

if [[ -d $dir ]]; then
  cd "$dir"
else
  mkdir -p "$dir"
fi
```

## Ссылки

- `help if`, `help case`
- `bash(1)`
- ShellCheck (https://www.shellcheck.net)

---

Вернуться к [главной странице](../README.md).
