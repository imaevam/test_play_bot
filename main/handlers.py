from glob import glob
import os
from random import choice

from utils import get_smile, is_dog, play_random_numbers, main_keyboard

def greet_user(update, context): #при вводе команды start
    print('Вызван /start')
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f"Привет, пользователь! Ты вызвал команду /start {context.user_data['emoji']}",
        reply_markup=main_keyboard()
        )  #ответ пользователю


def talk_to_me(update, context): #для ответа пользователю
    context.user_data['emoji'] = get_smile(context.user_data)
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(f"{user_text}{context.user_data['emoji']}", reply_markup=main_keyboard())


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
    update.message.reply_text(message, reply_markup=main_keyboard())


def send_dog_picture(update, context):
    dog_photo_list = glob('images/dog*.jp*g')
    dog_pic_filename = choice(dog_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(dog_pic_filename, 'rb'), reply_markup=main_keyboard()) #функция отправки фото, принимает аргументы: в какой чат отправить картинку и открываем файл с картинкой в формате rb


def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}",
        reply_markup=main_keyboard()
    )


def check_user_photo(update, context):
    update.message.reply_text('Обрабатываем фотографию')
    os.makedirs('downloads', exist_ok=True)
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('downloads', f'{user_photo.file_id}.jpg')
    user_photo.download(file_name)
    if is_dog(file_name):
        update.message.reply_text("Обнаружена собака, добавляю в библиотеку.")
        new_filename = os.path.join('images', f'dog_{user_photo.file_id}.jpg')
        os.rename(file_name, new_filename)
    else:
        update.message.reply_text("Тревога, собака не обнаружена!")
        os.remove(file_name)

