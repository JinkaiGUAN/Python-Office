# -*- coding: UTF-8 -*-
"""
@Project : ConcurrencyAndParallelism 
@File    : queue_thread.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 04/12/2021 16:33 
@Brief   : 
"""
import time
from collections import deque
from queue import Queue
from threading import Thread, Lock


def download(item):
    pass

def resize(itme):
    pass

def upload(item):
    pass


class MyQueue:
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            return self.items.popleft()


class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return
                yield item
            finally:
                self.task_done()

class Worker(Thread):
    def __init__(self, func, in_queue: MyQueue, out_queue: MyQueue):
        super(Worker, self).__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                time.sleep(0.01)
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1


if __name__ == '__main__':
    download_queue = MyQueue()
    resize_queue = MyQueue()
    upload_queue = MyQueue()
    done_queue = MyQueue()

    threads = [
        Worker(download, download_queue, resize_queue),
        Worker(resize, resize_queue, upload_queue),
        Worker(upload, upload_queue, done_queue)
    ]

    for thread in threads:
        thread.start()

    for _ in range(1000):
        download_queue.put(object())

    while len(download_queue.items) <= 1000:
        time.sleep(1)

    processed = len(done_queue.items)
    polled = sum(t.polled_count for t in threads)
    print(f'Processed {processed} items after polling {polled} times')

