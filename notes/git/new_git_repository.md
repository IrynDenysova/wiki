
### …or create a new repository on the command line

echo "# wiki" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:viktorplus/name.git
git push -u origin main

### …or push an existing repository from the command line

git remote add origin git@github.com:viktorplus/namegit
git branch -M main
git push -u origin main


Классическая ситуация: **локальная история и удалённая история не связаны**, Git пишет:

```
fatal: refusing to merge unrelated histories
```

Это значит, что Git считает, что твой локальный репозиторий и удалённый — **две разные истории**, и он по умолчанию не хочет их объединять.

---

# ✅ **Шаг 1 — попробовать стянуть удалённые изменения с разрешением “несвязанных историй”**

Выполни:

```bash
git pull origin main --allow-unrelated-histories
```

Это скажет Git: _«Я знаю, что истории отличаются, всё равно объединяй»._

# **Шаг 2 — отправляем локальные изменения обратно на GitHub**

Выполни:

`git push origin main`

Это зафиксирует синхронизацию и завершит цикл работы.

(use "git restore <file>..." to discard changes in working directory

git rm -r --cached .

# Что делает `--force-with-lease`

```bash
git push --force-with-lease
```
Git говорит:
> «Я перезапишу историю **только если удалённая ветка выглядит так, как я ожидаю**. 
> Если кто-то успел внести изменения — я остановлюсь».
---