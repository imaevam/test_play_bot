# Проект Playground_bot
My test bot for telegram. He provides main information about constellation of planets. Mostly just a playground.

Это бот для Телеграм, который присылает пользователю фотографии собачек.

## Установка

1. Клонируйте репазиторий с github
2. Создайте виртуальное окружение
3. Установите зависимости `pip install -r requirements.txt`
4. Создайте файл `settings.py`
5. Впишите в settings.py переменные: 
```
API_KEY = "API-ключ бота"
PROXY_URL = 'Адрес прокси'
PROXY_USERNAME = 'Логин на прокси'
PROXY_PASSWORD = 'Пароль на прокси'
USER_EMOJI = [':smiley_cat:', ':kissing_cat:', ':-1:', ':thumbsdown:', ':ok_hand:', ':punch:', ':facepunch:',
':fist:', ':v:', ':wave:', ':hand:', ':raised_hand:', ':open_hands:']
```
6. Запустите бота командой `playground_bot.py`