# News Assistant Bot

Телеграм-бот для фильтрации и доставки экономических новостей с FastAPI-интерфейсом управления.

## Структура
- `news_assistant_ready/` — код бота
- `bot_config_panel/` — панель управления
- `weekly_news_notebook_bot/` — отдельный подпроект с ручным weekly workflow через notebook

## Деплой на Render
Проект автоматически стартует как FastAPI-панель и Telegram-бот.

## Weekly / manual notebook workflow (локально)
Для подпроекта `weekly_news_notebook_bot` используется **только локальный ручной запуск**:
- настройка локального `config_local.json` (секреты и пути);
- локальный `sources.json` со списком источников;
- запуск `weekly_news_notebook_bot/notebook.ipynb` вручную в Jupyter.

Важно: этот сценарий не предполагает Render/облачный деплой.
