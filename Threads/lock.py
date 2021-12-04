# -*- coding: UTF-8 -*-
"""
@Project : ConcurrencyAndParallelism 
@File    : lock.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 04/12/2021 16:06 
@Brief   : 
"""
from threading import Thread, Lock


class Counter:
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


class LockingCounter:
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset


def worker(sensor_index, how_many, counter: Counter):
    for _ in range(how_many):
        counter.increment(1)


if __name__ == '__main__':
    how_many = 10**5
    # counter = Counter()
    counter = LockingCounter()

    threads = []
    for i in range(5):
        thread = Thread(target=worker, args=(i, how_many, counter))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    expected = how_many * 5
    found = counter.count
    assert found == expected, f'We got different value in count {found} and {expected}'
