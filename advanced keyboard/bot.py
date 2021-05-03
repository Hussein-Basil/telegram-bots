from telegram import *
from telegram.ext import *
from handlers import updater,dispatcher
from datetime import datetime
from key import Key
from helpers import Helpers
from data import *
from custom_filters import *
import re

(NAVIGATION, BUTTON_EDITOR) = 0,1
DIRECTION = 2
(CANCEL, EXIT) = 3,4
ADDING_BUTTON = 5
END = 6
ADD_BUTTON = 7

h = Helpers
c = Config

def start(update,context) -> int:
    global user 
    user = User(update.effective_chat.id)
    main_menu = h.reply_kb(c.keyboards['Main Menu'])
    update.effective_message.reply_text('Welcome', reply_markup=main_menu)
    
    return NAVIGATION

def ping(update,context):
    before = datetime.now()
    context.bot.get_me()
    after = datetime.now()
    diff = (after - before).microseconds // 1000 
    update.effective_message.reply_text(f'Pong {diff}ms')

def navigate(update,context) -> None:
    text = update.effective_message.text
    chat_id = update.effective_chat.id
    keyboards = c.keyboards

    if text == "Main Menu":
        user.steps = []

    h.update_reply_kb(update, keyboards[text])
    user.steps.append(text)


def back(update,context) -> None:
    text = update.effective_message.text
    chat_id = update.effective_chat.id
    keyboards = c.keyboards

    user.steps.pop(-1)
    last_keyboard = keyboards[user.steps[-1]]
    context.bot.send_message(chat_id, text, reply_markup=h.reply_kb(last_keyboard))


def editor_clicked(update,context) -> int:
    text = update.effective_message.text
    chat_id = update.effective_chat.id

    h.swap(['Button Editor'], ['Add Button','Exit Editor'], c.keyboards)
    context.bot.send_message(chat_id, text, reply_markup=h.reply_kb(c.keyboards[user.steps[-1]]))

    return BUTTON_EDITOR
    

