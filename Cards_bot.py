import telebot
from telebot import types
import random
import json
import time
nisk_simvols = ["1","2","3","4","5","6","7","8","9","0", "A", "B", "C", "D"]
bot = telebot.TeleBot ('8514122137:AAGnjK6LTQjasvOL9esPTU_EL1OXCVnW-B8')
@bot.message_handler(commands=['start'])
def start (message) :
    msg = bot.send_message(message.from_user.id, '''Привет, я бот для карточной игры "Цифры"\n
Введите "rules" чтобы узнать правила игры\n
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
        json.dump (nisks, f, indent=4, ensure_ascii=False)
    msg = bot.send_message(message.from_user.id, "Ваш ник: {}.".format (user_nick))
    bot.register_next_step_handler (message, x)

def x (message) :
    if message.text == "rules" :
        msg = bot.send_message(message.from_user.id, '''Правила игры:\nВы с другим игроком кладёте карты по очереди.\nЕсли атака вашей карты превышает защиту карты
                               внизу, то вы можете положить её сверху, если таких карт у вас нет, возьмите карту и пропустите ход.\nВыигрывает тот кто первым
                               избавится от всех своих карт.''')
        bot.register_next_step_handler (message, x)
    else :
        Nisk_id (message)

def Nisk_id (message) :
    with open ("Nisks.json", "r") as f :
        nisks = json.load (f)
    if message.text in nisks :
        with open (message.from_user.id + "txt", "w") as f :
            f.write (message.text)
        with open (message.text + "txt") as f :
            f.write (message.from_user.id)
        start_game (message)
    else :
        msg = bot.send_message(message.from_user.id, "Такого ника не существует!")
        bot.register_next_step_handler (message, x)

def start_game (message) :
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Да! ✅")
    btn2 = types.KeyboardButton("Нет! ❌")
    markup.add (btn1, btn2, row_width=1)
    with open (message.from_user.id + "txt", "r") as f :
        id_player2 = f.read ()
    with open ("Nisks.json", "r") :
        nisks = json.load (f)
    msg = bot.send_message(id_player2, "Игрок {} хочет с вами сыграть. А вы хотите?".format (nisks [message.from_user.id]), reply_markup= markup)
    bot.register_next_step_handler (msg, message, x2)

def x2 (msg, message) :
    if msg.text == "Да! ✅" :
        with open (msg.from_user.id + "txt", "r") as f :
            id_player1 = f.read ()
        msg = bot.send_message(id_player1, "Игрок согласен")
        game_start (message, msg)
    elif msg.text == "Нет! ❌" :
        msg = bot.send_message(id_player1, "Предложение отклонено!")
        bot.register_next_step_handler (message, x)

def game_start (message, msg) :
    player1_cards = []
    for i in range (5) :
        player1_cards [i] = [random.randint (0,20), random.randint (0,20)]
    with open (message.from_user.id + "json", "w") as f :
        json.dump (player1_cards, f, indent=4, ensure_ascii=False)

def check_internet_connection():
    import socket
    try:
        socket.create_connection(("api.telegram.org", 443), timeout=5)
        print("Соединение с Telegram API установлено")
        return True
    except OSError:
        print("Нет соединения с интернетом или Telegram API")
        return False
def check_internet_connection():
    import socket
    try:
        socket.create_connection(("api.telegram.org", 443), timeout=5)
        print("Соединение с Telegram API установлено")
        return True
    except OSError:
        print("Нет соединения с интернетом или Telegram API")
        return False

if __name__ == "__main__":
    while True:
        if check_internet_connection():
            try:
                print("Бот запущен и работает...")
                bot.polling(none_stop=True, interval=2, timeout=60)
            except Exception as e:
                print(f"Ошибка: {e}, перезапуск через 3 секунды")
                time.sleep(3)
        else :
            print("Нет интернет-соединения, проверка через 3 секунды")
            time.sleep (3)