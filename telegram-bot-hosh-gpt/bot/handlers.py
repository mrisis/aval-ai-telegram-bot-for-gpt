import logging
import requests
from telegram import Update
from telegram.ext import CallbackContext, ContextTypes
from .models.user_model import User
from .crud.user_crud import UserCRUD
from .config import settings
from .keyboards.inline_keyboards import get_join_channel_keyboard

logger = logging.getLogger(__name__)


def chat_with_gpt(message: str) -> str:
    headers = {
        'Authorization': f'Bearer {settings.aval_ai_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': message}],
    }
    response = requests.post(settings.aval_ai_url, headers=headers, json=data)

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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome! How can I assist you today?')
    user = update.message
    if user.from_user.username:
        new_user = User(username=user.from_user.username, chat_id=user.from_user.id)
    else:
        new_user = User(username=f'{user.from_user.first_name}-{user.from_user.last_name}', chat_id=user.from_user.id)
    UserCRUD.create(new_user)
    logger.info(f'New user registered: {new_user.username}')

    channel_id = settings.channel_id
    await update.message.reply_text(
        "خوش آمدید! برای استفاده از این ربات ابتدا باید درکانال ما عضو شوید .",
        reply_markup=get_join_channel_keyboard(channel_id=channel_id)
    )


async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    logger.info(f'Received message: {user_message}')
    response_message = chat_with_gpt(user_message)
    await update.message.reply_text(response_message)
