from emoji import emojize
from random import choice
import logging #для записи отчета о работе бота
from random import randint
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
    print('Вызван /start')
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Привет, пользователь! Ты вызвал команду /start {context.user_data['emoji']}")  #ответ пользователю

def talk_to_me(update, context): #для ответа пользователю
    context.user_data['emoji'] = get_smile(context.user_data)
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(f"{user_text}{context.user_data['emoji']}")

def get_smile(user_data): # передаем функции словарь 
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']

def play_random_numbers(user_number):
    bot_number = randint(user_number-10, user_number+10) # левая и правая граница (минимум и максимум)
    if user_number > bot_number:
        message = f"Ты загадал {user_number}, а я загадал {bot_number}, ты выиграл!"
    elif user_number == bot_number:
        message = f"Ты загадал {user_number}, а я загадал {bot_number}, ничья!"
    else:
        message = f"Ты загадал {user_number}, а я загадал {bot_number}, я выиграл!"
    return message

def guess_number(update, context): # то, что ввел пользователь будет доступно в переменной context.args
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Пожалуйста, ведите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message)

def main(): # Функция, которая соединяется с платформой Telegram, "тело" нашего бота
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user)) # Важен порядок Handler, в начале идут общие
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) # реагировать только на текстовые сообщения
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if  __name__ == "__main__":
    main()

#кодировка для логов windows 1251