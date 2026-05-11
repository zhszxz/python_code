"""
多进程
"""
from multiprocessing import Process, current_process, Lock, RLock
import os
import time


# 1.演示多进程交替执行
def coding(name, count):
    print(f"{current_process().name}子进程开始了... pid:[{os.getpid()}], ppid:[{os.getppid()}]")
    for i in range(count):
        print(f"{name}正在敲第{i}遍代码!")
        time.sleep(0.1)


def music(name, count):
    print(f"{current_process().name}子进程开始了... pid:[{os.getpid()}], ppid:[{os.getppid()}]")
    for i in range(count):
        print(f"{name}正在听第{i}首歌......")
        time.sleep(0.1)


# 2.锁
def study(lock):
    """
    Lock锁的使用 方式一
        lock.acquire() 加锁
        lock.release() 释放锁

    问题:
        一旦出现异常,锁无法释放
    """
    try:
        for i in range(10):
            lock.acquire()
            lock.acquire()  # 演示可重入锁
            print("好好", end="")
            print("学习", end="")
            print("天天", end="")
            print("向上")
            lock.release()
            lock.release()  # 上锁几次就要释放几次
            time.sleep(1)
    finally:
        # 被 terminate 终止的进程,finally块不会执行
        print("我是p1的finally块")


def spell(lock):
    """
        Lock锁的使用 方式二
            with 关键字
            自动获取和释放锁,即使出现异常
        """
    for i in range(15):
        with lock:
            print("A", end="")
            print("B", end="")
            print("C", end="")
            print("D")
        time.sleep(1)


if __name__ == '__main__':
    print(f"主进程开始了... pid:[{os.getpid()}]")

    # 1.演示多进程交替执行
    """
    Process 类参数说明:
        - target: 要执行的目标函数,子进程将执行这个函数
        - args: 传递给 target 函数的位置参数,以元组形式传入,即使只有一个参数也需要加逗号
        - kwargs: 传递给 target 函数的关键字参数,以字典形式传入
        - name: 进程的名称,可选参数,默认为 "Process-N" 格式
        - daemon: 是否为守护进程,True/False,守护进程会在主进程结束时自动终止
    
    """
    # p1 = Process(target=coding, args=("本拉登", 10))
    # p2 = Process(target=music, kwargs={"name": "卡扎菲", "count": 20})
    #
    # p1.start()
    # p2.start()

    # 2.锁
    # # lock = Lock()  # 创建锁
    # lock = RLock()  # 创建可重入锁
    # p1 = Process(target=study, args=(lock,))
    # p2 = Process(target=spell, args=(lock,))
    # p1.start()
    # p2.start()
    # p1.join()  # 等待子进程执行完毕
    # p2.join()

    # 3.terminate
    lock = RLock()
    p1 = Process(target=study, args=(lock,))
    p2 = Process(target=spell, args=(lock,))
    p1.start()
    p2.start()
    time.sleep(5)
    print("主进程准备终止p1...")
    p1.terminate()  # 申请终止p1,可能不会立即终止
    print(p1.is_alive())
    print("主进程结束了...")
