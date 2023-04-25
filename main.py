import telebot
from telebot import types

bot = telebot.TeleBot("2013984642:AAENYF3qOYFbU-i0wFqO9neNLUu4RNNu7fk")
TO_CHAT_ID = 869656178  # Не забудь подставить нужный id!
poj = open('doc/pojar.txt', 'rb')
photo = open('pict/edds.jpg', 'rb')
dtp_b = open('pict/algoritm/dtp(bez).png', 'rb')

'''
# переслать мне сообщение
@bot.message_handler(content_types=['text'])
def all_messages(message):
    bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
'''

# хелло
@bot.message_handler(commands=['hi', 'Hi'])
def send_hello(message):
    bot.send_message(message.chat.id, "Hello, world!")
    print(message.text, message.from_user.first_name, message.from_user.id)


# отправить фотку
@bot.message_handler(commands=['send'])
def send(message):

    bot.send_photo(message.chat.id, photo)
    bot.reply_to(message, "Лови фотку")


# отправить список команд
@bot.message_handler(commands=['start'], content_types=['text'])
def commands(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    if message.text.lower() == '/start':

        # keyboard
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Ртуть")
        item2 = types.KeyboardButton("Алгоритмы")
        item3 = types.KeyboardButton("❓ Что ты умеешь?")
        item4 = types.KeyboardButton("Справочник Дежурных служб")

        markup.add(item1, item2, item3, item4)

        bot.send_message(message.chat.id,
             "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом. \n Напиши мне Привет и я добавлю тебя в Базу данных".format(
                 message.from_user, bot.get_me()),
             parse_mode='html', reply_markup=markup)


#начальные кнопки клавиатуры под сообщением
@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Ртуть':
            bot.send_photo(message.chat.id, dtp_b)

        elif message.text == 'Алгоритмы':

            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("Пожарная", callback_data='good')
            item2 = types.InlineKeyboardButton("Полиция", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Что нужно?', reply_markup=markup)

        elif message.text == 'Справочник Дежурных служб':
            bot.send_message(message.chat.id, 'Справочные телефоны:')
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("Пожарная", callback_data='good')
            item2 = types.InlineKeyboardButton("Полиция", callback_data='bad')
            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Что нужно?', reply_markup=markup)

        elif message.text == '❓ Что ты умеешь?':
            bot.send_message(message.chat.id,
                             'Вот команды, которые я умею читать:'
                             # '\n /start - стартовое приветствие'
                             '\n/help - помощь по командам '
                             '\n/send - отправить фотографию '
                             '\n/check - проверка статуса пользователя')

        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')

    print(message.text, message.from_user.first_name, message.from_user.id)  # отсы


#ответ на насторение
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):



    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Держи алгоритм пожарной')
                bot.send_document(call.message.chat.id, poj)
                bot.send_document(call.message.chat.id, "FILEID")
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Держи алгоритм полиции')
                bot.send_photo(call.message.chat.id, photo)



            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Держи",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ЭТО УВЕДОМЛЕНИЕ!)")

    except Exception as e:
        print(repr(e))

# bot.infinity_polling()
bot.polling(none_stop=True)
