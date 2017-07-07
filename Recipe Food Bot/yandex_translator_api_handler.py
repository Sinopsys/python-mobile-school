# coding: utf8
from yandex_translate import YandexTranslate
import json

# Перевод на русский язык
def translate_to_russian(word):
    try:
        translate = YandexTranslate('trnsl.1.1.20170706T092852Z.10d7c655ee1fdace.01556c907414b5567661a59f1262de440da1938e')
        js = translate.translate(word, 'en-ru')    
        fs = js["text"][0]
        return(fs)
    except:
        return 'null'

# Перевод на английский язык
def translate_to_english(word):
    try:
        translate = YandexTranslate('trnsl.1.1.20170706T092852Z.10d7c655ee1fdace.01556c907414b5567661a59f1262de440da1938e')
        js = translate.translate(word, 'ru-en')    
        fs = js["text"][0]
        return(fs)
    except:

        return 'null'


