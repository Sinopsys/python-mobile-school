import sqlite3 as sql
from bs4 import BeautifulSoup
import requests

def create_db():
    conn = sql.connect('banks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS banks
                 (bank_name text PRIMARY KEY, usd_sv real, usd_bv real, eu_sv real, eu_bv real, time text)''')
    conn.commit()
    conn.close()


def create_info(bank_name, usd_sv, usd_bv, eu_sv, eu_bv, time):
    conn = sql.connect('banks.db')
    c = conn.cursor()
    c.executemany('''INSERT INTO banks(bank_name, usd_sv, usd_bv, eu_sv, eu_bv, time) VALUES (?,?,?,?,?,?)''', [(bank_name, usd_sv, usd_bv, eu_sv, eu_bv, time)])
    conn.commit()
    conn.close()


def renew_info(bank_name, usd_sv, usd_bv, eu_sv, eu_bv):
    conn = sql.connect('banks.db')
    c = conn.cursor()
    c.executemany('''UPDATE banks SET usd_sv = ?, usd_bv = ?, eu_sv = ?, eu_bv = ? WHERE bank_name = ?''', [(usd_sv, usd_bv, eu_sv, eu_bv, bank_name)])
    conn.commit()
    conn.close()


def top_5(s):
    if s == "eu sell":
        arg = "eu_sv"
    elif s == "eu buy":
        arg = "eu_bv"
    elif s == "usd sell":
        arg = "usd_sv"
    elif s == "usd buy":
        arg = "usd_bv"

    conn = sql.connect("banks.db")
    c = conn.cursor()
    banks = list()
    x = 0
    if arg == "usd_sv" or arg == "eu_sv":
        for row in c.execute("SELECT * FROM banks ORDER BY "+arg):
            banks.append(row)
            if x == 4:
                conn.commit()
                conn.close()
                return banks
            x+=1
    elif arg == "usd_bv" or arg == "eu_bv":

        for row in c.execute("SELECT * FROM banks ORDER BY "+arg+" DESC"):
            banks.append(row)
            if x == 4:
                conn.commit()
                conn.close()
                return banks
            x+=1
    conn.commit()
    conn.close()
    return banks

def get_banks():
    source_code = requests.get('https://finance.rambler.ru/currencies/exchange/')
    source_code.encoding = 'utf-8'
    soup =  BeautifulSoup(source_code.text, 'lxml')
    inf1 = soup.find_all('td')
    ch = 0
    x = 0
    for item in inf1:
        if ch>=49:
            if x == 0:
                name = item.text
            elif x == 1:
                u_b = item.text
            elif x == 2:
                u_s = item.text
            elif x == 3:
                e_b = item.text
            elif x == 4:
                e_s = item.text
            elif x == 5:
                time = item.text
            if x == 5:
                try:
                    create_info(name.rstrip(), u_s, u_b, e_s, e_b, time)
                except:
                    print(1)
                x = -1
            x +=1
        else:
            ch +=1


def bank_search(name):
    conn = sql.connect("banks.db")
    c = conn.cursor()
    b=''
    for row in c.execute("SELECT * FROM banks WHERE bank_name = '"+name +"'"):
        b = row
    conn.commit()
    conn.close()
    return b
