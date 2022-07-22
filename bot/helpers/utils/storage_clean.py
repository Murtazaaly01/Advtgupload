import os
import shutil
from bot import Config

async def clean_up(file_path, reply_to_id):
    try:
        os.remove(file_path)
    except:
        pass
    try:
        shutil.rmtree(f"{Config.DOWNLOAD_BASE_DIR}/{str(reply_to_id)}")
    except:
        pass

