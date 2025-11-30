# Linux шпаргалки

Всегда под рукой: коллекция кратких справочников по командам, базовым структурам и шаблонам `bash`.

## Командные утилиты

- [`awk.md`](./awk.md) — обработка полей, регулярные выражения, BEGIN/END-блоки.
- [`sed.md`](./sed.md) — потоковый редактор, замены, адреса, in-place.
- [`grep.md`](./grep.md) — поиск по регулярным выражениям, опции, контекст.
- [`find.md`](./find.md) — рекурсивный поиск по имени, типу, времени, `-exec`, `-prune`.
- [`locate.md`](./locate.md) — быстрый поиск по базе `updatedb`.
- [`tree.md`](./tree.md) — визуальный обзор дерева каталогов.

## Работа с файлами и правами

- [`ls.md`](./ls.md) — длинные списки, цвета, сортировки, скрытые файлы.
- [`cp.md`](./cp.md), [`mv.md`](./mv.md), [`mkdir.md`](./mkdir.md), [`touch.md`](./touch.md) — стандартные операции копирования/перемещения/создания.
- [`chmod.md`](./chmod.md) — символьные/окталевые режимы, спецбиты, рекурсивное применение.
- [`wc.md`](./wc.md) — счётчики строк/слов/байтов.
- [`head.md`](./head.md), [`tail.md`](./tail.md) — первые/последние строки, `follow`, `+N`.

## Сеть и безопасность

- [`scp.md`](./scp.md) — копирование по SSH, опции, примеры.
- [`ssh-keygen.md`](./ssh-keygen.md) — генерация ключей, управление `known_hosts`, fingerprint.
- [`networking.md`](./networking.md) — `ip`, `ss`, `curl`, `dig`, `ethtool`, состояния соединений.

## Мониторинг и процессы

- [`monitoring.md`](./monitoring.md) — `free`, `df`, `cpuinfo`, `vmstat`, `iostat`, переменные среды.
- [`ps.md`](./ps.md) — статический снимок процессов, фильтры, `%CPU/%MEM`.
- [`top-htop.md`](./top-htop.md) — интерактивные мониторы, сортировки, ярлыки.

## Bash и шаблоны

Поддиректория `bash/` содержит практики и конструкции для написания надёжных скриптов:

- [`bash/script-guidelines.md`](./bash/script-guidelines.md) — структура, `set -euo pipefail`, `usage`, `trap`.
- [`bash/variables.md`](./bash/variables.md) — объявление, параметрическое расширение, массивы.
- [`bash/functions.md`](./bash/functions.md) — шаблон `main`, локальные переменные, возвраты.
- [`bash/error-handling.md`](./bash/error-handling.md) — `set`, `trap`, логирование ошибок.
- [`bash/input-output.md`](./bash/input-output.md) — `read`, `mapfile`, here-doc, редиректы.
- [`bash/debugging.md`](./bash/debugging.md) — `set -x`, `PS4`, `shellcheck`, отладка.
- [`bash/cron-jobs.md`](./bash/cron-jobs.md) — cron-ready шаблон, `PATH`, `flock`, лог-файлы.
- [`bash/for.md`](./bash/for.md), [`bash/while.md`](./bash/while.md), [`bash/if.md`](./bash/if.md) — основные циклы и условия.

## Как использовать

1. Откройte нужную шпаргалку (например, `grep.md`) и изучите ключевые опции.
2. Скопируйте готовые примеры в терминал, адаптируя пути/имена.
3. Добавьте новые шпаргалки по мере необходимости и обновляйте `README.md` ссылками.

---
https://publish.obsidian.md/help-ru/