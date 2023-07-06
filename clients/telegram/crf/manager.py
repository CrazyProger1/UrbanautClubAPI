import json

import aiohttp
import enum

from .serializer import Serializer
from .exceptions import *


class APIRoute(enum.Enum):
    POST = 1
    GET = 2
    UPDATE = 3
    DELETE = 4
    COMMON = 5


class APIManager:
    class Meta:
        serializer_class: type[Serializer]
        routes: dict[APIRoute, str]

    @classmethod
    def get_api_route(cls, route: APIRoute) -> str:
        try:
            url = cls.Meta.routes.get(route, cls.Meta.routes.get(APIRoute.COMMON))
            if not url:
                raise
            return url
        except AttributeError:
            raise AttributeError('Meta.routes not specified')

    @classmethod
    def get_serializer(cls) -> type[Serializer]:
        try:
            serializer = cls.Meta.serializer_class
            if not issubclass(serializer, Serializer):
                raise TypeError('Meta.serializer_class must be a subclass of serializer')
            return serializer
        except AttributeError:
            raise AttributeError('Meta.serializer_class class not specified')

    @classmethod
    async def create(cls, **data):
        serializer = cls.get_serializer()
        instance = serializer.deserialize(data)

        headers = {'Content-Type': 'application/json'}
        json_data = json.dumps(data, indent=1)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=cls.get_api_route(APIRoute.POST),
                    data=json_data,
                    headers=headers
            ) as response:
                data = await response.json()
                if response.status != 201:
                    raise HTTPResponseError(response.status, data)
                print(json.dumps(data, indent=1))

                # print(response.status)
                # print('Data:', data)
        return instance

    @classmethod
    async def retrieve(cls):
        pass

    @classmethod
    async def update(cls):
        pass

    @classmethod
    async def destroy(cls):
        pass

    @classmethod
    async def list(cls):
        serializer = cls.get_serializer()
        async with aiohttp.ClientSession() as session:
            async with session.get(url=cls.get_api_route(APIRoute.GET)) as response:
                data = await response.json()
                print(response.status)
                print('Data:', data)

    @classmethod
    async def list_paginated(cls, params: dict = None, auto_pagination: bool = True):
        if not params:
            params = {}

        objects = []
        serializer = cls.get_serializer()

        async with aiohttp.ClientSession() as session:
            async def get_page(url):
                async with session.get(url=url, params=params) as response:
                    data = await response.json()
                    if response.status == 200:
                        results = data['results']
                        next_page = data['next']

                        for dataset in results:
                            objects.append(serializer.deserialize(dataset))

                        if next_page:
                            if auto_pagination:
                                await get_page(next_page)

            await get_page(cls.get_api_route(APIRoute.GET))
        return objects
