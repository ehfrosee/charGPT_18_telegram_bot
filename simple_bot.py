from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.ext import ApplicationBuilder
from telegram import Update
from dotenv import load_dotenv
import openai
import os
import requests
import aiohttp
import json


# подгружаем переменные окружения
load_dotenv()

# передаем секретные данные в переменные
TOKEN = os.environ.get("TG_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# передаем секретный токен chatgpt
openai.api_key = OPENAI_API_KEY


# функция для синхронного общения с chatgpt
async def get_answer(text):
    payload = {"text": text}
    response = requests.post("http://127.0.0.1:5000/api/get_answer", json=payload)
    return response.json()


# функция для асинхронного общения с сhatgpt
async def get_answer_async(text):
    payload = {"text": text}
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:5000/api/get_answer_async', json=payload) as resp:
            return await resp.json()


# функция-обработчик команды /start 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # при первом запуске бота добавляем этого пользователя в словарь
    if update.message.from_user.id not in context.bot_data.keys():
        context.bot_data[update.message.from_user.id] = 1
    
    # возвращаем текстовое сообщение пользователю
    await update.message.reply_text('Задайте любой вопрос ChatGPT')


# функция-обработчик команды /data 
async def data(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # создаем json и сохраняем в него словарь context.bot_data
    with open('data.json', 'w') as fp:
        json.dump(context.bot_data, fp)
    
    # возвращаем текстовое сообщение пользователю
    await update.message.reply_text('Данные сгружены')


# функция-обработчик текстовых сообщений
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # проверка доступных запросов пользователя
    if context.bot_data[update.message.from_user.id] > 0:

        # выполнение запроса в chatgpt
        first_message = await update.message.reply_text('Ваш запрос обрабатывается, пожалуйста подождите...')
        # res = await get_answer(update.message.text)
        res = await get_answer_async(update.message.text)
        await context.bot.edit_message_text(text=res['message'], chat_id=update.message.chat_id, message_id=first_message.message_id)

        # уменьшаем количество доступных запросов на 1
        context.bot_data[update.message.from_user.id]-=1
        await update.message.reply_text(f'Осталось запросов: {context.bot_data[update.message.from_user.id]}')
    
    else:

        # сообщение если запросы исчерпаны
        await update.message.reply_text('Ваши запросы на сегодня исчерпаны')


# функция, которая будет запускаться раз в сутки для обновления доступных запросов
async def callback_daily(context: ContextTypes.DEFAULT_TYPE):

    # проверка базы пользователей
    if context.bot_data != {}:

        # проходим по всем пользователям в базе и обновляем их доступные запросы
        for key in context.bot_data:
            context.bot_data[key] = 3
        print('Запросы пользователей обновлены')
    else:
        print('Не найдено ни одного пользователя')

def main():


    # создаем приложение и передаем в него токен бота
#    application = Application.builder().token(TOKEN).build()
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()
    print('Бот запущен...')

    # создаем job_queue 
    job_queue = application.job_queue
    job_queue.run_repeating(callback_daily, interval=60, first=10)

    #job = context.job_queue.run_repeating(callback, interval=5)
    # добавление обработчиков
    application.add_handler(CommandHandler("start", start, block=True))
    application.add_handler(CommandHandler("data", data, block=True))
    application.add_handler(MessageHandler(filters.TEXT, text, block=True))

    # запуск бота (нажать Ctrl+C для остановки)
    application.run_polling()
    print('Бот остановлен')


if __name__ == "__main__":
    main()

