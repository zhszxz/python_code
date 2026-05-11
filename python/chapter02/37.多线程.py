"""
多线程
"""
from threading import Thread, get_native_id, RLock
import os
import time


def coding(lock):
    for i in range(5):
        with lock:
            print(f"我正在敲代码{i},进程id：{os.getpid()},线程id：{get_native_id()}")
        time.sleep(1)


def music(lock):
    for i in range(5):
        with lock:
            print(f"我正在听音乐{i},进程id：{os.getpid()},线程id：{get_native_id()}")
        time.sleep(1)


if __name__ == '__main__':
    print(f"主进程开始了... 进程id:[{os.getpid()}]，线程id:[{get_native_id()}]")

    lock = RLock()

    p1 = Thread(target=coding, args=(lock,))
    p2 = Thread(target=music, args=(lock,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
