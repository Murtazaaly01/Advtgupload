from bot.helpers.database.db_handle import db

async def check_user(user_id):
    id = int(user_id)
    user = await db.is_user_exist(id)
    if user is False:
        await db.add_user(id)

async def fetch_media_details(user_id):
    id = int(user_id)
    video_type = await db.video_type(id)
    photo_type = await db.photo_type(id)
    return video_type, photo_type