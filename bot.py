
import os
import telebot
from dotenv import load_dotenv
from handlers import register_handlers
from db import init_db

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not API_TOKEN:
    try:
        from config import TELEGRAM_BOT_TOKEN as API_TOKEN_FROM_CONFIG
        API_TOKEN = API_TOKEN_FROM_CONFIG
    except Exception:
        raise SystemExit("Set TELEGRAM_BOT_TOKEN in .env or config.py")

bot = telebot.TeleBot(API_TOKEN, parse_mode="HTML")

def main():
    init_db()
    register_handlers(bot)
    print("Bot is running...")
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    main()
