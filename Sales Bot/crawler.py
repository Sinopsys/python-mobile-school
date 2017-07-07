from bs4 import BeautifulSoup
import requests
from time import sleep

dixy_items = {}
auchan_items = {}

dixy = 'https://dixy.ru/akcii/skidki-nedeli{}/?PAGEN_1={}'
auchan = 'https://www.auchan.ru/pokupki/rasprodaja{}.html?p={}'

dnc = 'product-name'
dpc = 'product-price-container'
ddc = 'inner-wrapper'
dopc = 'inner-wrapper'
anc = 'products__item-link'
apc = 'products__item-current-price current-price'
adc = 'products__item-badge badge badge--yellow badge--discount'
aopc = 'products__item-old-price old-price'

class_dixy = 'product'
class_auchan = 'products__item-inner'

category_li = ['(', ')', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '\t', '\n', '\r']
discount_li = ['*', '-', '\t', '\n', '\r']
text_li = ['\t', '\n', '\r']


class Item:
    def __init__(self, name, price, old_price, discount, pic):
        self.name = name
        self.price = price
        self.old_price = old_price
        self.discount = discount
        self.pic = pic


def get_max_pages(link, category):
    source_code = requests.get(link.format('/' + category, '1'))
    source_code.encoding = 'utf-8'
    soup = BeautifulSoup(source_code.text, 'lxml')
    # print(link.format('/' + category, '1'))
    if link == auchan:
        try:
            ul = soup.find('ul', {'class': 'pagination__list'})
            # print(ul.get_text())
            # print(category)
            max_pages = int(len(ul.findChildren()) / 2)
        except:
            max_pages = 1
    elif link == dixy:
        ppl = soup.find_all('ul', {'class': 'page-pagination-list'})
        try:
            max_pages = (len(ppl[0].find_all('li')) - 1)
        except:
            max_pages = 1
    return max_pages


def clear(string, li):
    string = string.strip()
    for ch in li:
        if ch in string:
            string = string.replace(ch, '')
    return string


def get_names(link, category, el, class_h):
    items = []
    current_page = 1
    max_page = get_max_pages(link, category)
    while current_page <= max_page:
        source_code = requests.get(link.format('/' + category, current_page))
        source_code.encoding = 'utf-8'
        soup = BeautifulSoup(source_code.text, 'lxml')
        for name in soup.find_all(el, {'class': class_h}):
            name = clear(name.string, text_li)
            # print(name)
            item = Item(name, '', '', '', ' ')
            items.append(item)
        current_page += 1
    return items


def get_prices(items, link, category, class_h):
    current_page = 1
    max_page = get_max_pages(link, category)
    curr_index = 0
    while current_page <= max_page:
        source_code = requests.get(link.format('/' + category, current_page))
        source_code.encoding = 'utf-8'
        soup = BeautifulSoup(source_code.text, 'lxml')
        for price in soup.find_all('div', {'class': class_h}):
            if (link == dixy):
                children = price.findChildren()
                for child in children:
                    if child.has_attr('class') and child['class'][0] == 'price':
                        price = child.get_text()
                    elif child.has_attr('class') and child['class'][0] == 'fract':
                        price += '.' + child.get_text()
            elif (link == auchan):
                price = price.get_text()
            price = clear(price, discount_li)
            items[curr_index].price = price
            curr_index += 1
        current_page += 1
    return items


def get_old_prices(items, link, category, class_h):
    current_page = 1
    max_page = get_max_pages(link, category)
    curr_idx = 0
    while current_page <= max_page:
        source_code = requests.get(link.format('/' + category, current_page))
        source_code.encoding = 'utf-8'
        soup = BeautifulSoup(source_code.text, 'lxml')
        for old_price in soup.find_all('div', {'class': class_h}):
            if (link == dixy):
                children = old_price.findChildren()
                for child in children:
                    if child.has_attr('class') and len(child['class']) > 1 and (
                                child['class'][0] == 'product-price') and (child['class'][1] == 'only'):
                        old_price = 'Нет'
                    elif child.has_attr('class') and (child['class'][0] == 'product-price'):
                        grandchildren = child.findChildren()
                        for grandchild in grandchildren:
                            if grandchild.has_attr('class') and (grandchild['class'][0] == 'old-price'):
                                old_price = grandchild.get_text()
                                old_price = old_price[:-3] + '.' + old_price[-3:-1]
                                # print(old_price)
            elif (link == auchan):
                old_price = old_price.get_text()
            old_price = clear(old_price, text_li)
            items[curr_idx].old_price = old_price
            curr_idx += 1
        current_page += 1
    return items


