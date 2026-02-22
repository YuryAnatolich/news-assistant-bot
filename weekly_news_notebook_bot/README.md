# Weekly news notebook bot

Подпроект с ручным weekly-workflow через Jupyter Notebook.

## Что внутри
- `notebook.ipynb` — основной ноутбук (ручной запуск, без деплоя).
- `config.example.json` — пример локального конфига.
- `sources.example.json` — пример списка источников.
- `.gitignore` — исключения для локальных секретов и runtime-артефактов.
- `requirements.txt` — минимальные зависимости для ноутбука.

## Локальный запуск (manual workflow)
1. Создайте и активируйте виртуальное окружение.
2. Установите зависимости из `weekly_news_notebook_bot/requirements.txt`.
3. Скопируйте `config.example.json` в `config_local.json` и заполните:
   - `telegram.bot_token`
   - `telegram.chat_id`
   - `files.*` пути к локальным файлам.
4. Скопируйте `sources.example.json` в `sources.json` и настройте источники.
5. Откройте `weekly_news_notebook_bot/notebook.ipynb` в Jupyter и выполните ячейки по порядку.

## Важные замечания
- `config_local.json` содержит секреты и не должен коммититься.
- `seen_news.json`, `outputs/`, `logs/`, `.ipynb_checkpoints/` — runtime-данные, исключены из git.
- Этот подпроект предполагает локальный запуск; Render/деплой для него не требуется.
