import telebot
from telebot import types
import config
import pytz
import datetime


def main():
    def enter_city(message):
        BOT.delete_message(message.chat.id, message.message_id)
        if message.text.lower() == 'отмена':
            message_handler(message)
        else:
            try:
                BOT.delete_message(message.chat.id, mdict[message.chat.id].id)
            except:
                pass
            try:
                stags[message.chat.id].update({'s_flyfrom': config.cities[message.text.capitalize()]})
                mdict.update({message.chat.id: BOT.send_message(message.chat.id,
                                                                text=f'Город вылета: {message.text.capitalize()}')})
                enter_country(message)
            except KeyError:
                mdict.update({message.chat.id: BOT.send_message(message.chat.id, text='Город не найден. '
                                                                                      'Попробуйте еще раз или напишите "отмена" для отмены')})
                BOT.register_next_step_handler(message, enter_city)

    def get_country(message):
        if message.text.lower() == 'отмена':
            message_handler(message)
        try:
            stags[message.chat.id].update({'s_country': config.countries[message.text.capitalize()]})
            mdict.update(
                {message.chat.id: BOT.send_message(message.chat.id, text='Введите количество взрослых туристов',
                                                   reply_markup=tourist_amount)})
        except KeyError:
            mdict.update({message.chat.id: BOT.send_message(message.chat.id, text='Страна не найдена. '
                                                                                  'Попробуйте еще раз или напишите '
                                                                                  '"отмена" для отмены')})

    def enter_country(message):
        mdict.update({message.chat.id: BOT.send_message(message.chat.id,
                                                        text='Выберите страну, в которой хотите отдохнуть',
                                                        reply_markup=country_arr)})
        BOT.register_next_step_handler(message, get_country)

    @BOT.message_handler(commands=['start'])
    def message_handler(message):
        try:
            BOT.delete_message(message.chat.id, mdict[message.chat.id].id)
        except KeyError:
            pass
        finally:
            stags.update({message.chat.id: dict()})
            BOT.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            mdict.update(
                {message.chat.id: BOT.send_message(message.chat.id, text='Привет! Нажми на одну из кнопок ниже',
                                                   reply_markup=start_mk)})

    @BOT.callback_query_handler(func=lambda call: True)
    def callback_query_handler(call):
        try:
            BOT.delete_message(call.message.chat.id, message_id=mdict[call.message.chat.id].id)
        finally:
            pass
        if call.data == 'start':
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id, text='Выберите город вылета',
                                                                 reply_markup=city_dep)})
        if 'arr' in call.data:
            stags[call.message.chat.id].update({'s_country': config.countries[call.data.replace('arr_', '')]})
            BOT.delete_message(call.message.chat.id, mdict[call.message.chat.id].id)
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                 text='Введите количество взрослых туристов',
                                                                 reply_markup=tourist_amount)})
        if 'tourist' in call.data:
            stags[call.message.chat.id].update({'s_adults': call.data.replace('tourists_', '')})
        if 'dep' in call.data:
            if 'nocity' in call.data:
                mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id, text='Без перелета')})
                enter_country(call.message)
            elif 'other' in call.data:
                mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                     text='Введите желаемый город вылета')})
                BOT.register_next_step_handler(call.message, enter_city)
            else:
                mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                     text=f'Город вылета: '
                                                                          f'{config.cities_swap[call.data.replace('dep_', '')]}')})
                stags[call.message.chat.id].update({'s_flyfrom': call.data.replace('dep_', '')})
                enter_country(call.message)

    BOT.infinity_polling()


if __name__ == '__main__':
    mdict = dict()
    BOT = telebot.TeleBot(token=config.token)
    stags = dict()
    start_mk = types.InlineKeyboardMarkup(row_width=1)
    start_mk.add(types.InlineKeyboardButton('Найти тур!', callback_data='start'))
    city_dep = types.InlineKeyboardMarkup(row_width=2)
    city_dep.add(types.InlineKeyboardButton('Москва', callback_data='dep_1'))
    city_dep.add(types.InlineKeyboardButton('Екатеринбург', callback_data='dep_3'),
                 types.InlineKeyboardButton('Новосибирск', callback_data='dep_9'),
                 types.InlineKeyboardButton('Санкт-Петербург', callback_data='dep_5'))
    city_dep.add(types.InlineKeyboardButton('Другой город', callback_data='dep_other'),
                 types.InlineKeyboardButton('Без перелета', callback_data='dep_nocity'))
    country_arr = types.InlineKeyboardMarkup(row_width=2)
    country_arr_list = []
    for i in config.dflt_countries:
        country_arr_list.append(types.InlineKeyboardButton(i[0], callback_data=f'arr_{i[1]}'))
    country_arr.add(*country_arr_list)
    tourist_amount = types.InlineKeyboardMarkup(row_width=2)
    tourist_amount.add(types.InlineKeyboardButton('👤', callback_data='tourist_1'),
                       types.InlineKeyboardButton('👤👤', callback_data='tourist_2'),
                       types.InlineKeyboardButton('👤👤👤', callback_data='tourist_3'),
                       types.InlineKeyboardButton('👤👤👤👤', callback_data='tourist_4'),
                       types.InlineKeyboardButton('👤👤👤👤👤', callback_data='tourist_5'),
                       types.InlineKeyboardButton('👤👤👤👤👤👤', callback_data='tourist_6'),
                       types.InlineKeyboardButton('НАЗАД', callback_data='backto_country'))

    main()
