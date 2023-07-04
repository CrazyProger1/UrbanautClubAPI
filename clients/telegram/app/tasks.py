import aiogram

from aiogram import types
from tbf.task import Task
from tbf.models import TelegramUser
from .services import *
from .exceptions import *
from .limits import *


class SendAllObjectsTask(Task):
    async def on_execute(self, user: TelegramUser):
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

        await self.done(user=user)


class InputTask(Task):
    caption_key: str = None

    def __init__(self, *args, **kwargs):
        super(InputTask, self).__init__(*args, **kwargs)
        self.page.subscribe(self.page.Event.MESSAGE, self.on_message)

    async def on_execute(self, user: TelegramUser):
        if self.caption_key:
            await self.sender.send_translated(user, self.caption_key)

    async def validate(self, user: TelegramUser, value: str):
        pass

    async def set_value(self, user: TelegramUser, value: str):
        pass

    async def on_message(self, page, message: types.Message, user: TelegramUser, **kwargs):
        if self.is_executing(user=user):
            try:
                value = message.text
                await self.validate(user=user, value=value)
                await self.set_value(user=user, value=value)
            except ValidationError as e:
                await self.sender.send_translated(user, e.message_key, format_kwargs=e.format_kwargs)
            return 'break'


class InputObjectName(InputTask):
    caption_key = 'contents.objects.creation.name'

    async def validate(self, user: TelegramUser, value: str):
        if len(value) > OBJECT_NAME_LENGTH:
            raise ValidationError('exceptions.objects.creation.name.length')

    async def set_value(self, user: TelegramUser, value: str):
        print('Object name:', value)
        await self.done(user=user)


class InputObjectDescription(InputTask):
    caption_key = 'contents.objects.creation.description'

    async def validate(self, user: TelegramUser, value: str):
        if len(value) > OBJECT_DESCRIPTION_LENGTH:
            raise ValidationError('exceptions.objects.creation.description.length')

    async def set_value(self, user: TelegramUser, value: str):
        print('Object description:', value)
        await self.done(user=user)


class InputObjectCoordinates(InputTask):
    caption_key = 'contents.objects.creation.coordinates'

    async def set_value(self, user: TelegramUser, value: str):
        try:
            lat, lon = map(float, value.split('x'))
            print(f'Object coordinates: {lat}x{lon}')
        except Exception as e:
            raise ValidationError('exceptions.objects.creation.coordinates.format')
        await self.done(user=user)