def get_discount(items, link, category, class_h):
    current_page = 1
    max_page = get_max_pages(link, category)
    curr_idx = 0
    while current_page <= max_page:
        source_code = requests.get(link.format('/' + category, current_page))
        source_code.encoding = 'utf-8'
        soup = BeautifulSoup(source_code.text, 'lxml')
        for discount in soup.find_all('div', {'class': class_h}):
            if (link == dixy):
                flag = True
                children = discount.findChildren()
                for child in children:
                    if child.has_attr('class') and len(child['class']) > 1 and child['class'][1] == 'discount-size':
                        discount = child.get_text()
                    elif child.has_attr('class') and len(child['class']) > 1 and child['class'][1] == 'only':
                        discount = 'Только сейчас'
            elif (link == auchan):
                discount = discount.get_text()
            try:
                discount = clear(discount, discount_li)
            except:
                discount = 'Скидка не указана'
            items[curr_idx].discount = discount
            curr_idx += 1
        current_page += 1
    return items


def get_categories(link, h_class):
    item = []
    categories = []
    # print(link.format('', '1'))
    source_code = requests.get(link.format('', '1'))
    source_code.encoding = 'utf-8'
    soup = BeautifulSoup(source_code.text, 'lxml')
    ul = soup.find('ul', {'class': h_class})
    children = ul.findChildren()
    for child in children:
        # print(child.get('href'))
        category = child.get('href')
        # print(category)
        if category != None:
            category = category.strip()
            # print(category)
        else:
            continue
        if (link == dixy):
            # print(category);
            category = category[len('/akcii/skidki-nedeli/'):-1]
        elif (link == auchan):
            category = category[len('https://www.auchan.ru/pokupki/rasprodaja/'): - 5]
        categories.append(category)
        item.append(clear(child.get_text(), category_li))
    return item, categories


def get_number_of_sales(link):
    if link == dixy:
        chosen_class = class_dixy
    else:
        chosen_class = class_auchan

        # Начинаем с первой страницы
    current_page = 1
    # Инициализируем сумму нулём
    sales_number = 0
    # Получаем количество страниц
    max_pages = get_max_pages(link, '/')
    # Проходимся по каждой страние
    while current_page <= max_pages:
        source_code = requests.get(link.format('', current_page))
        source_code.encoding = 'utf-8'
        soup = BeautifulSoup(source_code.text, 'lxml')
        # Находим все 'div'ы и с классом product
        # И инкрементируем счетчик
        for item in soup.find_all('div', {'class': chosen_class}):
            sales_number += 1
        # Переходим на следующую страницу
        current_page += 1
    return sales_number


def notify_auchan():
    current_number_of_sales_auchan = get_number_of_sales(auchan)
    while True:
        if current_number_of_sales_auchan != get_number_of_sales(auchan):
            current_number_of_sales_auchan = get_number_of_sales(auchan)
            return 1
        sleep(60)


def notify_dixy():
    current_number_of_sales_dixy = get_number_of_sales(dixy)
    while True:
        if current_number_of_sales_dixy != get_number_of_sales(dixy):
            current_number_of_sales_dixy = get_number_of_sales(dixy)
            return 1
        sleep(60)


def update_dixy():
    for category, item in zip(dixy_categories, d_item):
        item = item.strip()
        dixy_items[item] = get_names(dixy, category, 'div', dnc)
        dixy_items[item] = get_prices(dixy_items[item], dixy, category, dpc)
        dixy_items[item] = get_discount(dixy_items[item], dixy, category, ddc)
        dixy_items[item] = get_old_prices(dixy_items[item], dixy, category, dopc)


def update_auchan():
    for category, item in zip(auchan_categories, a_item):
        item = item.strip()
        auchan_items[item] = get_names(auchan, category, 'a', anc)
        auchan_items[item] = get_prices(auchan_items[item], auchan, category, apc)
        auchan_items[item] = get_discount(auchan_items[item], auchan, category, adc)
        auchan_items[item] = get_old_prices(auchan_items[item], auchan, category, aopc)


def reply(category, items_type):
    reply = ''
    length = 0
    for item in items_type[category]:
        name = item.name
        price = item.price
        old_price = item.old_price
        discount = item.discount
        line = name + ',' + ' ' + old_price + ' > ' + price + ' ' + '(' + discount + ')' + '\n'
        if (len(reply) + len(line)) - length >= 4000:
            reply += '#'
            length = len(reply)
        reply += name + ',' + ' ' + old_price + ' > ' + price + ' ' + '(' + discount + ')' + '\n'
    if reply.strip() == '':
        reply = 'Ничего нет'
    return reply



d_item, dixy_categories = get_categories(dixy, 'catalog-menu-list')
a_item, auchan_categories = get_categories(auchan, 'filter__list')

dixy_categories = dixy_categories[1:]
d_item = d_item[1:]

update_dixy()

update_auchan()
