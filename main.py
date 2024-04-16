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
        if 'meal' in call.data:
            stags[call.message.chat.id].update({'s_meal': call.data[-1:]})
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                 text=f'Питание: {config.meals[call.data]}')})
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                 text='Выберите питание',
                                                                 reply_markup=meal_markup)})
        if 'hotel' in call.data:
            stags[call.message.chat.id].update({'s_stars': call.data[-1:]})
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                 text=f'Категория отеля: {call.data[-1:]}')})
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                 text='Выберите питание',
                                                                 reply_markup=meal_markup)})
        if 'arr' in call.data:
            stags[call.message.chat.id].update({'s_country': call.data.replace('arr_', '')})
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                 text=f'Страна вылета: '
                                                                      f'{config.countries_swap[call.data.replace("arr_", "")]}')})
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                 text='Введите количество взрослых туристов',
                                                                 reply_markup=tourist_amount)})
        if 'children' in call.data:
            stags[call.message.chat.id].update({'s_children': call.data[-1:]})
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id, text=f'Кол-во детей: '
                                                                                            f'{call.data[-1:]}')})
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                 text='Выберите минимальную категорию отеля',
                                                                 reply_markup=hotel_category)})
        if 'tourist' in call.data:
            stags[call.message.chat.id].update({'s_adults': call.data[-1:]})
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id, text=f'Кол-во туристов: '
                                                                                            f'{call.data[-1:]}')})
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id, text='Выберите кол-во детей, '
                                                                                            'едущих с вами в '
                                                                                            'путешествие',
                                                                 reply_markup=children_amount)})
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
    children_amount = types.InlineKeyboardMarkup(row_width=3)
    children_amount.add(types.InlineKeyboardButton('БЕЗ ДЕТЕЙ', callback_data='children_0'))
    children_amount.add(types.InlineKeyboardButton('🧒', callback_data='children_1'),
                        types.InlineKeyboardButton('🧒🧒', callback_data='children_2'),
                        types.InlineKeyboardButton('🧒🧒🧒', callback_data='children_3'))
    children_amount.add(types.InlineKeyboardButton('НАЗАД', callback_data='backto_adults'))
    hotel_category = types.InlineKeyboardMarkup(row_width=3)
    hotel_category.add(types.InlineKeyboardButton('⭐', callback_data='hotel_1'),
                       types.InlineKeyboardButton('⭐⭐', callback_data='hotel_2'),
                       types.InlineKeyboardButton('⭐⭐⭐', callback_data='hotel_3'),
                       types.InlineKeyboardButton('⭐⭐⭐⭐', callback_data='hotel_4'),
                       types.InlineKeyboardButton('⭐⭐⭐⭐⭐', callback_data='hotel_5'))
    hotel_category.add(types.InlineKeyboardButton('НАЗАД', callback_data='backto_children'))
    meal_markup = types.InlineKeyboardMarkup(row_width=2)
    meal_markup.add(types.InlineKeyboardButton('Любое', callback_data='meal_0'),
                    types.InlineKeyboardButton('Завтрак', callback_data='meal_3'),
                    types.InlineKeyboardButton('Завтрак и ужин', callback_data='meal_4'),
                    types.InlineKeyboardButton('Полный пансион', callback_data='meal_5'),
                    types.InlineKeyboardButton('Все включено', callback_data='meal_7'),
                    types.InlineKeyboardButton('Ультра все включено', callback_data='meal_9'),
                    types.InlineKeyboardButton('НАЗАД', callback_data='backto_hotel'))
    nights_markup = types.InlineKeyboardMarkup(row_width=3)
    nights_markup.add(types.InlineKeyboardButton('6 - 8', callback_data='nights_6'),
                      types.InlineKeyboardButton('9 - 11', callback_data='nights_9'),
                      types.InlineKeyboardButton('12 - 14', callback_data='nights_12'),
                      types.InlineKeyboardButton('НАЗАД', callback_data='backto_meal'))


    main()
