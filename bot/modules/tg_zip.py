from bot import Config, LOGGER, CMD
from pyrogram import Client, filters
from bot.helpers.translations import lang

@Client.on_message(filters.command([CMD.UPLOAD, f"{CMD.UPLOAD}@{Config.BOT_USERNAME}"]))
async def zip_tg_files(bot, update):
    