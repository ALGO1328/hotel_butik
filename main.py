import telebot
from telebot import types
import datetime
from datetime import date

import cl
import config


def main():
    def datecheck(c_date):
        now = datetime.datetime.now()
        print(c_date)
        print(now)

    def checker(message):
        try:
            new_message = ('✈️ Из города ' + config.cities_swap[stags[message.chat.id]['s_flyfrom']] + 'В страну ' +
                           config.countries_swap[stags[message.chat.id]['s_country']])
        except:
            new_message = '✈️ Без перелета \n'
        new_message += '👤 Взрослых: ' + stags[message.chat.id]['s_adults'] + ' \n'
        new_message += '👶 Детей: ' + stags[message.chat.id]['s_children'] + ' \n'
        new_message += '🏠 Отель: ' + stags[message.chat.id]['s_stars'] + '* и лучше' + ' \n'
        new_message += '🍔 Питание: ' + config.meals[stags[message.chat.id]['s_meal']] + ' \n'
        new_message += '🌙' + stags[message.chat.id]['s_nights_from'] + str(
            int(stags[message.chat.id]['s_nights_from']) + 2) + ' \n'
        new_message += '📆 Даты вылета с ' + stags[message.chat.id]['s_j_date_from'] + ' \n'
        return new_message

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
                mdict.update({message.chat.id: BOT.send_message(message.chat.id, text='Город не найден. \n'
                                                                                      'Нажмите "отмена" для отмены',
                                                                reply_markup=manual_city_markup)})
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

    def link_creator(message):
        link = 'https://tourvisor.ru/search.php?ts_dosearch=1'
        for k, v in stags[message.chat.id].items():
            link += f'&{k}={v}'
        return link

    def phone_checker(message):
        BOT.delete_message(message.chat.id, mdict[message.chat.id].id)
        if message.text.startswith('+7') and len(message.text) == 12:
            link = link_creator(message)
            text = f'[Ссылка]({link})'
            BOT.send_message(message.chat.id, text=f'Результаты поиска: {text}', parse_mode='MarkdownV2')

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
                {message.chat.id: BOT.send_message(message.chat.id, text=f'Привет, {message.from_user.first_name}!'
                                                                         f' Нажми на одну из кнопок ниже',
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
        if 'nights' in call.data:
            if '12' in call.data:
                stags[call.message.chat.id].update({'s_nights_from': call.data[-2:]})
                nights_to = str(int(call.data[-2:]) + 2)
                stags[call.message.chat.id].update({'s_nights_to': nights_to})
                mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                     text=f'Кол-во ночей: {call.data[-2:]} - {nights_to}')})
            else:
                stags[call.message.chat.id].update({'s_nights_from': call.data[-1:]})
                nights_to = str(int(call.data[-1:]) + 2)
                stags[call.message.chat.id].update({'s_nights_to': nights_to})
                mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                     text=f'Кол-во ночей: {call.data[-1]} - {nights_to}')})
            year_now = date.today().year
            month_now = date.today().month
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                 text='Выберите примерную дату вылета',
                                                                 reply_markup=cl.create_cal(year_now, month_now))})
        if 'date' in call.data:
            if 'change' in call.data:
                mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                     text='Выберите примерную дату вылета',
                                                                     reply_markup=cl.create_cal(call.data[12:16],
                                                                                                call.data[-2:]))})
            else:
                if datecheck(call.data.remove('date_')):
                    stags[call.message.chat.id].update({'s_j_date_from': call.data[-2:]})
                    mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                         text=f'Примерная дата вылета: {call.data[5:]}')})
                    mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                         text='Давайте проверим, верно ли мы все записали')})
                    mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                         text=checker(call.message))})
                else:
                    mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                         text='Выберите корректную дату')})

        if 'confirm' in call.data:
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                 text='Введите свой номер телефона в формате +79000000000.'
                                                                      'и мы прямо сейчас отправим Вам результаты поиска. \n'
                                                                      'Также наш специалист подготовит для Вас индивидуальное предложение '
                                                                      'по заданным параметрам и свяжется с Вами по указанному номеру телефона. \n'
                                                                      'Указывая номер телефона, Вы подтверждаете согласие на обработку своих персональных данных.')})
            BOT.register_next_step_handler(call.message, phone_checker)

        if 'meal' in call.data:
            stags[call.message.chat.id].update({'s_meal': call.data[-1:]})
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                 text=f'Питание: {config.meals[call.data[-1:]]}')})
            mdict.update({call.message.chat.id: BOT.send_message(call.message.chat.id,
                                                                 text='Выберите количество ночей',
                                                                 reply_markup=nights_markup)})
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
                       types.InlineKeyboardButton('👤👤👤👤👤👤', callback_data='tourist_6'))
    children_amount = types.InlineKeyboardMarkup(row_width=3)
    children_amount.add(types.InlineKeyboardButton('БЕЗ ДЕТЕЙ', callback_data='children_0'))
    children_amount.add(types.InlineKeyboardButton('🧒', callback_data='children_1'),
                        types.InlineKeyboardButton('🧒🧒', callback_data='children_2'),
                        types.InlineKeyboardButton('🧒🧒🧒', callback_data='children_3'))
    hotel_category = types.InlineKeyboardMarkup(row_width=3)
    hotel_category.add(types.InlineKeyboardButton('⭐', callback_data='hotel_1'),
                       types.InlineKeyboardButton('⭐⭐', callback_data='hotel_2'),
                       types.InlineKeyboardButton('⭐⭐⭐', callback_data='hotel_3'),
                       types.InlineKeyboardButton('⭐⭐⭐⭐', callback_data='hotel_4'),
                       types.InlineKeyboardButton('⭐⭐⭐⭐⭐', callback_data='hotel_5'))
    meal_markup = types.InlineKeyboardMarkup(row_width=2)
    meal_markup.add(types.InlineKeyboardButton('ЛЮБОЕ', callback_data='meal_0'),
                    types.InlineKeyboardButton('ЗАВТРАК', callback_data='meal_3'),
                    types.InlineKeyboardButton('ЗАВТРАК', callback_data='meal_4'),
                    types.InlineKeyboardButton('ПОЛНЫЙ ПАНСИОН', callback_data='meal_5'),
                    types.InlineKeyboardButton('ВСЕ ВКЛЮЧЕНО', callback_data='meal_7'),
                    types.InlineKeyboardButton('УЛЬТРА ВСЕ ВКЛЮЧЕНО', callback_data='meal_9'))
    nights_markup = types.InlineKeyboardMarkup(row_width=3)
    nights_markup.add(types.InlineKeyboardButton('6 - 8', callback_data='nights_6'),
                      types.InlineKeyboardButton('9 - 11', callback_data='nights_9'),
                      types.InlineKeyboardButton('12 - 14', callback_data='nights_12'))
    confirmation_markup = types.InlineKeyboardMarkup(row_width=1)
    confirmation_markup.add(types.InlineKeyboardButton('ВСЕ ВЕРНО, ПОДТВЕРДИТЬ', callback_data='confirm_confirm'),
                            types.InlineKeyboardButton('ИЗМЕНИТЬ', callback_data='start'))
    manual_city_markup = types.InlineKeyboardMarkup(row_width=1)
    manual_city_markup.add(types.InlineKeyboardButton('ОТМЕНА', callback_data='start'))
    main()
