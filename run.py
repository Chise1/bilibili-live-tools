from TCP_monitor import TCP_monitor
from OnlineHeart import OnlineHeart
from Silver import Silver
from LotteryResult import LotteryResult
from Tasks import Tasks
from connect import connect
from rafflehandler import Rafflehandler
import asyncio
from login import login
from printer import Printer
from statistics import Statistics
from bilibili import bilibili
import biliconsole
from pkLottery import PKLottery
from guardLottery import GuardLottery
from schedule import Schedule
import configloader
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
file_user = fileDir + "/conf/user.conf"
dic_user = configloader.load_user(file_user)

loop = asyncio.get_event_loop()
printer = Printer(dic_user['thoroughly_log']['on'])
bilibili()
Statistics()
rafflehandler = Rafflehandler()
biliconsole.Biliconsole()

task = OnlineHeart()  # 在线心跳
task1 = Silver()  # 领取银瓜子
task2 = Tasks()  # 获取每日包裹奖励，签到功能，领取每日任务奖励，应援团签到，过期礼物处理，银瓜子兑换硬币，硬币换瓜子，将当前佩戴的勋章亲密度送满，
task3 = LotteryResult()  # 广播抽奖检测
task4 = connect()  # 新的战疫分区直播间实际上没有弹幕区???
task5 = PKLottery()  # 大乱斗抽奖？
task6 = GuardLottery()  # 上船奖励？

tasks1 = [
    login().login_new()
]
loop.run_until_complete(asyncio.wait(tasks1))

# 任务
# import threading
# console_thread = threading.Thread(target=biliconsole.controler)
# console_thread.start()


tasks = [
    task.run(),
    task1.run(),
    task2.run(),
    biliconsole.Biliconsole().run(),#？？？？？
    task4.create(),
    task3.query(),
    rafflehandler.run(),
    task5.run(),
    task6.run()
]

if dic_user['monitoy_server']['on']:#监控服务器
    monitor = TCP_monitor()
    task_tcp_conn = monitor.connectServer(
        dic_user['monitoy_server']['host'], dic_user['monitoy_server']['port'], dic_user['monitoy_server']['key'])
    task_tcp_heart = monitor.HeartbeatLoop()
    tasks.append(task_tcp_conn)
    tasks.append(task_tcp_heart)

schedule = Schedule()
if dic_user['regular_sleep']['on']:
    tasks.append(schedule.run(dic_user['regular_sleep']['schedule']))
    Schedule().scheduled_sleep = True

tasks = list(map(asyncio.ensure_future, tasks))
loop.run_until_complete(asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION))
Printer().printer('\n'.join(map(repr, asyncio.Task.all_tasks())), "Info", "green")
for task in tasks:
    Printer().printer(repr(task._state), "Info", "green")
    if task._state == 'FINISHED':
        Printer().printer(f"Task err: {repr(task.exception())}", "Error", "red")
loop.close()

# console_thread.join()