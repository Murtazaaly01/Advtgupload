from bot import Config, LOGGER
from pyrogram import Client, filters
from bot.helpers.translations import lang
from bot.helpers.utils.buttons import *
from pyrogram.types.bots_and_keyboards import CallbackQuery
from bot.helpers.database.database import fetch_media_details, change_video_type_db, change_photo_type_db

@Client.on_callback_query(filters.regex(pattern="helpmsg"))
async def help_cb(c: Client, cb: CallbackQuery):
    user_id = cb.data.split("_")[1]
    if int(user_id) != cb.from_user.id:
        await cb.answer(lang.NOT_AUTH_CB)
        return
    await c.edit_message_text(
        chat_id=cb.message.chat.id,
        text=lang.HELP_TEXT.format(cb.message.reply_to_message.from_user.first_name),
        message_id=cb.message.message_id,
        reply_markup=await help_buttons(user_id),
    )

@Client.on_callback_query(filters.regex(pattern="botinfo"))
async def botinfo_cb(c: Client, cb: CallbackQuery):
    user_id = cb.data.split("_")[1]
    if int(user_id) != cb.from_user.id:
        await cb.answer(lang.NOT_AUTH_CB)
        return
    await c.edit_message_text(
        chat_id=cb.message.chat.id,
        text=lang.BOT_INFO.format(Config.OWNER_USERNAME),
        message_id=cb.message.message_id,
        reply_markup=await main_menu_buttons(user_id)
    )

@Client.on_callback_query(filters.regex(pattern="uploadhelp"))
async def upload_files_help_cb(c: Client, cb: CallbackQuery):
    user_id = cb.data.split("_")[1]
    if int(user_id) != cb.from_user.id:
        await cb.answer(lang.NOT_AUTH_CB)
        return
    await c.edit_message_text(
        chat_id=cb.message.chat.id,
        text=lang.UPLOAD_HELP.format(Config.BOT_USERNAME),
        message_id=cb.message.message_id,
        reply_markup=await upload_helper_buttons(user_id)
    )

@Client.on_callback_query(filters.regex(pattern="changevideotype"))
async def change_video_type_cb(c: Client, cb: CallbackQuery):
    user_id = cb.data.split("_")[1]
    if int(user_id) != cb.from_user.id:
        await cb.answer(lang.NOT_AUTH_CB)
        return
    user_id = cb.message.reply_to_message.from_user.id
    user_name = cb.message.reply_to_message.from_user.first_name
    video_type, photo_type = await fetch_media_details(user_id)
    if video_type == "video":
        video_type = "doc"
        await change_video_type_db(user_id, video_type)
    else:
        video_type = "video"
        await change_video_type_db(user_id, video_type)
    await c.edit_message_text(
        chat_id=cb.message.chat.id,
        text=lang.SETTINGS_TEXT.format(user_name) + "\n\nChanged Video Type to " + video_type,
        message_id=cb.message.message_id,
        reply_markup=await settings_buttons(video_type, photo_type, user_id)
    )

@Client.on_callback_query(filters.regex(pattern="changephototype"))
async def change_photo_type_cb(c: Client, cb: CallbackQuery):
    user_id = cb.data.split("_")[1]
    if int(user_id) != cb.from_user.id:
        await cb.answer(lang.NOT_AUTH_CB)
        return
    user_id = cb.message.reply_to_message.from_user.id
    user_name = cb.message.reply_to_message.from_user.first_name
    video_type, photo_type = await fetch_media_details(user_id)
    if photo_type == "photo":
        photo_type = "doc"
        await change_photo_type_db(user_id, photo_type)
    else:
        photo_type = "photo"
        await change_photo_type_db(user_id, photo_type)
    await c.edit_message_text(
        chat_id=cb.message.chat.id,
        text=lang.SETTINGS_TEXT.format(user_name) + "\nChanged Photo Type to " + photo_type,
        message_id=cb.message.message_id,
        reply_markup=await settings_buttons(video_type, photo_type, user_id)
    )

@Client.on_callback_query(filters.regex(pattern="close"))
async def close_cb(c: Client, cb: CallbackQuery):
    user_id = cb.data.split("_")[1]
    if int(user_id) != cb.from_user.id:
        await cb.answer(lang.NOT_AUTH_CB)
        return
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