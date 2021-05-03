from telegram.ext import *
from constants import Constants

TOKEN = Constants.BOT_TOKEN

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

class Handlers:
    def on_command(*args, **kwargs):
        def command_handler(function):
            handler = CommandHandler(kwargs['command'], function)
            handler.run_async = True
            dispatcher.add_handler(handler)
        return command_handler
    
    def on_message(function):
        handler = MessageHandler(Filters.text & ~Filters.command, function)        
        dispatcher.add_handler(handler)

    def on_message_(filters=None):
        def message_handler(func):
            handler = MessageHandler(filters, func)
            handler.run_async = True
            dispatcher.add_handler(handler)
        return message_handler

    def on_photo(function):
        handler = MessageHandler(Filters.photo & Filters.animation, function)
        dispatcher.add_handler(handler)

    def on_document(function):
        handler = MessageHandler(Filters.document, function)
        dispatcher.add_handler(handler)

    def on_reply(function):
        handler = MessageHandler(Filters.reply, function)
        dispatcher.add_handler