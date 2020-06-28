# -*- encoding: utf-8 -*-
"""
@File    : __init__.py.py
@Time    : 2020/6/28 21:20
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
# -*- encoding: utf-8 -*-
import asyncio
import json
from multiprocessing import Process
from typing import List

import aiohttp
from settings import server_host2, server_host, server_id, server_host3


class Sign():
    @classmethod
    def add_sign(cls, data: dict):
        return data

    @classmethod
    def check_sign(cls, data: dict):
        return data

    @classmethod
    def get_sign(cls, data: dict):
        return data


class aioClient(Sign):
    """
    临时交互
    """

    @classmethod
    async def send(cls, data: dict) -> dict:
        session = aiohttp.ClientSession()
        async with session.ws_connect(server_host2) as ws:
            data = cls.add_sign(data)
            await ws.send_str(json.dumps(data))
            ret = await ws.receive()
        await session.close()
        assert ret, "返回数据异常"
        ret=ret.json()
        cls.check_sign(ret)
        return ret


processes = {}

from run2 import start


class WebClient(Sign):
    """
    全局交互
    """
    instance = None
    session = None
    tasks: List[dict] = []  # 用户执行中的任务的名称列表
    ws_client = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls, *args, **kwargs)

        return cls.instance

    @classmethod
    def get_all_user(cls, accounts):
        """
        启动所有user
        :param accounts:
        :return:
        """
        for account in accounts:
            process = Process(target=start, args=(account['id'],))
            processes[account['id']] = process
            process.start()

    @classmethod
    def get_user(cls, account):
        """
            启动一个user
            :param account:
            :return:
            """
        process = Process(target=start, args=(account['id'],))
        processes[account['id']] = process
        process.start()

    @classmethod
    async def receive(cls):
        cls.session = aiohttp.ClientSession()
        async with cls.session.ws_connect(server_host3) as ws:
            cls.ws_client = ws
            await ws.send_str(json.dumps({"message": "start", "server_id": server_id}))
            while True:
                data = await ws.receive()
                data = data.json()
                cls.check_sign(data)
                if data['message'] == 'get_user':
                    cls.get_user(data['account_id'])
                elif data['message'] == 'get_all_user':
                    cls.get_all_user(data['accounts'])

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