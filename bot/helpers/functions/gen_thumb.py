import ffmpeg
from bot import LOGGER, Config

async def generate_thumbnail(file, msg_id):
    thumb_name = Config.DOWNLOAD_LOCATION + f"{msg_id}-Thumbnail.jpg"
    probe = await ffmpeg.probe(file)
    time = float(probe['streams'][0]['duration']) // 2
    width = probe['streams'][0]['width']
    try:
        (
            await ffmpeg
            .input(file, ss=time)
            .filter('scale', width, -1)
            .output(thumb_name, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        LOGGER.error(e.stderr.decode('utf-8'))