from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup

bot_token = 'token'
updater = Updater(bot_token)
dispatcher = updater.dispatcher


class Handlers:
    def on_start(function):
        handler = CommandHandler('start',function)
        dispatcher.add_handler(handler)

    def on_message(function):
        handler = MessageHandler(Filters.text & ~Filters.command, function)
        dispatcher.add_handler(handler)


class Keyboard:
    steps = []
    
    def markup(key_names):
        '''
        keyboard consists of rows
        each row consists of single /or multiple button(s)
        input : rows = [['First','Second'],['Third']]
        '''
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

        if text == 'First':
            display_text = 'This is full directory of first'
            first_keyboard = Keyboard.markup([['1', '2'], ['3'], ['Main Menu', 'Back']])
            context.bot.send_message(chat_id, display_text, reply_markup=first_keyboard)
            Keyboard.steps.append(first_keyboard)
        
        if text == 'Second':
            display_text = 'full directory of second'
            second_keyboard = Keyboard.markup([['Not Dead End'], ['Main Menu', 'Back']])
            context.bot.send_message(chat_id, display_text, reply_markup=second_keyboard)
            Keyboard.steps.append(second_keyboard)
        
        if text == "Main Menu":
            display_text = 'menu'
            main_menu = Keyboard.markup([['First', 'Second'], ['Third']])
            context.bot.send_message(chat_id, display_text, reply_markup=main_menu)
            Keyboard.steps = [main_menu]

        if text == "Back":
            display_text = 'back'
            Keyboard.steps.pop(-1)
            back_keyboard = Keyboard.steps[-1]
            context.bot.send_message(chat_id, display_text, reply_markup=back_keyboard)
            
        if text == 'Not Dead End':
            display_text = 'Not Dead End'
            not_dead_end = Keyboard.markup([['Files'], ['Photos'], ['Voice Notes'], ['Main Menu', 'Back']])
            context.bot.send_message(chat_id, display_text, reply_markup=not_dead_end)
            Keyboard.steps.append(not_dead_end)


@Handlers.on_start
def start(update,context):
    main_menu = Keyboard.markup([['First', 'Second'], ['Third']])
    update.effective_message.reply_text('Welcome', reply_markup=main_menu)
    Keyboard.steps.append(main_menu)
    Handlers.on_message(Bot.reply)

updater.start_polling()
updater.idle()