# Импортируем необходимые библиотеки
#
from bs4 import BeautifulSoup
import requests
from time import sleep
import smtplib


# Метод для получения максимального количества страниц на сайте
#
def get_max_pages():
    # Получаем исходный код в формате request
    source_code = requests.get(
        'https://dixy.ru/akcii/skidki-nedeli/?PAGEN_1=1')
    source_code.encoding = 'utf-8'
    # Создаём объект "супа" - парсера html кода
    # Иногда вместо 'lxml' нужно передавать 'html parser'
    soup = BeautifulSoup(source_code.text, 'lxml')

    # ------ способ 1, нормальный ------
    # Находим все теги ссылок (тег 'a')
    ppl = soup.find_all('a')
    res = 0
    # Проходимся по каждой ссылке и если в ней
    for item in ppl:
        if 'PAGEN_1' in item.get('href'):
            res += 1

    # ------ способ 2, побыстрее ------
    # ppl = soup.find_all('ul', {'class': 'page-pagination-list'})
    # return (len(ppl[0].find_all('li')) - 1)
    return res


# Метод для определения общего количества акций
#
def get_number_of_sales():
    # Начинаем с первой страницы
    current_page = 1
    # Инициализируем сумму нулём
    sales_number = 0
    # Получаем количество страниц
    max_pages = get_max_pages()
    # Проходимся по каждой страние
    while current_page <= get_max_pages():
        source_code = requests.get(
            'https://dixy.ru/akcii/skidki-nedeli/?PAGEN_1={}'.format(current_page))
        source_code.encoding = 'utf-8'
        soup = BeautifulSoup(source_code.text, 'lxml')
        # Находим все 'div'ы и с классом product
        # И инкрементируем счетчик
        for item in soup.find_all('div', {'class': 'product'}):
            sales_number += 1
        # Переходим на следующую страницу
        current_page += 1
    return sales_number


# Метод для отправки e-mail с тестового аккаунта на GMail
#
def send_email(msg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('cabinet327@gmail.com', '1234QWER')
    server.sendmail('cabinet327@gmail.com', 'cabinet327@gmail.com', msg)
    server.quit()

# Раз 30 секунд смотрим на новое количество акций и сравниваем с текущим -
# Если не совпало, то изменились скидки
#
def track_changes():
    current_number_of_sales = get_number_of_sales()
    while True:
        if current_number_of_sales != get_number_of_sales():
            # send_email('sales has changed')
            return 1
        current_number_of_sales = get_number_of_sales()
        sleep(30)

# EOF
