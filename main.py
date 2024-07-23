import telebot
import datetime
import time
import threading
import random

bot = telebot.TeleBot('6827280483:AAHsl-FGn4FB4N5Na1U-5zrJojbw7WY29I4')

user_reminders = {}
user_reminder_texts = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, 'Привет! Я чат-бот, который будет напоминать тебе пить водичку! Используй команды /add_reminder, /remove_reminder и /edit_reminder_text для настройки.')
    if message.chat.id not in user_reminders:
        user_reminders[message.chat.id] = ['09:00', '14:00', '21:00']
    if message.chat.id not in user_reminder_texts:
        user_reminder_texts[message.chat.id] = "Напоминание - выпей стакан воды"
    reminder_thread = threading.Thread(target=send_reminders, args=(message.chat.id,))
    reminder_thread.start()

facts = [
    "Вода на Земле может быть старше самой Солнечной системы: Исследования показывают, что от 30% до 50% воды в наших океанах возможно присутствовала в межзвездном пространстве еще до формирования Солнечной системы около 4,6 миллиарда лет назад.",
    "Горячая вода замерзает быстрее холодной: Это явление известно как эффект Мпемба. Под определенными условиями горячая вода может замерзать быстрее, чем холодная, хотя ученые до сих пор полностью не разгадали механизм этого процесса.",
    "Больше воды в атмосфере, чем во всех реках мира: Объем водяного пара в атмосфере Земли в любой момент времени превышает объем воды во всех реках мира вместе взятых. Это подчеркивает важную роль атмосферы в гидрологическом цикле, перераспределяя воду по планете."
]

@bot.message_handler(commands=['fact'])
def send_random_fact(message):
    random_fact = random.choice(facts)
    bot.reply_to(message, f'Лови факт о воде: \n{random_fact}')

@bot.message_handler(commands=['add_reminder'])
def add_reminder(message):
    try:
        time_str = message.text.split()[1]
        datetime.datetime.strptime(time_str, '%H:%M')
        if message.chat.id in user_reminders:
            user_reminders[message.chat.id].append(time_str)
        else:
            user_reminders[message.chat.id] = [time_str]
        bot.reply_to(message, f'Напоминание на {time_str} добавлено.')
    except (IndexError, ValueError):
        bot.reply_to(message, 'Пожалуйста, укажите время в формате HH:MM. Пример: /add_reminder 15:30')

@bot.message_handler(commands=['remove_reminder'])
def remove_reminder(message):
    try:
        time_str = message.text.split()[1]
        if message.chat.id in user_reminders and time_str in user_reminders[message.chat.id]:
            user_reminders[message.chat.id].remove(time_str)
            bot.reply_to(message, f'Напоминание на {time_str} удалено.')
        else:
            bot.reply_to(message, 'Такого напоминания нет.')
    except IndexError:
        bot.reply_to(message, 'Пожалуйста, укажите время в формате HH:MM. Пример: /remove_reminder 15:30')

@bot.message_handler(commands=['edit_reminder_text'])
def edit_reminder_text(message):
    new_text = message.text[len('/edit_reminder_text '):]
    if new_text:
        user_reminder_texts[message.chat.id] = new_text
        bot.reply_to(message, 'Текст напоминания обновлен.')
    else:
        bot.reply_to(message, 'Пожалуйста, укажите новый текст напоминания. Пример: /edit_reminder_text Не забудь выпить воды!')

# Функция автоматического напоминания
def send_reminders(chat_id):
    while True:
        now = datetime.datetime.now().strftime('%H:%M')
        if chat_id in user_reminders and now in user_reminders[chat_id]:
            reminder_text = user_reminder_texts.get(chat_id, "Напоминание - выпей стакан воды")
            bot.send_message(chat_id, reminder_text)
            time.sleep(61)  # Ждем 61 секунду, чтобы избежать повторных отправок в эту же минуту
        time.sleep(1)

bot.polling(none_stop=True)