from glob import glob
import logging #для записи отчета о работе бота
from random import choice
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings


logging.basicConfig(filename='bot.log', level=logging.INFO)
# Настройки прокси
PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
         'password': settings.PROXY_PASSWORD
    }
}

def greet_user(update, context): #при вводе команды start
    print("Вызван /start")
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')  #ответ пользователю

def send_dog_picture(update, context):
    dog_photo_list = glob('images/dog*.jp*g')
    dog_pic_filename = choice(dog_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(dog_pic_filename, 'rb')) #функция отправки фото, принимает аргументы: в какой чат отправить картинку и открываем файл с картинкой в формате rb

def main(): # Функция, которая соединяется с платформой Telegram, "тело" нашего бота
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user)) # Важен порядок Handler, в начале идут общие
    dp.add_handler(CommandHandler("dog", send_dog_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) # реагировать только на текстовые сообщения
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

def talk_to_me(update, context): #для ответа пользователю
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)

if  __name__ == "__main__":
    main()

#кодировка для логов windows 1251