# -*- encoding: utf-8 -*-
"""
@File    : user_info.py
@Time    : 2020/6/9 19:03
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
import copy
import hashlib
from typing import Optional
from . import server_id, BASE_URL, APPSERECT
import requests


def add_sign(extra_params: Optional[dict] = None) -> dict:
    """
    签名
    :param extra_params:
    :return:
    """
    dict_params = copy.deepcopy(extra_params)
    print(dict_params)
    if dict_params.get('sign'):
        dict_params.pop('sign')
    list_params = [f'{key}={value}' for key, value in dict_params.items()]
    list_params.sort()
    text = "&".join(list_params)
    app_secret = APPSERECT
    text_with_appsecret = f'{text}{app_secret}'
    print(text_with_appsecret)
    sign = hashlib.md5(text_with_appsecret.encode('utf-8')).hexdigest()
    dict_params['sign'] = sign
    return dict_params


def get_userInfo(account_id: int):
    data = {
        "server_id": server_id,
        "id": account_id
    }
    req = add_sign(data)
    ret = requests.get(BASE_URL + "accountInfo/UserInfo", params=req)
    assert ret.status_code == 200, "请求错误：" + ret.json()['msg']
    return ret.json()


def get_all_userInfo():
    data = {
        "server_id": server_id
    }
    req = add_sign(data)
    ret = requests.get(BASE_URL + "accountInfo", params=req)
    assert ret.status_code == 200, "请求错误：" + str(ret.json())
    return ret.json()


def update_userInfo(user_id, dict_new: dict):
    if dict_new.get('username'):
        dict_new.pop('username')
    if dict_new.get('password'):
        dict_new.pop('password')
    if dict_new.get('tasks') or dict_new.get('tasks') == []:
        dict_new.pop('tasks')
    if dict_new.get('id'):
        dict_new.pop('id')
    dict_new['server_id'] = server_id
    req = add_sign(dict_new)
    ret = requests.put(BASE_URL + "accountInfo/" + str(user_id) + "/", data=req)
    assert ret.status_code == 200, "请求错误：" + str(ret.json())
    return ret.json()


def write_account_log(username,  msg, num, ):
    """
    写入日志
    :param task_id:
    :param msg:
    :param num:
    :param status:
    :return:
    """
    data = {
        "username": username,
        "msg": msg,
        "num": num,
        "server_id": server_id,
        "sign": "test_sign"
    }
    print(msg)
    print(requests.post(BASE_URL.replace('Slaver/','') + "bili/log/", data=data).json())
    # assert ret.status_code == 200, "请求错误：" + str(ret.json())
    # return ret.json()