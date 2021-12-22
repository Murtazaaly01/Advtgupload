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
                callback_data="upload_files_help"
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
                callback_data="upload_folder_help"
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

async def settings_buttons(video_type, photo_type):
    video = str(video_type).upper
    photo = str(photo_type).upper

    buttons = [
        [
            InlineKeyboardButton(
                text=f"Video Type - {video}",
                callback_data="change_video_type"
            )
        ],
        [
            InlineKeyboardButton(
                text=f"Photo Type - {photo}",
                callback_data="change_photo_type"
            )
        ]
        [
            InlineKeyboardButton(
                text="Close",
                callback_data="close"
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)