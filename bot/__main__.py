import os
import logging
from bot import Config
from pyrogram import Client

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

if __name__ == "__main__":
    if not os.path.isdir(Config.DOWNLOAD_BASE_DIR):
        os.makedirs(Config.DOWNLOAD_BASE_DIR)
    plugins = dict(
        root="bot/modules"
    )
    app = Client(
        "UseLessMediaBot",
        bot_token=Config.TG_BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        plugins=plugins,
        workdir=Config.WORK_DIR
    )
    LOGGER.info("Bot Started......Now Enjoy")
    app.run()
    LOGGER.info('Bot Stopped ! Bye..........')