class EN(object):

    INIT_MSG = "<b>Hello {} Sir</b>"
    START_TEXT = """
<b>Hello {} Sir</b>,
Iam a Mirror Group Helper Bot which can do some advanced stuffs for you.

Use the help button to see how to use me.
"""
    HELP_TEXT = """
<b>Hello {} Sir</b>,

Please Choose the Category for the help.
"""
    BOT_INFO = """
<b>Version :</b> <code>1.2.0</code>
<b>Owner :</b> <code>@{}</code>
<b>Source :</b> <code>Open</code>
<b>GitHub :</b> <code>Open</code>
<b>Framework :</b> <code>Python</code>
<b>Server :</b> <code>Heroku</code>
<b>Database :</b> <code>NoSQL - MongoDB</code>
"""
    SETTINGS_TEXT = """
<b>Hello {} Sir</b>,

Change your preffered options here from the buttons below.
"""
    UPLOAD_HELP = """
You can use the below commands to upload the files to TG.

<code>/{} url</code> -> Uploads the file from the given url.

<b>This upload command only supports :</b>
Direct file links
Index folder links (beta)

Thumbnails & Media types can be modified in the settings.
Open the settings by using <code>/{}</code> command.
"""

    SCREENSHOTS_HELP = """
You can use the below commands to take screenshots of the media.

<code>/{}</code> as a reply to the Media File or to a Direct Link
To specify the amount of screenshots to take, mention the amount with the command.

Default amount is 8.
"""

    ERR_USAGE = "Use <code>/help</code> to see how to use me."

    INIT_INDEX_LINK = "<b>Index Links Found</b>\nTrying to fetch child links..."
    INIT_DOWNLOAD_FILE = "Trying to download file..."
    INIT_UPLOAD_FILE = "Trying to upload file..."
    START_DOWNLOAD = "Downloading File......."
    UPLOAD_SUCCESS = "File Uploaded Successfully."

    NOT_AUTH_CB = "Why you clicking others buttons? 🤨"

    COMMON_ERR = "Something went wrong. Please try again later."

    INIT_SS_GEN = "Trying To Generate Screenshot..."
    ERR_SS_TOO_SHORT = "Video Duration is too short. Please try again."

    YTDL_MENU = "Choose the required quality for the video from the below buttons."
    YTDL_EXT_MENU = "Choose the required extension for the resolution <b>{}</b> from the below buttons."
    YTDL_AUDIO_MENU = "Choose the required audio quality for the video from the below buttons."