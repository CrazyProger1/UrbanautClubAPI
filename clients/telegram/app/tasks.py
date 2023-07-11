import aiogram
import geopy

from aiogram import types
from conf import settings
from tbf.task import Task
from crf.exceptions import HTTPResponseError
from .services import *
from .exceptions import *
from .limits import *
from .keyboards import *


class SendAllObjectsTask(Task):
    def __init__(self, *args, **kwargs):
        super(SendAllObjectsTask, self).__init__(*args, **kwargs)
        self.keyboard = AllObjectsNavKeyboard()

        self.keyboard.subscribe(self.keyboard.Event.BUTTON_PRESSED, self.on_button_pressed)
        self.limit = 2
        self.offset = 0
        self.last_offset = 0

    async def send_part(self, user: TelegramUser):
        self.last_offset = 0
        for obj in await get_all_objects(
                user=user,
                params={'limit': self.limit, 'offset': self.offset},
                auto_pagination=False
        ):
            self.last_offset += 1
            self.offset += 1
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
        if self.last_offset == 0:
            await self.sender.send_translated(user, 'contents.search.all.end')

    async def on_execute(self, user: TelegramUser):
        await self.send_part(user=user)

    async def on_button_pressed(self, keyboard: Keyboard, button: str, user: TelegramUser, **kwargs):
        if isinstance(keyboard, AllObjectsNavKeyboard) and self.is_executing(user=user):
            if 'back' in button:
                self.offset = 0
                self.last_offset = 0
                await self.done(user=user)
                await self.page.back(user=user)

            elif 'next' in button:
                await self.send_part(user=user)
            elif 'prev' in button:
                self.offset -= self.limit + self.last_offset
                if self.offset < 0:
                    self.offset = 0
                    await self.sender.send_translated(user, 'contents.search.all.start')
                else:
                    await self.send_part(user=user)
            return 'break'


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


class SelectTask(Task):
    keyboard_class: type[Keyboard] = None

    def __init__(self, *args, **kwargs):
        super(SelectTask, self).__init__(*args, **kwargs)
        self.keyboard = self.keyboard_class()
        self.keyboard.subscribe(self.keyboard.Event.BUTTON_PRESSED, self.on_button_pressed)
        self.subscribe(self.Event.DONE, self.hide_keyboard)
        self.subscribe(self.Event.CANCEL, self.hide_keyboard)

    async def hide_keyboard(self, user: TelegramUser):
        await self.page.hide_object(user=user, obj=self.keyboard)

    async def on_execute(self, user: TelegramUser):
        if self.keyboard_class:
            await self.page.show_object(user=user, obj=self.keyboard_class)

    async def set_value(self, user: TelegramUser, keyboard: Keyboard, button: str):
        pass

    async def on_button_pressed(self, keyboard: Keyboard, button: str, user: TelegramUser, **kwargs):
        if isinstance(keyboard, self.keyboard_class) and self.is_executing(user=user):
            try:
                await self.set_value(user=user, keyboard=keyboard, button=button)
            except ValidationError as e:
                await self.sender.send_translated(user, e.message_key, format_kwargs=e.format_kwargs)
            return 'break'


class InputObjectName(InputTask):
    caption_key = 'contents.objects.creation.name'

    async def validate(self, user: TelegramUser, value: str):
        if len(value) > OBJECT_NAME_LENGTH:
            raise ValidationError('exceptions.objects.creation.name.length')

    async def set_value(self, user: TelegramUser, value: str):
        user.state.ocs.data['name'] = value
        await self.done(user=user)


class InputObjectDescription(InputTask):
    caption_key = 'contents.objects.creation.description'

    async def validate(self, user: TelegramUser, value: str):
        if len(value) > OBJECT_DESCRIPTION_LENGTH:
            raise ValidationError('exceptions.objects.creation.description.length')

    async def set_value(self, user: TelegramUser, value: str):
        user.state.ocs.data['description'] = value
        await self.done(user=user)


