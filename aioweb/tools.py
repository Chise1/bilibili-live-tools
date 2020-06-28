# -*- encoding: utf-8 -*-
"""
@File    : tools.py
@Time    : 2020/6/28 21:20
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
import asyncio
from typing import List
from comments import load_one_task


async def restart(tasks: list):
    """
    执行任务重启
    :param tasks:
    :return:
    """
    syncs = asyncio.all_tasks()
    for sync in syncs:
        for task in tasks:
            if task['name'] == sync.get_name():
                sync.cancel()
        else:
            pass
    for task in tasks:
        asyncio.create_task(task['task'], name=task['name'])


async def stop_task(tasks: List[dict], task_name):
    """
    停止任务
    :param tasks:
    :param task_name:
    :return:
    """
    now_tasks = asyncio.all_tasks()
    for task in now_tasks:
        if task.get_name() == task_name:
            task.cancel()
            for i in tasks:
                if i['name'] == task_name:
                    tasks.remove(i)


async def start_task(tasks: List[dict], user_task):
    """
    启动任务
    :param tasks:
    :param task_name:
    :return:
    """
    for i in tasks:
        if i['name'] == user_task['name']:
            return
    await load_one_task(tasks, user_task)


from multiprocessing import Process
from run2 import run

