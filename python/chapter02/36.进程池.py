import time

import os
from concurrent.futures import ProcessPoolExecutor, as_completed


def work(n):
    print(f"进程{os.getpid()}正在执行任务{n}......")
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
#     executor = ProcessPoolExecutor(3)
#     # submit: 提交任务
#     future_list = [executor.submit(work, i) for i in range(1, 8)]
#     for future in future_list:
#         # add_done_callback: 为 Future 添加一个回调函数,任务执行完成后自动调用
#         future.add_done_callback(callback)
#     # as_completed: 按照任务完成的顺序返回 Future
#     for future in as_completed(future_list):
#         print(future.result())
#     print('--------------------------')
#     print(res_list)
#     # shutdown: 关闭进程池，不再接受新任务，但是会继续执行完已提交的任务    wait=True：等待任务执行完
#     executor.shutdown(wait=True)
#     print("----------end-------------")

if __name__ == '__main__':
    print("----------start-------------")
    # with: 自动关闭进程池
    with ProcessPoolExecutor(3) as executor:
        # map: 批量提交任务，返回任务结果的生成器，获取结果的顺序与提交任务的顺序一致
        results = executor.map(work, range(1, 8))
        print(results)
        print(list(results))
