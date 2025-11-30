# Bash отладка — шпаргалка

Коротко: включайте вывод команд и используйте `shellcheck`/`bash -n`, чтобы быстро находить проблемы.
#bash, #debugging, #shell
---

## Включение режимов

```bash
set -xv
PS4='+${BASH_SOURCE}:${LINENO}:${FUNCNAME[0]}: '
```

- `set -x` — печатает команды перед выполнением.
- `set -v` — печатает строки по мере чтения.
- `PS4` помогает увидеть контекст (файл, строку, функцию).

## Отдельные блоки

```bash
{ set -x; expensive_cmd; set +x; }
```

Включайте debug только вокруг подозрительных участков.

## Дополнительные инструменты

- `bash -n script.sh` — проверка синтаксиса.
- `shellcheck script.sh` — статический анализ.
- `bash -x script.sh` — трассировка.
- `env -i bash --noprofile --norc script.sh` — чистая среда.
- `strace -e trace=open bash script.sh` — для проблем с файлами.

## Логирование

```
exec 3>&1 4>&2
exec > >(tee -a script.log) 2>&1
```

Можно отключать `set -x` через `exec 1>&3 2>&4`.

## Советы

- В CI добавьте `-x` только при ошибке: `bash -n script && bash -x script || true`.
- `PS4='+ ${BASH_SOURCE}:$LINENO:$FUNCNAME: '` делает трассировку понятнее.
- `trap 'ret=$?; echo "Exited $ret"; exit $ret' EXIT` помогает узнать код.

## Ресурсы

- https://www.shellcheck.net
- https://wiki.bash-hackers.org/scripting/debugging

---


Вернуться к [главной странице](../README.md).