class InputObjectCoordinates(InputTask):
    caption_key = 'contents.objects.creation.coordinates'

    @staticmethod
    def split_coords(value: str) -> tuple[float, ...]:
        for sep in {'x', ',', ';'}:
            coords = value.split(sep)
            if len(coords) == 2:
                return tuple(map(float, value.split(sep)))
        raise ValidationError('exceptions.objects.creation.coordinates.format')

    async def set_value(self, user: TelegramUser, value: str):
        try:
            lat, lon = self.split_coords(value)

            user.state.ocs.data['latitude'] = round(lat, 5)
            user.state.ocs.data['longitude'] = round(lon, 5)

            geolocator = geopy.Nominatim(user_agent=settings.APP.NAME)
            try:
                location = geolocator.reverse(f'{lat}, {lon}', language='en')
            except ValueError:
                raise ValidationError('exceptions.objects.creation.coordinates.invalid')

            address = location.raw['address']

            try:
                country = get_country_by_name(address['country'], raise_exceptions=False)
                if not country:
                    raise ValidationError('exceptions.objects.creation.country.not_supported')
            except KeyError:
                country = None

            city = get_city_by_name(address.get('city'), raise_exceptions=False)
            house_number = address.get('house_number')
            postcode = address.get('postcode')
            street = address.get('road')

            user.state.ocs.data['street'] = street
            user.state.ocs.data['country'] = country
            user.state.ocs.data['city'] = city
            user.state.ocs.data['street_number'] = house_number
            user.state.ocs.data['zipcode'] = postcode
        except ValidationError:
            raise
        except Exception as e:
            print(type(e), e)
            raise ValidationError('exceptions.objects.creation.coordinates.format')
        await self.done(user=user)


class SelectObjectCategoryTask(SelectTask):
    keyboard_class = SelectObjectCategoryKeyboard

    async def set_value(self, user: TelegramUser, keyboard: Keyboard, button: str):
        category_name = button.split('.')[-1]
        user.state.ocs.data['category'] = category_name
        await self.done(user=user)


class SelectObjectStateTask(SelectTask):
    keyboard_class = SelectObjectStateKeyboard

    async def set_value(self, user: TelegramUser, keyboard: Keyboard, button: str):
        state = button.split('.')[-1]
        user.state.ocs.data['state'] = state
        await self.done(user=user)


class ConfirmObjectCreationTask(SelectTask):
    keyboard_class = CreateObjectConfirmationKeyboard

    async def set_value(self, user: TelegramUser, keyboard: Keyboard, button: str):
        if 'cancel' in button:
            return await self.page.back(user=user)

        await self.done(user=user)


class CreateObjectTask(Task):
    async def on_execute(self, user: TelegramUser):
        data = user.state.ocs.data
        city = data['city']

        try:
            await create_object(**{
                "name": data['name'],
                "description": data['description'],
                "state": data['state'],
                "category": data['category'],
                "location": {
                    "coordinates": {
                        "latitude": data['latitude'],
                        "longitude": data['longitude']
                    },
                    "address": {
                        "street": data['street'],
                        "street_number": data['street_number'],
                        "zipcode": data['zipcode'],
                        "country": data['country'].id,
                        "city": city.id if city else None
                    }
                }
            })
            await self.sender.send_translated(user, 'contents.objects.creation.created')
        except HTTPResponseError as e:
            print(e.status, e.content)
            if e.status == 400:
                location = e.content.get('location')
                if location:
                    coordinates = location.get('coordinates')
                    if coordinates:
                        try:
                            if 'longitude must make a unique set' in list(coordinates.values())[0][0]:
                                await self.sender.send_translated(user,
                                                                  'exceptions.objects.creation.location.not_unique')
                                await self.page.cancel_task(user=user, task=self)
                                return await self.page.execute_task(user=user, task=InputObjectCoordinates)
                        except IndexError:
                            pass
        await self.done(user=user)
