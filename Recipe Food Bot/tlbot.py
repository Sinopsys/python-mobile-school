# coding: utf8
import telebot
import tltoken
from telebot import types
import foodapiHandler as fH
from telebot import util
import yandex_translator_api_handler as yatra
import langmodule
from fastnumbers import fast_real

# Инициализация бота
tlbot_one = telebot.TeleBot(tltoken.token)

# Обработчик стартовой команды
@tlbot_one.message_handler(commands=['start'])
def command_handler(message):
    check = tltoken.check_started_chat(str(message.chat.id))
    if check == False:
        tltoken.set_started_chat(str(message.chat.id))

        tlbot_one.send_message(message.chat.id, langmodule.return_local(tltoken.check_lang(message.chat.id), 1))
        markup = types.ReplyKeyboardMarkup(True, False)
        markup.row('/find_recipe_by_ingridients')
        markup.row('/settings')
        markup.row('/about')
         
        tlbot_one.send_message(message.chat.id,
                               langmodule.return_local(tltoken.check_lang(message.chat.id), 2),
                               reply_markup=markup)
    else:
        check = tltoken.check_started_chat(str(message.chat.id))
        if check == 1:
            markup = types.ReplyKeyboardMarkup(True, False)
            markup.row('/find_recipe_by_ingridients')
            markup.row('/settings')
            markup.row('/about')
             
            tlbot_one.send_message(message.chat.id, langmodule.return_local(tltoken.check_lang(message.chat.id), 3))
            tlbot_one.send_message(message.chat.id, langmodule.return_local(tltoken.check_lang(message.chat.id), 2), reply_markup=markup)
        
# Обработчик поиска рецептов по ингредиентам
@tlbot_one.message_handler(commands=['find_recipe_by_ingridients'])
def command_find_handler(message):
    check = tltoken.check_started_chat(str(message.chat.id))
    if check == False:
        markup = types.ReplyKeyboardMarkup(True, False)
        markup.row('/start')
        tlbot_one.send_message(message.chat.id,
                               langmodule.return_local(tltoken.check_lang(message.chat.id), 4),
                               reply_markup=markup)
    else:
        markup = types.ReplyKeyboardRemove()
        tltoken.work_with_command(str(message.chat.id), 2)
        tlbot_one.send_message(message.chat.id,
                               langmodule.return_local(tltoken.check_lang(message.chat.id), 5), reply_markup=markup)

# Обработчик настроек
@tlbot_one.message_handler(commands=['settings'])
def command_find_handler(message):
    check = tltoken.check_started_chat(str(message.chat.id))
    if check == False:
        markup = types.ReplyKeyboardMarkup(True, False)
        markup.row('/start')
        tlbot_one.send_message(message.chat.id,
                               langmodule.return_local(tltoken.check_lang(message.chat.id), 4),
                               reply_markup=markup)
    else:
        if check == 1:
            markup = types.ReplyKeyboardMarkup(True, False)
            markup.row('/change_language')
            markup.row('/change_max_count')
            markup.row('/back')
            tltoken.work_with_command(str(message.chat.id), 4)
            tlbot_one.send_message(message.chat.id,
                               langmodule.return_local(tltoken.check_lang(message.chat.id), 10), reply_markup=markup)

# Возвращение назад
@tlbot_one.message_handler(commands=['back'])
def command_find_handler(message):
    check = tltoken.check_started_chat(str(message.chat.id))
    if check == False:
        markup = types.ReplyKeyboardMarkup(True, False)
        markup.row('/start')
        tlbot_one.send_message(message.chat.id,
                               langmodule.return_local(tltoken.check_lang(message.chat.id), 4),
                               reply_markup=markup)
    else:
        if check == 4:
            markup = types.ReplyKeyboardMarkup(True, False)
            markup.row('/find_recipe_by_ingridients')
            markup.row('/settings')
            markup.row('/about')
            tltoken.work_with_command(str(message.chat.id), 1)
            tlbot_one.send_message(message.chat.id, langmodule.return_local(tltoken.check_lang(message.chat.id), 2), reply_markup=markup)

