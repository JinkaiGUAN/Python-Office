# -*- coding: UTF-8 -*-
"""
@Project : 3-Proxy-IP 
@File    : verify.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 03/09/2021 22:08 
@Brief   : 
"""
import requests
from database import RedisClient
import concurrent.futures
from config import TEST_URL


# TEST_URL = 'https://ww.baidu.com/'

redis_client = RedisClient()


def verify_proxy(proxy: str):
    """检查代理是否可用"""

    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }

    try:
        response = requests.get(url=TEST_URL, proxies=proxies, timeout=2)
        if response.status_code in [200, 206, 302]:
            # 代理score设置为20
            print("{} can be as a proxy to being used!".format(proxy))
            redis_client.max(proxy)
        else:
            # 代理减分
            print("The status code of {} is not so good!\tStatus code: {}".format(proxy, response.status_code))
            redis_client.decrease(proxy)
    except:
        print("Time out Error for {}!".format(proxy))
        redis_client.decrease(proxy)


def verify_multithreading():
    proxies = redis_client.all()

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as exector:
        for proxy in proxies:
            exector.submit(verify_proxy, proxy)


if __name__ == "__main__":
    # proxies = redis_client.all()
    #
    # for proxy in proxies:
    #     verify_proxy(proxy)
    verify_multithreading()
    # print(__name__)