# -*- encoding: utf-8 -*-
"""
@File    : ttt.py
@Time    : 2020/6/26 20:27
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
import aiohttp
import asyncio

async def fetch(client):
    async with client.ws_connect('ws://39.98.132.68:8000/ws/Slaver/1') as resp:
        assert resp.status == 200
        return await resp.text()
# async def test(client):
#     async with client.get('http://39.98.132.68:8000/admin/') as resp:
#         assert resp.status == 200
#         return await resp.text()
async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as client:
        html = await fetch(client)
        # html=await test(client)
        print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))