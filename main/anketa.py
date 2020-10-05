from telegram import ReplyKeyboardRemove

def anketa_start(update, context):
    update.message.reply_text(
        'Привет! Как Вас зовут?',
        reply_markup=ReplyKeyboardRemove()
    )
    return "name"