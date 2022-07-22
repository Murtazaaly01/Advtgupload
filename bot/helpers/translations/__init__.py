from bot.helpers.translations import tr_en
from bot import Config

lang = tr_en.EN if Config.BOT_LANGUAGE == "EN" else None
