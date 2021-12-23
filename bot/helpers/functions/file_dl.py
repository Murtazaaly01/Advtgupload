import time
import asyncio
from pyaiodl import Downloader
from bot import Config, LOGGER
from bot.helpers.translations import lang
from bot.helpers.functions.display_progress import progress_for_aiodl, progress_for_pyrogram
from pyrogram.errors import MessageNotModified

start_time = time.time()
dl = Downloader(download_path=Config.DOWNLOAD_LOCATION, chunk_size=Config.CHUNK_SIZE*1000)

async def file_dl(bot, update, init_msg, link, s_vid, s_pht):
    uuid = await dl.download(link)
    while await dl.is_active(uuid):
        status = await dl.status(uuid)
        filename = status['filename']
        detail_msg = await progress_for_aiodl(status)
        try:
            msg = await bot.send_message(
                chat_id=update.chat.id,
                text=lang.START_DOWNLOAD,
                reply_to_message_id=init_msg.reply_to_message.message_id
            )
            asyncio.sleep(3)
            await msg.edit_text(
                text=detail_msg
            )
            #await msg.edit(detail_msg)
        except MessageNotModified:
            pass
        except Exception as e:
            LOGGER.error(e)
            
    if filename != "Unknown":
        if filename.endswith((".mkv", ".mp4", ".flv", ".avi", ".webm")):
            bot.send_video(
                chat_id=update.chat.id,
                video=Config.DOWNLOAD_LOCATION + "/" + filename,
                caption=filename,
                supports_streaming=s_vid,
                progress=progress_for_pyrogram,
                reply_to_message_id=init_msg.reply_to_message.message_id,
                progress_args=(
                    lang.INIT_UPLOAD_FILE,
                    msg,
                    start_time
                )
            )
        elif filename.endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")) and s_pht == "photo":
            bot.send_photo(
                chat_id=update.chat.id,
                photo=Config.DOWNLOAD_LOCATION + "/" + filename,
                caption=filename,
                progress=progress_for_pyrogram,
                reply_to_message_id=init_msg.reply_to_message.message_id,
                progress_args=(
                    lang.INIT_UPLOAD_FILE,
                    msg,
                    start_time
                )
            )
        else:
            bot.send_document(
                chat_id=update.chat.id,
                document=Config.DOWNLOAD_LOCATION + "/" + filename,
                caption=filename,
                progress=progress_for_pyrogram,
                reply_to_message_id=init_msg.reply_to_message.message_id,
                progress_args=(
                    lang.INIT_UPLOAD_FILE,
                    msg,
                    start_time
                )
            )