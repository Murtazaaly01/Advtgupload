import motor.motor_asyncio
from bot import Config

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        
    def new_user(self, user_id):
        return dict(
            id=user_id,
            lang='EN',
            video_type='video',
            photo_type='photo',
        )

    async def add_user(self, user_id):
        user = self.new_user(user_id)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, user_id):
        user = await self.col.find_one({'id': (user_id)})
        return user is not None

    async def video_type(self, user_id):
        user = await self.col.find_one({'id': (user_id)})
        return user.get('video_type')

    async def photo_type(self, user_id):
        user = await self.col.find_one({'id': (user_id)})
        return user.get('photo_type')

    async def change_video_type(self, user_id, video_type):
        self.col.update_one(
            {"id": user_id},
            {
                "$set": {
                    "video_type": video_type

            }
        }
        )
    
    async def change_photo_type(self, user_id, photo_type):
        self.col.update_one(
            {"id": user_id},
            {
                "$set": {
                    "photo_type": photo_type

            }
        }
        )

db = Database(Config.DATABASE_URL, Config.BOT_USERNAME)