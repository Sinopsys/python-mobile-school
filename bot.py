# Импортируем необходимые библиотеки
#
import telebot
import lib.crawler as crawler # Наш кроулер
from time import sleep

# Токен заменяем на свой
# Создаем асинхронного бота чтобы он мог следить за изменениями в отдельном потоке
#
bot = telebot.AsyncTeleBot('402521476:AAEtZLd206MeRQw-mr2CPQFSj8-vdt_fKkE')


# Хэндлер для команды /start
#
@bot.message_handler(commands=['start'])
def handle_start(msg):
    # Создадим клавиатуру, параметр True - автоматически подгоняет размер клавиатуры под устройство
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('/start', '/stop')
    keyboard.row('Количество акций')
    keyboard.row('Отслеживать изменения')
    # Отправили клавиатуру
    bot.send_message(msg.from_user.id, 'Welcome!', reply_markup=keyboard)

# Хэндлер для команды /stop
#
@bot.message_handler(commands=['stop'])
def handle_start(msg):
    # По команде /stop мы скрываем клавиатуру
    keyboard = telebot.types.ReplyKeyboardRemove()
    bot.send_message(msg.from_user.id, 'Good bye!', reply_markup=keyboard)

# Хэндлер для получения простого текста
#
@bot.message_handler(content_types=['text'])
def handle_text(msg):
    # Если пользователь хочет получить количство акций, вызовится метод get_number_of_sales из нашего кроулера
    if msg.text.lower() == 'количество акций':
        bot.send_message(msg.from_user.id, '...считается количество акций на данный момент...')
        # Якобы бот печатает
        bot.send_chat_action(msg.from_user.id, 'typing')
        bot.send_message(msg.from_user.id, crawler.get_number_of_sales())
    # Если пользователь захочет узнать об изменениях в скидках, будем вызывать track_changes()
    elif msg.text.lower() == 'отслеживать изменения':
        bot.send_message(msg.from_user.id, '...следим...')
        if crawler.track_changes() == 1:
            bot.send_message(msg.from_user.id, 'Изменение! Прекращаем отслеживание. Для возобновления введите команду снова.')

# Запускаем бота
bot.polling(none_stop=True)


# EOF
