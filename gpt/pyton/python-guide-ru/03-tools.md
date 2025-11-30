# 03 • Инструменты и поддержка

## Редакторы и IDE
- VS Code + расширение Python (Microsoft) для IntelliSense, отладки и тестов.
- PyCharm Professional для продвинутых возможностей; Community покрывает базовые задачи.
- Установить расширение VS Code: `code --install-extension ms-python.python`.

## Линтеры и форматтеры
- **Форматтер**: `black` для единого стиля.
  ```powershell
  python -m pip install black
  black src tests
  ```
- **Линтер**: `ruff` или `flake8` для стиля и статического анализа.
  ```powershell
  python -m pip install ruff
  ruff check src tests
  ```
- Добавляйте pre-commit хуки для `black`, `ruff`, `isort`, `mypy`.

## Тестирование
- Стандарт: `pytest` для юнитов и интеграционных проверок.
  ```powershell
  python -m pytest tests
  ```
- `pytest -k pattern` запускает только нужные тесты.
- Покрытие: `pip install pytest-cov`, `pytest --cov=package`.

## Отладка
- VS Code: настройте `.vscode/launch.json` с `program`, `args` и переменными.
- Консольная отладка: `python -m pdb script.py`.
- Предпочитайте `logging` вместо `print` для продакшен-логов.

## Статическая типизация
- `mypy` проверяет типы.
  ```powershell
  python -m pip install mypy
  mypy src
  ```
- Используйте `# type: ignore` только в крайних случаях, добавляйте stub-файлы для библиотек.

## Сборка и выпуск
- Собирайте `wheel` и `sdist` через `python -m build`.
- Публикация: `twine upload dist/*`, храните креды отдельно (например, keyring).

## Автоматизация
- `tox` для матричного тестирования на разных Python.
- `nox` как инструмент сессий на Python.
- `invoke` или `make` (через `invoke run task`) для кастомных команд.
