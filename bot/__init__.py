import os
import logging
from bot.helpers.utils.bot_cmd import BOT_CMD

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

CMD = BOT_CMD

class Config(object):
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH")

    AUTH_CHAT = set(int(x) for x in os.environ.get("AUTH_CHAT", "").split())
    DOWNLOAD_LOCATION = "./DOWNLOADS"

    BOT_USERNAME = os.environ.get("BOT_USERNAME", "")
    if BOT_USERNAME.startswith("@"):
        BOT_USERNAME = BOT_USERNAME[1:]
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "")

    GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", '/app/.apt/usr/bin/google-chrome')
    CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH", '/app/.chromedriver/bin/chromedriver')

    BOT_LANGUAGE = os.environ.get("BOT_LANGUAGE", "EN")

    DATABASE_URL = os.environ.get("DATABASE_URL", "")

CMD = BOT_CMD
