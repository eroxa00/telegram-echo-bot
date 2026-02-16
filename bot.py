from flask import Flask, request
import telebot
import os

app = Flask(__name__)

# Токен из переменной окружения Render (безопасно!)
TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    raise ValueError("BOT_TOKEN not set in environment variables!")

bot = telebot.TeleBot(TOKEN)

# Секретный путь для webhook (чтобы никто не угадал)
WEBHOOK_PATH = f'/{TOKEN}'

# Эхо — повторяет сообщение
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Для пинга Render (чтобы показать, что бот жив)
@app.route('/', methods=['GET'])
def home():
    return "Telegram bot is running!", 200

# Webhook — сюда приходят сообщения от Telegram
@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid request', 403

if __name__ == '__main__':
    # Только для локального теста (на Render не используется)
    app.run(host='0.0.0.0', port=5000)