import os
import asyncio
from pyaiodl import Downloader
from bot import Config, LOGGER
from bot.helpers.translations import lang
from pyrogram.errors import MessageNotModified
from bot.helpers.functions.file_upload import pyro_upload
from bot.helpers.database.database import checkUserSet
from bot.helpers.utils.storage_clean import clean_up
from bot.helpers.functions.display_progress import progress_for_aiodl


async def file_dl(bot, update, link, init_msg, reply_to_id, \
            return_path=None, upload=None, i=0, ovrr_name=None, rename=None):
    dl = Downloader(download_path=f"{Config.DOWNLOAD_BASE_DIR}/{reply_to_id}")
    uuid = await dl.download(link)
    while await dl.is_active(uuid):
        status = await dl.status(uuid)
        filename = status['filename']
        detail_msg = await progress_for_aiodl(status, ovrr_name)
        try:
            status_msg = await bot.edit_message_text(
                chat_id=update.chat.id,
                text=detail_msg,
                message_id=init_msg.message_id,
                parse_mode="html"
            )
        except MessageNotModified:
            pass
        except Exception as e:
            LOGGER.error(e)

        await asyncio.sleep(Config.STATUS_UPDATE_INTERVAL)
    # For Accurate Values
    status = await dl.status(uuid)
    file_path = status['download_path']
    filename = status['filename']

    if filename == "Unknown" or filename.endswith("/"):
        if i < 5:
            await file_dl(bot, update, link, init_msg, reply_to_id, return_path, upload, i+1)
        else:
            await bot.send_message(
                chat_id=update.chat.id,
                text=lang.COMMON_ERR,
                reply_to_message_id=reply_to_id
            )
    elif upload:
        if rename:
            filename = rename
            new_file_path = f"{Config.DOWNLOAD_BASE_DIR}/{reply_to_id}/{rename}"
            os.rename(file_path, new_file_path)
            file_path = new_file_path
        s_vid, s_pht = await checkUserSet(update.from_user.id)
        await pyro_upload(bot, update, file_path, filename, s_vid, s_pht, reply_to_id, init_msg)
        await clean_up(file_path, reply_to_id)
    if return_path:
        return file_path