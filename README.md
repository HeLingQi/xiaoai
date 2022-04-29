# 小爱音箱降级 #

## # 前言

##### 目前程序只适用此版本（见下图）。降级请勿大版本降级，如15 降到12，小米关闭了部分接口，可能导致小爱变砖。

![产品](https://p3.toutiaoimg.com/origin/2b28e00034d22d5c3cb25 "产品")


## #1 配置user.ini 文件 ##

user 对应你的小米账号
pwd 对应你的密码

配置前请确认你user.ini 是否存在，如不存在则无法继续下一步。

## #2 运行xiaoai-cookie.exe ##

**进入文件所在的文件夹下，选择空白处，然后按住 shift + 鼠标右键，选择“在此处打开powershell 窗口”**

运行 ```./xiaoai-cookie.exe```

一般来说，一次运行即可，如果不在常用地登录，可能会出现验证码或其他无法登录情况。
这个功能目前还没设计，暂时不做开发，留待后续填坑。

运行完成后，会在同一路径下生成一个 ``xiaoai-res.txt `` 文件，一般包含这些信息

```
    -------账号参数-------
    serviceToken：sXEJMjSxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxCP807vgDIiGmi8o+c3ORITf57CvDWs9JBW2Zodvd8EaoqrSWKNe3c1z/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx==
    userId：10100000x 
    cUserId:52Dxxxxxxxxxxx
    -------设备参数-------
    deviceID：xxxx50-e4e5-xxxx-xxxx-57faef904889
    sn：xxxx/8823xxx 
``` 

如果你家里有多台小爱同学，可能设备会参数有多个，请通过确认SN参数，确认你要降级的设备。

## #3 配置 ota.ini 文件 ##

打开 ` xiaoai-res.txt ` 文件，将对应参数一一复制到 ` ota.ini ` 里，注意serviceToken 参数后的等号要保留。

然后运行 ` ./xiaoai-ota.exe `，如果返回以下内容则表示成功

```
{
    "code":0,"message":"Success","data":""
}
```

其他内容则表示需要检测上述步骤。

## # 固件可选版本 
对应 `` ota.ini `` 文件 ``version`` 参数


 - mico_all_f86a5_1.44.4.bin
 - mico_all_c731c_1.52.1.bin
 - mico_all_9d15e_1.54.13.bin
