from logging import disable
import os
import time
import asyncio
from pyaiodl import Downloader
from bot import Config, LOGGER
from hachoir.parser import createParser
from bot.helpers.translations import lang
from hachoir.metadata import extractMetadata
from bot.helpers.functions.display_progress import progress_for_aiodl, progress_for_pyrogram
from pyrogram.errors import MessageNotModified

start_time = time.time()
dl = Downloader(download_path=Config.DOWNLOAD_LOCATION, chunk_size=Config.CHUNK_SIZE*1000)

async def file_dl(bot, update, init_msg, msg_id, link, s_vid, s_pht):
    uuid = await dl.download(link)
    while await dl.is_active(uuid):
        status = await dl.status(uuid)
        filename = status['filename']
        detail_msg = await progress_for_aiodl(status)
        try:
            await bot.edit_message_text(
                chat_id=update.chat.id,
                text=detail_msg,
                message_id=init_msg.message_id,
                parse_mode="html"
            )
        except MessageNotModified:
            pass
        except Exception as e:
            LOGGER.error(e)
        await asyncio.sleep(6)
    await asyncio.sleep(1)
    file_path = os.path.join(Config.DOWNLOAD_LOCATION, filename)
    metadata = extractMetadata(createParser(file_path))
    if filename != "Unknown":
        if filename.endswith((".mkv", ".mp4", ".flv", ".avi", ".webm")) and s_vid:
            if metadata.has("duration"):
                duration = metadata.get("duration").seconds
            width = 1280
            height = 720
            await bot.send_video(
                chat_id=update.chat.id,
                video=file_path,
                duration=duration,
                width=width,
                height=height,
                caption=filename,
                supports_streaming=True,
                disable_notification=True,
                progress=progress_for_pyrogram,
                reply_to_message_id=msg_id,
                progress_args=(
                    lang.INIT_UPLOAD_FILE,
                    init_msg,
                    start_time
                )
            )
        elif filename.endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")) and s_pht:
            await bot.send_photo(
                chat_id=update.chat.id,
                photo=file_path,
                caption=filename,
                progress=progress_for_pyrogram,
                disable_notification=True,
                reply_to_message_id=msg_id,
                progress_args=(
                    lang.INIT_UPLOAD_FILE,
                    init_msg,
                    start_time
                )
            )
        else:
            await bot.send_document(
                chat_id=update.chat.id,
                document=file_path,
                caption=filename,
                disable_notification=True,
                progress=progress_for_pyrogram,
                reply_to_message_id=msg_id,
                progress_args=(
                    lang.INIT_UPLOAD_FILE,
                    init_msg,
                    start_time
                )
            )
        os.remove(Config.DOWNLOAD_LOCATION + "/" + filename)