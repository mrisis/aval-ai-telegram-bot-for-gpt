from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_join_channel_keyboard(channel_id):
    keyboard = [
        [InlineKeyboardButton(text="عضو شدن در کانال", url=f"https://t.me/{channel_id}")]
    ]

    return InlineKeyboardMarkup(keyboard)
