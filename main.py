import telebot
from telebot import types
import config
import pytz
import datetime

"""import datetime
import pytz
import telebot
from telebot import types
import calendar

bot = telebot.TeleBot('7080192611:AAFA3GziINC_BRz8u0nEmxmP_NfVNMFHbwg')
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

cal.add(types.InlineKeyboardButton('П'),
        types.InlineKeyboardButton('В'),
        types.InlineKeyboardButton('С'),
        types.InlineKeyboardButton('Ч'),
        types.InlineKeyboardButton('П'),
        types.InlineKeyboardButton('С'),
        types.InlineKeyboardButton('В'))
but_cou = 7
for _ in range(wd):
    cal.add(types.InlineKeyboardButton(' '))
    but_cou += 1
dinm = calendar.monthrange(ctime.year, ctime.month)[1]
for day_num in range(1, dinm):
    call = datetime.datetime.now().replace(day=day_num,
                                           hour=0,
                                           minute=0,
                                           second=0,
                                           microsecond=0)

    call_day = str(call.day)
    call_month = str(call.month)
    call_year = str(call.year)
    cal.add(types.InlineKeyboardButton(str(day_num + 1),
                                       callback_data=f'{02:call_day}.{call_month:02}.{call_year}'))
    but_cou += 1
print(cal)
while but_cou < 49:
    cal.add(types.InlineKeyboardButton(' '))
    but_cou += 1
cal.add(types.InlineKeyboardButton('<--', callback_data=f'prev_{1}'))

print(cal.to_dict()['inline_keyboard'][13]['callback_data'])"""


def calendar():
    current_day = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    print(current_day)
def enter_city(message):
    try:
        config.cities[message.text.capitalize()]
    except:
        BOT.send_message(message.chat.id, text='Город не найден')

def main():
    @BOT.message_handler(commands=['start'])
    def message_handler(message):
        mdict.update({message.chat.id: BOT.send_message(message.chat.id, text='Привет! Нажми на одну из кнопок ниже',
                                                        reply_markup=start_mk)})

    @BOT.callback_query_handler(func=lambda call: True)
    def callback_query_handler(call):
        if call.data == 'start':
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id, text='Выберите город вылета',
                                                                 reply_markup=city_dep)})
        if 'dep' in call.data:
            if 'nocity' in call.data:
                BOT.delete_message(call.message.chat.id, mdict[call.message.chat.id])
                BOT.send_message(call.message.chat.id, text='Без перелета')
            elif 'other' in call.data:
                BOT.delete_message(call.message.chat.id, mdict[call.message.chat.id])
                BOT.send_message(call.message.chat.id, text='Введите желаемый город вылета')
                BOT.register_next_step_handler(call.message, enter_city)

    BOT.infinity_polling()


if __name__ == '__main__':
    mdict = dict()
    BOT = telebot.TeleBot(token=config.token)
    start_mk = types.InlineKeyboardMarkup(row_width=1)
    start_mk.add(types.InlineKeyboardButton('Найти тур!', callback_data='start'))
    city_dep = types.InlineKeyboardMarkup(row_width=2)
    city_dep.add(types.InlineKeyboardButton('Москва', callback_data='dep_Msc'))
    city_dep.add(types.InlineKeyboardButton('Екатеринбург', callback_data='dep_Ekb'),
                 types.InlineKeyboardButton('Новосибирск', callback_data='dep_Nsb'),
                 types.InlineKeyboardButton('Санкт-Петербург', callback_data='dep_Spb'))
    city_dep.add(types.InlineKeyboardButton('Другой город', callback_data='dep_other'),
                 types.InlineKeyboardButton('Без перелета', callback_data='dep_nocity'))
    main()
