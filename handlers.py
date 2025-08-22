import json
from telebot import types
from db import add_request

FAQ = {}
try:
    with open("faq.json", "r", encoding="utf-8") as f:
        FAQ = json.load(f)
except Exception:
    FAQ = {}

def kb_main():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("FAQ", "Задать вопрос")
    kb.row("О магазине")
    return kb

def kb_departments():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row("Технический", "Продажи")
    kb.row("Назад")
    return kb

def ikb_faq_questions():
    markup = types.InlineKeyboardMarkup()
    for q in FAQ.keys():
        markup.add(types.InlineKeyboardButton(text=q[:60], callback_data=f"faq::{q}"))
    return markup

def register_handlers(bot):

    @bot.message_handler(commands=["start", "help"])
    def cmd_start(message):
        bot.send_message(
            message.chat.id,
            "Привет! Я бот техподдержки магазина <b>«Продаем всё на свете»</b>.\n"
            "— Найду ответ в FAQ\n"
            "— Передам ваш вопрос в нужный отдел\n\n"
            "Выберите действие ниже ",
            reply_markup=kb_main(),
        )

    @bot.message_handler(func=lambda m: m.text == "FAQ")
    def on_faq(message):
        if not FAQ:
            bot.send_message(message.chat.id, "FAQ пока пуст. Обратитесь к администратору.")
            return
        bot.send_message(message.chat.id, "Выберите вопрос из списка:", reply_markup=ikb_faq_questions())

    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("faq::"))
    def on_faq_click(call):
        _, question = call.data.split("::", 1)
        answer = FAQ.get(question, "Ответ не найден.")
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"<b>{question}</b>\n\n{answer}",
            parse_mode="HTML"
        )

    @bot.message_handler(func=lambda m: m.text == "Задать вопрос")
    def on_ask(message):
        bot.send_message(message.chat.id, "Выберите отдел:", reply_markup=kb_departments())

    @bot.message_handler(func=lambda m: m.text in ["Технический", "Продажи"])
    def on_department_chosen(message):
        department = "technical" if "Технический" in message.text else "sales"
        msg = bot.send_message(message.chat.id, "Опишите вашу проблему/вопрос максимально подробно:")
        bot.register_next_step_handler(msg, lambda m: save_request_flow(m, department))

    def save_request_flow(message, department):
        add_request(
            user_id=message.from_user.id,
            username=message.from_user.username or "",
            message=message.text,
            department=department,
        )
        bot.send_message(
            message.chat.id,
            "Ваш запрос сохранён и передан специалистам.\n"
            "Мы свяжемся с вами в ближайшее время.\n\n"
            "Вернуться в меню: /start"
        )

    @bot.message_handler(func=lambda m: m.text == "Назад")
    def on_back(message):
        bot.send_message(message.chat.id, "Главное меню:", reply_markup=kb_main())

    @bot.message_handler(func=lambda m: m.text == "О магазине")
    def on_about(message):
        bot.send_message(
            message.chat.id,
            "Мы — интернет-магазин «Продаем всё на свете».\n"
            "Работаем 24/7, доставка по всей стране.\n"
            "Поддержка: через этого бота."
        )

    @bot.message_handler(content_types=["text"])
    def on_text(message):
        bot.send_message(
            message.chat.id,
            "Не совсем понял запрос. Нажмите /start и выберите нужный раздел."
        )
