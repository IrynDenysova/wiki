# Bash `for` — шпаргалка

Коротко: `for` — основной цикл в bash: обходит списки, файлы, числа, массивы, позволяет применять команды к каждому элементу в компактной форме.
#bash, #for, #loops
---

## Синтаксис и формы

1. **Globbing / слова** (самая частая форма):
   ```bash
   for file in *.sh; do
     echo "Processing $file"
   done
   ```
2. **Список значений**:
   ```bash
   for stage in build test deploy; do
     echo "running $stage"
   done
   ```
3. **C-style** (bash 3+):
   ```bash
   for ((i=0; i<5; i++)); do
     echo "$i"
   done
   ```
4. **Числовые последовательности**:
   ```bash
   for num in {1..5}; do
     echo "#${num}"
   done
   ```
5. **Чтение строк из команды / файла (while)** – безопаснее с `while` и `read`:
   ```bash
   mapfile -t lines < file.txt
   for line in "${lines[@]}"; do
     echo "Line: $line"
   done
   ```

## Советы по безопасности и quoting

- Всегда оборачивайте переменную в `"$var"`, иначе пробелы/спецсимволы разрушат цикл.
- Если нужно разбить строки с пробелами, используйте `mapfile` или `IFS=$'\n'` перед циклом.
- Для обработки вывода команды используйте `while IFS= read -r line; do ...; done < <(cmd)` — безопасней, чем `for line in $(cmd)`.
- Избегайте `for var in $(cat file)` — приводит к word splitting и globbing.

## Пример: обход файлов, сохранение в массив

```bash
files=(/etc/*.conf)
for path in "${files[@]}"; do
  [[ -e $path ]] || continue
  echo "basename=$(basename "$path") size=$(stat -c%s "$path")"
done
```

## Перебор параметров скрипта

```bash
for arg in "${@}"; do
  case $arg in
    --help) usage; exit 0 ;;)
    *) args+=("$arg") ;;
  esac
done
```

## Соединение с `seq` и `printf`

```bash
for i in $(seq -w 1 10); do
  printf -v formatted "%02d" "$i"
  echo "item-${formatted}"
done
```

## Обработка ошибок

- Проверяйте `[[ -e $item ]]` и `[[ -d $dir ]]` внутри цикла.
- Для параллельных задач используйте `&` и `wait`, но контролируйте число фоновых задач (например, `jobs -rp | wc -l`).

## Полезные комбинации

- `for dir in */; do ...; done` — только каталоги, благодаря `/`.
- `for ((i=${#array[@]}-1; i>=0; i--)); do ...; done` — обратный порядок.
- `for (( ; ; )); do` — бесконечный цикл (обязательно `break`).

## Ресурсы

- `help for`
- `bash(1)`
- https://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO.html

---


Вернуться к [главной странице](../README.md).
