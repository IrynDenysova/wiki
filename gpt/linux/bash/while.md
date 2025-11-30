# Bash `while` — шпаргалка

Коротко: `while` обходит поток данных, команды или проверку условия и продолжает выполнять тело до тех пор, пока условие истинно (или `until` — пока ложно).
#bash, #while, #loops
---

## Синтаксис

```bash
while CONDITION; do
  commands
done
```

Или с `until`:

```bash
until CONDITION; do
  commands
done
```

### Примеры

```bash
count=0
while [[ $count -lt 5 ]]; do
  echo "count=$count"
  ((count++))
done
```

Или читая строки из файла:

```bash
while IFS= read -r line; do
  echo "Line: $line"
done < file.txt
```

Можно использовать `process substitution`:

```bash
while read -r file; do
  wc -l "$file"
done < <(find . -name '*.sh')
```

## Важные рекомендации

- Всегда пишите `IFS=` и `read -r`, чтобы сохранить пробелы и слэши в строке.
- Не используйте `cat file | while ...` если вам нужно обновить переменные цикла вне цикла; лучше перенаправьте файл (`while ...; done < file`).
- Для проверки команд без `[` используйте `[[ ... ]]` и `(( ... ))`.
- Добавляйте `break`/`continue` для управления (например, `[[ $line == skip ]] && continue`).
- В shell-скриптах `while true; do ...; done` — бесконечный цикл; обязательно ставьте `sleep` и `break` при необходимости.

## Работа с прерываниями

```
trap 'echo "Interrupted"; exit 1' INT
while ...; do
  ...
done
```

`while` часто используется вместе с тайм-аутом:

```bash
timeout=10
while [[ $timeout -gt 0 ]]; do
  if check_ready; then
    break
  fi
  sleep 1
  ((timeout--))
done
```

## Завершение с кодом

```
while cmd; do :; done
status=$?
```

Можно сохранять результат последней итерации (например, `command && break`).

## Ресурсы

- `help while`
- `shellcheck`: проверяет `while` на проблемы с `read` и word splitting.

---

Вернуться к [главной странице](../README.md).
