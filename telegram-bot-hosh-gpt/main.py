import logging
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler
from bot.handlers import handle_message, start
from bot.config import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    application = ApplicationBuilder().token(settings.telegram_token).build()

    # /start & create new user
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()


if __name__ == '__main__':
    main()
