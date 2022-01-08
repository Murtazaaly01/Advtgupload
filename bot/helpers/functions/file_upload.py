import os
import time
from bot import LOGGER
from hachoir.parser import createParser
from bot.helpers.translations import lang
from hachoir.metadata import extractMetadata
from bot.helpers.functions.gen_thumb import generate_thumbnail
from bot.helpers.functions.display_progress import progress_for_pyrogram

video_files = (".mkv", ".mp4", ".flv", ".avi", ".webm")
audio_files = (".mp3", ".m4a", ".wav", ".flac", ".ogg", ".opus")
photo_files = (".jpg", ".jpeg", ".png", ".bmp", ".gif")

start_time = time.time()

async def pyro_upload(bot, update, file_path, filename, s_vid,\
    s_pht, reply_to_id, init_msg):

    if filename.endswith(video_files):
        metadata = extractMetadata(createParser(file_path))
        try:
            thumb = await generate_thumbnail(file_path)
        except Exception as e:
            LOGGER.error(e)
            thumb = None
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
            thumb=thumb,
            supports_streaming=s_vid,
            disable_notification=True,
            progress=progress_for_pyrogram,
            reply_to_message_id=reply_to_id,
            progress_args=(
                lang.INIT_UPLOAD_FILE,
                init_msg,
                start_time
            )
        )   
    elif filename.endswith(photo_files) and s_pht:
       await bot.send_photo(
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
    else:
        await bot.send_document(
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
    # CLEAN UP
    os.remove(file_path)
    try:
        os.remove(thumb)
    except:
        pass

