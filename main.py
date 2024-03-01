import telebot
from telebot import types
import logging
import time

# Указываем токен вашего бота
TOKEN = '7161762216:AAH_tQZnX-0S5rj43BKD_Yk6qhmSyyTd5Zk'

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения данных о машине
user_data = {}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Создаем клавиатуру с кнопками
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton("Акции 🔥🎁")
    button2 = types.KeyboardButton("⚙️ Подбор автозапчастей")
    button4 = types.KeyboardButton("📞 Контакты")
    keyboard.add(button1, button2, button4)

    # Отправляем сообщение с клавиатурой
    bot.send_message(message.chat.id, "Привет! Я бот для поиска автозапчастей. Что вас интересует?",
                     reply_markup=keyboard)

# Обработчик кнопки "Акции 🔥🎁"
@bot.message_handler(func=lambda message: message.text == "Акции 🔥🎁")
def handle_promotions(message):
    # Отправляем текст с акциями
    bot.send_message(message.chat.id, "Посмотрите наши актуальные акции:", parse_mode="HTML")

    # Отправляем фотографии с акциями
    with open('260.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption="PEMCО 10W-40 SN/CH-44л полусинт Всего 1700 руб.")
    with open('furo.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption="Furo OPTI 10W40 (4,5L) масло моторное Всего 1150 руб.")
    with open('korson.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption="KORSON 10W-40 SEMI SYNTHETIC A3/B3 4л Всего 2000 руб.")
    with open('standart.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption="ЛУКОЙЛ 10W40 Стандарт (4L) Всего 1050 руб.")

# Обработчик кнопки "📞 Контакты"
@bot.message_handler(func=lambda message: message.text == "📞 Контакты")
def handle_contacts(message):
    # Отправляем контактную информацию
    bot.send_message(message.chat.id, "Адрес: Механическая 14/3\nНомер: +79127916684")


# Обработчик кнопки "⚙️ Подбор автозапчастей"
@bot.message_handler(func=lambda message: message.text == "⚙️ Подбор автозапчастей")
def handle_auto_selection(message):
    # Создаем клавиатуру с кнопками "Да" и "Нет"
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_yes = types.KeyboardButton("Да 👍")
    button_no = types.KeyboardButton("Нет 👎")
    keyboard.add(button_yes, button_no)

    # Отправляем сообщение с вопросом и клавиатурой
    bot.send_message(message.chat.id, "У вас есть VIN код авто? (номер кузова)", reply_markup=keyboard)


# Обработчик кнопки "Да 👍"
@bot.message_handler(func=lambda message: message.text == "Да 👍")
def handle_yes(message):
    # Отправляем сообщение с запросом VIN кода
    bot.send_message(message.chat.id, "Введите VIN код вашего авто🚗:")
    # Добавляем ответ пользователя в словарь
    user_data[message.chat.id] = {"VIN код": None}

    # Устанавливаем следующий шаг в обработке
    bot.register_next_step_handler(message, ask_for_name)


# Функция для запроса имени пользователя
def ask_for_name(message):
    # Сохраняем VIN код в user_data
    user_data[message.chat.id]["VIN код"] = message.text

    # Отправляем запрос имени
    bot.send_message(message.chat.id, "Сначала давайте познакомимся, как Вас зовут? 😉")
    # Устанавливаем следующий шаг в обработке
    bot.register_next_step_handler(message, handle_name_input)


# Функция для обработки введенного имени пользователя
def handle_name_input(message):
    # Сохраняем имя пользователя в user_data
    user_data[message.chat.id]["Имя"] = message.text

    # Отправляем запрос о марке автомобиля
    bot.send_message(message.chat.id, "Для подбора запчастей нужна информация о машине:\n1. Марка Вашего авто🚗?")
    # Устанавливаем следующий шаг в обработке
    bot.register_next_step_handler(message, handle_brand)


# Обработчик кнопки "Нет 👎"
@bot.message_handler(func=lambda message: message.text == "Нет 👎")
def handle_no(message):
    # Отправляем сообщение с запросом о марке автомобиля
    bot.send_message(message.chat.id, "Для подбора запчастей нужна информация о машине:\n1. Марка Вашего авто🚗?")
    # Добавляем ответ пользователя в словарь
    user_data[message.chat.id] = {"Марка": None}


# Обработчик ответа на вопрос о марке автомобиля
@bot.message_handler(func=lambda message: user_data.get(message.chat.id) and user_data[message.chat.id].get("Марка") is None)
def handle_brand(message):
    # Убеждаемся, что значение для ключа "Марка" было установлено
    if user_data.get(message.chat.id) and user_data[message.chat.id].get("Марка") is None:
        # Сохраняем ответ пользователя
        user_data[message.chat.id]["Марка"] = message.text
        # Запрашиваем модель автомобиля
        bot.send_message(message.chat.id, "2. Модель🚗?")


# Обработчик ответа на вопрос о модели автомобиля
@bot.message_handler(func=lambda message: user_data.get(message.chat.id) and user_data[message.chat.id].get("Модель") is None)
def handle_model(message):
    # Убеждаемся, что значение для ключа "Модель" было установлено
    if user_data.get(message.chat.id) and user_data[message.chat.id].get("Модель") is None:
        # Сохраняем ответ пользователя
        user_data[message.chat.id]["Модель"] = message.text
        # Запрашиваем список необходимых запчастей
        bot.send_message(message.chat.id, "Напишите список необходимых запчастей ⚙️ (одним сообщением):")


# Обработчик ответа на список необходимых запчастей
@bot.message_handler(func=lambda message: user_data.get(message.chat.id) and user_data[message.chat.id].get("Список запчастей") is None)
def handle_parts_list(message):
    # Убеждаемся, что значение для ключа "Список_запчастей" было установлено
    if user_data.get(message.chat.id) and user_data[message.chat.id].get("Список запчастей") is None:
        # Сохраняем список необходимых запчастей
        user_data[message.chat.id]["Список запчастей"] = message.text

        # Подготовка данных в красивом формате
        user_info = user_data[message.chat.id]  # Получаем информацию о пользователе
        formatted_info = "<b>Информация о пользователе:</b>\n"
        for key, value in user_info.items():
            if key == "Марка" or key == "Модель":
                formatted_info += f"<b>{key} автомобиля:</b> {value}\n"
            else:
                formatted_info += f"<b>{key}:</b> {value}\n"

        # Получаем username пользователя
        user = bot.get_chat_member(message.chat.id, message.from_user.id).user
        if user.username:
            user_link = f'<a href="https://t.me/{user.username}">{user.first_name}</a>'
            formatted_info += f"\n<b>Профиль пользователя:</b> {user_link}"

        # После сбора всей необходимой информации
        # Отправляем информацию в указанный чат
        chat_id = '7089777142'  # Указываем chat_id чата
        bot.send_message(chat_id, formatted_info, parse_mode="HTML")  # Отправляем сообщение в указанный чат

        # Отправляем ссылку
        bot.send_message(message.chat.id, "Напишите сюда: [Avtozapchel](https://t.me/avtozapchel)", parse_mode="Markdown")


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(e)
        time.sleep(15)
