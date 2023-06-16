import asyncio
from models import *
from serializers import *
from managers import *


async def main():
    db.create_tables(Model.__subclasses__())
    aobj1 = await AbandonedObjectAPIManager.create(
        name='test',
        description='kuku epta',
        state='a',
        category='Bunker entrance',
        id=10
    )
    # print(aobj1.name)
    # print(aobj1.description)
    # print(AbandonedObjectSerializer.serialize(aobj1))

    objects = await AbandonedObjectAPIManager.list_paginated()

    for obj in objects:
        print('---------------------------------------------')
        print(obj.id)
        print(obj.name)
        print(obj.description)
        print(obj.location.address.street)
        print(obj.category)


asyncio.run(main())
