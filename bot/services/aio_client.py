from aiohttp import ClientSession


async def get(url: str, data=None, params=None, headers=None) -> dict:
    async with ClientSession() as session:
        response = await session.get(
            url=url, data=data, params=params, headers=headers
        )
        data = await response.json()
        await session.close()
        return data


async def post(url: str, data=None) -> None:
    async with ClientSession() as session:
        await session.post(url=url, data=data)
        await session.close()