# Обработчик about-запроса
@tlbot_one.message_handler(commands=['about'])
def command_find_handler(message):
    check = tltoken.check_started_chat(str(message.chat.id))
    if check == False:
        markup = types.ReplyKeyboardMarkup(True, False)
        markup.row('/start')
        tlbot_one.send_message(message.chat.id,
                               langmodule.return_local(tltoken.check_lang(message.chat.id), 4),
                               reply_markup=markup)
    else:
        if check == 1:
            tlbot_one.send_message(message.chat.id,
                               langmodule.return_local(tltoken.check_lang(message.chat.id), 16))



       

# Обработчик изменения языка
@tlbot_one.message_handler(commands=['change_language'])
def command_find_handler(message):
    check = tltoken.check_started_chat(str(message.chat.id))
    if check == False:
        markup = types.ReplyKeyboardMarkup(True, False)
        markup.row('/start')
        tlbot_one.send_message(message.chat.id,
                               langmodule.return_local(tltoken.check_lang(message.chat.id), 4),
                               reply_markup=markup)
    else:
         if check == 4:
             markup = types.ReplyKeyboardMarkup(True, False)
             markup.row('/rus')
             markup.row('/eng')
             tltoken.work_with_command(str(message.chat.id), 6)
             tlbot_one.send_message(message.chat.id,
                               langmodule.return_local(tltoken.check_lang(message.chat.id), 11), reply_markup=markup)

# Обработчик изменения максимального количества элементов
@tlbot_one.message_handler(commands=['change_max_count'])
def command_find_handler(message):
    check = tltoken.check_started_chat(str(message.chat.id))
    if check == False:
        markup = types.ReplyKeyboardMarkup(True, False)
        markup.row('/start')
        tlbot_one.send_message(message.chat.id,
                               langmodule.return_local(tltoken.check_lang(message.chat.id), 4),
                               reply_markup=markup)
    else:
        markup = types.ReplyKeyboardRemove()
        tltoken.work_with_command(str(message.chat.id), 5)
        tlbot_one.send_message(message.chat.id,
                               langmodule.return_local(tltoken.check_lang(message.chat.id), 15), reply_markup=markup)

# Обработчик изменения языка
@tlbot_one.message_handler(commands=['rus', 'eng'])
def command_find_handler(message):
    check = tltoken.check_started_chat(str(message.chat.id))
    if check == False:
        markup = types.ReplyKeyboardMarkup(True, False)
        markup.row('/start')
        tlbot_one.send_message(message.chat.id,
                               langmodule.return_local(tltoken.check_lang(message.chat.id), 4),
                               reply_markup=markup)
    else:
        if check == 6:
             if message.text == "/rus":
                 tltoken.set_lang_chat(message.chat.id, 'rus')
                 tltoken.work_with_command(str(message.chat.id), 1)
                 markup = types.ReplyKeyboardMarkup(True, False)
                 markup.row('/find_recipe_by_ingridients')
                 markup.row('/settings')
                 markup.row('/about')
                  
                 tlbot_one.send_message(message.chat.id,
                                           'Язык успешно сменён на русский')   
                 tlbot_one.send_message(message.chat.id,
                                           langmodule.return_local(tltoken.check_lang(message.chat.id), 2),
                                           reply_markup=markup)   
             else:
                 if message.text == "/eng":
                     tltoken.set_lang_chat(message.chat.id, 'eng')
                     tltoken.work_with_command(str(message.chat.id), 1)
                     markup = types.ReplyKeyboardMarkup(True, False)
                     markup.row('/find_recipe_by_ingridients')
                     markup.row('/settings')
                     markup.row('/about')
                      
                     tlbot_one.send_message(message.chat.id,
                                           'Language successfully was changed to English') 
                     tlbot_one.send_message(message.chat.id,
                                           langmodule.return_local(tltoken.check_lang(message.chat.id), 2),
                                           reply_markup=markup)     


