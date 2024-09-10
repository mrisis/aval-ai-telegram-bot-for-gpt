import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# توکن بات تلگرام و کلید API چت جی‌پی‌تی
TELEGRAM_TOKEN = '7305555261:AAEPqi2FNtSIihZSjF7WtgQNeNFfgIBFDpA'
OPENAI_API_KEY = 'aa-rUEgSkkInYIUG0GLJ5UVrbUzqA7I9QAktmoO5fSqIC9Hwym1'
OPENAI_API_URL = 'https://api.avalai.ir/v1/chat/completions'

# راه‌اندازی لاگینگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# تابع برای پاسخ به پیام‌ها
def chat_with_gpt(message: str) -> str:
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    data = {
        'model': 'gpt-3.5-turbo',  # یا مدل دیگر
        'messages': [{'role': 'user', 'content': message}],
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    print('-------------')
    print(response)


    # بررسی وضعیت پاسخ API
    if response.status_code != 200:
        logger.error(f'Error from API: {response.status_code} - {response.text}')
        return "خطایی رخ داد. لطفاً بعداً دوباره امتحان کنید."

    try:
        response_json = response.json()
        return response_json['choices'][0]['message']['content']
    except ValueError:
        logger.error('Invalid JSON received from API')
        return "پاسخ دریافتی از API معتبر نیست."
    except (KeyError, IndexError):
        logger.error('Unexpected JSON structure from API')
        return "ساختار پاسخ API قابل پردازش نیست."


# تابع برای پاسخ به پیام‌های دریافتی
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    logger.info(f'Received message: {user_message}')
    response_message = chat_with_gpt(user_message)
    await update.message.reply_text(response_message)


# تابع اصلی برای راه‌اندازی بات
def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # هندلر برای پیام‌های متنی
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # شروع بات
    application.run_polling()


if __name__ == '__main__':
    main()
