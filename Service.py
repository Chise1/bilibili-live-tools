# -*- encoding: utf-8 -*-
"""
@File    : Service.py
@Time    : 2020/6/26 18:14
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :WEBSOCKET服务端
"""
import asyncio
from typing import Optional
from secret.Crsa import rsa_long_decrypt
# from settings import server_host
#
# class WebsocketClient(object):
#     """docstring for WebsocketClient"""
#     instance = None
#     address: str = server_host
#
#     def __new__(cls, *args, **kwargs):
#         if not cls.instance:
#             cls.instance = super(WebsocketClient, cls).__new__(cls, *args, **kwargs)
#         return cls.instance
#
#     def on_message(self, ws, message):
#         """
#         处理数据
#         :param ws:
#         :param message:
#         :return:
#         """
#         raise Exception("未重写on_message")
#
#     def on_error(self, ws, error):
#         print("client error:", error)
#
#     def on_close(self, ws):
#         print("### client closed ###")
#         self.ws.close()
#         self.is_running = False
#
#     def on_open(self, ws):
#         self.is_running = True
#         print("on open")
#
#     def close_connect(self):
#         self.ws.close()
#
#     def send_message(self, message: dict):
#         """
#         对数据进行签名，并发送数据
#         :param message:
#         :return:
#         """
#         data = json.dumps(message)
#         self.ws.send(data)
#
#     def run(self, address):
#         websocket.enableTrace(True)
#         self.ws = websocket.WebSocketApp(address, on_message=lambda ws, message: self.on_message(ws, message),
#                                          on_error=lambda ws, error: self.on_error(ws, error),
#                                          on_close=lambda ws: self.on_close(ws))
#         self.ws.on_open = lambda ws: self.on_open(ws)
#         self.is_running = False
#         while True:
#             print(self.is_running)
#             if not self.is_running:
#                 self.ws.run_forever()
#             time.sleep(10)  # 如果掉线则重启websocket
#
#     def start(self, address=None) -> Thread:
#         if address:
#             self.address = address
#         else:
#             self.address = server_host
#         self.th = Thread(target=self.run, args=(self.address,))
#         self.th.start()
#         return self.th
from aioweb import aioClient
from settings import server_id


class User:
    instance = None
    account_id = None
    account_conf: Optional[dict] = None
    bilibili_conf: Optional[dict] = None
    tasks: Optional[dict] = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(User, cls).__new__(cls)
            cls.client = aioClient()
            cls.account_id = kwargs['account_id']
        return cls.instance

    async def load_account_conf(self, update=False) -> dict:
        """
        通过账户id获取账户配置信息
        :param update: 是否重新加载该数据
        :return:
        """
        if not update or not self.account_conf:
            data = await self.client.send({"message": "load_account_conf","server_id":server_id,"account_id":self.account_id})
            self.account_conf = data['message']
        return self.account_conf
    async def load_bilibili_conf(self, update=False):
        """获取bilibili登录配置"""
        if not update or not self.bilibili_conf:
            data = await  self.client.send({"message": "load_bilibili_conf","server_id":server_id,"account_id":self.account_id})
            self.bilibili_conf = data['message']
        self.bilibili_conf['account']['password']=rsa_long_decrypt(eval(self.bilibili_conf['account']['password']))
        return self.bilibili_conf

    async def update_account_conf(self, data: dict):
        await self.client.send({"message": "update_account_conf", "data": data})

    async def update_bilibili_conf(self, data: dict):
        await self.client.send({"message": "update_bilibili_conf", "data": data})

    async def load_tasks(self, update=False):
        if not update or not self.tasks:
            data = await  self.client.send({"message": "load_tasks","server_id":server_id,"account_id":self.account_id})
            self.tasks = data['message']
        return self.tasks