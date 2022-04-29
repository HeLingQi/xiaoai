# -*- coding: utf-8 -*-
import requests
import urllib
import time
import os
import sys
import json


def uniqid(prefix=''):
    return prefix + hex(int(time.time()))[2:10] + hex(int(time.time() * 1000000) % 0x100000)[2:7]


api = 'https://bigota.miwifi.com/xiaoqiang/rom/s12a/'
# 自行替换低版本文件地址
path = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(path + '/user.ini') is False:
    print('账号配置文件不存在，请确认')
    sys.exit()
userFile = open(path + '/ota.ini', 'r', encoding='UTF-8').read()
array = json.loads(userFile)
if isinstance(array, dict) is False:
    print('参数配置错误，请检查')
    sys.exit()
else:
    userId = array['userId']
    serviceToken = array['serviceToken']
    cUserId = array['cUserId']
    deviceId = array['deviceId']
    sn = array['sn']
    version = array['version']
    if not all([userId, serviceToken, cUserId, cUserId, deviceId, sn, version]):
        print('参数配置不完整，请确认')
        sys.exit()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Connection": "keep-alive",
        "Cookie": "userId=" + userId + ";serviceToken=" + serviceToken + ";cUserId=" + cUserId + ";deviceId=" + deviceId + ";sn=" + sn,
        "Accept-Language": "zh-cn",
        "User-Agent": "MiSoundBox/2.0.41 CFNetwork/978.0.7 Darwin/18.5.0",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }
    bodyData = {
        "checksum": "00c355fbae2104aa6051aa34893f86a5",
        "deviceId": deviceId,
        "extra": '{"cfe":1000002,"linux":1,"rootfs":1,"weight":1,"sqafs":1,"ramfs":1}',
        "hardware": "S12A",
        "requestId": uniqid(),
        "url": api + version,
        "version": "1.44.4"
    }
    body = urllib.parse.urlencode(bodyData)
    url = "https://api.mina.mi.com/remote/ota/v2"
    try:
        response = requests.post(url, data=body, headers=headers)
        print(response.text)
    except Exception as e:
        print(e)
