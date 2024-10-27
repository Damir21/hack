from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

# Состояния для управления диалогом
USER_INPUT, CONFIRM_TEXT, CHOOSE_GENDER, CHOOSE_GENRE = range(4)

async def start(update: Update, context):
    """Обработчик команды /start"""
    await update.message.reply_text("Привет! Я бот, который генерирует песни. Напиши слова через запятую, которые должны присутствовать в песне.")
    return USER_INPUT

async def user_input(update: Update, context):
    """Обработка пользовательского ввода слов"""
    user_message = update.message.text
    context.user_data['words'] = user_message.split(',')  # Сохраняем слова
    await update.message.reply_text("Генерирую текст песни...")  # Заглушка

    # Генерация текста песни (пока заглушка)
    generated_text = "Это текст песни на основе: " + ", ".join(context.user_data['words'])  # Заглушка
    context.user_data['generated_text'] = generated_text

    # Запрос подтверждения текста
    await confirm_text(update, context)

async def confirm_text(update: Update, context):
    """Подтверждение текста песни"""
    keyboard = [
        [
            InlineKeyboardButton("Согласен", callback_data='confirm'),
        ],
        [
            InlineKeyboardButton("Перегенерировать", callback_data='regenerate'),
        ],
        [
            InlineKeyboardButton("Другие слова", callback_data='other_words'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Используем context для доступа к сгенерированному тексту
    await update.message.reply_text(context.user_data['generated_text'], reply_markup=reply_markup)

async def button_handler(update: Update, context):
    """Обработка нажатий кнопок"""
    query = update.callback_query
    await query.answer()

    if query.data == 'confirm':
        await choose_gender(update, context)
    elif query.data == 'regenerate':
        await query.message.reply_text("Генерирую текст песни...")  # Заглушка
        # Логика перегенерации текста песни
    elif query.data == 'other_words':
        await query.message.reply_text("Напиши слова через запятую.")
        return USER_INPUT
    elif query.data in ['male', 'female']:
        context.user_data['gender'] = query.data  # Сохраняем выбранный пол
        await choose_genre(update)  # Переходим к выбору жанра
    elif query.data in ['pop', 'rock', 'hiphop']:
        context.user_data['genre'] = query.data  # Сохраняем выбранный жанр
        await send_audio(update)  # Выдаем аудиофайл

async def choose_gender(update: Update, context):
    """Выбор пола вокала"""
    query = update.callback_query  # Получаем объект CallbackQuery
    await query.answer()  # Подтверждаем нажатие кнопки

    keyboard = [
        [InlineKeyboardButton("Мужской", callback_data='male')],
        [InlineKeyboardButton("Женский", callback_data='female')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Используем edit_message_text вместо reply_text
    await query.message.edit_text("Выбери пол вокала:", reply_markup=reply_markup)

async def choose_genre(update: Update):
    """Выбор жанра"""
    query = update.callback_query  # Получаем объект CallbackQuery
    await query.answer()  # Подтверждаем нажатие кнопки

    keyboard = [
        [InlineKeyboardButton("Поп", callback_data='pop')],
        [InlineKeyboardButton("Рок", callback_data='rock')],
        [InlineKeyboardButton("Хип-хоп", callback_data='hiphop')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text("Выбери жанр:", reply_markup=reply_markup)

async def send_audio(update: Update):
    """Выдача аудиофайла"""
    query = update.callback_query  # Получаем объект CallbackQuery
    await query.answer()  # Подтверждаем нажатие кнопки

    # Заглушка для отправки аудиофайла
    await query.message.reply_text("Ваш аудиофайл будет здесь (заглушка).")  # Заглушка для аудиофайла

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_input))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