def select_button(update,context) -> int:
    if 'button_selected' in context.user_data:
        h.deselect_button(context.user_data.pop('button_selected'), c.keyboards[user.steps[-1]])
        context.user_data.pop('button_selected_msg').delete()

    button_name = context.user_data['button_name'] = update.effective_message.text

    h.select_button(button_name, c.keyboards[user.steps[-1]])
    
    reply_markup = h.reply_kb(c.keyboards[user.steps[-1]])
    msg = update.effective_message.reply_text(".", reply_markup=reply_markup)
    
    buttons = [
        [
            InlineKeyboardButton('Up', callback_data='up'),
        ],
        [
            InlineKeyboardButton('Left', callback_data='left'),
            InlineKeyboardButton('Down', callback_data='down'),
            InlineKeyboardButton('Right', callback_data='right'),
        ],
        [
            InlineKeyboardButton('Cancel', callback_data='cancel')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    msg = update.effective_message.reply_text(button_name, reply_markup=reply_markup)

    context.user_data['button_selected'] = button_name
    context.user_data['button_selected_msg'] = msg

    return DIRECTION

def move_button(update,context) -> None:
    if 'moved' in context.user_data:
        context.user_data.pop('moved').delete()
    button_name = f"[{context.user_data['button_name']}]"
    k = Key(button_name, user.steps[-1], c.keyboards)
    k.move(update.callback_query.data)
    reply_markup = h.reply_kb(c.keyboards[user.steps[-1]])
    msg = context.bot.send_message(update.effective_chat.id, 'Moved', reply_markup=reply_markup)
    context.user_data['moved'] = msg
    update.callback_query.answer(f'Moved {update.callback_query.data}')

def cancel_edit(update,context) -> int:

    if 'button_selected' in context.user_data:
        h.deselect_button(context.user_data.pop('button_selected'), c.keyboards[user.steps[-1]])
        context.user_data.pop('button_selected_msg').delete()
    
    reply_markup = h.update_reply_kb(update, c.keyboards[user.steps[-1]])
    context.bot.send_message(update.effective_chat.id, 'Exit from editing button', reply_markup=reply_markup)
    ConversationHandler.END

def deselect_button(update,context):
    ConversationHandler.END

def exit_editor(update,context) -> int:
    
    if 'button_selected' in context.user_data:
        h.deselect_button(context.user_data.pop('button_selected'), c.keyboards[user.steps[-1]])
        context.user_data.pop('button_selected_msg').delete()
        
    h.swap(['Add Button', 'Exit Editor'], ['Button Editor'], c.keyboards)
    reply_markup = h.reply_kb(c.keyboards[user.steps[-1]])
    update.effective_message.reply_text("Exited from Button Editor", reply_markup=reply_markup)
    
    return NAVIGATION


def add_button(update,context) -> int:
    msg = context.bot.send_message(update.effective_chat.id, "You are in Adding Buttons Window!", reply_markup=ReplyKeyboardRemove())
    msg.delete()
    reply_markup = InlineKeyboardMarkup.from_button(InlineKeyboardButton('Cancel Adding Button', callback_data='cancel'))
    msg2 = context.bot.send_message(update.effective_chat.id, "Enter Button Name :", reply_markup=reply_markup)
    context.user_data['msg2'] = msg2
    return ADD_BUTTON

def add_button_name(update,context) -> int:
    button_name = update.effective_message.text
    c.keyboards[user.steps[-1]].insert(0,[button_name])
    c.keyboards[button_name] = [["Back","Main Menu"],['Button Editor']]
    reply_markup = h.reply_kb(c.keyboards[user.steps[-1]])
    context.bot.send_message(update.effective_chat.id, f"Button {button_name} Added!", reply_markup=reply_markup)

    return BUTTON_EDITOR

def button_exist(update,context) -> None:
    chat_id = update.effective_chat.id
    button_name = update.effective_message.text
    context.bot.send_message(chat_id, f"Button {button_name} is already taken. Try another name please!")

def cancel_adding_button(update,context) -> int:
    msg2 = context.user_data['msg2']
    msg2.delete()
    reply_markup = h.reply_kb(c.keyboards[user.steps[-1]])
    context.bot.send_message(update.effective_chat.id, "Adding Button Cancelled.", reply_markup=reply_markup)
    
    return BUTTON_EDITOR

def stop(update,context) -> int:
    context.bot.send_message(update.effective_chat.id, "Conversation has ended.")
    context.user_data.clear()
    ConversationHandler.END


# secondary conversation handler inside primary conv_handler
button_editor_handler = ConversationHandler(
    entry_points = [MessageHandler(filter_keyboard, select_button)],
    states = {
        DIRECTION : [CallbackQueryHandler(move_button, pattern=re.compile('(up|down|right|left)'))]
        },
    fallbacks = [
        CallbackQueryHandler(cancel_edit, pattern='cancel'),
        MessageHandler(filter_keyboard, deselect_button)
        ],
    allow_reentry = True,
    map_to_parent = {CANCEL : BUTTON_EDITOR, ADD_BUTTON : ADD_BUTTON}
)

# main conversation handler
conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('start'), start)],
    states = {
        NAVIGATION : [
            MessageHandler(filter_keyboard, navigate),
            MessageHandler(Filters.regex('ping'), ping),
            MessageHandler(Filters.regex('Button Editor'), editor_clicked),
            MessageHandler(Filters.regex('Back'), back)
        ],
        BUTTON_EDITOR : [
            button_editor_handler,
            MessageHandler(Filters.regex('Back'), back),
            MessageHandler(Filters.regex('Exit Editor'), exit_editor),
            MessageHandler(Filters.regex('Add Button'), add_button)
        ],
        ADD_BUTTON : [
            MessageHandler(~filter_keyboard, add_button_name), 
            MessageHandler(filter_keyboard, button_exist),
            CallbackQueryHandler(cancel_adding_button, pattern='cancel')
        ]
    },
    allow_reentry = True,
    fallbacks = [MessageHandler(Filters.regex('stop'), stop)],
)

dispatcher.add_handler(conv_handler)
updater.start_polling()
updater.idle()