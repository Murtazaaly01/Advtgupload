import json
import asyncio
from bot import Config
from bot.helpers.translations import lang
from bot.helpers.functions.file_upload import pyro_upload
from bot.helpers.database.database import checkUserSet

async def jsonYTDL(url, msg_id):
    command_to_exec = [
        "yt-dlp",
        "--no-warnings",
        "--youtube-skip-dash-manifest",
        "-j",
        url
    ]
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if e_response and "nonnumeric port" not in e_response:
        return e_response
    if t_response:
        x_reponse = t_response
        if "\n" in x_reponse:
            x_reponse, _ = x_reponse.split("\n")
        response_json = json.loads(x_reponse)
        save_path = Config.DOWNLOAD_BASE_DIR + "/" + str(msg_id) + ".json"
        with open(save_path, "w", encoding="utf8") as outfile:
            json.dump(response_json, outfile, ensure_ascii=False)
        if "formats" in response_json:
            list = []
            for format in response_json["formats"]:
                if format["format_note"] not in list and format["format_note"] != "storyboard":
                    list.append(format["format_note"])
        return None, list

async def ytdl_audio(client, message, link, reply_to_id, user_id, yt_quality, title):
    await client.edit_message_text(
        chat_id=message.chat.id,
        text=lang.INIT_DOWNLOAD_FILE,
        message_id=message.message_id
    )
    download_path = Config.DOWNLOAD_BASE_DIR + "/" + str(reply_to_id) + "/" + title
    ext = "mp3"
    command_to_exec = [
        "yt-dlp",
        "-c",
        "--prefer-ffmpeg",
        "--extract-audio",
        "--audio-format", ext,
        "--audio-quality", yt_quality,
        link,
        "-o", download_path,
        "--no-warnings",
    ]
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if e_response:
        return e_response
    if t_response:
        s_vid, s_pht = await checkUserSet(int(user_id))
        await pyro_upload(client, message, download_path, title, s_vid, s_pht, reply_to_id, message)
