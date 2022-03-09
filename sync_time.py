import os
import platform
import urllib.request
import time
import ssl
import datetime
import demjson3

# 全局禁用http请求ssl验证
ssl._create_default_https_context = ssl._create_unverified_context
time_url = "https://quan.suning.com/getSysTime.do"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62"
}

def int_to_str_zfill2(int:int):
    return str(int).zfill(2)

try:
    req = urllib.request.Request(time_url, headers=headers)
    time_response = urllib.request.urlopen(req)
    net_time_json = demjson3.decode(time_response.read().decode("utf-8"))

    time_offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    offset_hour = int(time_offset / 60 / 60 * -1)

    utc_time = datetime.datetime.strptime(net_time_json['sysTime2'], '%Y-%m-%d %H:%M:%S')

    tz = datetime.timezone(datetime.timedelta(hours=offset_hour))

    obj_tz_time = utc_time.astimezone(tz)
    # print(utc_time.astimezone(tz).hour,utc_time.astimezone(tz).minute, utc_time.astimezone(tz).second)
    # print(int(time.mktime(time.strptime(net_time_json['sysTime2'], '%Y-%m-%d %H:%M:%S'))))

    # windows
    if platform.system() == "Windows":
        # date 2021/09/21
        # time 12:12:12
        # pass
        # print("date %s/%s/%s"  % (utc_time.astimezone(tz).year,utc_time.astimezone(tz).month,utc_time.astimezone(tz).day))
        os.system("date %s/%s/%s" % (obj_tz_time.year, int_to_str_zfill2(obj_tz_time.month), int_to_str_zfill2(obj_tz_time.day)))
        os.system("time %s:%s:%s" % (int_to_str_zfill2(obj_tz_time.hour), int_to_str_zfill2(obj_tz_time.minute), int_to_str_zfill2(obj_tz_time.second))) 

    # macos
    elif platform.system() == "Darwin":
        # date 062614102014.30
        # 06是月，26是日，14是时，10是分，2014是年，30是秒
        # pass
        os.system("sudo date %s%s%s%s%s.%s" % (int_to_str_zfill2(obj_tz_time.month), int_to_str_zfill2(obj_tz_time.day), int_to_str_zfill2(obj_tz_time.hour), int_to_str_zfill2(obj_tz_time.minute), obj_tz_time.year, int_to_str_zfill2(obj_tz_time.second)))



    # linux
    elif platform.system() == "Linux":
        # date -s 06/18/2014
        # date -s 14:20:50
        os.system("date -s %s/%s/%s" % (int_to_str_zfill2(obj_tz_time.month), int_to_str_zfill2(obj_tz_time.day), obj_tz_time.year))
        os.system("date -s %s:%s:%s" % (int_to_str_zfill2(obj_tz_time.hour), int_to_str_zfill2(obj_tz_time.minute), int_to_str_zfill2(obj_tz_time.second)))
    else:
        print(platform.system())
        print("Other systems are not supported, only windows mac and linux are supported")
except:
    print("There is an error in the synchronization time, the network may not be accessible or the system is not supported")