# Обработчик любых текстовых сообщений (кроме команд)
@tlbot_one.message_handler(func=lambda message: True, content_types=['text'])
def echo_msg(message):
    check = tltoken.check_started_chat(str(message.chat.id))
    if check == False:
        markup = types.ReplyKeyboardMarkup(True, False)
        markup.row('/start')
        tlbot_one.send_message(message.chat.id,
                               langmodule.return_local(tltoken.check_lang(message.chat.id), 4),
                               reply_markup=markup)
    else:
        if check == 2:
            mess = message.text
            la = tltoken.check_lang(message.chat.id)
            if(la == 'rus'):
                pr1 = yatra.translate_to_english(mess)
                if pr1 != 'null':
                    mess = pr1
            print(mess)
            vr = str(mess).split()                 
            if len(vr) >= 2:
                tlbot_one.send_message(message.chat.id, langmodule.return_local(tltoken.check_lang(message.chat.id), 8))
               # tlbot_one.se
                tltoken.work_with_command(str(message.chat.id), 3)
                f = fH.find_food(vr, tltoken.check_count(message.chat.id))               
                print(f)
                if f != 'null':
                    for i in f:     
                        try:
                            m = str(str(i[1]) + "\n" + str(i[3]) + "\n" + str(i[4]) + " min")
                        except:
                            m = 'null'
                        if m != 'null':
                            la = tltoken.check_lang(message.chat.id)
                            l = m
                            if(la == 'rus'):
                                pr = yatra.translate_to_russian(m)
                                if pr != 'null':
                                    l = pr
                            l = l + "\n" + str(i[2])
                            splitted_text = util.split_string(l, 3000)
                            for text in splitted_text:
                                tlbot_one.send_message(message.chat.id, text) 
                        else:
                            tlbot_one.send_message(message.chat.id, langmodule.return_local(tltoken.check_lang(message.chat.id), 18))
                                               
                    tltoken.work_with_command(str(message.chat.id), 1)
                    markup = types.ReplyKeyboardMarkup(True, False)
                    markup.row('/find_recipe_by_ingridients')
                    markup.row('/settings')
                    markup.row('/about')
                     
                    tlbot_one.send_message(message.chat.id,
                                           langmodule.return_local(tltoken.check_lang(message.chat.id), 2),
                                           reply_markup=markup)       
                   
                else:
                    markup = types.ReplyKeyboardRemove()
                    tltoken.work_with_command(str(message.chat.id), 2)
                    tlbot_one.send_message(message.chat.id,
                                           langmodule.return_local(tltoken.check_lang(message.chat.id), 7),
                                           reply_markup=markup)                   

            else:
                markup = types.ReplyKeyboardRemove()
                tltoken.work_with_command(str(message.chat.id), 2)
                tlbot_one.send_message(message.chat.id, langmodule.return_local(tltoken.check_lang(message.chat.id), 9), reply_markup=markup)
        else:
            if check == 1:
                markup = types.ReplyKeyboardMarkup(True, False)
                markup.row('/find_recipe_by_ingridients')
                markup.row('/settings')
                markup.row('/about')
                 
                tlbot_one.send_message(message.chat.id,
                                       langmodule.return_local(tltoken.check_lang(message.chat.id), 2),
                                       reply_markup=markup)
            else:
                if check == 3:
                    tlbot_one.send_message(message.chat.id, langmodule.return_local(tltoken.check_lang(message.chat.id), 6))
                else:
                    if check == 5:
                        mess1 = message.text
                        inmess = fast_real(mess1)
                        if (type(inmess) == int):
                            if inmess > 0:
                                tltoken.set_count(message.chat.id, inmess)
                                tlbot_one.send_message(message.chat.id, langmodule.return_local(tltoken.check_lang(message.chat.id), 12) + str(inmess))
                                markup = types.ReplyKeyboardMarkup(True, False)
                                markup.row('/find_recipe_by_ingridients')
                                markup.row('/settings')
                                markup.row('/about')                                 
                                tltoken.work_with_command(str(message.chat.id), 1)
                                tlbot_one.send_message(message.chat.id, langmodule.return_local(tltoken.check_lang(message.chat.id), 2), reply_markup=markup)

                            else:
                                tlbot_one.send_message(message.chat.id, langmodule.return_local(tltoken.check_lang(message.chat.id), 13))
                        else:
                             tlbot_one.send_message(message.chat.id, langmodule.return_local(tltoken.check_lang(message.chat.id), 14))



if __name__ == '__main__':
    tlbot_one.polling(none_stop=True)
    
    







