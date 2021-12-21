from bot.helpers.translations import tr_en
from bot import Config

lang = None

if Config.BOT_LANGUAGE == "EN":
    lang = tr_en.EN
