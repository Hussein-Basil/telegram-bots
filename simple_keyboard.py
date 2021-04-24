from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup

bot_token = 'token'
updater = Updater(bot_token)
dispatcher = updater.dispatcher

def on_start(function):
    handler = CommandHandler('start',start)
    dispatcher.add_handler(handler)

@on_start
def start(update,context):
    keyboard = [
        [KeyboardButton('First'),KeyboardButton('Second')],
        [KeyboardButton('Third')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.effective_message.reply_text('Welcome',reply_markup=reply_markup)

updater.start_polling()
updater.idle()