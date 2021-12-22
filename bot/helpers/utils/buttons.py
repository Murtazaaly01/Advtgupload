from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def start_buttons():
    buttons = [
        [
            InlineKeyboardButton(
                text="Help",
                callback_data="help"
            )
        ],
        [
            InlineKeyboardButton(
                text="Bot Info",
                callback_data="botinfo"
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)

async def help_buttons():
    buttons = [
        [
            InlineKeyboardButton(
                text="Upload Files",
                callback_data="upload_files"
            )
        ],
        [
            InlineKeyboardButton(
                text="Close",
                callback_data="close"
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)

async def upload_helper_buttons():
    buttons = [
        [
            InlineKeyboardButton(
                text="Upload Index Folder",
                callback_data="upload_folder"
            )
        ],
        [
            InlineKeyboardButton(
                text="Close",
                callback_data="close"
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)

async def main_menu_buttons():
    buttons = [
        [
            InlineKeyboardButton(
                text="Main Menu",
                callback_data="help"
            )
        ],
        [
            InlineKeyboardButton(
                text="Close",
                callback_data="close"
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)