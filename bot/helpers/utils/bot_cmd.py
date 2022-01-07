from bot import Config

bot = Config.BOT_USERNAME

class BOT_CMD(object):
    START = ["start", f"start@{bot}"]
    HELP = ["help", f"help@{bot}"]
    SETTINGS = ["settings", f"settings@{bot}"]
    UPLOAD = ["upload", f"upload@{bot}"]
    
    