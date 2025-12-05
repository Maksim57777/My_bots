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
        json.dump (nisks, f, indent=4, ensure_ascii=False)
    msg = bot.send_message(message.from_user.id, "Ваш ник: {}.".format (user_nick))
    bot.register_next_step_handler (message, x)

def x (message) :
    if message.text == "/rules" :
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
        start_game (message)
    else :
        msg = bot.send_message(message.from_user.id, "Такого ника не существует!")
        bot.register_next_step_handler (message, x)

def start_game (message) :
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Да! ✅")
    btn2 = ypes.KeyboardButton("Нет! ❌")
    markup.add (btn1, btn2, row_width=1)
    with open (message.from_user.id + "txt", "r") as f :
        nisk_player2 = f.read ()
    with open ("Nisks.json", "r") :
        nisks = json.load (f)
    msg = bot.send_message(nisk_player2, "Игрок {} хочет с вами сыграть. А вы хотите?".format (nisks [message.from_user.id]), reply_markup= markup)

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
        else:
            print("Нет интернет-соединения, проверка через 3 секунды")
            time.sleep(3)
