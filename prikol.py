import datetime
import pytz
import telebot
from telebot import types
from datetime import ca
print(datetime.datetime.now(pytz.timezone('Europe/Moscow')))
bot = telebot.TeleBot('7080192611:AAFA3GziINC_BRz8u0nEmxmP_NfVNMFHbwg')


def make_cal(message, month, *args):
    if month == 'curr':
        pass
    elif month == 'next':
        delta = datetime.datetime.now().replace(month=(args[0]) + 1)

    ctime = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    year = ctime.year
    month = ctime.month
    day = ctime.day
    month_desc = {'1': 'Январь',
                  '2': 'Февраль',
                  '3': 'Март',
                  '4': 'Апрель',
                  '5': 'Май',
                  '6': 'Июнь',
                  '7': 'Июль',
                  '8': 'Август',
                  '9': 'Сентябрь',
                  '10': 'Октябрь',
                  '11': 'Ноябрь',
                  '12': 'Декабрь'}

    cal = types.InlineKeyboardMarkup(row_width=7)
    a = datetime.datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    wd = a.weekday()
    temp_set = list()

    cal.add(types.InlineKeyboardButton('Пн', callback_data='x'),
            types.InlineKeyboardButton('Вт', callback_data='x'),
            types.InlineKeyboardButton('Ср', callback_data='x'),
            types.InlineKeyboardButton('Чт', callback_data='x'),
            types.InlineKeyboardButton('Пт', callback_data='x'),
            types.InlineKeyboardButton('Сб', callback_data='x'),
            types.InlineKeyboardButton('Вс', callback_data='x'))
    but_cou = 7
    for _ in range(wd):
        temp_set.append(types.InlineKeyboardButton(' ', callback_data='x'))
        but_cou += 1
    dinm = datetime.monthrange(ctime.year, ctime.month)[1]
    for day_num in range(1, dinm + 1):
        call = datetime.datetime.now().replace(day=day_num,
                                               hour=0,
                                               minute=0,
                                               second=0,
                                               microsecond=0)

        call_day = str(call.day)
        call_month = str(call.month)
        call_year = str(call.year)
        temp_set.append(types.InlineKeyboardButton(str(day_num),
                                                   callback_data=f'{call_day.rjust(2, '0')}.'
                                                                 f'{call_month.rjust(2, '0')}.'
                                                                 f'{call_year}'))
        but_cou += 1
    print(but_cou)
    temparr = list(temp_set)
    nec_emp_b = (but_cou - 20) % 7
    try:
        dop_butt = list(temparr[-(7 - nec_emp_b):])
        temparr = temparr[:-(6 - nec_emp_b) + 1]
    finally:
        pass

    cal.add(*temparr)
    temparr2 = list()
    curr_time_chosen = cal.to_dict()['inline_keyboard'][1][6]['callback_data']
    curr_month_chosen = str(int(curr_time_chosen[3:5]))
    curr_year_chosen = str(int(curr_time_chosen[6:]))
    print(but_cou)
    but_cou += 2
    while but_cou < 42:
        dop_butt.append(types.InlineKeyboardButton(' ', callback_data='x'))
        but_cou += 1
    cal.add(*dop_butt)
    cal.add(types.InlineKeyboardButton('<--', callback_data=f'prev_{curr_month_chosen}'),
            types.InlineKeyboardButton(f'{month_desc[curr_month_chosen]} {curr_year_chosen}', callback_data='x'),
            types.InlineKeyboardButton('-->', callback_data=f'next_{curr_month_chosen}'))

    bot.send_message(message.chat.id, text='Календарико', reply_markup=cal)
def cland():
    @bot.message_handler(commands=['start'])
    def a(message):
        make_cal(message, month='curr')

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if 'prev' in call.data:
            pass
            bot.send_message(call.message.chat.id, text=f'{call.data}')
        elif 'next' in call.data: pass


    bot.infinity_polling()


cland()
