# coding: utf8
# Ключ бота
token = '330752641:AAHQRwWMqHjyH2GBaZazKpMcE2Z_dBJDGMQ'
# Словарь статусов бота (для каждого чата)
d = dict()
# Словарь текущих языков (для каждого чата)
l = dict()
# Словарь текущего количества возвращаемых запрос (для каждого чата)
c = dict()

# Проверка начала работы и возврат статуса
def check_started_chat(chat_id):
    global d
    try:
        v = d[chat_id]
        return v
    except BaseException:
        return False

# Начало работы (индекс начала = 1)
def set_started_chat(chat_id):
    global d
    d[chat_id] = 1
    return True

# Изменение статуса работы бота в чате по ID
def work_with_command(chat_id, number):
    global d
    d[chat_id] = number
    return True

# Проверка заданного языка (по-умолчанию возвращается - rus)
def check_lang(chat_id):
    global l
    try:
        v = l[chat_id]
        if v == 'rus':
            return 'rus'
        else:
            return 'eng'        
    except BaseException:
        return 'rus'

# Выбор другого языка
def set_lang_chat(chat_id, lang):
    global l
    l[chat_id] = lang
    return True

# Проверка количества (по-умолчанию возвращается 3)
def check_count(chat_id):
    global c
    try:
        v = c[chat_id]
        return int(v)     
    except BaseException:
        return 3

# Выбор другого количества
def set_count(chat_id, count):
    global c
    c[chat_id] = count
    return True

# Метод удаления чата из базы бота (не используется)
def destroy_all(chat_id):
    global c
    global l
    global d
    c.pop(chat_id)
    l.pop(chat_id)
    d.pop(chat_id)
    return True
