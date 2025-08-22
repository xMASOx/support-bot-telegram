
# Telegram-бот техподдержки — «Продаем всё на свете»

Бот помогает пользователям:
- находить ответы в FAQ
- отправлять запросы в техподдержку или отдел продаж
- сохранять все обращения в SQLite

## Быстрый старт

1) Клонируйте проект и перейдите в папку:
```bash
git clone <url>
cd support_bot
```

2) Создайте и активируйте виртуальную среду (рекомендуется):
```bash
python -m venv .venv
.venv\Scripts\activate
source .venv/bin/activate
```

3) Установите зависимости:
```bash
pip install -r requirements.txt
```

4) Укажите токен бота:
- создайте файл `.env` и добавьте строку:
  ```
  TELEGRAM_BOT_TOKEN= "TOKEN"
  ```
  или укажите токен в `config.py`:
  ```python
  TELEGRAM_BOT_TOKEN = "TOKEN"
  ```

5) Запуск:
```bash
python bot.py
```

## Структура
```
support_bot/
├─ bot.py
├─ handlers.py
├─ db.py
├─ utils.py
├─ faq.json
├─ requirements.txt
├─ README.md
├─ .env.example
└─ .gitignore
```

## Команды
- `/start` — главное меню
- `/help` — помощь

## FAQ
Изменяйте `faq.json` чтобы обновлять вопросы/ответы без изменения кода.

## База данных
SQLite файл `support.db` создается автоматически при первом запуске.
Таблица `requests` содержит поля: `id, user_id, username, message, department, status, created_at`.

## Переменные окружения
- `TELEGRAM_BOT_TOKEN` — токен вашего бота из @BotFather

## Деплой
- Хостинг на любой VPS/VM, убедитесь что процесс запущен постоянно (systemd, pm2, screen).
- При желании заверните в Docker самостоятельно.
