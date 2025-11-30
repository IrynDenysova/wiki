# git — шпаргалка

Коротко: `git` — распределённая система контроля версий. Позволяет отслеживать изменения, работать с ветками, сливать, делать ревью и управлять историей.
#git, #linux, #vcs
---

## Базовый рабочий цикл

1. Редактировать файлы
2. `git add` — индексировать (staging)
3. `git commit` — зафиксировать в истории
4. `git push` — отправить на удалённый репозиторий

## Инициализация и клон

```
git init                      # создать репозиторий в текущей директории
git clone URL [DIR]           # клонировать удалённый репозиторий
```

## Статус и просмотр

```
git status                    # состояние рабочего дерева и индекса
git diff                      # изменения в рабочем дереве относительно индекса
git diff --staged             # изменения, добавленные в индекс
git log --oneline --graph --decorate --all  # компактная история
```

Полезно: `git log -p`, `git show <commit>`.

## Индексация и коммиты

```
git add file                  # добавить файл в индекс
git add .                     # добавить все изменения
git commit -m "message"       # простой коммит
git commit -am "message"      # добавить отслеживаемые и коммит
```

Аменд последнего коммита:
```
git commit --amend            # изменить сообщение или включить новые изменения
```

## Ветки

```
git branch                    # список локальных веток
git branch -r                 # список удалённых веток
git branch new-feature        # создать ветку
git checkout new-feature      # переключиться (устарело, лучше switch)
git switch new-feature        # современный переход
git switch -c new-feature     # создать и перейти
git checkout -b <имя ветки>   #Создание и переключение на новую ветку
git checkout -b ＜remotebranch＞ origin/＜remotebranch＞  Создание новой ветки на основе удаленного репозитория
```

Удаление ветки:
```
git branch -d old             # удалить слитую ветку
git branch -D old             # принудительно удалить
```

## Слияние (merge) и ребейз (rebase)

```
git merge feature             # слить ветку feature в текущую
git merge --no-ff feature     # сохранить коммит merge (не fast-forward)

git rebase main               # перенести коммиты поверх main
```

Остановка и продолжение ребейза:
```
git rebase --abort
git rebase --continue
```

## Stash (временное сохранение)

```
git stash                     # сохранить незакоммиченные изменения
git stash list                # список сохранений
git stash show -p stash@{0}   # показать diff конкретного stash
git stash apply stash@{0}     # применить без удаления
git stash pop                 # применить и удалить из списка
git stash drop stash@{0}      # удалить конкретный
```

## Удалённые репозитории

```
git remote -v                 # список удалённых
git remote add origin URL     # добавить origin
git fetch origin              # получить обновления (без merge)
git pull origin main          # fetch + merge (или rebase при настройке)
git push origin main          # отправить локальные коммиты
```

Удаление и переименование:
```
git remote remove origin
git remote rename origin upstream
```

Отправка новой ветки:
```
git push -u origin feature    # задать upstream для feature
```

## Теги (release метки)

```
git tag                       # список тегов
git tag v1.2.0                # создать аннотированный? (нет — лёгкий)
git tag -a v1.2.0 -m "Release" # аннотированный тег
```

Отправка тегов:
```
git push origin v1.2.0
git push origin --tags        # все отсутствующие теги
```

Удаление:
```
git tag -d v1.2.0
git push origin :refs/tags/v1.2.0
```

## Просмотр и поиск

```
git show COMMIT               # показать содержимое коммита
git blame file                # кто последний изменил каждую строку
```

Поиск строки в истории:
```
git log -S 'pattern' -- file
```

## Undo / Отмена

- Убрать файл из индекса, не трогая рабочее дерево: `git reset HEAD file`
- Вернуть файл к версии в индексе: `git checkout -- file` (устарело) / `git restore file`
- Вернуть файл к версии из коммита: `git restore --source <commit> file`
- Мягкий reset (оставить изменения): `git reset --soft HEAD~1`
- Жёсткий reset (стереть изменения в рабочем дереве): `git reset --hard HEAD~1`
- Создать отменяющий коммит: `git revert <commit>`

## Cherry-pick

```
git cherry-pick <commit>          # перенести один коммит
git cherry-pick A..B              # перенести диапазон (не включая A)
```

## Reflog (история перемещений)

```
git reflog                    # список изменений ссылок HEAD/веток
```

Восстановление потерянного коммита:
```
git checkout <hash>
```
(Затем создать ветку: `git switch -c rescued`)

## Submodule

```
git submodule add URL path    # добавить сабмодуль
git submodule update --init --recursive
```

Обновление:
```
git submodule update --remote --merge
```

## Конфигурация

```
git config --global user.name "Your Name"
git config --global user.email you@example.com
git config --global core.editor "nvim"
```

Локальная (в репозитории): `git config user.email other@example.com`.

Список настроек:
```
git config --list --show-origin
```

## Оптимизация и чистка

```
git gc --prune=now --aggressive   # уборка и оптимизация (осторожно, редко нужно)
```

Удаление неиспользуемых remote-tracking веток:
```
git fetch --prune
```

## Полезные опции

- `--depth N` при `git clone` — shallow клон
- `--recurse-submodules` — сразу инициализировать сабмодули при клонировании
- `-p` / `--patch` для интерактивного добавления: `git add -p`
- `git restore --staged file` — убрать из индекса
- `git switch -c` — создание ветки (замена `checkout -b`)

## Советы

- Делайте маленькие атомарные коммиты с понятными сообщениями
- Используйте защищённые ветки и Pull Request для code review
- Избегайте `git push --force` на общих ветках; если нужно — `--force-with-lease`
- Для релизов используйте аннотированные теги
- Прежде чем ребейзить — убедитесь, что ветка приватна (не опубликована)
- Настройте `.gitignore` до первых коммитов
- Храните глобальные настройки в `~/.gitconfig`, локальные — в `.git/config`

## Справка

- `man git` / `git help <command>`
- Документация: https://git-scm.com/docs
- Руководство: https://git-scm.com/book/en/v2

---

Вернуться к [главной странице](linux/README.md).
