# -*- encoding: utf-8 -*-
"""
@File    : test_class_fun.py
@Time    : 2020/6/28 21:17
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
class A:
    @classmethod
    def test(cls,data):
        print("get_data:",data)

A.test("shadiao")