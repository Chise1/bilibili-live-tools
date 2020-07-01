# -*- encoding: utf-8 -*-
"""
@File    : sign.py
@Time    : 2020/6/9 19:21
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
import copy
import hashlib
from typing import Optional
from django.conf import settings


def get_sign(extra_params: Optional[dict] = None) -> str:
    """
    签名
    :param extra_params:
    :return:
    """
    dict_params = copy.deepcopy(extra_params)
    if dict_params.get('sign'):
        dict_params.pop('sign')
    list_params = [f'{key}={value}' for key, value in dict_params.items()]
    list_params.sort()
    text = "&".join(list_params)
    app_secret = settings.APPSERECT
    text_with_appsecret = f'{text}{app_secret}'
    return hashlib.md5(text_with_appsecret.encode('utf-8')).hexdigest()