# -*- encoding: utf-8 -*-
"""
@File    : crsa.py
@Time    : 2020/5/5 21:49
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :RSA分段加密
"""
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

from secret.rsaLis import PublicKey, PrivateKey


def rsa_long_encrypt(msg:str, length=100)->bytes:
    """
    单次加密串的长度最大为 (key_size/8)-11
    1024bit的证书用100， 2048bit的证书用 200
    """
    msg = base64.b64encode(msg.encode("utf-8"))
    pubobj = RSA.importKey(PublicKey)
    pubobj = PKCS1_v1_5.new(pubobj)
    res = []
    for i in range(0, len(msg), length):
        res.append(pubobj.encrypt(msg[i:i + length]))
    return b"".join(res)


def rsa_long_decrypt(message:bytes, default_length=128)->str:
    """解密"""
    # msg = base64.b64decode(message)
    msg = message
    length = len(msg)
    # default_length = 256
    # 私钥解密
    priobj = PKCS1_v1_5.new(RSA.importKey(PrivateKey))
    # 长度不用分段
    if length < default_length:
        return b''.join(priobj.decrypt(msg, b'ubout'))
    # 需要分段
    offset = 0
    res = []
    while length - offset > 0:
        if length - offset > default_length:
            res.append(priobj.decrypt(msg[offset:offset + default_length], b'ubout'))
        else:
            res.append(priobj.decrypt(msg[offset:], b'ubout'))
        offset += default_length
        m = b''.join(res)
        n = m.decode("utf-8")
        # print(n)
    return base64.b64decode(n).decode('utf-8')


# if __name__ == "__main__":
#     x = "我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊我是张三啊"
#     encrypt_x = rsa_long_encrypt(x)
#     print(str(encrypt_x))
#     exec('x='+str(encrypt_x))
#     print(x)
#     print(rsa_long_decrypt(encrypt_x))
