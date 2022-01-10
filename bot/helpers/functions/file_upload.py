import os
import time
from bot import LOGGER, Config
from hachoir.parser import createParser
from bot.helpers.translations import lang
from hachoir.metadata import extractMetadata
from bot.helpers.functions.media_tools import generate_thumbnail
from bot.helpers.functions.display_progress import progress_for_pyrogram

video_files = (".mkv", ".mp4", ".flv", ".avi", ".webm")
audio_files = (".mp3", ".m4a", ".wav", ".flac", ".ogg", ".opus")
photo_files = (".jpg", ".jpeg", ".png", ".bmp", ".gif")

start_time = time.time()

async def pyro_upload(bot, update, file_path, filename, s_vid,\
    s_pht, reply_to_id, init_msg, force_thum=None):

    if filename.endswith(video_files) and s_vid:
        metadata = extractMetadata(createParser(file_path))
        if force_thum:
            thumb = force_thum
        else:
            try:
                thumb = await generate_thumbnail(file_path)
            except Exception as e:
                LOGGER.error(e)
                thumb = None
        if metadata.has("duration"):
            duration = metadata.get("duration").seconds
        width = 1280
        height = 720
        s_msg = await bot.send_video(
            chat_id=update.chat.id,
            video=file_path,
            duration=duration,
            width=width,
            height=height,
            caption=filename,
            thumb=thumb,
            supports_streaming=True,
            disable_notification=True,
            progress=progress_for_pyrogram,
            reply_to_message_id=reply_to_id,
            progress_args=(
                lang.INIT_UPLOAD_FILE,
                init_msg,
                start_time
            )
        )
        if Config.ALLOW_DUMP:
            await s_msg.copy(   
                chat_id=Config.LOG_CHANNEL_ID
            )
    elif filename.endswith(photo_files) and s_pht:
        s_msg = await bot.send_photo(
            chat_id=update.chat.id,
            photo=file_path,
            caption=filename,
            progress=progress_for_pyrogram,
            disable_notification=True,
            reply_to_message_id=reply_to_id,
            progress_args=(
                lang.INIT_UPLOAD_FILE,
                init_msg,
                start_time
            )
        ) 
        if Config.ALLOW_DUMP:
            await s_msg.copy(   
                chat_id=Config.LOG_CHANNEL_ID
            )
    else:
        s_msg = await bot.send_document(
            chat_id=update.chat.id,
            document=file_path,
            caption=filename,
            disable_notification=True,
            progress=progress_for_pyrogram,
            reply_to_message_id=reply_to_id,
            progress_args=(
                lang.INIT_UPLOAD_FILE,
                init_msg,
                start_time
            )
        )
        if Config.ALLOW_DUMP:
            await s_msg.copy(   
                chat_id=Config.LOG_CHANNEL_ID
            )
    # CLEAN UP
    os.remove(file_path)
    try:
        os.remove(thumb)
    except:
        pass

