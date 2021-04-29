from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


token = "token"
updater = Updater(token)
dispatcher = updater.dispatcher

class Handlers():
    def on_command(*args, **kwargs):
        def command_handler(function):
            handler = CommandHandler(kwargs['command'], function)
            dispatcher.add_handler(handler)
        return command_handler

    def on_message(function):
        handler = MessageHandler(Filters.text & ~Filters.command, function)        
        dispatcher.add_handler(handler)

    def on_photo(function):
        handler = MessageHandler(Filters.photo & Filters.animation, function)
        dispatcher.add_handler(handler)

    def on_document(function):
        handler = MessageHandler(Filters.document, function)
        dispatcher.add_handler(handler)

    def on_reply(function):
        handler = MessageHandler(Filters.reply, function)
        dispatcher.add_handler