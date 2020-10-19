import logging #для записи отчета о работе бота
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from anketa import (anketa_start, anketa_name, anketa_rating, anketa_skip, anketa_comment,
                    anketa_dontknow)
from handlers import (greet_user, guess_number, send_dog_picture, user_coordinates,
                         talk_to_me, check_user_photo, subscribe, unsubscribe)
import settings
from jobs import send_updates

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}


def main():  # соединяет с платформой Telegram, "тело" нашего бота
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    jq = mybot.job_queue  # очередь задач
    jq.run_repeating(send_updates, interval=10, first=0)  # first=0 - запуск на нулевой секунде
    dp = mybot.dispatcher
    anketa = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Заполнить анкету)$'), anketa_start)
        ],
        states={
            'name': [MessageHandler(Filters.text, anketa_name)],
            'rating': [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), anketa_rating)],
            'comment': [
                CommandHandler('skip', anketa_skip),
                MessageHandler(Filters.text, anketa_comment)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, anketa_dontknow)
        ]
    )
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler("start", greet_user)) # Важен порядок Handler, в начале идут конкретные, частные, и только потом самые общие
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("dog", send_dog_picture))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать собаку)$'), send_dog_picture))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if  __name__ == "__main__":
    main()

# кодировка для логов windows 1251