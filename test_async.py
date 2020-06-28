# -*- encoding: utf-8 -*-
"""
@File    : test_async.py
@Time    : 2020/6/27 16:28
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :测试创建任务以及取消任务
"""
import asyncio


async def coro():
    print("start")
    await asyncio.sleep(1)
    print("wait cancel")
    await asyncio.sleep(5)
    print("cancel fail")


async def t():
    print(coro())
    task = asyncio.create_task(coro(), name="coro111")
    print("get_task:", task)
    await asyncio.sleep(3)
    # task.cancel()
    print("???")
    x = asyncio.all_tasks()
    for k in x:
        if k.get_name() == "coro111":
            if not k.cancelled():
                print(k.get_coro())
                k.cancel()
    # for k in x:
    #     if k.get_name()=="coro111":
    #         if k.cancelled():
    #             k.r
    await asyncio.sleep(5)
    x = asyncio.all_tasks()
    for k in x:
        print(k.get_name())
    print(x)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(t())
    loop.run_forever()
    # asyncio.run(t())
