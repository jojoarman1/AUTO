import telebot
from telebot import types
import logging
import time

TOKEN = '7161762216:AAH_tQZnX-0S5rj43BKD_Yk6qhmSyyTd5Zk'
bot = telebot.TeleBot(TOKEN)
user_data = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton("Акции 🔥🎁")
    button2 = types.KeyboardButton("⚙️ Подбор автозапчастей")
    button4 = types.KeyboardButton("📞 Контакты")
    keyboard.add(button1, button2, button4)
    bot.send_message(message.chat.id, "Привет! Я бот для поиска автозапчастей. Что вас интересует?", reply_markup=keyboard)

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
    # Инициализируем хранилище данных пользователя для этого шага
    user_data[message.chat.id] = {"VIN код": None}
    # Устанавливаем следующий шаг в обработке
    bot.register_next_step_handler(message, handle_vin)

# Функция для обработки введенного VIN кода
def handle_vin(message):
    # Сохраняем VIN код в user_data
    user_data[message.chat.id]["VIN код"] = message.text
    # Запрашиваем номер телефона
    bot.send_message(message.chat.id, "Пожалуйста, укажите Ваш номер телефона:")
    # Устанавливаем следующий шаг в обработке
    bot.register_next_step_handler(message, handle_phone_number)

# Обработчик ответа на вопрос о номере телефона
def handle_phone_number(message):
    # Убеждаемся, что значение для ключа "Номер телефона" было установлено
    if user_data.get(message.chat.id) and user_data[message.chat.id].get("Номер телефона") is None:
        # Сохраняем ответ пользователя
        user_data[message.chat.id]["Номер телефона"] = message.text
        # Переходим к запросу списка необходимых запчастей
        bot.send_message(message.chat.id, "Напишите список необходимых запчастей ⚙️ (одним сообщением):")
        # Устанавливаем следующий шаг в обработке
        bot.register_next_step_handler(message, handle_parts_list)

# Обработчик кнопки "Нет 👎"
@bot.message_handler(func=lambda message: message.text == "Нет 👎")
def handle_no(message):
    # Отправляем сообщение с запросом о марке автомобиля
    bot.send_message(message.chat.id, "Для подбора запчастей нужна информация о машине:\n1. Марка Вашего авто🚗?")
    # Добавляем ответ пользователя в словарь
    user_data[message.chat.id] = {"Марка": None}
    # Устанавливаем следующий шаг в обработке
    bot.register_next_step_handler(message, handle_brand)

# Обработчик ответа на вопрос о марке автомобиля
def handle_brand(message):
    # Убеждаемся, что значение для ключа "Марка" было установлено
    if user_data.get(message.chat.id) and user_data[message.chat.id].get("Марка") is None:
        # Сохраняем ответ пользователя
        user_data[message.chat.id]["Марка"] = message.text
        # Запрашиваем модель автомобиля
        bot.send_message(message.chat.id, "2. Модель🚗?")
        # Устанавливаем следующий шаг в обработке
        bot.register_next_step_handler(message, handle_model)

# Обработчик ответа на вопрос о модели автомобиля
def handle_model(message):
    # Убеждаемся, что значение для ключа "Модель" было установлено
    if user_data.get(message.chat.id) and user_data[message.chat.id].get("Модель") is None:
        # Сохраняем ответ пользователя
        user_data[message.chat.id]["Модель"] = message.text
        # Запрашиваем год автомобиля
        bot.send_message(message.chat.id, "3. Год выпуска Вашего авто🚗?")
        # Устанавливаем следующий шаг в обработке
        bot.register_next_step_handler(message, handle_year)

# Обработчик ответа на вопрос о годе выпуска автомобиля
def handle_year(message):
    # Убеждаемся, что значение для ключа "Год выпуска" было установлено
    if user_data.get(message.chat.id) and user_data[message.chat.id].get("Год выпуска") is None:
        # Сохраняем ответ пользователя
        user_data[message.chat.id]["Год выпуска"] = message.text
        # Запрашиваем объем двигателя
        bot.send_message(message.chat.id, "4. Объем двигателя Вашего авто🚗? (в литрах)")
        # Устанавливаем следующий шаг в обработке
        bot.register_next_step_handler(message, handle_engine_capacity)

# Обработчик ответа на вопрос об объеме двигателя
def handle_engine_capacity(message):
    # Убеждаемся, что значение для ключа "Объем двигателя" было установлено
    if user_data.get(message.chat.id) and user_data[message.chat.id].get("Объем двигателя") is None:
        # Сохраняем ответ пользователя
        user_data[message.chat.id]["Объем двигателя"] = message.text
        # Запрашиваем номер телефона
        bot.send_message(message.chat.id, "5. Пожалуйста, укажите Ваш номер телефона на котором установлен Телеграм:")
        # Устанавливаем следующий шаг в обработке
        bot.register_next_step_handler(message, handle_phone_number)

# Обработчик ответа на вопрос о номере телефона
def handle_phone_number(message):
    # Убеждаемся, что значение для ключа "Номер телефона" было установлено
    if user_data.get(message.chat.id) and user_data[message.chat.id].get("Номер телефона") is None:
        # Сохраняем ответ пользователя
        user_data[message.chat.id]["Номер телефона"] = message.text
        # Запрашиваем список необходимых запчастей
        bot.send_message(message.chat.id, "Напишите список необходимых запчастей ⚙️ (одним сообщением):")
        # Устанавливаем следующий шаг в обработке
        bot.register_next_step_handler(message, handle_parts_list)

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
        chat_id = '735291377'  # Указываем chat_id чата
        bot.send_message(chat_id, formatted_info, parse_mode="HTML")  # Отправляем сообщение в указанный чат

        # Отправляем ссылку
        bot.send_message(message.chat.id, "Напишите сюда: [Avtozapchel](https://t.me/avtozapchel)", parse_mode="Markdown")

        # Добавляем кнопку "Выход в меню"
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_exit = types.KeyboardButton("Выход в меню")
        keyboard.add(button_exit)
        bot.send_message(message.chat.id, "Вскоре наши менеджеры свяжутся с Вами!\n\nЕсли вам не ответили,то причина это закрытый аккаунт , просьба написать напрямую менеджеру", reply_markup=keyboard)

        # Очищаем данные пользователя
        del user_data[message.chat.id]

# Обработчик кнопки "Выход в меню"
@bot.message_handler(func=lambda message: message.text == "Выход в меню")
def handle_exit_to_menu(message):
    handle_start(message)  # Вызываем функцию, которая показывает начальное меню

while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        logging.error(e)
        time.sleep(15)
