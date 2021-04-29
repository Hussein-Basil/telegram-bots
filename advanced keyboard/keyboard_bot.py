from telegram import KeyboardButton, ReplyKeyboardMarkup
from handlers import Handlers,updater,dispatcher
from key import Key


class Config:
    keyboards = {
        'Main Menu' : [['First', 'Second'], ['Third'],['Button Editor']],
        'First' : [["Back","Main Menu"],['Button Editor']],
        'Second' : [["Back","Main Menu"],['Button Editor']]

        }
    steps = ["Main Menu"]
    handlers_waiting = []
    
    def markup(keyboard):
        rows = []
        for row in keyboard:
            cols = [KeyboardButton(col) for col in row]
            rows.append(cols)
        return ReplyKeyboardMarkup(rows)

class Bot:
    
    def reply(update,context):
        text = update.effective_message.text
        chat_id = update.effective_chat.id
        keyboards = Config.keyboards
        
        if text == "Main Menu":
            Config.steps = []

        if text == "Back":
            Config.steps.pop(-1)
            last_keyboard = keyboards[Config.steps[-1]]
            context.bot.send_message(chat_id, text, reply_markup=Config.markup(last_keyboard))

        if text == "Button Editor":
            for key in keyboards:
                keyboards[key] = [['Add Button','Exit Editor'] if x==['Button Editor'] else x for x in keyboards[key]]
            context.bot.send_message(chat_id, text, reply_markup=Config.markup(keyboards[Config.steps[-1]]))
        
        if text == "Exit Editor":
            for key in keyboards:
                keyboards[key] = [['Button Editor'] if x==['Add Button','Exit Editor'] else x for x in keyboards[key]]
            context.bot.send_message(chat_id, text, reply_markup=Config.markup(keyboards[Config.steps[-1]]))
                
        
        if text == "Add Button":
            reply_handler = dispatcher.handlers[0][-1]
            dispatcher.remove_handler(reply_handler)
            Config.handlers_waiting.append(reply_handler)

            context.bot.send_message(chat_id, 'Enter Button Name')
            Handlers.on_message(Bot.add_button)

        if text in keyboards:
            keyboard = keyboards[text]
            context.bot.send_message(chat_id, text, reply_markup=Config.markup(keyboard))
            Config.steps.append(text)
    
    
    def add_button(update,context):

        name = update.effective_message.text
        chat_id = update.effective_chat.id
        keyboards = Config.keyboards

        if name == "Exit Editor":
            for key in Config.keyboards:
                Config.keyboards[key] = [['Button Editor'] if x==['Add Button','Exit Editor'] else x for x in Config.keyboards[key]]
            reply_markup = Config.markup(Config.keyboards[Config.steps[-1]])
            context.bot.send_message(chat_id, name, reply_markup=reply_markup)

        elif name in keyboards:
            context.bot.send_message(chat_id, 'Name is already taken. Try Again')

        else :
            button = Key(name, Config.steps[-1], Config.keyboards)
            Config.keyboards[button]=[['Button Editor']]
            reply_markup = Config.markup(Config.keyboards[Config.steps[-1]])
            context.bot.send_message(chat_id, 'Adding Button is Done', reply_markup=reply_markup)
            dispatcher.remove_handler(dispatcher.handlers[0][-1])
            dispatcher.add_handler(Config.handlers_waiting.pop())
        

@Handlers.on_command(command='start')
def start(update,context):
    main_menu = Config.markup(Config.keyboards['Main Menu'])
    update.effective_message.reply_text('Welcome', reply_markup=main_menu)
    Handlers.on_message(Bot.reply)


updater.start_polling()
updater.idle()