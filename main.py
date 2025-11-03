import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('')

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('telegram.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT,
                   userpass TEXT
                   
                   )''')

    conn.commit()
    cursor.close()
    conn.close()
    
    bot.send_message(message.chat.id, 'Привет, сейчас я тебя зарегистрирую!\nВведите ваше имя:')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    name = message.text.strip()

    bot.send_message(message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(message, user_pass, name)

def user_pass(message, name):
    password = message.text.strip()

    conn = sqlite3.connect('telegram.db')
    cur = conn.cursor()

    cur.execute('''INSERT INTO Users (username, userpass) VALUES (?, ?)''', (name, password))
    conn.commit()
    
    cur.execute('''SELECT * FROM Users''')
    items = cur.fetchall()

    text = 'Вот все данные из таблицы:\n'
    
    for item in items:
        text += (f"ID: {item[0]}, Имя: {item[1]}, Пароль: {item[2]}\n")

    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('Вывести все пользователей', callback_data='database')
    markup.row(bt1)

    bot.send_message(message.chat.id,'Успешно зарегистрирован!', reply_markup=markup)
    cur.close()
    conn.close()

@bot.callback_query_handler(func= lambda call: True)
def callback(call):
    conn = sqlite3.connect('telegram.db')
    cur = conn.cursor()
    cur.execute('''SELECT * FROM Users''')
    items = cur.fetchall()

    text = 'Вот все данные из таблицы:\n'
    
    for item in items:
        text += (f"ID: {item[0]}, Имя: {item[1]}, Пароль: {item[2]}\n")
    bot.send_message(call.message.chat.id, text)
    


bot.polling(none_stop=True)