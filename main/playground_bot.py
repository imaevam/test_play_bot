from datetime import time
import logging
from anketa import (anketa_start, anketa_name, anketa_rating, anketa_skip, anketa_comment,
                    anketa_dontknow)
from jobs import send_updates
from handlers import (greet_user, guess_number, send_dog_picture, user_coordinates,
                        talk_to_me, check_user_photo, subscribe, unsubscribe, set_alarm,
                        dog_picture_rating)
import pytz
import settings
from telegram.bot import Bot
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, 
                                ConversationHandler, CallbackQueryHandler)
from telegram.ext import messagequeue as mq
from telegram.ext.jobqueue import Days
from telegram.utils.request import Request


logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

class MQBot(Bot):  # наследование на базе обычного бота
    def __init__(self, *args, is_queued_def=True, msg_queue=None, **kwargs):
        super().__init__(*args, **kwargs)  # в начале отрабатывают методы класса Bot 
        self._is_messages_queued_default = is_queued_def  # очередь по умолчанию
        self._msg_queue = msg_queue or mq.MessageQueue()  # модуль, который создает очередь, установление лимитов

    def __del__(self):
        try:
            self._msg_queue.stop()  
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        return super().send_message(*args, **kwargs)  # рассылка сообщений из jobs.py


def main():  # соединяет с платформой Telegram, "тело" нашего бота
    request = Request(   # для запроса к платформе телеграм
        con_pool_size=8,  # до 8 соединений
        proxy_url=PROXY['proxy_url'],
        urllib3_proxy_kwargs=PROXY['urllib3_proxy_kwargs']  # для обхода блокировок
    )
    bot = MQBot(settings.API_KEY, request=request)
    mybot = Updater(bot=bot, use_context=True)

    jq = mybot.job_queue  # очередь задач
    target_time = time(12, 0, tzinfo=pytz.timezone('Europe/Moscow'))  # 12:00; поддержка часовых поясов
    target_days = (Days.MON, Days.WED, Days.FRI)  # рассылка сообщений по понедельникам, средам и пятницам
    jq.run_daily(send_updates, target_time, target_days)
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
    dp.add_handler(CommandHandler('alarm', set_alarm))
    dp.add_handler(CallbackQueryHandler(dog_picture_rating, pattern='^(rating|)'))
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