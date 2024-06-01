from aiogram import Bot, Dispatcher, types
import pyqrcode
from urllib.request import Request, urlopen
import html2text
import pandas as pd
from lxml import html
from tabulate import tabulate
import requests
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
import pprint
from html.parser import HTMLParser #імпортуєм бібліотеки
import numpy
from os import environ
import logging

FORMAT = '%(asctime)-15s %(name)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logging.basicConfig(level=logging.ERROR, format=FORMAT)
logger = logging.getLogger()

tg_bot_token = environ.get("TG_BOT_TOKEN","define me")

class Holidays(StatesGroup): #створюєм клас свята
    holidays = State()
#змінні для класу з парсиром html сторінки
start_tags = []
end_tags = []
all_data = []
comments = []

class Parser(HTMLParser):
    # метод для додавання початкового тега до списку start_tags.
    def handle_starttag(self, tag, attrs):
        global start_tags
        start_tags.append(tag)
        # метод для додавання кінцевого тегу до списку end_tags.

    def handle_endtag(self, tag):
        global end_tags
        end_tags.append(tag)

    # метод для додавання даних між тегами до списку all_data.
    def handle_data(self, data):
        global all_data
        all_data.append(data)

    # метод додавання коментаря до списку коментарів.
    def handle_comment(self, data):
        global comments
        comments.append(data)

def hero(): # функцыя яка виводить масив який виводить данні про героїв
    global start_tags
    global end_tags
    global all_data
    global comments
    # Створення екземпляра нашого класу.
    parser = Parser()
    # Надання вхідних даних.

    req = Request('https://uk.dotabuff.com/heroes/winning', headers={'User-Agent': 'Mozilla/5.0'}) #Отримуємо html сторінку сайту
    webpage_b = urlopen(req).read()
    webpage = webpage_b.decode('utf-8')

    table_startindex = -1 #початок з відки берем данні і кінець
    table_endtindex = -1

    parser.feed(webpage) #пошук меж в яких міститься інформація про героїв
    for i in range(len(all_data)):
        if all_data[i] == "Герой":
            table_startindex = i
        if all_data[i] == "Останнє оновлення ":
            table_endtindex = i

    new_array = numpy.split(all_data, [table_startindex, table_endtindex])[1] #масив в якому містяться данні про героїв
    data_array = numpy.reshape(new_array, (-1, 4))
    logger.info(data_array)
    return data_array



bot = Bot(token=tg_bot_token) #токен бота
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
data_array_T = hero()

logger.info('Bot Started')

@dp.message_handler(commands=['help']) # вивід вітання від бота
async def welcome(massage: types.Message):
 await massage.reply("/start - команда яка зустрічає користувача\n" \
 "'/meta' виводить перших 20 героїв на екран користувачу\n" \
 "'/meta 12-23' -Виводить героїв залежно від данних які ввели, наприклад " \
 "список почнеться від 12 героя закінчиться 23\n" \
 "'/hero' -виводить конкретного героя, наприклад '/hero Visage' " \
 "надає детальну інформацію про одного героя\n" \
 "'/holiday (і рік)' - Надає данні про свята у вказаному році, наприклад " \
 "'holiday 2020'\n" \
 "'/holiday (рік) info' при введені цієї команди користувачу запропонують вибрати " \
 "свято, надає інформацію про конкретно введене свято")

@dp.message_handler(commands=['start']) # вивід вітання від бота
async def welcome(massage: types.Message):
 await massage.reply("Hello I am bot")

@dp.message_handler(commands=['cat'])
async def cat(nmessege:types.Message):
    await nmessege.answer_photo('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8FHWcXpZPGEFmQmuLVmMTXuCUfqDmxCbXiQ&usqp=CAU') #показує зображення кота


