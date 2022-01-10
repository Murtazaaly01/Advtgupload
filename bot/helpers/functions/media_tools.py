import os
import time
import asyncio
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

async def generate_thumbnail(file):
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

async def generate_screenshot(file_path, output_path , no_photos, min_duration=5):
    metadata = extractMetadata(createParser(file_path))
    duration = 0
    if metadata is not None:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    if duration > min_duration:
        images = []
        ttl_step = duration // no_photos
        current_ttl = ttl_step
        for looper in range(0, no_photos):
            ss_img = await take_screen_shot(file_path, output_path, current_ttl)
            current_ttl = current_ttl + ttl_step
            images.append(ss_img)
        return images
    else:
        return None
    
async def take_screen_shot(video_file, output_directory, ttl):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + \
        "/" + str(time.time()) + ".jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    # width = "90"
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None

async def checkDuration(file_path):
    metadata = extractMetadata(createParser(file_path))
    duration = 0
    if metadata is not None:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    return duration
