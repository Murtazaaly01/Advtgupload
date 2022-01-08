from bot import CMD, LOGGER, Config
from pyrogram import Client, filters
from bot.helpers.translations import lang
from bot.helpers.functions.file_dl import file_dl

@Client.on_message(filters.command(CMD.UPLOAD))
async def upload(bot, update):
    try:
        link = update.text.split(" ", maxsplit=1)[1]
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
    reply_to_id = init_msg.reply_to_message.message_id
    await file_dl(bot, update, link, init_msg, reply_to_id)
    await bot.send_message(
        chat_id=update.chat.id,
        text=lang.UPLOAD_SUCCESS,
        reply_to_message_id=init_msg.message_id
    )
