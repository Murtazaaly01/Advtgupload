import os
import time
import asyncio
from bot import LOGGER, Config, CMD
from pyrogram import Client, filters
from bot.helpers.translations import lang
from bot.helpers.functions.file_dl import file_dl
from bot.helpers.utils.storage_clean import clean_up
from bot.helpers.functions.file_upload import pyro_upload
from bot.helpers.functions.media_tools import checkDuration
from bot.helpers.functions.media_tools import generate_screenshot
from bot.helpers.database.database import check_user, checkUserSet
from bot.helpers.functions.display_progress import progress_for_pyrogram

@Client.on_message(filters.command(CMD.SCREENSHOTS))
async def screenshots(bot, update):
    user_id = update.from_user.id
    await check_user(user_id)
    if update.chat.id in Config.AUTH_CHAT or user_id in Config.ADMINS:
        # CASE WHERE REPLY CAN BE A LINK OR FILE
        if update.reply_to_message:
            reply_to_id = update.reply_to_message.message_id
            try:
                ss_no = update.text.split(" ", maxsplit=1)[1]
            except:
                ss_no = Config.DEFAULT_SS_GEN_LIM
            try:
                init_msg = await bot.send_message(
                    chat_id=update.chat.id,
                    text=lang.INIT_DOWNLOAD_FILE,
                    reply_to_message_id=update.message_id
                )
                c_time = time.time()
                file_path = await bot.download_media(
                    message=update.reply_to_message,
                    file_name=f"{Config.DOWNLOADS_FOLDER}/{reply_to_id}/",
                    progress=progress_for_pyrogram,
                    progress_args=(
                        lang.INIT_DOWNLOAD_FILE,
                        init_msg,
                        c_time
                    )
                )
                link = None
            except:
                try:
                    link = update.reply_to_message.text
                    if not link.startswith("http"):
                        return await bot.send_message(
                            chat_id=update.chat.id,
                            text=lang.ERR_USAGE,
                            reply_to_message_id=update.message_id
                        )
                except:
                    return await bot.send_message(
                        chat_id=update.chat.id,
                        text=lang.ERR_USAGE,
                        reply_to_message_id=update.message_id
                    )
        else:
            try:
                link = update.text.split(" ", maxsplit=1)[1]
                reply_to_id = update.message_id
                try:
                    ss_no = link.split(" ", maxsplit=1)[1]
                    link = link.split(" ", maxsplit=1)[0]
                except:
                    ss_no = Config.DEFAULT_SS_GEN_LIM
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
        if link:
            file_path = await file_dl(bot, update, link, init_msg, reply_to_id, return_path=True, upload=False)

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

            ss_dir = f"{Config.DOWNLOAD_BASE_DIR}/" + f"{user_id}" + "/" + "screenshots"
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
                    await clean_up(image, reply_to_id)
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
