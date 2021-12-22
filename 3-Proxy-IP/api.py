# -*- coding: UTF-8 -*-
"""
@Project : 3-Proxy-IP 
@File    : api.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 04/09/2021 17:29 
@Brief   : 
"""

import flask
from flask import request  # 获取地址中查询参数
from flask import jsonify  # 把对象转换成字符串
from database import RedisClient


app = flask.Flask(__name__)
redis_client = RedisClient()


@app.route('/')
def index():
    """视图函数只能返回一个字符串"""
    return '<h2>Welcome to the Proxy Pool!</h2>'


@app.route('/get')
def get_proxy():
    """随机获取一个代理"""
    return redis_client.random()


@app.route('/getcount')
def get_any_proxies():
    """获取指定数量代理"""
    num = request.args.get('num', '')
    if not num:
        num = 1
    else:
        num = int(num)

    proxies = redis_client.count_for_num(num)
    return jsonify(proxies)  # 序列化操作


@app.route('/getnum')
def get_proxy_number():
    """获取代理数量"""
    return 'There are {} proxies can be used!'.format(redis_client.count())


@app.route('/getall')
def get_all_proxy():
    """获取所有代理"""
    all_proxies = redis_client.all()

    return jsonify(all_proxies)


if __name__ == "__main__":
    # 实例化一个app
    app.run()
