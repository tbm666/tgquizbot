from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def generate_options_keyboard(current_index, answer_options):
    builder = InlineKeyboardBuilder()
    for option_index, option in enumerate(answer_options):
        callback_data = f"{current_index}:{option_index}"
        builder.add(types.InlineKeyboardButton(text=option, callback_data=callback_data))
    builder.adjust(1)
    return builder.as_markup()


def main_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="🎮 Начать игру"))
    builder.add(types.KeyboardButton(text="📊 Результаты"))
    return builder.as_markup(resize_keyboard=True)
