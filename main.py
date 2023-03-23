import telebot

from confic import *
from extensions import APIException, Convertor

bot = telebot.TeleBot(TOKEN)


# декораторы, отлавливающие команды (start, help, currency) и обработчики.
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = f'здравствуйте, {message.chat.username}\n\nПравилами ввода: /help\n' \
           'Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Через пробел введите три параметра:\n\n<переводимая валюта>\n<в какую валюту перевести>\n' \
           '<количество переводимой валюты>'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for key in exchanges.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


# декоратор отлавливающий ввод от пользователя и обработчик.
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        accept = message.text.lower().split()
        if len(accept) != 3:
            raise APIException('Не верное количество параметров.')

        sym, base, amount = accept
        total_base = Convertor.get_price(sym, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {sym} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()

