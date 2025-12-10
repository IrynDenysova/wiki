# Урок 15. Merge конфликты и Monorepo

## План урока
- Merge конфликты
- Монорепозиторий или Monorepo
- Задание для закрепления

---

## 1) Merge конфликты

**Merge конфликты** возникают в Git, когда Git не может автоматически слить изменения из разных веток из-за конфликта в изменениях в одном и том же файле или строке кода.

### Виды merge конфликтов

#### Конфликты файлов
Когда две ветки вносят изменения в один и тот же файл, а изменения несовместимы. 

**Пример:** 
- Изменения в одной ветке могут затрагивать строки кода, которые были удалены или изменены в другой ветке.

#### Конфликты слияния директорий
Возникают, когда Git не может определить, как объединить изменения в директории из-за конфликтующих файлов.

---

## 2) Создание merge conflict (практический пример)

### Шаг 1: Инициализация репозитория

Создадим новую директорию и инициализируем репозиторий в ней:

```bash
$ mkdir git-merge-test
$ cd git-merge-test
$ git init .
```

### Шаг 2: Создание файла

Создадим новый текстовый файл `merge.txt` с некоторым содержимым:

```bash
$ echo "this is some content to mess with" > merge.txt
```

### Шаг 3: Первый коммит

Добавим `merge.txt` в репозиторий и зафиксируем его:

```bash
$ git add merge.txt
$ git commit -am "we are commiting the inital content"
[main (root-commit) d48e74c] we are commiting the inital content
 1 file changed, 1 insertion(+)
 create mode 100644 merge.txt
```

Теперь у нас есть новый репозиторий с одной веткой `main` и файлом `merge.txt` с содержимым.

### Шаг 4: Создание новой ветки

Далее мы создадим новую ветку, которая будет использоваться в качестве конфликтующего слияния:

```bash
$ git checkout -b new_branch_to_merge_later
```

### Шаг 5: Изменение в новой ветке

Изменим содержимое файла `merge.txt`:

```bash
$ echo "totally different content to merge later" > merge.txt
$ git commit -am "edited the content of merge.txt to cause a conflict"
[new_branch_to_merge_later 6282319] edited the content of merge.txt to cause a conflict
 1 file changed, 1 insertion(+), 1 deletion(-)
```

### Шаг 6: Изменение в основной ветке

Вернемся на ветку `main` и внесем другие изменения:

```bash
$ git checkout main
Switched to branch 'main'

$ echo "content to append" >> merge.txt
$ git commit -am "appended content to merge.txt"
[main 24fbe3c] appended content to merge.txt
 1 file changed, 1 insertion(+)
```

### Шаг 7: Попытка слияния

Теперь попробуем слить эти ветки:

```bash
$ git merge new_branch_to_merge_later
Auto-merging merge.txt
CONFLICT (content): Merge conflict in merge.txt
Automatic merge failed; fix conflicts and then commit the result.
```

**Появляется конфликт!** Git сообщил нам об этом!

---

## 3) Решение merge конфликтов

### Метод 1: Ручное разрешение конфликтов

Откройте конфликтующий файл в текстовом редакторе и разрешите конфликт вручную, удаляя ненужные строки или объединяя изменения.

**Пример конфликтующего файла:**
```
<<<<<<< HEAD
content to append
=======
totally different content to merge later
>>>>>>> new_branch_to_merge_later
```

Вам нужно выбрать, какой вариант оставить, или объединить оба варианта:

```
this is some content to mess with
content to append
totally different content to merge later
```

После редактирования:
```bash
git add merge.txt
git commit -m "Resolved merge conflict"
```

### Метод 2: Использование инструментов для разрешения конфликтов

Некоторые интегрированные среды разработки предоставляют инструменты для разрешения конфликтов, которые упрощают процесс.

**Примеры IDE с поддержкой разрешения конфликтов:**
- VS Code
- IntelliJ IDEA
- PyCharm
- Visual Studio

### Метод 3: Использование команд Git

#### `git status`
Показывает, какие файлы имеют конфликты после попытки слияния:

```bash
$ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   merge.txt
```

#### `git log --merge`
Создаст журнал со списком коммитов, конфликтующих между объединяющимися ветвями:

```bash
$ git log --merge
```

