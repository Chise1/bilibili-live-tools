# -*- encoding: utf-8 -*-
"""
@File    : __init__.py.py
@Time    : 2020/6/9 19:03
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :服务端操作
"""
import os
BASE_URL="http://127.0.0.1:8000/Slaver/"
# BASE_URL="http://39.98.132.68:8000/Slaver/"
server_id= os.getenv('server_id') or  "0612c18a-b321-42cf-a2d1-09d1d4e1be1a"
APPSERECT="560c52ccd288fed045859ed18bffd973"