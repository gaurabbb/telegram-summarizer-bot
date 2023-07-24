import logging
from processor.checks import *
from processor.preprocess import *
from processor.summarizer import *
from telegram import __version__ as TG_VER
import json


message_count = 0
user_ids = set()


with open('config.json', 'r') as f:
    config = json.load(f)
tg_token = config['tg_token']



try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )


from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf'''Hi {user.mention_html()}Welcome to our Telegram bot - Text Summarizer! Get concise summaries for any text instantly. Try it now! 📚🤖
''',
        reply_markup=ForceReply(selective=True),
    )


async def recieve(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Recieve messages and send for checks."""

    global message_count
    global user_ids
    message_count += 1
    user_ids.add(update.message.from_user.id)

    if message_count % 10 == 0:
        logger.info(f'Messages handled: {message_count}')
        logger.info(f'Unique users: {len(user_ids)}')

    user_input = update.message.text
    await update.message.reply_text("🤖 Processing your input...")
    await checks(user_input, update)

def error(update: Update, context):
    """Log errors caused by updates."""
    logger.warning(f'Update {update} caused error {context.error}')

async def send(message, update):
    await update.message.reply_text(message)


def main() -> None:
    #BOTSTART
    application = Application.builder().token(tg_token).build()

    application.add_handler(CommandHandler("Start", start))
  
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recieve))
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()