"""
守护进程
"""
import os
import time
from multiprocessing import Process


def monitor():
    while True:
        try:
            with open('./log/log.txt', 'r', encoding='utf-8') as f:
                lines = sum(1 for _ in f)
        except FileNotFoundError:
            lines = 0
        print(f'[守护进程]({os.getpid()}),log.txt共有{lines}行')
        time.sleep(1)


if __name__ == '__main__':
    print(f"主进程开始了... pid:[{os.getpid()}]")

    """
    守护进程特点:
    1. 守护进程会在主进程结束时自动终止,不会继续运行
    2. 守护进程不能创建子进程
    3. 守护进程中不能使用 join() 方法等待其他进程
    4. 守护进程的 daemon 属性必须在 start() 之前设置
    5. 守护进程退出时不会执行清理操作
    """
    p = Process(target=monitor, daemon=True)
    p.start()

    with open('./log/log.txt', 'a', encoding='utf-8') as f:
        for i in range(10):
            f.write(f'出师未捷身先死{i}\n')
            f.flush()
            time.sleep(1)

    print(f"主进程结束了... pid:[{os.getpid()}]")
