# Bash ввод/вывод — шпаргалка

Коротко: контроль ввода/вывода — ключ к надёжному скрипту: используйте `read`, `printf`, `heredoc`, перенаправления и `process substitution`.
#bash, #io, #shell
---

## Чтение данных

```bash
read -r line
read -r -p "Name: " name
```

- `-r` выключает интерпретацию `\`.
- `IFS= read -r line` сохраняет пробелы и табы.
- `mapfile -t lines < file` читает массив строк.
- `while IFS= read -r line; do ...; done < file` — безопасный цикл.

## Here-document / here-string

```
cat <<EOF > config.ini
key=value
EOF
```

```
while read -r line; do echo "$line"; done <<< "$TEXT"
```

## Перенаправления

| Оператор | Что делает |
|----------|------------|
| `> file` | запись (перезаписать) |
| `>> file` | дописать |
| `< file` | stdin из файла |
| `2>&1` | stderr в stdout |
| `&> file` | stdout+stderr в файл |
| `cmd > >(sort)` | process substitution |

## Process substitution

```bash
while read -r user; do
  printf "%s\n" "$user"
done < <(cut -d: -f1 /etc/passwd)
```

## Абстрактные потоки

- `exec 3< config` — открыть новый дескриптор 3.
- `cat <&3` — читать из 3, `echo hi >&3` — писать.
- Используйте `exec` для временного перенаправления `stdout`/`stderr`.

## Советы

- Используйте `printf` вместо `echo` для стабильного вывода: `printf '%s
' "$value"`.
- Для логов: `exec > >(tee -a script.log)` и `exec 2>&1`.
- В функцию можно передавать stdin: `process() { while IFS= read -r line; do ...; done; }` и потом `process < data.txt`.

## Ресурсы

- `help read`, `help printf`
- https://wiki.bash-hackers.org/scripting/io_redirection

---

Вернуться к [главной странице](../README.md).
