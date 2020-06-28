# -*- encoding: utf-8 -*-
"""
@File    : aioWebsocket.py
@Time    : 2020/6/28 21:21
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
import json
from typing import List
from settings import server_host
import aiohttp
import asyncio
from .tools import restart, start_task, stop_task, load_one_task

from . import Sign


class aioWebsocket(Sign):
    instance = None
    session = None
    tasks: List[dict] = []  # 用户执行中的任务的名称列表
    ws_client = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls, *args, **kwargs)

        return cls.instance

    @classmethod
    async def receive(cls):
        cls.session = aiohttp.ClientSession()
        async with cls.session.ws_connect(server_host) as ws:
            cls.ws_client = ws
            while True:
                data = await ws.receive()
                data = data.json()
                cls.check_sign(data)
                if data['message'] == 'restart':
                    await restart(cls.tasks)
                elif data['message'] == 'stopTask':
                    await stop_task(cls.tasks, data['task_name'])
                elif data['message'] == "startTask":  # user_task:name,status
                    await start_task(cls.tasks, data['user_task'])
    @classmethod
    async def send(cls, data: dict):
        if not cls.ws_client:
            await asyncio.sleep(1)
        if not cls.ws_client:
            raise Exception("websocket客户端启动失败")
        return await cls.ws_client.send_str(json.dumps(data))

    @classmethod
    async def modify_msg(cls, data: dict):
        """
        处理获取到的信息
        :param data:
        :return:
        """
        pass
