import os
import asyncio
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

async def generate_thumbnail(file, msg_id):
    thumb_name = f"{file}.jpg"
    metadata = extractMetadata(createParser(file))
    if metadata.has("duration"):
        duration = str(metadata.get("duration") / 2)
    else:
        duration = "00:00:00.000"
        
    ss_command = [
        "ffmpeg",
        "-ss",
        duration,
        "-i",
        file,
        "-vframes",
        "1",
        thumb_name
    ]
    process = await asyncio.create_subprocess_exec(
        *ss_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(thumb_name):
        return thumb_name
    else:
        return None

    
