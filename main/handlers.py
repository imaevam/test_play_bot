from glob import glob
from jobs import alarm
import os
from random import choice
from db import (db, get_or_create_user, subscribe_user, unsubscribe_user,
                    save_dog_image_vote, user_voted, get_image_rating)
from utils import (is_dog, play_random_numbers, main_keyboard,
                    dog_rating_inline_keyboard)


def greet_user(update, context):  # при вводе команды start
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    print('Вызван /start')
    update.message.reply_text(
        f"Привет, пользователь! Ты вызвал команду /start {user['emoji']}",
        reply_markup=main_keyboard()
        )


def talk_to_me(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(f"{user_text}{user['emoji']}", reply_markup=main_keyboard())


def guess_number(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
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
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    dog_photo_list = glob('images/dog*.jp*g')
    dog_pic_filename = choice(dog_photo_list)
    chat_id = update.effective_chat.id
    if user_voted(db, dog_pic_filename, user['user_id']):
        rating = get_image_rating(db, dog_pic_filename)
        keyboard = None
        caption = f'Рейтинг картинки {rating}'
    else:
        keyboard = dog_rating_inline_keyboard(dog_pic_filename)
        caption = None
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(dog_pic_filename, 'rb'),
        reply_markup=keyboard,
        caption=caption
    )


def user_coordinates(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {user['emoji']}",
        reply_markup=main_keyboard()
    )


def check_user_photo(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
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


def subscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    subscribe_user(db, user)
    update.message.reply_text('Вы успешно подписались')


def unsubscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    unsubscribe_user(db, user)
    update.message.reply_text('Вы успешно отписались')


def set_alarm(update, context):
    try:
        alarm_seconds = abs(int(context.args[0]))
        context.job_queue.run_once(alarm, alarm_seconds, context=update.message.chat_id)
        update.message.reply_text(f'Уведомление через {alarm_seconds} секунд')
    except (ValueError, TypeError):
        update.message.reply_text('Введите целое число секунд после команды')


def dog_picture_rating(update, context):
    update.callback_query.answer()
    callback_type, image_name, vote = update.callback_query.data.split('|')
    vote = int(vote)
    user = get_or_create_user(db, update.effective_user, update.effective_chat.id)
    save_dog_image_vote(db, user, image_name, vote)
    rating = get_image_rating(db, image_name)
    update.callback_query.edit_message_caption(f"Рейтинг картинки {rating}")