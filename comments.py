# -*- encoding: utf-8 -*-
"""
@File    : comments.py
@Time    : 2020/6/27 17:41
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import List
from OnlineHeart import OnlineHeart
from Service import User
from Silver import Silver
from LotteryResult import LotteryResult
from Tasks import Tasks
from connect import connect
from rafflehandler import Rafflehandler
import asyncio
import biliconsole
from pkLottery import PKLottery
from guardLottery import GuardLottery


async def load_one_task(tasks, user_task):
    if user_task['name'] == 'Silver' and user_task['status']:
        task = Silver().run()
        tasks.append({
            "name": "Silver",
            "task": task
        })
        asyncio.create_task(task, name="Silver")
        # tasks.append(Silver().run())  # 领取银瓜子
    elif user_task['name'] == 'EverydayTask' and user_task['status']:
        task = Tasks().run()
        tasks.append({
            "name": "EverydayTask",
            "task": task
        })
        asyncio.create_task(task, name="Tasks")
        # tasks.append(Tasks().run())  # 获取每日包裹奖励，签到功能，领取每日任务奖励，应援团签到，过期礼物处理，银瓜子兑换硬币，硬币换瓜子，将当前佩戴的勋章亲密度送满，
    elif user_task['name'] == 'LotteryResult' and user_task['status']:
        task = LotteryResult().query()
        tasks.append({
            "name": "LotteryResult",
            "task": task
        })
        asyncio.create_task(task, name="LotteryResult")
        # tasks.append(LotteryResult().query())# 广播抽奖检测
    elif user_task['name'] == 'connect' and user_task['status']:
        task = connect().create()
        tasks.append({
            "name": "connect",
            "task": task
        })
        asyncio.create_task(task, name="connect")
        # tasks.append(connect().create())  # 新的战疫分区直播间实际上没有弹幕区???
    elif user_task['name'] == 'PKLottery' and user_task['status']:
        task = PKLottery().run()
        tasks.append({
            "name": "PKLottery",
            "task": task
        })
        asyncio.create_task(task, name="PKLottery")
        # tasks.append(PKLottery().run())  # 大乱斗抽奖？
    elif user_task['name'] == 'GuardLottery' and user_task['status']:
        task = GuardLottery().run()
        tasks.append({
            "name": "GuardLottery",
            "task": task
        })
        asyncio.create_task(task, name="GuardLottery")
        # tasks.append('GuardLottery')
        # tasks.append(GuardLottery().run())  # 上船奖励？
    else:
        pass


async def load_tasks(user: User) -> List[dict]:
    asyncio.create_task(OnlineHeart().run(), name="OnlineHeart")
    asyncio.create_task(Rafflehandler().run(), name="Rafflehandler")
    tasks = []
    for user_task in await user.load_tasks():
        await load_one_task(tasks, user_task)
    asyncio.create_task(biliconsole.Biliconsole().run(), name="biliconsole")
    return tasks
