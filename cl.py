import calendar
from telebot import types
from config import month_desc


def create_cal(year, month):
    cal = calendar.Calendar()
    monthiter = cal.itermonthdays(2024, 4)
    daysset = set()
    for elem in monthiter:
        daysset.add(elem)
    monthrange = max(daysset)
    markup_calendar = types.InlineKeyboardMarkup(row_width=7)
    markup_calendar.add(types.InlineKeyboardButton(text='Пн', callback_data='x'),
                        types.InlineKeyboardButton(text='Вт', callback_data='x'),
                        types.InlineKeyboardButton(text='Ср', callback_data='x'),
                        types.InlineKeyboardButton(text='Чт', callback_data='x'),
                        types.InlineKeyboardButton(text='Пт', callback_data='x'),
                        types.InlineKeyboardButton(text='Сб', callback_data='x'),
                        types.InlineKeyboardButton(text='Вс', callback_data='x'))
    first_weekday = 0
    button_counter = 0
    for i in cal.itermonthdays2(year, month):
        first_weekday = i[1] + 1  # пн - 1, вт - 2
        break
    buttons_arr = list()
    if first_weekday > 1:
        for i in range(0, first_weekday):
            buttons_arr.append(types.InlineKeyboardButton(' ', callback_data='x'))
            button_counter += 1
    for i in range(1, int(calendar.monthrange(year, month)[1]) + 1):
        buttons_arr.append(types.InlineKeyboardButton(f'{i}', callback_data=f'{i}.{month}.{year}'))
        button_counter += 1
    while button_counter < 35:
        buttons_arr.append(types.InlineKeyboardButton(' ', callback_data='x'))
        button_counter += 1
    markup_calendar.add(*buttons_arr)
    markup_calendar.add(types.InlineKeyboardButton('<--', callback_data=f'prev_{month}'),
                        types.InlineKeyboardButton(f'{month_desc[str(month)]} {year}', callback_data='x'),
                        types.InlineKeyboardButton('-->', callback_data=f'next_{month}'))
    return markup_calendar