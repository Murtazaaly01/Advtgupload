from bot import Config, LOGGER, CMD
from pyrogram import Client, filters
from bot.helpers.translations import lang
from bot.helpers.functions.file_dl import file_dl
from bot.helpers.database.database import fetch_media_details

@Client.on_message(filters.command([CMD.UPLOAD, f"@{Config.BOT_USERNAME}{CMD.UPLOAD}"]))
async def upload_files(bot, update):
    try:
        link = update.text.split(" ")[1]
    except IndexError:
        await update.reply(lang.ERR_USAGE)
        return
    
    if link.endswith("/"):
        await bot.send_message(
            chat_id=update.chat.id,
            text=lang.INIT_INDEX_LINK,
            reply_to_message_id=update.message_id
        )
        # ADD FOLDER FETCH HERE TODO
    else:
        init_msg = await bot.send_message(
            chat_id=update.chat.id,
            text=lang.INIT_DOWNLOAD_FILE,
            reply_to_message_id=update.message_id
        )
        msg_id = update.message_id
        video, photo = await fetch_media_details(update.from_user.id)
        if video == "video":
            s_vid = True
        else:
            s_vid = False
        if photo == "photo":
            s_pht = True
        else:
            s_pht = False

        await file_dl(bot, update, init_msg, msg_id, link, s_vid, s_pht)

        