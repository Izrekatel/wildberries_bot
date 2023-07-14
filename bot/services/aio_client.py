from aiohttp import ClientSession


async def get(url, data):
    async with ClientSession() as session:
        async with session.get(url=url, data=data) as response:
            data = await response.json()
            return data


async def post(url, data):
    async with ClientSession() as session:
        await session.post(url=url, data=data)
