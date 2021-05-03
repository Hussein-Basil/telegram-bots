from telegram.ext import MessageFilter
from data import Config

class FilterKeyboard(MessageFilter):
    def filter(self, message):
        return message.text in Config.keyboards
        
filter_keyboard = FilterKeyboard()