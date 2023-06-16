import asyncio
from models import *
from serializers import *
from managers import *


async def main():
    aobj1 = await AbandonedObjectAPIManager.create(
        name='test',
        description='kuku epta',
        state='a',
        category='Bunker entrance'
    )
    print(aobj1.name)
    print(aobj1.description)
    print(AbandonedObjectSerializer.serialize(aobj1))


asyncio.run(main())
