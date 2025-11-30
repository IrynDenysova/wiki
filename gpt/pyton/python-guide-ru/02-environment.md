# 02 • Окружение и менеджмент версий

## Сборки Python
- Узнать версию: `python --version` и `python -c "import sys; print(sys.executable)"`.
- Для новых проектов выбирайте актуальную стабильную ветку Python 3.x; обновляйте `pip` через `python -m pip install -U pip`.

## Виртуальные окружения
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
- Храните `.venv` в корне проекта и добавьте его в `.gitignore`.
- Для выхода используйте `deactivate`.
- Можно задавать подсказку: `python -m venv --prompt myproj`.

## Менеджеры версий
- Инструменты: `pyenv-win`, `conda`, `asdf`, диспетчер `py.exe`.
- На Windows `py -3.12` вызывает конкретный интерпретатор.

## Файлы зависимостей
- `requirements.txt`: `pip freeze > requirements.txt` для фиксированных версий.
- `pyproject.toml`: общая конфигурация для сборки, линтинга и форматтратора.
- `pip-tools`: храните `requirements.in` и компилируйте в `requirements.txt`.

## Скрипты проекта
```toml
[tool.poetry.scripts]
cli = "mypkg.cli:main"
```
или в `setup.cfg`:
```ini
[options.entry_points]
console_scripts =
    run-app = mypkg.app:main
```

## Переменные окружения
- Чувствительные данные храните вне репозитория, например, в `.env` с `python-dotenv`.
- Используйте `os.getenv('VAR', 'default')` для безопасного чтения.

## Предложенная структура
```
project/
├── .venv/
├── src/
│   └── package/
├── tests/
├── pyproject.toml
└── README.md
```
- `src/` layout помогает избежать конфликтов при редактируемых установках.