#### `git diff`
Показывает изменения, которые вызвали конфликты:

```bash
$ git diff
```

#### `git mergetool`
Запускает внешний инструмент для разрешения конфликтов:

```bash
$ git mergetool
```

### Метод 4: Повторное слияние после разрешения конфликтов

После разрешения конфликтов файлов:

1. Добавьте изменения в индекс с помощью `git add`
2. Завершите слияние с помощью `git merge --continue`

```bash
$ git add merge.txt
$ git merge --continue
```

Или просто:
```bash
$ git add merge.txt
$ git commit
```

---

## 4) Монорепозиторий или Monorepo

**Монорепозиторий (monorepo)** — это концепция укрупнения репозиториев в Git, которая означает объединение нескольких проектов или компонентов в один общий репозиторий.

### Концепция
Вместо того чтобы каждый проект имел свой собственный репозиторий, все проекты объединяются в один монорепозиторий.

**Особенно полезно**, когда у нас много разрозненных репозиториев, каждый из которых был посвящен одному занятию или одной домашней работе.

### Преимущества монорепозитория

#### 1. Улучшение совместной работы
- Весь код находится в одном месте
- Легче координировать изменения между проектами
- Упрощается совместная работа команды

#### 2. Упрощение поиска
- Один поиск по всему коду
- Легче найти зависимости и использование кода
- Централизованная документация

#### 3. Увеличение комфорта работы с проектами
- Не нужно переключаться между репозиториями
- Единая история изменений
- Упрощенное управление версиями

#### 4. Удобная группировка репозиториев
- Логическая структура проектов
- Общие конфигурации и настройки
- Единые стандарты кодирования

### Недостатки монорепозитория

#### 1. Увеличение размера репозитория
Увеличение размера репозитория и сложности его управления.

#### 2. Увеличение времени загрузки
Увеличение времени загрузки репозитория при клонировании.

#### 3. Возможные конфликты
Возможные конфликты при работе над различными частями кода в одном репозитории.

---

## 5) Задание для закрепления

### Задание 1: Миграция в monorepo

Попробуем мигрировать наши разрозненные репозитории в monorepo, тем самым проделав укрупнение.

**Было (разрозненные репозитории):**
```
lesson1/
lesson2/
lesson3/
homework1/
homework2/
...
```

**Стало (monorepo):**
```
linux-course/
├── lessons/
│   ├── lesson1/
│   ├── lesson2/
│   ├── lesson3/
│   └── ...
├── homeworks/
│   ├── homework1/
│   ├── homework2/
│   └── ...
└── README.md
```

**Структуру для укрупнения вы выбираете сами.**

### Полезные инструменты для миграции

#### Удаление .git директорий

```bash
find . -type d -name ".git" -exec rm -rf {} +
```

**Что делает эта команда:**
- `find .` — выполняет поиск в текущей директории
- `-type d` — ищет директории
- `-name ".git"` — с именем ".git"
- `-exec rm -rf {} +` — и удаляет их рекурсивно

**⚠️ Важно:** Мы потеряем коммиты в индивидуальных репозиториях, так как удаляется .git вместе с содержимым.

### Пример процесса миграции

**Шаг 1: Создать структуру monorepo**

```bash
mkdir linux-course
cd linux-course
git init
mkdir lessons homeworks
```

**Шаг 2: Копировать репозитории**

```bash
# Копируем содержимое репозиториев в новую структуру
cp -r ~/lesson1/* lessons/lesson1/
cp -r ~/lesson2/* lessons/lesson2/
cp -r ~/homework1/* homeworks/homework1/
# и т.д.
```

**Шаг 3: Удалить .git директории из скопированных проектов**

```bash
find . -type d -name ".git" -exec rm -rf {} +
```

**Шаг 4: Создать первый коммит в monorepo**

```bash
git add .
git commit -m "Initial commit: migrate to monorepo structure"
```

### Задание 2: Проверка нового укрупненного репозитория

Работая с укрупненным репозиторием, проработайте добавление новой директории с уроком или домашним заданием. 

**Обратите внимание:**
- Как работает git в директориях на разных уровнях
- Как отслеживаются изменения в поддиректориях
- Как выглядит история коммитов

