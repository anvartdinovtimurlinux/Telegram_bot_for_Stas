import telebot
from main import main


with open('token.txt', 'r', encoding='utf-8') as t:
    TOKEN = t.readline()
bot = telebot.TeleBot(TOKEN)
chat_id = ''

# Настройки прокси
# from telebot import apihelper
# ip = '163.172.189.32'
# port = '8811'
# apihelper.proxy = {
#   'https': f'http://{ip}:{port}'
# }


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Стас, я тупой бот, но уже кое что умею.'
                          'Напиши /help')
    global chat_id
    chat_id = message.chat.id


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, напиши /help?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Просто загрузи сюда файл в формате .xlsx.\n"
                                               "Кошельки должны быть перечислены в первом столбце. "
                                               "Заголовок столбцу не нужен.")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.message_handler(content_types=['document'])
def get_fuck_you(file):
    # print(file.document.file_id)  # строка для дебаггинга
    file_info = bot.get_file(file.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    bot.send_message(file.from_user.id, "Fuck the System!")
    bot.send_message(file.from_user.id, "Сервер обрабатывает запрос. возможно займет минуту - две")
    with open('wallets.xlsx', 'wb') as new_file:
        new_file.write(downloaded_file)

    main('wallets.xlsx')

    doc = open('result.xlsx', 'rb')
    bot.send_document(chat_id, doc)


bot.polling(none_stop=True, interval=1)
