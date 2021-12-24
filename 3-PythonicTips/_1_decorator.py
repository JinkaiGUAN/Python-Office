# -*- coding: UTF-8 -*-
"""
@Project : 3-PythonicTips 
@File    : _1_decorator.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 24/12/2021 14:01 
@Brief   : 
"""
from functools import wraps
from typing import Callable


# ----------------------------------------- 1. Function Decoration - 2 -----------------------------------------

def a_new_decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrap_function():
        print("I am doing some boring work before executing a_func()")
        func()
        print("I am doing some boring work after executing a_func()")

    return wrap_function


@a_new_decorator
def a_function_requiring_decoration():
    """Hey yo! Decorate me!"""
    print("I am the function which needs some decoration to remove my foul smell")


# You might found that the function name is `a_function_requiring_decoration`, this is because we use decorator
# `wraps`. If you do not use it, the name is `wrap_function`, and all docstring will be rewritten by function
# `wrap_function`.
print(a_function_requiring_decoration.__name__)


# ----------------------------------------- 1. Function Decoration - 2 -----------------------------------------
def decorator_name(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not can_run:
            return "Function will not run"
        return f(*args, **kwargs)

    return decorated


@decorator_name
def func():
    return ("Function is running")


can_run = True
print(func())
# Output: Function is running

can_run = False
print(func())
# Output: Function will not run


# ----------------------------------------- 2. Application -----------------------------------------
# 1. Authorization: https://www.runoob.com/w3cnote/python-func-decorators.html

# 2. Logging
def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)

    return with_logging


@logit
def addition_func(x):
    """Do some math."""
    return x + x


result = addition_func(4)
# Output: addition_func was called


# ----------------------------------------- 3. Function Decorator with args -----------------------------------------
def logit(logfile='out.log'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)
            # 打开logfile，并写入内容
            with open(logfile, 'a') as opened_file:
                # 现在将日志打到指定的logfile
                opened_file.write(log_string + '\n')
            return func(*args, **kwargs)

        return wrapped_function

    return logging_decorator


@logit()
def myfunc1():
    pass


myfunc1()


# Output: myfunc1 was called
# 现在一个叫做 out.log 的文件出现了，里面的内容就是上面的字符串

@logit(logfile='func2.log')
def myfunc2():
    pass


myfunc2()
# Output: myfunc2 was called
# 现在一个叫做 func2.log 的文件出现了，里面的内容就是上面的字符串


# ----------------------------------------- 4. Decorator Class -----------------------------------------

class logit(object):
    def __init__(self, logfile='out.log'):
        self.logfile = logfile

    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)
            # 打开logfile并写入
            with open(self.logfile, 'a') as opened_file:
                # 现在将日志打到指定的文件
                opened_file.write(log_string + '\n')
            # 现在，发送一个通知
            self.notify()
            return func(*args, **kwargs)

        return wrapped_function

    def notify(self):
        # logit只打日志，不做别的
        pass


# Use logit
@logit()
def myfunc1():
    pass


class email_logit(logit):
    '''
    一个logit的实现版本，可以在函数调用时发送email给管理员
    '''

    def __init__(self, email='admin@myproject.com', *args, **kwargs):
        self.email = email
        super(email_logit, self).__init__(*args, **kwargs)

    def notify(self):
        # 发送一封email到self.email
        # 这里就不做实现了
        pass

