# -*- coding: UTF-8 -*-
"""
@Project : 3-Proxy-IP 
@File    : dispatch.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 04/09/2021 17:56 
@Brief   : 
"""
import time

from grasp_ip import proxy_fuc_list
from database import RedisClient
from verify import verify_multithreading
from api import app
import multiprocessing
from config import GETTER_PROXY, VERIFY_PROXY, SERVER_HOST, SERVER_PORT

redis_client_2 = RedisClient()  # 实例化数据库对象


class DispatchEngine:
    # 1. 调度获取代理模块
    def getter_proxy(self):
        while True:
            for func in proxy_fuc_list:
                proxies = func()
                for proxy in proxies:
                    print("Add {} into the database!".format(proxy))
                    redis_client_2.add(proxy)

            time.sleep(GETTER_PROXY)

    # 2. 调度检测模块
    def verify_proxy(self):
        while True:
            verify_multithreading()
            time.sleep(VERIFY_PROXY)

    # 3. 调度api模块
    def api_server(self):
        # app.run(debug=True, host='0.0.0.0', port=5000)
        app.run(host=SERVER_HOST, port=SERVER_PORT)

    def run(self):
        print('<------------------------- Grasp IPs ------------------------->')
        getter_proxy_process = multiprocessing.Process(target=self.getter_proxy)
        getter_proxy_process.start()

        print('<------------------------- Verify IPs ------------------------>')
        if redis_client_2.count() > 0:
            verify_proxy_process = multiprocessing.Process(target=self.verify_proxy)
            verify_proxy_process.start()

        print('<------------------------- Start API Server ------------------------->')
        api_server_process = multiprocessing.Process(target=self.api_server)
        api_server_process.start()


if __name__ == "__main__":
    dispatcher = DispatchEngine()
    dispatcher.run()
