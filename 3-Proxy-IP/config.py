# -*- coding: UTF-8 -*-
"""
@Project : 3-Proxy-IP 
@File    : config.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 04/09/2021 18:28 
@Brief   : 
"""


# 数据库配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DATABASE = 0

REDIS_OBJECT = 'PROXIES'

# 时间间隔配置
GETTER_PROXY = 60 * 60 * 24
VERIFY_PROXY = 60 * 60 * 10

# 服务器配置
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

# 测试地址
TEST_URL = 'https://www.baidu.com/'