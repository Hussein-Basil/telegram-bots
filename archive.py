from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
import logging

bot_token = 'token'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(bot_token)
dispatcher = updater.dispatcher

hashmap = {}

def on_photo(function):
	handler = MessageHandler(Filters.photo, function)
	dispatcher.add_handler(handler)

def on_message(function):
	handler = MessageHandler(Filters.text & ~Filters.command, function)
	dispatcher.add_handler

def save_file(update,context):
		print('ho')
		hashmap[update.effective_message.text] = 'AQADOcjSmi4AAz-zBQAB'


@on_photo
def save(update,context):
	print('he')
	file_id = update.effective_message.photo[-1].file_unique_id
	print(file_id)
	on_message(save_file)

@on_message
def send(update,context):
	print('ha')
	text = update.effective_message.text
	if text in hashmap:
		update.effective_message.reply_photo(photo=hashmap[text])

updater.start_polling()

