from telegram import ReplyKeyboardMarkup, KeyboardButton

class Helpers:
    def inline_kb(inline_keyboard: list):
        return InlineKeyboardMarkup(inline_keyboard, resize_keyboard=True)

    def reply_kb(inline_keyboard: list):
        return ReplyKeyboardMarkup(inline_keyboard,resize_keyboard=True)
        
    def update_reply_kb(update, kb) -> None:
        if hasattr(update, "data"):
            message = update.callback_query.message
        else:
            message = update.effective_message
        text = message.text
        reply_markup = Helpers.reply_kb(kb)
        message.reply_text(text, reply_markup=reply_markup)

    def swap(from_: list, to: list, keyboards: dict):
        for key in keyboards:
            keyboards[key] = [to if x==from_ else x for x in keyboards[key]]

    def select_button(target: str, keyboard):
        for r in range(len(keyboard)):
            for c in range(len(keyboard[r])):
                if keyboard[r][c] == target:
                    keyboard[r][c] = f"[{keyboard[r][c]}]"

    def deselect_button(target, keyboard):
        for r in range(len(keyboard)):
            for c in range(len(keyboard[r])):
                if keyboard[r][c] == f"[{target}]":
                    keyboard[r][c] = target