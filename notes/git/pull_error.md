Похоже, ты про «как сделать `git pull`, когда…»  
— есть **незакоммиченные изменения**, **или** выскакивает ошибка про **unrelated histories**. Вот короткая шпаргалка на оба случая.

https://git-scm.com/book/ru/v2/%d0%92%d0%b5%d1%82%d0%b2%d0%bb%d0%b5%d0%bd%d0%b8%d0%b5-%d0%b2-Git-%d0%9e%d1%81%d0%bd%d0%be%d0%b2%d1%8b-%d0%b2%d0%b5%d1%82%d0%b2%d0%bb%d0%b5%d0%bd%d0%b8%d1%8f-%d0%b8-%d1%81%d0%bb%d0%b8%d1%8f%d0%bd%d0%b8%d1%8f#r_basic_merge_conflicts

# 1) Есть незакоммиченные изменения (pull не проходит)

## Вариант А. Хочу сохранить правки и подтянуть чужие

```bash
git status                  # посмотрел, что изменено
git pull --rebase --autostash   # Git сам спрятал → подтянул → вернул правки
# если конфликт — реши, затем:
git rebase --continue
```

> Если у тебя старый Git без `--autostash`:

```bash
git stash push -u -m "pre-pull"
git pull --rebase
git stash pop               # вернуть свои правки
# реши конфликты → git add ... → git rebase --continue
```

## Вариант Б. Готов быстро закоммитить и подтянуть

```bash
git add -A
git commit -m "WIP"
git pull --rebase
```

## Вариант В. Мои локальные правки можно выбросить

⚠️ безвозвратно удалит несохранённое:

```bash
git reset --hard
git clean -df
git pull
```

# 2) Ошибка: `fatal: refusing to merge unrelated histories`

Это когда у локальной и удалённой веток **несвязанные истории** (создали два независимых репо с одинаковым именем и т.п.).

```bash
git pull origin main --allow-unrelated-histories
# реши конфликты → git add ... → git commit
```

(Подставь твою ветку вместо `main`.)

# 3) Ещё полезно

- Убедиться, что ветка привязана к удалённой:
    

```bash
git branch -vv
git branch --set-upstream-to=origin/main main
```

- Тянуть без автослияния (сначала посмотреть):
    

```bash
git fetch
git log --oneline --graph --decorate --all
git diff origin/main          # посмотреть, что придёт
```

Если хочешь, скажи текущее сообщение ошибки `git pull` (точно как в терминале) — я дам конкретную команду под твою ситуацию.