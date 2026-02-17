from flask import Flask, request
import telebot
import os
import traceback

app = Flask(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN, parse_mode=None)

WEBHOOK_PATH = f'/{TOKEN}'

# ==================== ОБРАБОТЧИК СООБЩЕНИЙ ====================
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        print(f"✅ Получено сообщение от {message.from_user.username or message.from_user.id}: {message.text}")
        
        response = bot.reply_to(message, message.text)
        
        print(f"✅ Ответ отправлен: {message.text}")
        return response
    except Exception as e:
        print(f"❌ ОШИБКА при отправке ответа: {e}")
        print(traceback.format_exc())
        # Отправляем пользователю сообщение об ошибке (чтобы ты видел)
        try:
            bot.reply_to(message, "Извини, произошла ошибка на сервере 😔 Попробуй позже.")
        except:
            pass

# ==================== ДЛЯ ПИНГА ====================
@app.route('/', methods=['GET'])
def home():
    return "Telegram bot is running! ✅", 200

# ==================== WEBHOOK ====================
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