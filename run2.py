import asyncio

async def run(account_id: int):
    from Service import User
    import asyncio
    from login import login
    from bilibili import bilibili
    import biliconsole
    from schedule import Schedule
    from aioweb.aioWebsocket import aioWebsocket
    user = User(account_id=account_id)
    dic_user = await user.load_account_conf()
    x = bilibili()
    await x.init()
    from statistics import Statistics
    Statistics()
    biliconsole_task = biliconsole.Biliconsole()
    login_tasks = login().login_new()
    asyncio.create_task(login_tasks, name="login")
    from comments import load_tasks
    tasks = await load_tasks(user)
    asyncio.create_task(biliconsole_task.run(), name="biliconsole")
    schedule = Schedule()
    print(dic_user)
    if dic_user['regular_sleep']['on']:
        Schedule().scheduled_sleep = True
        asyncio.create_task(schedule.run(dic_user['regular_sleep']['schedule']), name="schedule")
    aioWebsocket.tasks = tasks
    asyncio.create_task(aioWebsocket().receive(), name="aiowebsocket")


def start(account_id):
    asyncio.run(run(account_id))