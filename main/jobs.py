def send_hello(context):
    context.bot.send_message(chat_id=1395040186, text=f'Привет {context.job.interval}!')  # chat_id посмотреть в mongodb compass
    context.job.interval += 5
    if context.job.interval > 15:
        context.bot.send_message(chat_id=1395040186, text="Задание выполнено!")
        context.job.schedule_removal()