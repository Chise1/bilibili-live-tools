# -*- encoding: utf-8 -*-
"""
@File    : enums.py
@Time    : 2020/6/27 18:05
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from enum import Enum
class TaskEnum(Enum):
    Silver='Silver'
    EverydayTask= 'EverydayTask'
    LotteryResult='LotteryResult'
    connect='connect'
    PKLottery='PKLottery'
    GuardLottery='GuardLottery'

if __name__ == '__main__':
    x=TaskEnum('Silver2')
    print(x)