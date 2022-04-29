# -*- coding: utf-8 -*-
import requests
import sys
import hashlib
import json
import urllib
import base64
import os
import time


# MD5 混淆
def MD5(str):
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()


# 登录
def loginByAccount(user, pwd):
    if len(user) == 0 or len(pwd) == 0:
        print('请输入账号或密码')
        sys.exit()
    sign = getLoginSign()
    time.sleep(3)
    authInfo = serviceAuth(sign, user, pwd)
    if authInfo['code'] != 0:
        print(authInfo['desc'])
        sys.exit()
    time.sleep(3)
    resp = loginMiAi(authInfo)
    return {'serviceToken': resp['serviceToken'], 'userId': resp['userId'], 'cUserId': authInfo['cUserId']}



# 获取登录签名
def getLoginSign():
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Connection": "keep-alive",
        "Accept-Language": "zh-cn",
        "User-Agent": MINA_UA,
    }
    try:
        resp = requests.get(API['SERVICE_LOGIN'],
                            params=COMMON_PARAM, headers=headers, timeout=times)
        result = (resp.text).replace('&&&START&&&', '')
        info = json.loads(result)
        return {'_sign': info['_sign'], 'qs': info['qs']}
    except Exception as e:
        print('getLoginSign {}'.format(e))
        sys.exit()


# 授权
def serviceAuth(signData, user, pwd):
    data = {
        'user': user,
        'hash': MD5(pwd).upper(),
        'callback': 'https://api.mina.mi.com/sts',
        'sid': COMMON_PARAM['sid'],
        '_json': COMMON_PARAM['_json'],
        'serviceParam': '{"checkSafePhone":false}',
        'qs': signData['qs'],
        '_sign': signData['_sign'],
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Connection": "keep-alive",
        "Accept-Language": "zh-cn",
        "User-Agent": MINA_UA,
        'Cookie': "deviceId="+APP_DEVICE_ID+";sdkVersion="+SDK_VER,
    }

    try:
        resp = requests.post(API['SERVICE_AUTH'], params=data,
                             headers=headers, timeout=times)
        result = (resp.text).replace('&&&START&&&', '')
        authInfo = json.loads(result)
        return authInfo
    except Exception as e:
        print('serviceAuth {}'.format(e))
        sys.exit()


# 登录小米音箱
def loginMiAi(authInfo):
    clientSign = genClientSign(authInfo['nonce'], authInfo['ssecurity'])
    headers = {
        'User-Agent': APP_UA,
        'Accept-Language': 'zh-cn',
        'Connection': 'keep-alive'
    }
    url = authInfo['location']+"&clientSign=" + \
        urllib.parse.quote(clientSign.decode())
    try:
        resp = requests.get(url, headers=headers, timeout=times)
        if resp.status_code == 200:
            cookies = resp.cookies.get_dict()
            return {'userId': cookies['userId'], 'serviceToken': cookies['serviceToken']}
        else:
            return False
    except Exception as e:
        print('出错了，loginMiAi {}'.format(e))
        sys.exit()


# 签名
def genClientSign(nonce, secrity):
    tempStr = "nonce={}&{}".format(nonce, secrity)
    hashStr = hashlib.sha1(tempStr.encode('utf-8')).digest()
    return base64.b64encode(hashStr)


# 获取设备
def getDevice(serviceToken, userId):
    headers = {
        'User-Agent': APP_UA,
        'Accept-Language': 'zh-cn',
        'Connection': 'keep-alive',
        'Cookie': 'userId={};serviceToken={}'.format(userId, serviceToken)
    }

    try:
        resp = requests.get(API['DEVICE_LIST'], headers=headers, timeout=times)
        if resp.status_code != 200:
            return False
        else:
            resDist = json.loads(resp.text, encoding="UTF-8")
            if resDist['code'] != 0:
                print(resDist['message'])
                sys.exit()
            else:
                return resDist['data']
    except Exception as e:
        print('getDevice {}'.format(e))
        sys.exit()


COMMON_PARAM = {
    'sid': 'micoapi',
    '_json': 'true'
}
APP_DEVICE_ID = '3C861A5820190429'
SDK_VER = '3.4.1'
APP_UA = 'APP/com.xiaomi.mico APPV/2.1.17 iosPassportSDK/3.4.1 iOS/13.5'
MINA_UA = 'MISoundBox/2.1.17 (com.xiaomi.mico; build:2.1.55; iOS 13.5) Alamofire/4.8.2 MICO/iOSApp/appStore/2.1.17'
API = {
    'USBS': 'https://api.mina.mi.com/remote/ubus',
    'SERVICE_AUTH': 'https://account.xiaomi.com/pass/serviceLoginAuth2',
    'SERVICE_LOGIN': 'https://account.xiaomi.com/pass/serviceLogin',
    'DEVICE_LIST': 'https://api.mina.mi.com/admin/v2/device_list',
}

times = 20
if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(path+'/user.ini') is False:
        print('账号配置文件不存在，请确认')
        sys.exit()
    userFile = open(path+'/user.ini', 'r', encoding='UTF-8').read()
    array = json.loads(userFile)
    print('登录中……')
    res = loginByAccount(array['user'], array['pwd'])
    if res is None:
        print('登录失败')
        sys.exit()
    else:
        print('登录成功')
        time.sleep(5)
        f = open(path+'/xiaoai-res.txt', 'a', encoding="UTF-8")
        f.write('-------账号参数-------\n\n')
        content = "serviceToken：{}\nuserId：{}\ncUserId：{} \n".format(
            res['serviceToken'], res['userId'], res['cUserId'])
        print(content)
        f.write(content)
        f.write('-------设备参数-------\n\n')
        print('获取设备中……')
        devices = getDevice(res['serviceToken'], res['userId'])
        if isinstance(devices, list) is False:
            print('你没有小爱同学')
            sys.exit()
        for device in devices:
            deviceStr = "deviceID：{}\nsn：{} \n".format(
                device['deviceID'], device['serialNumber'])
            print(deviceStr)
            f.write(deviceStr)
