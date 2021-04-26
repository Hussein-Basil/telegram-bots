from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
from telegram.ext.dispatcher import run_async
from telegram import KeyboardButton, ReplyKeyboardMarkup
f
bot_token = 'token'
updater = Updater(bot_token)
dispatcher = updater.dispatcher


class Handlers:
    def on_command(*args, **kwargs):
        def command_handler(function):
            handler = CommandHandler(kwargs['command'], function)
            dispatcher.add_handler(handler)
        return command_handler

    def on_message(function):
        handler = MessageHandler(Filters.text & ~Filters.command, function)        
        dispatcher.add_handler(handler)


class Keyboard:
    handlers_queue = []
    steps = ["Main Menu"]
    keyboards = {
        'Main Menu' : [['First', 'Second'], ['Third'], ['Button Editor']],
        'First' : [['1', '2'], ['3'], ['Back','Main Menu'], ['Button Editor']],
        'Second' : [['Not Dead End'], ['Back','Main Menu'], ['Button Editor']],
        'Not Dead End': [['Files'], ['Photos'], ['Voice Notes'], ['Back','Main Menu'], ['Button Editor']]
        }
        
    def markup(key_names):
        rows = []
        for r in key_names:
            cols = []
            for c in r:
                cols.append(KeyboardButton(c))
            rows.append(cols)
        return ReplyKeyboardMarkup(rows)


class Bot:
    
    def reply(update,context):
        text = update.effective_message.text
        chat_id = update.effective_chat.id
        keyboards = Keyboard.keyboards
        markup = Keyboard.markup

        if text == "Main Menu":
            Keyboard.steps = []

        if text == "Back":
            Keyboard.steps.pop(-1) # remove current keyboard from steps
            last_keyboard = keyboards[Keyboard.steps[-1]]
            context.bot.send_message(chat_id, text, reply_markup=markup(last_keyboard))

        if text == "Button Editor":
            for key in keyboards:
                keyboards[key] = [['Add Button','Exit Editor'] if x==['Button Editor'] else x for x in keyboards[key]]
            context.bot.send_message(chat_id, text, reply_markup=markup(keyboards[Keyboard.steps[-1]]))
        
        if text == "Exit Editor":
            for key in keyboards:
                keyboards[key] = [['Button Editor'] if x==['Add Button','Exit Editor'] else x for x in keyboards[key]]
            context.bot.send_message(chat_id, text, reply_markup=markup(keyboards[Keyboard.steps[-1]]))
                
        
        if text == "Add Button":
            reply_handler = dispatcher.handlers[0][-1]
            dispatcher.remove_handler(reply_handler)
            Keyboard.handlers_queue.append(reply_handler)

            context.bot.send_message(chat_id, 'Enter Button Name')
            Handlers.on_message(Bot.add_button)
            print(dispatcher.handlers[0])

        if text in keyboards:
            keyboard = keyboards[text]
            context.bot.send_message(chat_id, text, reply_markup=markup(keyboard))
            Keyboard.steps.append(text)

        print(Keyboard.steps)
    
    
    def add_button(update,context):
        chat_id = update.effective_chat.id
        keyboards = Keyboard.keyboards
        markup = Keyboard.markup

        if update.effective_message.text == "Exit Editor":
            for key in keyboards:
                keyboards[key] = [['Button Editor'] if x==['Add Button','Exit Editor'] else x for x in keyboards[key]]
            context.bot.send_message(chat_id, text, reply_markup=markup(keyboards[Keyboard.steps[-1]]))

        button_name = update.effective_message.text
        if button_name in keyboards:
            context.bot.send_message(chat_id, 'Name is already taken')
        else :
            keyboards[Keyboard.steps[-1]].insert(0,[button_name])
            current = keyboards[Keyboard.steps[-1]]
            context.bot.send_message(chat_id, 'Adding Button is Done', reply_markup=markup(current))

            dispatcher.remove_handler(dispatcher.handlers[0][-1]) # removeing button name handler
            dispatcher.add_handler(Keyboard.handlers_queue[-1]) # adding reply handler
        



@Handlers.on_command(command='start')
def start(update,context):
    print(dispatcher.handlers[0])
    main_menu = Keyboard.markup(Keyboard.keyboards['Main Menu'])
    update.effective_message.reply_text('Welcome', reply_markup=main_menu)
    Handlers.on_message(Bot.reply)
    print(dispatcher.handlers[0])


updater.start_polling()
updater.idle()