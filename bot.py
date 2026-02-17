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
        print(f"Получено сообщение от {message.from_user.id}: '{message.text}'")
        
        # Пытаемся отправить через send_message (стабильнее, чем reply_to)
        sent_msg = bot.send_message(
            chat_id=message.chat.id,
            text=f"Ты написал: {message.text or '(пусто)'} 🔥"
        )
        
        print(f"Ответ отправлен успешно, ID сообщения: {sent_msg.message_id}")
    except telebot.apihelper.ApiTelegramException as api_err:
        print(f"ApiTelegramException: {api_err.result_json}")
        print(traceback.format_exc())
        try:
            bot.send_message(message.chat.id, "Ошибка API Telegram 😔")
        except:
            pass
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

