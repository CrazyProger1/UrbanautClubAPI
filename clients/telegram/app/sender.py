from aiogram import types
from conf import settings
from tbf import sender
from tbf.models import TelegramUser
from tbf.translator import _
from .models import AbandonedObject
from .services import *
from .address import get_address


class Sender(sender.Sender):
    def __init__(self, *args, **kwargs):
        super(Sender, self).__init__(*args, **kwargs)

    async def send_object(self, user: TelegramUser, obj: AbandonedObject, **kwargs) -> types.Message:
        if not isinstance(obj, AbandonedObject):
            raise ValueError('obj must be an instance of AbandonedObject')

        coordinates = obj.location.coordinates
        address = obj.location.address

        # country = get_country_by_id(address.country)
        return await self.send_message(
            user,
            _('contents.objects.object_form', user=user).format(
                name=obj.name,
                desc=obj.description,
                category=_(f'contents.objects.categories.{obj.category.name}', user=user),
                state=_(f'contents.objects.states.{obj.state}', user=user),
                address=get_address(address.street_number, address.street, address.city, address.country),
                latitude=coordinates.latitude,
                longitude=coordinates.longitude
            ),
            **kwargs,
        )
