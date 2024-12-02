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

def add_todo(date, task, *category):
    if date in tasks:
        tasks.setdefault(date.lower(), []).append((task, category))
    else:
        tasks[date]=[]
        tasks.setdefault(date.lower(), []).append((task, category))

def get_command(message):
    command = message.text.split(maxsplit=2)
    date = command[1].lower()
    task = command[2]
    if len(task) < 3:
        bot.send_message(message.chat.id, "!!!Задача не может быть короче 3 символов!!!")
    else:
        add_todo(date, task)
        text = "Задача " + task + " добавлена на дату " + date
        bot.send_message(message.chat.id, text)

def date_print(date,message):
    if date in tasks:
        task_ = ""
        bot.send_message(message.chat.id, f'На дату {date} запланированы задачи:')
        for task, category in tasks[date]:
            if category is not None:
                bot.send_message(message.chat.id, f'{task.upper()}: @{category[0]}')
            else:
                bot.send_message(message.chat.id, f'{task.upper()}')
    else:
        bot.send_message(message.chat.id, f'На дату {date} нет запланированных задач')

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=["add"])
def add(message):
    command = message.text.split(maxsplit=2)
    task = command[2].lower()
    if len(task) > 3:
        if '@' in task:
            task_parts = task.split('@')
            task = task_parts[0].strip()
            category = task_parts[1].strip() if len(task_parts) > 1 else None
            add_todo(command[1], task, category)
            bot.send_message(message.chat.id, f'Задача {task.upper()} добавлена на дату: {command[1]} в категорию - {category.upper()}')
        else:
            add_todo(command[1], task)
            bot.send_message(message.chat.id, f'Задача {task.upper()} добавлена на дату: {command[1]}')
    else:
        bot.send_message(message.chat.id, "!!!Задача не может быть короче 3 символов!!!")

@bot.message_handler(commands=["random"])
def random_add(message):
    date = "Сегодня"
    task = random.choice(RANDOM_TASKS)
    add_todo(date, task)
    text = "Задача " + task + " добавлена на дату " + date
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["show"])
def show(message):
    command = message.text.split(maxsplit=2)
    date = command[1].lower()
    date_print(date, message)

@bot.message_handler(commands=["print"])
def print_(message):
    command = message.text.split()
    dates = command[1:]
    for date in dates:
        date_print(date, message)

@bot.message_handler(content_types=["text"])
def echo(message):
    bot.send_message(message.chat.id, message.text)

bot.polling(none_stop=True)
