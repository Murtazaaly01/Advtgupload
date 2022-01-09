from bot import CMD
from pyrogram import Client, filters
from bot.helpers.translations import lang
from bot.helpers.database.database import check_user, fetch_media_details
from bot.helpers.utils.buttons import help_buttons, start_buttons, settings_buttons

@Client.on_message(filters.command(CMD.START))
async def start(bot, update):
    user_id = update.from_user.id
    await check_user(user_id)
    await bot.send_message(
        chat_id=update.chat.id,
        text=lang.START_TEXT.format(update.from_user.first_name),
        reply_markup=await start_buttons(user_id),
        reply_to_message_id=update.message_id
    )

@Client.on_message(filters.command(CMD.HELP))
async def help(bot, update):
    user_id = update.from_user.id
    await check_user(user_id)
    await bot.send_message(
        chat_id=update.chat.id,
        text=lang.HELP_TEXT.format(update.from_user.first_name),
        reply_markup=await help_buttons(user_id),
        reply_to_message_id=update.message_id
    )

@Client.on_message(filters.command(CMD.SETTINGS))
async def settings(bot, update):
    user_id = update.from_user.id
    await check_user(user_id)
    video_type, photo_type = await fetch_media_details(user_id)
    first_name = update.from_user.first_name
    await bot.send_message(
        chat_id=update.chat.id,
        text=lang.SETTINGS_TEXT.format(first_name),
        reply_markup=await settings_buttons(video_type, photo_type, user_id),
        reply_to_message_id=update.message_id
    )

