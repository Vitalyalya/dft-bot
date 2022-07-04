# -*- coding: utf-8 -*-

import requests
import re
import time

from asyncio import shield

from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token='2106917801:AAHfCIvm25ukZTTAQ_GV8UGVVZHUmbt_d34', parse_mode=types.ParseMode.HTML, timeout=9999999)
dp = Dispatcher(bot)

print('Bot started')

id_list = []

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }

def no_links(text):
    if '](' in text:
        text_fixed = re.sub("\(.*?\)","()", text)
        text_fixed = text_fixed.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('**', '')
        return text_fixed
    else:
        return text


def get_news(titles, id):


    title = titles['title']
    print(f'{title} \n')

    s = f'<b>{title}</b>\n \n'
    
    for parts in titles['blocks']:

        if parts['type'] == 'text' or parts['type'] == 'header':

            text_part = parts['data']
            for key,value in text_part.items():
                if key == 'text':
                    if '#' in value:
                        value = value.replace("\\", '')
                    abzac = no_links(value)
                    print(abzac)
                    
                    s += f'{abzac}\n \n'



        elif parts['type'] == 'quote':
            text_part = parts['data']
            print('Начало цитаты')

            for key, value in text_part.items():
                if key == 'text':

                    print(no_links(value))
                    quote = no_links(value)
                    s += f'Начало цитаты:\n<i>{quote}</i>\nКонец цитаты \n'

                elif key == 'subline1':

                    print(no_links(value))
                    underquote = value
                    s += f'{underquote}\n'
                elif key == 'subline2':
                    print(no_links(value))
                    underquote2 = value
                    s += f'{underquote2}\n \n'

            print('Конец цитаты')
        elif parts['type'] == 'list':
            text_part = parts['data']['items']
            for i in text_part:
                print(f'*{no_links(i)}')
                lst = no_links(i)
                s += f'{lst}\n \n'
    print(f'Ссылка: https://dtf.ru/{id}')   
    s += f'Ссылка: https://dtf.ru/{id}'         
    print('_____________________________')
    print(id_list)
    print('_____________________________')
    return s
        

@dp.message_handler()
async def echo():

    url = ('https://api.dtf.ru/v2.1/news')    

    while True:       

        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        evrth = data['result']['news']
        
        for titles in evrth:
        

            id = titles['id']

            if id in id_list:

                pass

            else:
                id_list.append(id)
                print(id_list)

                s = get_news(titles, id)
                if len(s) > 4096:
                    pass
                else:
                    await shield(bot.send_message(-1001654271018, s, disable_web_page_preview=True))

        time.sleep(300)  
        print('5 minutes passed') 

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)