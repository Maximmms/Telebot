import random
import telebot

token = "7766217558:AAHeBy4VY7wnm-oznPl2exc6epWnXnPJ3j4"

bot = telebot.TeleBot(token)

RANDOM_TASKS = {"f", "d", "r", "u", "w"}

HELP = """
/help - Напечатать справку по программе.
/add - добавить задачу в список
/show - напечатать все добавленные задачи
/print - напечатать все задачи на несколько дат
/random - добавлять случайную задачу"""

tasks = {}

def add_todo(date, task):
    if date in tasks:
        tasks[date].append(task)
    else:
        tasks[date]=[]
        tasks[date].append(task)


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=["add"])
def add(message):
    command = message.text.split(maxsplit=2)
    date = command[1].lower()
    task = command[2]
    if len(task) < 3:
        bot.send_message(message.chat.id, "!!!Задача не может быть короче 3 символов!!!")
    else:
        add_todo(date, task)
        text = "Задача " + task + " добавлена на дату " + date
        bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["random"])
def random_add(message):
    date = "cегодня"
    task = random.choice(RANDOM_TASKS)
    add_todo(date, task)
    text = "Задача " + task + " добавлена на дату " + date
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["show"])
def show(message):
    command = message.text.split(maxsplit=1)
    date = command[1].lower()
    text = ""
    if date in tasks:
        text = date.upper() + "\n"
        for task in tasks[date]:
            text = text + "[] " + task + "\n"
    else:
        text = "Задач на эту дату нет"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["print"])
def print_(message):
    command = message.text.split()
    dates = command[1:]
    for date in dates:
        if date in tasks:
            bot.send_message(message.chat.id, f"На дату {date} установлены задачи: {', '.join(tasks[date])}")
        else:
            bot.send_message(message.chat.id, f"На дату {date} задач нет!")

@bot.message_handler(content_types=["text"])
def echo(message):
    bot.send_message(message.chat.id, message.text)

bot.polling(none_stop=True)