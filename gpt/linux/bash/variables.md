# Bash переменные — шпаргалка

Коротко: правильно объявляйте, экспортируйте и используйте переменные, чтобы избежать неожиданных значений и обеспечить переносимость.
#bash, #variables, #shell
---

## Объявление и экспорт

```bash
name="Alice"
readonly PI=3.14
export PATH="$HOME/bin:$PATH"
declare -r VERSION=1.2.3
```

`local` внутри функций ограничивает область видимости.

## Расширения параметров

| Выражение | Что делает |
|-----------|-------------|
| `${var:-default}` | подставляет `default`, если `var` пустой или unset |
| `${var:=default}` | присваивает `default`, если `var` unset |
| `${var:?msg}` | если unset — выводит `msg` и завершает скрипт |
| `${var:+replacement}` | заменяет `var` на `replacement` когда установлен |
| `${var#pattern}` | удаляет самую короткую часть `pattern` слева |
| `${var##pattern}` | удаляет самую длинную часть слева |
| `${var%pattern}` | удаляет короткую часть справа |
| `${var%%pattern}` | удаляет длинную часть справа |
| `${#var}` | длина строки |
| `${var,,}` / `${var^^}` | lower/upper case (bash 4+)

## Массивы и ассоциативные массивы

```bash
arr=(one "two words" three)
for item in "${arr[@]}"; do
  echo "$item"
done

declare -A config
config[env]=prod
```

Доступ к элементу: `${arr[0]}`, длина `${#arr[@]}`.

## Переменные окружения и `env`

- `env | grep APP` — посмотреть экспортированные значения.
- `unset VAR` — удалить переменную.
- `: "${VAR:?required}"` — аварийно завершить, если переменная unset.
- `read -r "var"` — внимательнее с вводом (см. input-output).

## Советы

- Используйте `set -u` (в script-guidelines) чтобы ловить неинициализированные переменные.
- Заменяйте хардкодированные строки через `${BASH_SOURCE[0]}` и `${BASH_SOURCE%/*}` для получения пути к скрипту.
- В конфигурациях применяйте `eval $(cat config.sh)` только после валидации, лучше `source`.

## Ресурсы

- `man bash`, раздел Parameter Expansion
- https://www.gnu.org/software/bash/manual/bash.html#Shell-Parameters

---

Вернуться к [главной странице](../README.md).
