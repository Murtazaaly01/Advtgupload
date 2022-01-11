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
    if update.chat.id in Config.AUTH_CHAT:
        # USING TG FILE
        if update.reply_to_message is not None:
            init_msg = await bot.send_message(
                chat_id=update.chat.id,
                text=lang.INIT_DOWNLOAD_FILE,
                reply_to_message_id=update.message_id
            )
            try:
                ss_no = update.text.split(" ", maxsplit=1)[1]
            except:
                ss_no = Config.DEFAULT_SS_GEN_LIM

            reply_to_id = update.reply_to_message.message_id
            try:
                file_path = Config.DOWNLOAD_BASE_DIR + "/" + f"{user_id}" + "/" + f"{update.reply_to_message.video.file_name}"
            except:
                return await bot.send_message(
                    chat_id=update.chat.id,
                    text=lang.ERR_USAGE,
                    reply_to_message_id=update.message_id
                )
            c_time = time.time()
            file_path = await bot.download_media(
                message=update.reply_to_message,
                file_name=file_path,
                progress=progress_for_pyrogram,
                progress_args=(
                    lang.INIT_DOWNLOAD_FILE,
                    init_msg,
                    c_time
                )
            )
            print(file_path)
        # USING LINK
        else:
            try:
                link = update.reply_to_message.text
                if link.startswith("http"):
                    try:
                        ss_no = update.text.split(" ", maxsplit=1)[1]
                    except:
                        ss_no = Config.DEFAULT_SS_GEN_LIM
                    reply_to_id = update.reply_to_message.message_id
            except:
                try:
                    link = update.text.split(" ", maxsplit=1)[1]
                    try:
                        ss_no = link.split(" ", maxsplit=1)[1]
                    except:
                        ss_no = Config.DEFAULT_SS_GEN_LIM
                    reply_to_id = update.message_id
                except:
                    return await bot.send_message(
                        chat_id=update.chat.id,
                        text=lang.ERR_USAGE,
                        reply_to_message_id=update.message_id
                    )
            LOGGER.info(f"{link - {ss_no}}")
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

            ss_dir = Config.DOWNLOAD_BASE_DIR + "/" + f"{user_id}" + "/" + "screenshots"
            if not os.path.isdir(ss_dir):
                os.makedirs(ss_dir)
            LOGGER.info(f"Generating {ss_no} screenshots for {user_id}")
            images = await generate_screenshot(file_path, ss_dir, no_photos=int(ss_no))
            if images:
                video, photo = await checkUserSet(update.from_user.id)
                print(video, photo)
                i = 1
                for image in images:
                    await pyro_upload(bot, update, image, f"SS - {i}.jpg", video, photo, reply_to_id, init_msg)
                    i += 1
                    await asyncio.sleep(1)
                    
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
        else:
            await bot.edit_message_text(
                chat_id=update.chat.id,
                message_id=init_msg.message_id,
                text=lang.COMMON_ERR
            )
