from bot import CMD, Config
from pyrogram import Client, filters
from bot.helpers.utils.buttons import *
from bot.helpers.translations import lang
from bot.helpers.database.database import check_user, fetch_media_details

@Client.on_message(filters.command([CMD.SETTINGS, f"{CMD.SETTINGS}@{Config.BOT_USERNAME}"]))
async def settings(bot, update):
    await check_user(update.from_user.id)
    video_type, photo_type = await fetch__media_details(update.from_user.id)
    first_name = update.from_user.first_name
    buttons = await settings_buttons(video_type, photo_type)
    await bot.send_message(
        chat_id=update.chat.id,
        text=lang.SETTINGS_TEXT.format(first_name),
        reply_markup=buttons,
        reply_to_message_id=update.message_id
    )