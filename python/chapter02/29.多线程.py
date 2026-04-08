import threading
import time

"""
创建线程
"""

# def task():
#     print("子线程执行")
#
#
# # 创建线程
# t = threading.Thread(target=task)
#
# # 启动线程
# t.start()
#
# print("主线程执行")

"""
带参数的线程
"""

# def task(name):
#     print(f"执行任务: {name}")
#
#
# # args必须是元组
# t = threading.Thread(target=task, args=("任务1",))
# t.start()

"""
案例:多线程交替执行
"""

# def task(name):
#     for i in range(3):
#         print(f"{name} - {i}")
#         time.sleep(1)
#
#
# t1 = threading.Thread(target=task, args=("线程1",))
# t2 = threading.Thread(target=task, args=("线程2",))
#
# t1.start()
# t2.start()

"""
等待子线程执行完
"""

# def task():
#     time.sleep(2)
#     print("子线程执行完毕")
#
#
# t = threading.Thread(target=task)
# t.start()
#
# t.join()
# print("主线程执行完毕")

"""
线程安全问题
"""
# counter = 0
#
#
# def add():
#     global counter
#     for _ in range(100000):
#         counter += 1
#
#
# threads = []
#
# for i in range(10):
#     t = threading.Thread(target=add)
#     threads.append(t)
#     t.start()
#
# for t in threads:
#     t.join()
#
# print(counter)

"""
锁
"""
# lock = threading.Lock()
# count = 0
#
#
# def add():
#     global count
#     for _ in range(100000):
#         lock.acquire()
#         count += 1
#         lock.release()
#
#
# t1 = threading.Thread(target=add)
# t2 = threading.Thread(target=add)
#
# t1.start()
# t2.start()
#
# t1.join()
# t2.join()
#
# print(count)

"""
线程池
"""
from concurrent.futures import ThreadPoolExecutor


def task(n):
    time.sleep(1)
    return n * n


with ThreadPoolExecutor(max_workers=3) as pool:
    results = pool.map(task, [1, 2, 3, 4, 5])

print(list(results))
