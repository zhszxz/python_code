"""
线程池
"""

import time, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import get_native_id, RLock


def work(n, lock):
    with lock:
        print(f"线程{get_native_id()}正在执行任务{n}......")
    if n == 1:
        time.sleep(15)
    elif n == 2:
        time.sleep(10)
    else:
        time.sleep(1)
    return f'我是任务{n}的结果'


res_list = []


def callback(future):
    res_list.append(future.result())


# if __name__ == '__main__':
#     print("----------start-------------")
#     executor = ThreadPoolExecutor(3)
#     lock = RLock()
#     future_list = [executor.submit(work, i, lock) for i in range(1, 8)]
#     for future in future_list:
#         future.add_done_callback(callback)
#     for future in as_completed(future_list):
#         with lock:
#             print(future.result())
#     print('--------------------------')
#     print(res_list)
#     executor.shutdown(wait=True)
#     print("----------end-------------")

if __name__ == '__main__':
    print("----------start-------------")
    lock = RLock()
    with ThreadPoolExecutor(3) as executor:
        results = executor.map(work, range(1, 8), [lock] * 7)
        print(results)
        print(list(results))
