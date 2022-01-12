from bot import LOGGER, Config, CMD
from pyrogram import Client, filters
from bot.helpers.translations import lang
from bot.helpers.functions.ytdlp import jsonYTDL
from bot.helpers.utils.buttons import ytdl_buttons
from bot.helpers.database.database import check_user

@Client.on_message(filters.command(CMD.YTDL))
async def ytdl(bot, update):
    user_id = update.from_user.id
    await check_user(user_id)
    if update.chat.id in Config.AUTH_CHAT or user_id in Config.ADMINS:
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
        msg, list = await jsonYTDL(link, reply_to_id)
        if msg:
            return await bot.send_message(
                chat_id=update.chat.id,
                text=msg,
                reply_to_message_id=update.message_id
            )
        else:
            return await bot.send_message(
                chat_id=update.chat.id,
                text=lang.YTDL_MENU,
                reply_markup=await ytdl_buttons(list, user_id),
                reply_to_message_id=update.message_id
            )