import telebot  
import requests  
from telebot import types  
import json  

bot = telebot.TeleBot('8170076644:AAHFE81Fk3ENkwB1LHE29QFFcMf07rUGi0w')   
API = 'ad7961451b64078ef4c282cc83cc5082'  

@bot.message_handler(commands=['start'])  
def start_and_main(message):  
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  
    button = types.KeyboardButton("Шахове🏡")  
    button1 = types.KeyboardButton("Доброполье🌆")  
    button2 = types.KeyboardButton("Сибирь🥶")  
    keyboard.add(button, button2)  
    keyboard.add(button1)  
    bot.send_message(message.chat.id, f'👋Привет, {message.from_user.first_name}, напиши название города или выбери ниже предложенные варианты, чтобы узнать погоду⛅️', reply_markup=keyboard)  

@bot.message_handler(content_types=['text'])  
def handle_message(message):  
    city = message.text.strip()  

    
    if city.endswith("🏡") or city.endswith("🌆") or city.endswith("🥶"):  
        city = city[:-1] 

    bot.reply_to(message, f"Вы выбрали {city}")  
    
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')  
    data = json.loads(res.text)  

    if "main" in data:  
        temp = data["main"]["temp"]  
        bot.reply_to(message, f'🌡Сейчас погода в {city}: {temp}°C')  

        image = 'sun.png' if temp > 5.0 else 'nosun.png'  
        with open('./' + image, 'rb') as file:                               
            if temp > 5.0:  
                bot.send_message(message.chat.id, 'Удачной прогулки🔆')  
            else:  
                bot.send_message(message.chat.id, 'Оденься потеплее, к примеру, пиджак❄️')  
            bot.send_photo(message.chat.id, file)  
    else:  
        bot.reply_to(message, "Город не найден. Пожалуйста, попробуйте другой.")  

@bot.message_handler(commands=['help'])  
def help_command(message):  
    bot.send_message(message.chat.id, 'Себе помоги')  

try:  
    bot.polling(none_stop=True)  
except Exception as e:  
    print(f'Error: {e}')  