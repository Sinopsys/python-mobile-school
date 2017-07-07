# coding: utf8
# Английский словарь
eng = { '1':'My work started.', '2':'Choose command: \n/find_recipe_by_ingridients find recipes by them ingredients\n/settings settings of the bot\n/about about the creators of the bot', '3':'My work has already started. Stop typing /start', '4' :"Hello! I'm RecipeFoodBot, who can recommend you some interesting recipes to cook food. Type /start to begin work with me", '5' : "So, write ingredients to find recipes with them", '6' : "I'm searching, just a second", '7' : "I can't find anything by this request. Try to write another ingredients", '8' : "I'm searching...", '9' : "I need in more then 1 ingredient", '10' : "Settings: \n/change_language change language of the bot\n/change_max_count change max number of recipes (3 as default)\n/back return to main menu", '11' : "Choose language", '12' : "New max count recieved. Current: ", '13' : "Count should be bigger then 0", '14' : "Invalid count. Try to write another", '15' : "Write max count", '16' : "Bot was developed by four young russian programmers in case of Summer School of Mobile development that supervised by HSE, Yandex and Samsung\nName of programmers: \nAndrey Vaulin\nAnatoliy Globin\nMihail Kolmykov\nVasiliy Safronov", '17' : "Goodbye!", '18' : "I can't download recipe"}
# Русский словарь
rus = { '1': "Я работаю.", '2':'Выберите команду: \n/find_recipe_by_ingridients находит рецепты по их ингредиентам\n/settings настройки бота\n/about о создателях бота', '3':"Я уже работаю. Прекратите писать /start", '4' : "Привет! Я RecipeFoodBot, могу порекомендовать тебе некоторые интересные рецепты для приготовления еды. Набери /start для начала работы", '5' : "Итак, напишите ингредиенты, чтобы я нашёл рецепты с ними", '6': "Одну минуточку, я ищу!", '7' : "Я не могу найти что-либо по этому запросу. Попробуйте написать другие ингредиенты", '8' : "Я ищу...", '9' : "Мне нужно больше одного ингердиента для поиска", '10' : "Настройки: \n/change_language меняет язык бота\n/change_max_count меняет максимальное количество присылаемых рецептов (по-умолчанию 3)\n/back вернуться в главное меню" , '11' : "Выберите язык", '12' : "Новое максимальное количество принято. Текущее: ", '13' : "Количество должно быть больше нуля", '14' : "Неверное количество. Попробуйте написать другое число", '15' : "Напишите максимальное количество", '16' : "Бот был разработан четырьмя молодыми российскими программистами в рамках летней школы мобильной разработки, которая курируется НИУ ВШЭ, Яндексом и компанией Samsung\nИмена программистов: \nАндрей Ваулин\nАнатолий Глобин\nМихаил Колмыков\nВасилий Сафронов", '17' : "До свидания!", '18' : "Я не могу прогрузить рецепт" }

# Возвращение локализации по её номеру и текущему языку
def return_local(lang, pos):
    global eng
    global rus   
    ph = ""
    if lang == 'rus':
        return rus[str(pos)]
    else:
        return eng[str(pos)]
    
