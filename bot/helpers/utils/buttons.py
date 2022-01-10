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

async def ytdl_buttons(list, user_id):
    inline_keyboard = []
    string_buttons = []
    i = 0
    while i < len(list):
        if not list[i][:1].isdigit():
            string_buttons.append(
                InlineKeyboardButton(
                    text=list[i],
                    callback_data=f"yt|{list[i]}|{user_id}"
                )
            )
        else:
            inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        text=list[i],
                        callback_data=f"yt|{list[i]}|{user_id}"
                    ),
                    InlineKeyboardButton(
                        text=list[i+1],
                        callback_data=f"yt|{list[i+1]}|{user_id}"
                    )
                ]
            )
            i += 1
        i += 1
    inline_keyboard.append(string_buttons)
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="Close",
                callback_data=f"close_{user_id}"
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard)