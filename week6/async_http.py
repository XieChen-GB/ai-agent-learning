import aiohttp
import asyncio
import time

async def fetch(session: aiohttp.ClientSession, url):
    async with session.get(url) as response:
        return await response.json()
    
async def main():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(
            fetch(session, "https://httpbingo.org/delay/2"),
            fetch(session, "https://httpbingo.org/delay/1"),
            fetch(session, "https://httpbingo.org/delay/3")
        )
        print(result)
    end = time.time()
    print(f"总耗时：{end - start:.1f} 秒")

asyncio.run(main())