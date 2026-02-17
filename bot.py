from flask import Flask, request
import telebot
import os
import traceback

app = Flask(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN, parse_mode=None)

WEBHOOK_PATH = f'/{TOKEN}'

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        user_text = message.text or '(пустое сообщение)'
        print(f"Получено от {message.from_user.id}: '{user_text}'")

        # Стабильный способ отправки
        sent = bot.send_message(
            chat_id=message.chat.id,
            text=f"Ты написал: {user_text} 🔥",
            parse_mode=None  # без форматирования, чтобы не глючило
        )

        print(f"Сообщение отправлено успешно, ID: {sent.message_id}")
    except telebot.apihelper.ApiTelegramException as api_err:
        print(f"Telegram API ошибка: {api_err.result_json}")
        print(traceback.format_exc())
    except Exception as e:
        print(f"Общая ошибка: {str(e)}")
        print(traceback.format_exc())

@app.route('/', methods=['GET'])
def home():
    return "Telegram bot is running! ✅", 200

@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return 'Invalid', 403

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)