**Действия:**
1. Создайте новый проект при помощи Visual Studio Code
2. Добавьте его в структуру monorepo
3. Отправьте коммиты в новый укрупненный репозиторий

```bash
# Создать новую директорию для урока
mkdir lessons/lesson15
cd lessons/lesson15

# Создать файлы
echo "# Lesson 15" > README.md
echo "console.log('Hello from lesson 15');" > script.js

# Вернуться в корень репозитория
cd ../..

# Добавить и закоммитить изменения
git add lessons/lesson15
git commit -m "Add lesson 15: Introduction to JavaScript"
git push
```

---

## Резюме

### Merge конфликты
- Возникают при несовместимых изменениях в одном файле
- Требуют ручного разрешения или использования инструментов
- Команды для работы с конфликтами: `git status`, `git diff`, `git mergetool`
- После разрешения: `git add` + `git commit`

### Monorepo
**Преимущества:**
- Централизованное управление кодом
- Упрощение совместной работы
- Единая история изменений
- Удобный поиск по всему коду

**Недостатки:**
- Больший размер репозитория
- Дольше клонирование
- Потенциально больше конфликтов

**Рекомендации:**
- Продумать логическую структуру
- Использовать четкую организацию директорий
- Документировать структуру проекта
- Установить правила для работы с monorepo


---

## Дополнительные материалы

### Инструменты для разрешения конфликтов

#### VS Code (встроенный)
- Открыть конфликтующий файл
- Интерфейс показывает варианты: "Accept Current", "Accept Incoming", "Accept Both"

#### Vimdiff
```bash
git config --global merge.tool vimdiff
git mergetool
```

#### Meld (GUI)
```bash
sudo apt install meld
git config --global merge.tool meld
git mergetool
```

### Стратегии слияния в конфликтных ситуациях

```bash
# Theirs стратегия (принять их изменения)
git merge -X theirs branch-name

# Ours стратегия (оставить наши изменения)
git merge -X ours branch-name

# Для конкретного файла
git checkout --theirs file.txt
git checkout --ours file.txt
```

### Предотвращение конфликтов

1. **Частые коммиты и pull/push**
2. **Небольшие feature ветки**
3. **Регулярная синхронизация с main**
```bash
git checkout feature
git pull origin main --rebase
```
4. **Избегать изменений одних и тех же файлов**

### Monorepo инструменты

#### Nx (для JavaScript/TypeScript)
```bash
npx create-nx-workspace@latest

# Структура
monorepo/
├── apps/
│   ├── web/
│   └── mobile/
├── libs/
│   ├── shared/
│   └── utils/
└── nx.json
```

#### Turborepo
```bash
npx create-turbo@latest

# Конфигурация turbo.json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    }
  }
}
```

#### Bazel (для больших проектов)
- Используется в Google
- Поддержка множества языков
- Инкрементальные сборки

### Git Worktree для monorepo

```bash
# Работа с несколькими ветками одновременно
git worktree add ../feature-1 feature-1
git worktree add ../feature-2 feature-2

# Список worktrees
git worktree list

# Удалить worktree
git worktree remove ../feature-1
```

### Sparse Checkout для больших репозиториев

```bash
# Клонировать только metadata
git clone --no-checkout repo.git
cd repo

# Включить sparse checkout
git sparse-checkout init --cone

# Указать директории для checkout
git sparse-checkout set folder1 folder2

git checkout main
```

### Практические советы для monorepo

**Преимущества:**
- Единая версия зависимостей
- Легче рефакторинг across проектов
- Одна CI/CD pipeline
- Проще code sharing

**Недостатки:**
- Большой размер репозитория
- Медленные git операции
- Сложность прав доступа

**Решения:**
- Использовать Git LFS для больших файлов
- Настроить CI для изменённых модулей
- Использовать специализированные инструменты (Nx, Turborepo)

### Ресурсы

- [Monorepo Tools](https://monorepo.tools/) — сравнение инструментов
- [Nx Documentation](https://nx.dev/)
- [Turborepo Documentation](https://turbo.build/)
- [Git Worktree Tutorial](https://git-scm.com/docs/git-worktree)
- [Atlassian: Monorepos](https://www.atlassian.com/git/tutorials/monorepos)
