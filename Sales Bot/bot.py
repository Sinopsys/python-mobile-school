import telebot
import crawler 
from time import sleep


link = ''

bot = telebot.TeleBot('442709449:AAEZLaE3Ja3K_HToUfDEB67z4hab-NEGII8')
shop_name = ''


def show_keyboard(type):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    if type is 'shops':
        keyboard.row('/stop')
        keyboard.row('Ашан', 'Дикси')
        return keyboard, 'Выберите магазин из списка:'
    elif type is 'options':
        keyboard.row('/stop')
        keyboard.row('Количество акций')
        keyboard.row('Список наименований')
        keyboard.row('Отслеживать изменения')
        return keyboard, 'Выберите опцию:'
    elif type is 'categoryDixy':
        keyboard.row('/stop')
        # keyboard.row('Все')
        keyboard.row('Овощи и фрукты', 'Консервы, соусы')
        keyboard.row('Кофе, чай', 'Детское питание')
        keyboard.row('Хлеб, торты', 'Молочная гастрономия')
        keyboard.row('Мясная гастрономия','Мясо, яйцо')
        keyboard.row('Кондитерские изделия')
        keyboard.row('Кулинария, заморозка, мороженое')
        keyboard.row('Напитки', 'Крупы, завтраки, специи')
        keyboard.row('Непродовольственные товары') 
        return keyboard, 'Выберите категорию:'
    elif type is 'categoryAuchan':
        keyboard.row('/stop')
        # keyboard.row('Все')
        keyboard.row('Игрушки', 'Мебель')
        keyboard.row('Дача', 'Электроника')
        keyboard.row('Детям', 'Спорт')
        keyboard.row('Горящие цены')
        keyboard.row('Зоотовары','Кухня')
        keyboard.row('Детская одежда', 'Все остальное', 'DVD')
        return keyboard, 'Выберите категорию:'
    elif type is 'start_button':
        keyboard.row('/start')
        return keyboard
    elif type is 'stop_button':
        keyboard.row('/stop')
        return keyboard


def hide_keyboard():
    keyboard = telebot.types.ReplyKeyboardRemove()
    return keyboard, 'До встречи!'
    

@bot.message_handler(commands=['start'])
def handle_start(msg):
    bot.send_message(msg.from_user.id, show_keyboard('shops')[1], reply_markup=show_keyboard('shops')[0])
   

@bot.message_handler(commands=['stop'])
def handle_stop(msg):
    bot.send_message(msg.from_user.id, hide_keyboard()[1], reply_markup=hide_keyboard()[0])
    bot.send_message(msg.from_user.id, 'Ждем Вас снова!', reply_markup=show_keyboard('start_button'))


@bot.message_handler(content_types=['text'])
def handle_text(msg):
    global shop_name
    if msg.text == 'Ашан':
        shop_name = 'Ашан'
        bot.send_message(msg.from_user.id, '...', reply_markup=hide_keyboard()[0])
        bot.send_message(msg.from_user.id, show_keyboard('options')[1], reply_markup=show_keyboard('options')[0])
        link = crawler.auchan

    elif msg.text == 'Дикси':
        shop_name = 'Дикси'
        bot.send_message(msg.from_user.id, '...', reply_markup=hide_keyboard()[0])
        bot.send_message(msg.from_user.id, show_keyboard('options')[1], reply_markup=show_keyboard('options')[0])
        link = crawler.dixy

    elif msg.text == 'Количество акций':
        if shop_name == 'Ашан':
            bot.send_message(msg.from_user.id, crawler.get_number_of_sales(crawler.auchan))
        elif shop_name == 'Дикси':
            bot.send_message(msg.from_user.id, crawler.get_number_of_sales(crawler.dixy))

    elif msg.text == 'Список наименований':
        bot.send_message(msg.from_user.id, '...', reply_markup=hide_keyboard()[0])
        if shop_name == 'Ашан':
            bot.send_message(msg.from_user.id, show_keyboard('categoryAuchan')[1], reply_markup=show_keyboard('categoryAuchan')[0])
        elif shop_name == 'Дикси':
            bot.send_message(msg.from_user.id, show_keyboard('categoryDixy')[1], reply_markup=show_keyboard('categoryDixy')[0])

    elif msg.text == 'Отслеживать изменения':
        bot.send_message(msg.from_user.id, '...следим...', reply_markup=show_keyboard('stop_button'))
        if shop_name == 'Ашан':
            if crawler.notify_auchan() == 1:
                bot.send_message(msg.from_user.id, 'Есть обновления! Прекращаем отслеживание.', reply_markup=hide_keyboard()[0])
                bot.send_message(msg.from_user.id, 'Для возобновления введите команду снова.',  reply_markup=show_keyboard('start_button'))
                crawler.update_auchan()
        elif shop_name == 'Дикси':
            if crawler.notify_dixy() == 1:
                bot.send_message(msg.from_user.id, 'Есть обновления! Прекращаем отслеживание.', reply_markup=hide_keyboard()[0])
                bot.send_message(msg.from_user.id, 'Для возобновления введите команду снова.',  reply_markup=show_keyboard('start_button'))    
                crawler.update_dixy()

    elif msg.text in crawler.d_item:
        reply_str = crawler.reply(msg.text, crawler.dixy_items)
        for message in reply_str.split('#'):
            bot.send_message(msg.from_user.id, message)

    elif msg.text + ' ' in crawler.a_item:
        reply_str = crawler.reply(msg.text, crawler.auchan_items)
        for message in reply_str.split('#'):
            bot.send_message(msg.from_user.id, message)


# Запускаем бота
bot.polling(none_stop=True)
