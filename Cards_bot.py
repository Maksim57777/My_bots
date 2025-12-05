import telebot
import random
import json
import time
nisk_simvols = ["1","2","3","4","5","6","7","8","9","0", "A", "B", "C", "D"]
bot = telebot.TeleBot ('8592594669:AAHybCJ4QxI2VB1r8dA32TwwXf-1L7hSXP4')
@bot.message_handler(commands=['start'])
def start (message) :
    msg = bot.send_message(message.from_user.id, '''Привет, я бот для карточной игры "Цифры"\n
Введите "/rules" чтобы узнать правила игры\n
Введите ник игрока для игры с ним''')
    show_nisk (message)


def show_nisk (message) :
    with open ("Nisks.json", "r") as f :
        nisks = json.load (f)
        user_nick = (random.shuffle (nisk_simvols) + random.shuffle (nisk_simvols) + random.shuffle (nisk_simvols) + random.shuffle (nisk_simvols) + random.shuffle (nisk_simvols) )
    while  user_nick in nisks :
        user_nick = (random.shuffle (nisk_simvols) + random.shuffle (nisk_simvols) + random.shuffle (nisk_simvols) + random.shuffle (nisk_simvols) + random.shuffle (nisk_simvols) )
        
    nisks [user_nick] = message.from_user.id
    with open ("Nisks.json", "w") as f :
        json.dump (nisks, f)
    msg = bot.send_message(message.from_user.id, "Ваш ник: {}.".format (user_nick))
    bot.register_next_step_handler (message, )

  