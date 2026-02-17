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
        print(f"Получено от {message.from_user.id}: {message.text}")
        
        bot.reply_to(message, f"Ты сказал: {message.text}")
        
        print("Ответ отправлен успешно")
    except Exception as e:
        print(f"Ошибка при reply_to: {str(e)}")
        print(traceback.format_exc())
        try:
            bot.send_message(message.chat.id, "Извини, ошибка на сервере 😔")
        except:
            pass

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
