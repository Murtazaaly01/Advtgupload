import re
from bot import CMD, Config
from pyrogram import Client, filters
from bot.helpers.translations import lang
from bot.helpers.functions.ytdlp import jsonYTDL
from bot.helpers.functions.file_dl import file_dl
from bot.helpers.database.database import check_user
from bot.helpers.utils.buttons import ytdl_buttons
from bot.helpers.functions.index_link_scrapper import fetch_index_links

yt_regex = "^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+"

@Client.on_message(filters.command(CMD.UPLOAD))
async def upload(bot, update):
    user_id = update.from_user.id
    await check_user(user_id)
    if update.chat.id in Config.AUTH_CHAT or user_id in Config.ADMINS:
        try:
            link = update.text.split(" ", maxsplit=1)[1]
            reply_to_id = update.message_id 
            try:
                rename_name = link.split(" | ")[1]
                link = link.split(" | ")[0]
            except:
                rename_name = None
        except:
            try:
                link = update.reply_to_message.text
                reply_to_id = update.reply_to_message.message_id
                try:
                    rename_name = update.text.split(" | ", maxsplit=1)[1]
                except:
                    rename_name = None
            except:
                return await bot.send_message(
                    chat_id=update.chat.id,
                    text=lang.ERR_USAGE,
                    reply_to_message_id=update.message_id
                )
        # FOR YTDL LINKS
        if re.match(yt_regex, link):
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
        # FOR DIRECT FILE LINKS
        init_msg = await bot.send_message(
            chat_id=update.chat.id,
            text=lang.INIT_DOWNLOAD_FILE,
            reply_to_message_id=update.message_id
        )
        try:
            await file_dl(bot, update, link, init_msg, reply_to_id, upload=True, rename=rename_name)
            await bot.send_message(
                chat_id=update.chat.id,
                text=lang.UPLOAD_SUCCESS,
                reply_to_message_id=reply_to_id
            )
        except Exception as e:
            await bot.send_message(
                chat_id=update.chat.id,
                text=e,
                reply_to_message_id=reply_to_id
            )
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=init_msg.message_id
        )

@Client.on_message(filters.command(CMD.INDEX_UPLOAD))
async def index_upload(bot, update):
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
        init_msg = await bot.send_message(
            chat_id=update.chat.id,
            text=lang.INIT_INDEX_LINK,
            reply_to_message_id=update.message_id
        )
        links = await fetch_index_links(link)
        if links == []:
            return await bot.edit_message_text(
                chat_id=update.chat.id,
                message_id=init_msg.message_id,
                text=lang.COMMON_ERR
            )
        else:
            await bot.edit_message_text(
                chat_id=update.chat.id,
                message_id=init_msg.message_id,
                text=lang.INDEX_LINK_FOUND.format(len(links))
            )
            for link in links:
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
            
