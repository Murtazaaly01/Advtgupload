from bot import Config, CMD
from pyrogram import Client, filters
from bot.helpers.translations import lang
from bot.helpers.utils.buttons import help_buttons, start_buttons, settings_buttons
from bot.helpers.database.database import check_user, fetch_media_details

@Client.on_message(filters.command([CMD.START, f"{CMD.START}@{Config.BOT_USERNAME}"]))
async def start(bot, update):
    if update.chat.id not in Config.AUTH_CHAT:
        await update.reply_text(
            "Bot only usable in the Authorized Chat"
        )
        return
    await check_user(update.from_user.id)
    buttons = await start_buttons()
    await bot.send_message(
        chat_id=update.chat.id,
        text=lang.START_TEXT.format(update.from_user.first_name),
        reply_markup=buttons,
        reply_to_message_id=update.message_id
    )

@Client.on_message(filters.command([CMD.HELP, f"{CMD.HELP}@{Config.BOT_USERNAME}"]))
async def help(bot, update):
    if update.chat.id not in Config.AUTH_CHAT:
        await update.reply_text(
            "Bot only usable in the Authorized Chat"
        )
        return
    await check_user(update.from_user.id)
    await bot.send_message(
        chat_id=update.chat.id,
        text=lang.HELP_TEXT.format(update.from_user.first_name),
        reply_markup=await help_buttons(),
        reply_to_message_id=update.message_id
    )

@Client.on_message(filters.command([CMD.SETTINGS, f"{CMD.SETTINGS}@{Config.BOT_USERNAME}"]))
async def settings(bot, update):
    await check_user(update.from_user.id)
    video_type, photo_type = await fetch_media_details(update.from_user.id)
    first_name = update.from_user.first_name
    buttons = await settings_buttons(video_type, photo_type)
    await bot.send_message(
        chat_id=update.chat.id,
        text=lang.SETTINGS_TEXT.format(first_name),
        reply_markup=buttons,
        reply_to_message_id=update.message_id
    )

