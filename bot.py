from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

async def start(update: Update, context):
    """Обработчик команды /start"""
    await update.message.reply_text("Привет! Я бот. Напиши мне что-нибудь!")

async def echo(update: Update, context):
    """Ответ на любое текстовое сообщение"""
    user_message = update.message.text
    if user_message.lower() == "привет":
        await update.message.reply_text("Привет! Я бот.")
    else:
        await update.message.reply_text("Я не понимаю тебя, но я учусь!")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()

if __name__ == "__main__":
    main()
