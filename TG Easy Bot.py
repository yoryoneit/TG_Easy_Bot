import telebot as tb
from telebot import types


bot = tb.TeleBot('Insert your token here.')

name, last_name, age = '', '', 0


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "What's your name?")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, 'Write /reg')


def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "What's your last name?")
    bot.register_next_step_handler(message, get_last_name)


def get_last_name(message):
    global last_name
    last_name = message.text
    bot.send_message(message.from_user.id, 'How old are you?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    if age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Enter only numbers!')

    key = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text='Yes', callback_data='Yes')
    key.add(yes)
    no = types.InlineKeyboardButton(text='No', callback_data='No')
    key.add(no)

    question = f"Your name is {name}, " \
               f"\nyour last name is {last_name} " \
               f"\nand you're {age} years old, right?"

    bot.send_message(message.from_user.id, text=question, reply_markup=key)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'Yes':
        bot.send_message(call.message.chat.id, 'Nice to meet you!')
    elif call.data == 'No':
        bot.send_message(call.message.chat.id, "Let's do it again! Write /reg")


bot.polling(none_stop=True, interval=1)
