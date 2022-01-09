from bot import CMD
from pyrogram import Client, filters
from bot.helpers.translations import lang
from bot.helpers.functions.file_dl import file_dl
from bot.helpers.database.database import check_user

@Client.on_message(filters.command(CMD.UPLOAD))
async def upload(bot, update):
    user_id = update.from_user.id
    await check_user(user_id)
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
    await file_dl(bot, update, link, init_msg, reply_to_id, upload=True)
    await bot.send_message(
        chat_id=update.chat.id,
        text=lang.UPLOAD_SUCCESS,
        reply_to_message_id=reply_to_id
    )
    await bot.delete_messages(
        chat_id=update.chat.id,
        message_ids=init_msg.message_id
    )
