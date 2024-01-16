from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_hi1 = KeyboardButton(text='🔎Поиск')

greet_kb1 = ReplyKeyboardMarkup(keyboard=[[button_hi1]], resize_keyboard=True)