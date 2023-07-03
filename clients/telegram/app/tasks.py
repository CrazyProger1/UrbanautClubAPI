import aiogram

from aiogram import types
from tbf.task import Task
from tbf.models import TelegramUser
from .services import *
from .exceptions import *
from .limits import *


class InputTask(Task):
    caption_key: str = None

    def __init__(self, *args, **kwargs):
        super(InputTask, self).__init__(*args, **kwargs)

   
class SendAllObjectsTask(Task):
    async def execute(self, user: TelegramUser):
        await self.async_publish(self.Event.EXECUTE, user=user)
        for obj in await get_all_objects(user=user):
            msg: types.Message = await self.sender.send_object(
                user=user,
                obj=obj
            )
            coords = obj.location.coordinates
            try:
                await self.sender.send_location(
                    user=user,
                    latitude=coords.latitude,
                    longitude=coords.longitude,
                    reply_to_message_id=msg.message_id
                )
            except aiogram.utils.exceptions.BadRequest:
                pass
        await self.async_publish(self.Event.DONE, user=user)


class InputObjectNameTask(InputTask):
    caption_key = 'contents.objects.creation.name'


class InputObjectDescTask(InputTask):
    caption_key = 'contents.objects.creation.description'


class InputObjectCoordinatesTask(InputTask):
    caption_key = 'contents.objects.creation.coordinates'
