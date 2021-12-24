# -*- coding: UTF-8 -*-
"""
@Project : 3-Proxy-IP 
@File    : database.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 03/09/2021 18:21 
@Brief   : 
"""
import random
from config import REDIS_HOST, REDIS_PORT, REDIS_OBJECT, REDIS_DATABASE
import redis


class RedisClient:
    """Database to get ip."""

    def __init__(self, host: str = REDIS_HOST, port:int =REDIS_PORT, db: int=REDIS_DATABASE):
        """Connect to the redis database.

        Args:
            host ():
            port ():
            db ():
        """
        self.db = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def exists(self, proxy: str):
        """判断传入的代理是否存在

        Args:
            proxy (str): proxy.

        Returns:
            - True: the proxy is in the database.
            - False: the proxy is not in the database.
        """
        return not self.db.zscore(REDIS_OBJECT, proxy) is None

    def add(self, proxy: str, score: int = 20):
        """Add proxy into the database and set the initial score equal to 10.

        Args:
            proxy (str): The proxy.
            score (int): The score.

        Returns:
            1 - 表示写入一个代理
            None - 表示没有写入数据， 一般是数据已经存在数据库
        """
        if not self.exists(proxy): # if the database does not include the identified proxy
            return self.db.zadd(name=REDIS_OBJECT, mapping={proxy: score})

    def random(self):
        """随机选择代理

        - 尝试获取满分代理
        - 尝试获取最低分到最高分中间代理的数据
        - 查询不到数据，， 提示没有数据
        """
        # 1. 尝试获取满分代理
        best_proxies = self.db.zrangebyscore(REDIS_OBJECT, min=40, max=100)
        if len(best_proxies):
            return random.choice(best_proxies)

        # 尝试获取最低分到最高分中间代理的数据
        less_better_proxies = self.db.zrangebyscore(name=REDIS_OBJECT, min=1, max=40)
        if len(less_better_proxies):
            return random.choice(less_better_proxies)

        return 'No proxy can be used'

    def decrease(self, proxy: str):
        """传入一个代理， 如果检测不过关， 那么评分执行减分操作"""
        self.db.zincrby(name=REDIS_OBJECT, amount=-2, value=proxy)
        score = self.db.zscore(name=REDIS_OBJECT, value=proxy)
        if score <= 0:
            self.db.zrem(REDIS_OBJECT, proxy)

    def max(self, proxy):
        """传入一个代理， 如果检测过关， 将代理设置为40"""
        return self.db.zadd(name=REDIS_OBJECT, mapping={proxy: 40})

    def count(self):
        """数据库中所有代理的数量"""
        return self.db.zcard(name=REDIS_OBJECT)

    def all(self):
        """获取所有代理"""
        proxies = self.db.zrangebyscore(name=REDIS_OBJECT, min=1, max=100)
        if proxies:
            return proxies
        else:
            return None

    def count_for_num(self, num: int):
        """指定数量获取代理。"""
        all_proxies = self.all()
        if all_proxies:
            return random.sample(all_proxies, k=num)


if __name__ == "__main__":
    redis_client = RedisClient()
    proxies = [
        '123.171.42.85:3256', '163.125.29.74:8118', '182.84.145.167:3256',
        '106.45.104.208:3256', '117.35.255.154:3000',
        '183.116.200:8118', '111.225.153.182:3256', '106.45.104.52:3256',
        '163.125.222.223:8118', '27.191.60.58:3256', '47.104.15.198:80',
    ]

    # for proxy in proxies:
        # print(redis_client.add(proxy))
    # print(redis_client.random())
    # redis_client.decrease('123.171.42.85:3256')
    # redis_client.max('123.171.42.85:3256')
    # print(redis_client.count())
    print(redis_client.count_for_num(3))