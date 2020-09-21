import logging #для записи отчета о работе бота
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from handlers import (greet_user, guess_number, send_dog_picture, user_coordinates,
                         talk_to_me)
import settings


logging.basicConfig(filename='bot.log', level=logging.INFO)
# Настройки прокси
PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
         'password': settings.PROXY_PASSWORD
    }
}


def main(): # Функция, которая соединяется с платформой Telegram, "тело" нашего бота
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user)) # Важен порядок Handler, в начале идут конкретные, частные, и только потом самые общие
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("dog", send_dog_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать собаку)$'), send_dog_picture))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) # реагировать только на текстовые сообщения
    
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if  __name__ == "__main__":
    main()

#кодировка для логов windows 1251