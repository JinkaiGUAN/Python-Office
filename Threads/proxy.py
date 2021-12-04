# -*- coding: UTF-8 -*-
"""
@Project : ConcurrencyAndParallelism 
@File    : proxy.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 04/12/2021 06:32 
@Brief   : 
"""
import typing as t
import time
from threading import Thread


def factorize(number: int) -> t.Generator:
    for i in range(1, number + 1):
        if number % i == 0:
            yield i


class FactorizeThread(Thread):
    def __init__(self, number: int):
        super(FactorizeThread, self).__init__()
        self.num = number

    def run(self):
        self.factors = list(factorize(self.num))


if __name__ == '__main__':
    # However, this kind of thread would not speed up this kind of problem compared to other languagaes due to GIL.
    start = time.time()

    threads = []
    numbers = [2139079, 1214759, 1516637, 1852285]
    for num in numbers:
        thread = FactorizeThread(num)
        thread.start()
        threads.append(thread)

    # wait for all of the threads to finish
    for thread in threads:
        thread.join()

    end = time.time()
    print(f'Time used is {end - start}')
