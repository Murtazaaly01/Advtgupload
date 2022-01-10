import json
import asyncio
from bot import Config

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
        save_path = Config.DOWNLOAD_BASE_DIR + "/" + msg_id + ".json"
        with open(save_path, "w", encoding="utf8") as outfile:
            json.dump(response_json, outfile, ensure_ascii=False)
        if "formats" in response_json:
            list = []
            for format in response_json["formats"]:
                if format["format_note"] not in list and format["format_note"] != "storyboard":
                    list.append(format["format_note"])