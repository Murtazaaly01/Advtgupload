from bot import LOGGER, Config, CMD
from pyrogram import Client, filters
from bot.helpers.translations import lang
from bot.helpers.utils.buttons import *
from bot.helpers.database.database import check_user
from pyrogram.types.bots_and_keyboards import CallbackQuery

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

@Client.on_callback_query(filters.regex(pattern="helpmsg"))
async def help_cb(c: Client, cb: CallbackQuery):
    buttons = await help_buttons()
    await c.edit_message_text(
        chat_id=cb.message.chat.id,
        text=lang.HELP_TEXT.format(cb.message.reply_to_message.from_user.first_name),
        message_id=cb.message.message_id,
        reply_markup=buttons
    )

@Client.on_callback_query(filters.regex(pattern="botinfo"))
async def botinfo_cb(c: Client, cb: CallbackQuery):
    buttons = await main_menu_buttons()
    await c.edit_message_text(
        chat_id=cb.message.chat.id,
        text=lang.BOT_INFO.format(Config.OWNER_USERNAME),
        message_id=cb.message.message_id,
        reply_markup=buttons
    )

@Client.on_callback_query(filters.regex(pattern="close"))
async def close_cb(c: Client, cb: CallbackQuery):
    await c.delete_messages(
        chat_id=cb.message.chat.id,
        message_ids=cb.message.message_id
    )
    try:
        await c.delete_messages(
            chat_id=cb.message.chat.id,
            message_ids=cb.message.reply_to_message.message_id
        )
    except:
        LOGGER.warning(f"Couldn't delete message in {cb.message.chat.id}")
        pass

@Client.on_callback_query(filters.regex(pattern="uploadhelp"))
async def upload_files_help_cb(c: Client, cb: CallbackQuery):
    buttons = await upload_helper_buttons()
    await c.edit_message_text(
        chat_id=cb.message.chat.id,
        text=lang.UPLOAD_HELP.format(Config.BOT_USERNAME),
        message_id=cb.message.message_id,
        reply_markup=buttons
    )
