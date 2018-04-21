#Подключаем конфиг с той же папки
import config
#подключаем библиотеку для работы с ботой
import telebot
#подключаем библиотеку для работы с датой и временем
from datetime import datetime
#Модуль библиотеки телебот для создания кнопок
from telebot import types
#добавляем библиотеку для работы с запросами
import requests
#подключаем библиотеку дял работы с форматом json
import json
#создаем объект класса TeleBot
bot = telebot.TeleBot(config.token)
#функция возвращает текущее время, служит для записи времени в логах
def get_Time_Now():
    return datetime.strftime(datetime.now(), "%d.%m.%y %H:%m:%S")
#Функция создает и дополняет файл лога в папке с ботом, на каждыое действие
def write_To_Log(mid,text):
    with open("log.txt","a+", encoding = "utf-8") as log:
        log.write(get_Time_Now()+" "+str(mid)+" "+text+"\n")
        log.close()
#обработчик команды /start
@bot.message_handler(commands = ['start'])
def start(message):
    #приветствие бота
    bot.send_message(message.chat.id, "Вас приветствует инфобот.")
    #запись в логи что бот поприветствовался
    write_To_Log(message.from_user.id, "user send /start , bot answer hello")
    #создание список кнопок
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #добавление названия кнопок в список
    buttons.add(*[types.KeyboardButton(name) for name in ["Курс валют","Погода"]])
    #выводим подсказки и кнопки
    bot.send_message(message.chat.id, "Выберите вариант:", reply_markup=buttons)
    #обращаемся к обработчику кнопок
    bot.register_next_step_handler(message, choice_User)

def choice_User(message):
    if message.text == "Курс валют":
        write_To_Log(message.from_user.id, "user get kurs")
        get_Kurs(message)
    else:
        message.text == "Погода"
        write_To_Log(message.from_user.id,"user get weather")
        get_weather(message)

def get_Kurs(message):
    try:
        response = requests.get("http://data.egov.kz/api/v2/valutalar_bagamdary4/v302?source={\"size\":200}")
        jsonAnswer = json.loads(response.text)
        bot.send_message(message.chat.id, "Курс валют на"+get_Time_Now())
        for i in jsonAnswer:
            if i["kod"] == "RUB" or i["kod"] == "USD" or i["kod"] == "EUR":
                bot.send_message(message.chat.id, "1 "+i["name_rus"]+" ="+i["kurs"]+i["edinica_izmerenia"])
        write_To_Log(message.from_user.id,"bot send kurs")
        bot.register_next_step_handler(message, choice_User)
    except:
        bot.send_message(message.chat.id,"Сервис недоступен.Попробуйте позже")
        write_To_Log(message.from_user.id, "bot not send kurs becouse portal not working")
        bot.register_next_step_handler(message, choice_User)
def get_weather(message):
    #try:
    data = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Astana&APPID=52eb7def3b115c2815f30a7b6ad3cfde")
    print(data.json())
    bot.send_message(message.chat.id,"Минимальная температура в Астане: "+str(int(data.json()["main"]["temp_min"]-273)))
    #except:
    #    bot.send_message(message.chat.id,"Сервис недоступен.Попробуйте позже")
    #    write_To_Log(message.from_user.id,"bot not send weather because portal not working")
#Проверка работоспособности бота
try:
    bot.polling(none_stop = True)
except:
    write_To_Log("","bot polling error")
