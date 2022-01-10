import os
from bot import Config, LOGGER, CMD
from pyrogram import Client, filters
from bot.helpers.translations import lang
from bot.helpers.utils.buttons import *
from pyrogram.types.bots_and_keyboards import CallbackQuery
from bot.helpers.database.database import fetch_media_details, change_video_type_db, change_photo_type_db, checkUserSet
from bot.helpers.functions.file_dl import file_dl
from bot.helpers.functions.file_upload import pyro_upload

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
        text=lang.UPLOAD_HELP.format(
            CMD.UPLOAD[1],
            CMD.SETTINGS[1]
            ),
        message_id=cb.message.message_id,
        reply_markup=await upload_helper_buttons(user_id)
    )

@Client.on_callback_query(filters.regex(pattern="sshelp"))
async def ss_help_cb(c: Client, cb: CallbackQuery):
    user_id = cb.data.split("_")[1]
    if int(user_id) != cb.from_user.id:
        await cb.answer(lang.NOT_AUTH_CB)
        return
    await c.edit_message_text(
        chat_id=cb.message.chat.id,
        text=lang.SCREENSHOTS_HELP.format(
            CMD.SCREENSHOTS[1]
            ),
        message_id=cb.message.message_id,
        reply_markup=await main_menu_buttons(user_id)
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

@Client.on_callback_query(filters.regex(pattern="y-t"))
async def yt_cb(c: Client, cb: CallbackQuery):
    user_id = cb.data.split("_")[2]
    if int(user_id) != cb.from_user.id:
        await cb.answer(lang.NOT_AUTH_CB)
        return
    reply_to_id = cb.message.reply_to_message.message_id
    resolution = cb.data.split("_")[1]
    await c.edit_message_text(
        chat_id=cb.message.chat.id,
        text=lang.YTDL_EXT_MENU.format(resolution),
        message_id=cb.message.message_id,
        reply_markup=await yt_ext_buttons(resolution, reply_to_id, user_id)
    )

@Client.on_callback_query(filters.regex(pattern="dlyt"))
async def ytdl_cb(c: Client, cb: CallbackQuery):
    user_id = cb.data.split("_")[3]
    if int(user_id) != cb.from_user.id:
        await cb.answer(lang.NOT_AUTH_CB)
        return
    reply_to_id = cb.message.reply_to_message.message_id
    ext = cb.data.split("_")[1]
    vcodec = cb.data.split("_")[2]

    json_file_path = Config.DOWNLOAD_BASE_DIR + "/" + str(reply_to_id) + ".json"
    with open(json_file_path, "r", encoding="utf8") as f:
        response_json = json.load(f)
    title = response_json["title"]
    for format in response_json["formats"]:
        if format["ext"] == ext:
            if format["vcodec"] == vcodec:
                url = format["url"]
                resolution = format["format_note"]
                break
    await c.edit_message_text(
        chat_id=cb.message.chat.id,
        text=lang.INIT_DOWNLOAD_FILE,
        message_id=cb.message.message_id
    )
    new_filename = title + "_" + resolution + "." + ext
    new_filepath = Config.DOWNLOAD_BASE_DIR + "/" + new_filename
    file_path = await file_dl(c, cb.message, url, cb.message, reply_to_id, return_path=True, upload=False, ovrr_name=new_filename)
    if file_path:
        os.rename(file_path, new_filepath)
        print(user_id)
        video, photo = await checkUserSet(int(user_id))
        await pyro_upload(c, cb.message, new_filepath, '', video, photo, reply_to_id, cb.message)
        

    