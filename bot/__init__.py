import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)



class Config_ENV(object):
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH")

    AUTH_CHAT = {int(x) for x in os.environ.get("AUTH_CHAT", "").split()}
    ADMINS = {int(x) for x in os.environ.get("ADMINS", "").split()}
    LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID", 12345))
    ALLOW_DUMP = bool(os.environ.get("ALLOW_DUMP", False))

    WORK_DIR = os.environ.get("WORK_DIR", "./bot/")
    DOWNLOADS_FOLDER = os.environ.get("DOWNLOADS_FOLDER", "DOWNLOADS")
    DOWNLOAD_BASE_DIR = WORK_DIR + DOWNLOADS_FOLDER

    STATUS_UPDATE_INTERVAL = int(os.environ.get("STATUS_UPDATE_INTERVAL", 6))
    DEFAULT_SS_GEN_LIM = int(os.environ.get("DEFAULT_SS_GEN_LIM", 8))

    BOT_USERNAME = os.environ.get("BOT_USERNAME", "")
    if BOT_USERNAME.startswith("@"):
        BOT_USERNAME = BOT_USERNAME[1:]
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "")

    GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", '/app/.apt/usr/bin/google-chrome')
    CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH", '/app/.chromedriver/bin/chromedriver')
    BOT_LANGUAGE = os.environ.get("BOT_LANGUAGE", "EN")
    DATABASE_URL = os.environ.get("DATABASE_URL", "")
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 128))




class Config_NON_ENV(object):
    TG_BOT_TOKEN = ""
    APP_ID = 12345
    API_HASH = ""

    AUTH_CHAT = set()
    ADMINS = set()
    LOG_CHANNEL_ID = 12345
    ALLOW_DUMP = False

    WORK_DIR = "./bot/"
    DOWNLOADS_FOLDER = "DOWNLOADS"
    DOWNLOAD_BASE_DIR = WORK_DIR + DOWNLOADS_FOLDER

    STATUS_UPDATE_INTERVAL = 6
    DEFAULT_SS_GEN_LIM = 8

    BOT_USERNAME = ""
    BOT_USERNAME = BOT_USERNAME.removeprefix("@")
    OWNER_USERNAME = ""

    GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google-chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    BOT_LANGUAGE = "EN"
    DATABASE_URL = ""
    CHUNK_SIZE = 128


Config = Config_ENV if os.environ.get("ENV") else Config_NON_ENV
bot = Config.BOT_USERNAME
class CMD(object):
    START = ["start", f"start@{bot}"]
    HELP = ["help", f"help@{bot}"]
    SETTINGS = ["settings", f"settings@{bot}"]
    UPLOAD = ["upload", f"upload@{bot}"]
    INDEX_UPLOAD = ["index_upload", f"index_upload@{bot}"]
    SCREENSHOTS  = ["screenshots", f"screenshots@{bot}"]
    SHELL = ["shell", f"shell@{bot}"]
    YTDL =  ["ytdl", f"ytdl@{bot}"]
    RENAME = ["rename", f"rename@{bot}"]