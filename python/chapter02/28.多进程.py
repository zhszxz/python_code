"""
多进程
"""
import multiprocessing
import os
import time

# def coding():
#     for i in range(10):
#         print(f"正在敲第{i}遍代码!")
#         time.sleep(0.1)
#
#
# def music():
#     for i in range(10):
#         print(f"正在听第{i}首歌......")
#         time.sleep(0.1)


"""
多进程带参数
"""

# def coding(name, count):
#     print(f"p1进程开始了... pid:[{os.getpid()}], ppid:[{os.getppid()}]")
#     for i in range(count):
#         print(f"{name}正在敲第{i}遍代码!")
#         time.sleep(0.1)
#
#
# def music(name, count):
#     print(
#         f"p2进程开始了... pid:[{multiprocessing.current_process().pid}], ppid:[{os.getppid()}]")
#     for i in range(count):
#         print(f"{name}正在听第{i}首歌......")
#         time.sleep(0.1)


"""
退出子进程
"""


def work():
    print(f"子进程开始了... pid:[{os.getpid()}], ppid:[{os.getppid()}]")
    for i in range(10):
        print(f"子进程正在努力工作...")
        time.sleep(0.2)


if __name__ == '__main__':
    print(f"主进程开始了... pid:[{os.getpid()}], ppid:[{os.getppid()}]")
    # p1 = multiprocessing.Process(target=coding, args=("本拉登", 10))
    # p2 = multiprocessing.Process(target=music, kwargs={"name": "卡扎菲", "count": 20})

    # 默认情况下,主进程会等待子进程结束
    p1 = multiprocessing.Process(target=work)
    # 不让主进程等待子进程 方式一:守护进程
    # p1.daemon = True
    p1.start()
    # p2.start()

    time.sleep(1)
    print("主进程结束了...")

    # 不让主进程等待子进程 方式二:terminate
    p1.terminate()
