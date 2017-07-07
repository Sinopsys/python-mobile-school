import telebot
from telebot import types
from database import top_5
from database import bank_search
from gapi import nearest_10


def start():


    bot = telebot.TeleBot('374322077:AAE3Ef7mjY0dkpQ0utCClXRFT0D79w9mJDs')
    markup = types.ReplyKeyboardMarkup(True, False)
    usd_b = types.KeyboardButton(text='Продажа доллара')
    usd_s = types.KeyboardButton(text='Покупка доллара')
    eu_b = types.KeyboardButton(text='Продажа евро')
    eu_s = types.KeyboardButton(text='Покупка евро')
    locbtn = types.KeyboardButton(text='Ближайшие к Вам банки', request_location=True)
    markup.row(usd_s, usd_b)
    markup.row(eu_s, eu_b)
    markup.row(locbtn)
    def handle_messages(messages):
        msg = 'ТОП-5 самых выгодных предложений: '
        for message in messages:
            if message.text == 'Продажа доллара':  # 1
                t = top_5('usd sell')
                s = msg + '\n'
                number = 0
                for i in t:
                    number += 1
                    s = s + str(number) + '. ' + i[0].rstrip() + ': $1 = ' + str(i[1]) + '₽   ' + str(i[5]) + '\n'
                mark = types.ReplyKeyboardMarkup(True, False, row_width=5)
                backbtn = types.KeyboardButton(text='Вернуться назад')
                mark.row(backbtn)
                bot.send_message(message.chat.id, s, reply_markup=mark)

            elif message.text == 'Покупка доллара':  # 2
                t = top_5('usd buy')
                s = msg + '\n'
                number = 0
                for i in t:
                    number += 1
                    s = s + str(number) + '. ' + i[0].rstrip() + ': $1 = ' + str(i[2]) + '₽   ' + str(i[5]) + '\n'
                mark = types.ReplyKeyboardMarkup(True, False, row_width=5)
                backbtn = types.KeyboardButton(text='Вернуться назад')
                mark.row(backbtn)
                bot.send_message(message.chat.id, s, reply_markup=mark)
            elif message.text == 'Продажа евро':  # 3
                t = top_5('eu sell')
                s = msg + '\n'
                number = 0
                for i in t:
                    number += 1
                    s = s + str(number) + '. ' + i[0].rstrip() + ': €1 = ' + str(i[3]) + '₽   ' + str(i[5]) + '\n'
                mark = types.ReplyKeyboardMarkup(True, False, row_width=5)
                backbtn = types.KeyboardButton(text='Вернуться назад')
                mark.row(backbtn)
                bot.send_message(message.chat.id, s, reply_markup=mark)
            elif message.text == 'Покупка евро':  # 4
                t = top_5('eu buy')
                s = msg + '\n'
                number = 0
                for i in t:
                    number += 1
                    s = s + str(number) + '. ' + i[0].rstrip() + ': €1 = ' + str(i[4]) + '₽   ' + str(i[5]) + '\n'
                mark = types.ReplyKeyboardMarkup(True, False, row_width=5)
                backbtn = types.KeyboardButton(text='Вернуться назад')
                mark.row(backbtn)
                bot.send_message(message.chat.id, s, reply_markup=mark)

            elif not message.location:
                bot.send_message(message.chat.id,
                                 'Желаете узнать актуальный курс обмена валют? \nВыберите подходящий вариант на клавиатуре.',
                                 reply_markup=markup)
            else:
                locmsg = message
                if locmsg.location:
                    msg = ''
                    banks = nearest_10(str(locmsg.location.latitude), str(locmsg.location.longitude))
                    banks = banks[:5]
                    for i in banks:
                        msg = msg + "<a href='" + i[3] + "'>" + i[0] + "</a>" + '\n'
                    bot.send_message(locmsg.chat.id,
                                msg, reply_markup=markup, parse_mode='HTML')

    bot.set_update_listener(handle_messages)
    bot.polling()