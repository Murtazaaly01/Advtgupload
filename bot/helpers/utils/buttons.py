import json
from bot import Config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def start_buttons(user_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="Help",
                callback_data=f"helpmsg_{user_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Bot Info",
                callback_data=f"botinfo_{user_id}"
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)

async def help_buttons(user_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="Upload Files",
                callback_data=f"uploadhelp_{user_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Screenshots",
                callback_data=f"sshelp_{user_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Close",
                callback_data=f"close_{user_id}"
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)

async def upload_helper_buttons(user_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="Close",
                callback_data=f"close_{user_id}"
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)

async def main_menu_buttons(user_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="Main Menu",
                callback_data=f"helpmsg_{user_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Close",
                callback_data=f"close_{user_id}"
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)

async def settings_buttons(video_type, photo_type, user_id):
    video = video_type.upper()
    photo = photo_type.upper()

    buttons = [
        [
            InlineKeyboardButton(
                text=f"Video Type - {video}",
                callback_data=f"changevideotype_{user_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text=f"Photo Type - {photo}",
                callback_data=f"changephototype_{user_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Close",
                callback_data=f"close_{user_id}"
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)

# FIRST MENU FOR CHOOSING QUALITY
async def ytdl_buttons(list, user_id):
    inline_keyboard = []
    string_buttons = []
    i = 0
    while i < len(list):
        if not list[i][:1].isdigit():
            string_buttons.append(
                InlineKeyboardButton(
                    text=list[i],
                    callback_data=f"y-t_{list[i]}_{user_id}"
                )
            )
        else:
            inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        text=list[i],
                        callback_data=f"y-t_{list[i]}_{user_id}"
                    ),
                    InlineKeyboardButton(
                        text=list[i+1],
                        callback_data=f"y-t_{list[i+1]}_{user_id}"
                    )
                ],
            )
            i += 1
        i += 1
    inline_keyboard.append(string_buttons)
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="AUDIOS",
                callback_data=f"y-a_{user_id}"
            )
        ]
    )
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="Close",
                callback_data=f"close_{user_id}"
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard)

# 2ND MENU FOR CHOOSING VIDEO EXTENSION
async def yt_ext_buttons(resolution, reply_to_id, user_id):
    json_file_path = Config.DOWNLOAD_BASE_DIR + "/" + str(reply_to_id) + ".json"
    with open(json_file_path, "r", encoding="utf8") as f:
            response_json = json.load(f)
    buttons = []
    for formats in response_json["formats"]:
        if formats["format_note"] == resolution:
            ext = formats["ext"]
            vcodec = formats["vcodec"]
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{ext} - {vcodec}",
                        callback_data=f"dlyt_{ext}_{vcodec}_{user_id}"
                    )
                ],
            )
    buttons.append(
        [
            InlineKeyboardButton(
                text="Close",
                callback_data=f"close_{user_id}"
            )
        ]
    )
    return InlineKeyboardMarkup(buttons)

async def yt_audio_buttons(user_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="MP3 - 64K",
                callback_data=f"dlyta_{user_id}_64k"
            )
        ],
        [
            InlineKeyboardButton(
                text="MP3 - 128K",
                callback_data=f"dlyta_{user_id}_128k"
            )
        ],
        [
            InlineKeyboardButton(
                text="MP3 - 320K",
                callback_data=f"dlyta_{user_id}_320k"
            )
        ],
        [
            InlineKeyboardButton(
                text="Close",
                callback_data=f"close_{user_id}"
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)
    


