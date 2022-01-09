import os
import time
import asyncio
from bot import LOGGER, Config, CMD
from pyrogram import Client, filters
from bot.helpers.translations import lang
from bot.helpers.functions.file_dl import file_dl
from bot.helpers.database.database import check_user, checkUserSet
from bot.helpers.functions.media_tools import checkDuration
from bot.helpers.functions.media_tools import generate_screenshot
from bot.helpers.functions.file_upload import pyro_upload
from bot.helpers.functions.display_progress import progress_for_pyrogram

@Client.on_message(filters.command(CMD.SCREENSHOTS))
async def screenshots(bot, update):
    user_id = update.from_user.id
    await check_user(user_id)
    # USING TG FILE
    if update.reply_to_message is not None:
        init_msg = await bot.send_message(
            chat_id=update.chat.id,
            text=lang.INIT_DOWNLOAD_FILE,
            reply_to_message_id=update.message_id
        )
        reply_to_id = update.reply_to_message.message_id
        file_path = Config.DOWNLOADS_FOLDER + "/" + f"{user_id}" + "/" + f"{update.reply_to_message.document.file_name}"
        c_time = time.time()
        await bot.download_media(
            message=update.reply_to_message,
            file_name=file_path,
            progress=progress_for_pyrogram,
            progress_args=(
                lang.INIT_DOWNLOAD_FILE,
                init_msg,
                c_time
            )
        )
        file_path = Config.DOWNLOAD_LOCATION + "/" + file_path
        files = os.listdir(file_path)
        for file in files:
            LOGGER.info(file)
    # USING LINK
    else:
        try:
            link = update.text.split(" ", maxsplit=1)[1]
            reply_to_id = update.message_id 
        except:
            try:
                link = update.reply_to_message.text
                reply_to_id = update.reply_to_message.message_id
            except:
                return await bot.send_message(
                    chat_id=update.chat.id,
                    text=lang.ERR_USAGE,
                    reply_to_message_id=update.message_id
                )
        init_msg = await bot.send_message(
            chat_id=update.chat.id,
            text=lang.INIT_DOWNLOAD_FILE,
            reply_to_message_id=update.message_id
        )
        file_path = await file_dl(bot, update, link, init_msg, reply_to_id, return_path=True, upload=False)
    # COMMON PART
    if file_path:
        await bot.edit_message_text(
            chat_id=update.chat.id,
            message_id=init_msg.message_id,
            text=lang.INIT_SS_GEN
        )
        check_dur = await checkDuration(file_path)
        if check_dur < 5:
            await bot.send_message(
                chat_id=update.chat.id,
                text=lang.ERR_SS_TOO_SHORT,
                reply_to_message_id=reply_to_id
            )
            return await bot.delete_messages(
                chat_id=update.chat.id,
                message_ids=init_msg.message_id
            )

        ss_dir = Config.DOWNLOAD_LOCATION + f"/screenshots-{update.from_user.id}"
        if not os.path.isdir(ss_dir):
            os.makedirs(ss_dir)
        images = await generate_screenshot(file_path, ss_dir, 8)
        video, photo = await checkUserSet(update.from_user.id)
        for image in images:
            await pyro_upload(bot, update, image, '', video, photo, reply_to_id, init_msg)
            asyncio.sleep(1)
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=init_msg.message_id
        )
        await bot.send_message(
            chat_id=update.chat.id,
            text=lang.UPLOAD_SUCCESS,
            reply_to_message_id=reply_to_id
        )
    else:
        await bot.edit_message_text(
            chat_id=update.chat.id,
            message_id=init_msg.message_id,
            text=lang.COMMON_ERR
        )
