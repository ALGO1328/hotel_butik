import telebot
import datetime
from telebot import TeleBot
import calendar
from telebot import types
bot = TeleBot('7080192611:AAFA3GziINC_BRz8u0nEmxmP_NfVNMFHbwg')
cal = calendar.Calendar()
monthiter = cal.itermonthdays(2024, 4)
daysset = set()
for elem in monthiter:
    daysset.add(elem)
monthrange = max(daysset)
markup_calendar = telebot.types.InlineKeyboardMarkup(row_width=7)
markup_calendar.row(types.InlineKeyboardButton(text='Пн', callback_data='x'),
                    types.InlineKeyboardButton(text='Вт', callback_data='x'),
                    types.InlineKeyboardButton(text='Ср', callback_data='x'),
                    types.InlineKeyboardButton(text='Чт', callback_data='x'),
                    types.InlineKeyboardButton(text='Пт', callback_data='x'),
                    types.InlineKeyboardButton(text='Сб', callback_data='x'),
                    types.InlineKeyboardButton(text='Вс', callback_data='x'))
first_weekday = 0
for i in cal.itermonthdays2(2024, 4):
    first_weekday = i[1] + 1  # пн - 1, вт - 2
    break
buttons_arr = []
for i in range(0, first_weekday):
    buttons_arr.append(types.InlineKeyboardButton(' ', callback_data='x'))

