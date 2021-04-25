from telegram.ext import Updater,CommandHandler,MessageHandler,Filters

bot_token = 'token'
updater = Updater(bot_token)
dispatcher = updater.dispatcher

hashmap = {}

def on_photo(function):
	handler = MessageHandler(Filters.photo, funciton)
	dispatcher.add_handler(handler)

def on_message(function):
	handler = MessageHandler(Filters.text & ~Filters.command, function)
	dispatcher.add_handler


@on_photo
def save(update,context):
	file_id = update.effective_message.photo[-1].file_unique_id
	@on_message
	def save_file(update,context):
		hashmap[update.effective_message.text] = file_id

@on_message
def send(update,context):
	text = update.effective_message.text
	if text in hashmap:
		update.effective_message.reply_photo(photo=hashmap[text])

updater.start_polling()
updater.idle()