@dp.message_handler(commands=['meta']) #виводить героїв по списку
async def echo(message: types.Message):
    responce_message=""
    arr = []
    data_array = hero() #викликає отримання масиву данних про героїв
    data_array_T = numpy.transpose(data_array)
    try:
        if len(message.text) > 6: #перевірка чи користувач ввів межі пошуку героїв за номером
            parametr = message.text[6:].split("-")
            if int(parametr[0]) > int(parametr[1]): # перевірка чи кінцевий індекс мешний за початковий
                parametr = [1, 5]
            elif int(parametr[1]) - int(parametr[0]) > 30: #перевірка чи різниця початкового і кінцевого індекса більше за 30
                parametr = [parametr[0], parametr[0] + 10]
        else:
            parametr = [1, 10]
            #Побудова масиву таблиці відносно заданих меж
        for i in range(int(parametr[0]), int(parametr[1]) + 1):
            arr.append([data_array_T[0][i], data_array_T[1][i], data_array_T[2][i], data_array_T[3][i]])
        temp = tabulate(arr, headers=['Герой ', 'Відсоток перемог ', 'Популярність ', 'Співвідношення УСП '])

        logger.info(temp)
        temp = "<pre>" + temp + "</pre>"
    except:
        temp="ви ввели некоректні данні"
    await message.answer(temp, parse_mode="HTML")

#ls = list((map(lambda x: x.lower(), list(data_array_T[0]))))   #Зменшує слова в масиві з іменами героями
#ls = list((map(lambda x: x.split(" ")[0], ls)))
#ls = list((map(lambda x: x.split("'")[0], ls)))
@dp.message_handler(commands=['hero']) #користувач вводить героя йому надають данні про данного героя
async def echo(message: types.Message):
    data_array = hero()
    data_array_T = numpy.transpose(data_array)
    t=1
    for i in range(1,len(data_array)):
        if data_array_T[0][i]==(message.text[6:]):
            t=i
    arr = [[data_array_T[0][t], data_array_T[1][t], data_array_T[2][t], data_array_T[3][t]]]
    temp = tabulate(arr, headers=['Герой ', 'Відсоток перемог ', 'Популярність ', 'Співвідношення УСП '])
    temp = "<pre>" + temp + "</pre>"
    await message.answer(temp,parse_mode="HTML")



@dp.message_handler(commands=['holiday']) #при вводі команди і року виводить свята на рік який задали
async def holiday(message: types.Message):
    global holiday_year
    global responce
    holiday_year = message.text[9:13]
    responce = requests.get(f"https://date.nager.at/api/v3/publicholidays/{holiday_year}/UA").json()
    logger.info(responce)
    newarray=[]
    # при введені параметра інфо користувач має ввести назву свята для якого він хоче отримати загальну іфнформацію
    if message.text[14:] == "info":
        await message.answer('Введіть назву свята про яке ви бажаєте отримати детальну інфомацію')
        await Holidays.holidays.set()
    else: #виведення списку всіх свят з короткою інформацією про них
        for holiday in responce:
            newarray.append([holiday['date'], holiday['localName']])
        temp = tabulate(newarray, headers=['Date ', 'Local Name holidays '])
        logger.info(temp)
        temp = "<pre>" + temp + "</pre>"
        await message.answer(temp, parse_mode="HTML")
@dp.message_handler(state=Holidays.holidays) #отримання від користувача назви свята та виведення інформації про нього
async def Holidayanswer(message: types.Message, state: FSMContext):
    searchname=message.text
    #responce = requests.get(f"https://date.nager.at/api/v3/publicholidays/{holiday_year}/UA").json()
    for i in range(len(responce)):
        if responce[i]['localName'] == searchname:
            responce_message = f"Місцева назва свята: {responce[i]['localName']}\n" \
                               f"Дата свядкування: {responce[i]['date']}\n" \
                               f"Код країни: {responce[i]['countryCode']}\n" \
                               f"Свято фіксоване на року: {responce[i]['fixed']}\n" \
                               f"Міжнародне свято: {responce[i]['global']}\n" \
                               f"Округ: {responce[i]['counties']}\n" \
                               f"Рік заснування: {responce[i]['launchYear']}\n" \
                               f"Тип міжнародного свята: {responce[i]['types'][0]}"

    await message.answer(responce_message)
    await state.finish()



executor.start_polling(dp)
