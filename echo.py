from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

bot_token = 'token'
updater = Updater(bot_token)
dispatcher = updater.dispatcher

def message_handler(function):
    handler = MessageHandler(Filters.text & ~Filters.command)
    dispatcher.add_handler(handler)

@message_handler
def echo(update,context):
    context.bot.send_message(update.effective_chat.id, update.effective_message.text)

updater.start_polling()
updater.idle()
