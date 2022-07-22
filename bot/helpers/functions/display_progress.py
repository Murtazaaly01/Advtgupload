import math
import time
import asyncio
from bot import Config

async def progress_for_pyrogram(
    current,
    total,
    ud_type,
    message,
    start
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
        progress = "[{0}{1}] \nP: {2}%\n".format(
            ''.join(["▰" for _ in range(math.floor(percentage / 10))]),
            ''.join(["▱" for _ in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )

        tmp = progress + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(text=f"{ud_type}\n {tmp}")
        except:
            pass
        await asyncio.sleep(Config.STATUS_UPDATE_INTERVAL)

def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return f"{str(round(size, 2))} {Dic_powerN[n]}B"

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)}d, " if days else "")
        + (f"{str(hours)}h, " if hours else "")
        + (f"{str(minutes)}m, " if minutes else "")
        + (f"{str(seconds)}s, " if seconds else "")
        + (f"{str(milliseconds)}ms, " if milliseconds else "")
    )

    return tmp[:-2]

async def progress_for_aiodl(r, ovrr_name=None):
    file_name = r['filename']
    if ovrr_name:
        file_name = ovrr_name
    size = r['total_size_str']
    downloaded = r['downloaded_str']
    progress = r['progress']
    speed = r['download_speed']
    progress_bar = "{0}{1}".format(
        ''.join(["▰" for _ in range(math.floor(progress / 10))]),
        ''.join(["▱" for _ in range(10 - math.floor(progress / 10))]),
    )

    msg = f"Filename :\n<code>{file_name}</code>\n\n" + "<b>╭─ Progress\n│\n├</b>"
    msg += "  {0}<b>\n│\n├</b>".format(progress_bar)
    msg += "<b> Speed : <code>{0}</code>\n│\n├</b>".format(speed)
    msg += f"<b> Done : <code>{downloaded}</code>\n│\n╰─</b>"
    msg += f"<b> Size : <code>{size}</code></b>"
    return msg