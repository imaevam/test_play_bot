from clarifai.rest import ClarifaiApp
import settings
from emoji import emojize
from random import randint, choice
from telegram import ReplyKeyboardMarkup, KeyboardButton

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


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Прислать собаку', KeyboardButton("Мои координаты", request_location=True), 'Заполнить анкету']
    ])


def is_dog(file_name):
    app = ClarifaiApp(api_key=settings.CLARIFAI_API_KEY)
    model = app.public_models.general_model
    response = model.predict_by_filename(file_name, max_concepts=5)
    if response['status']['code'] == 10000: #словарь внутри словаря, где лежит код
        for concept in response['outputs'][0]['data']['concepts']:
            if concept['name'] == 'dog':
                return True
    return False


if __name__ == "__main__":
    print(is_dog('images/dog1.jpg'))
    print(is_dog('images/cartoon.jpg'))