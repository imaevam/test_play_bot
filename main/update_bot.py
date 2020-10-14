import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem
import datetime
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
         'password': settings.PROXY_PASSWORD}}


def greet_user(update, context):
    text = """Welcome to the Solar System Bot
    Today I will be your guide to the Solar System and the Night Sky.
    Here are the planets listed in order of their distance from the Sun:
    Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune and Pluto. Please, use link /planet
    As well, you can try link /wordcount. It's a simple way to use bot that
    counts how many words user have typed.
    When is the next full moon? Try link /next_full_moon and your date.
    """
    update.message.reply_text(text)


def talk_to_me(update, context):
    user_text = update.message.text
    update.message.reply_text(f'You too, {user_text}. Please, try to use link /planet and your name of the planet or you can use link /wordcount and your question.')


def counting_words(update, context):
    try:
        user_text = update.message.text
        if user_text == '/wordcount':
            text = 'Did you write something after link /wordcount? Let\'s try one more time.'
        else:
            user_text = len(update.message.text.split())
            text = f'You have typed {user_text - 1} words.'
    except AttributeError:
        text = 'Did you write something after link /wordcount? Let\'s try one more time.'
    update.message.reply_text(text)


def planet_constellation(update, context):
    try:
        user_choose = update.message.text
        _, planet = user_choose.split()
        current_time = datetime.datetime.today().strftime("%Y/%m/%d")
        user_planet = getattr(ephem, planet)(current_time)
        result = ephem.constellation(user_planet)
        text = f'{planet} is currently in the constellation of {result}.'
    except AttributeError:
        text = 'Did you write the name of the planet correct?'
    update.message.reply_text(text)


def next_full_moon(update, context):
    try:
        user_text = update.message.text
        _, user_date = user_text.split()
        result = ephem.next_full_moon(user_date)
        text = f'The next full moon occur on {result}'
    except AttributeError:
        text = 'Please, write link \next_full_moon with your date'
    update.message.reply_text(text)
        

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet_constellation))
    dp.add_handler(CommandHandler("wordcount", counting_words))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Starting bot")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()

#кодировка для логов windows 1251
