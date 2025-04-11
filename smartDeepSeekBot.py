import re
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "TELEGRAM_TOKEN"
DEEPSEEK_API_KEY = "DEEPSEEK_API_KEY"
API_URL = "https://api.deepseek.com/v1/chat/completions"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добрый день! Чем вам помочь?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    print(user_input)
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": user_input}]
        }
        response = requests.post(API_URL, json=data, headers=headers)
        response_data = response.json()

        answer = response_data["choices"][0]["message"]["content"]
        answer = re.sub(r'<[^>]*>', '', answer)
        answer = re.sub(r'[*_#`]', '', answer)
        answer = re.sub(r'[ \t]+$', '', answer, flags=re.MULTILINE)

        print(answer)
        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")

if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()