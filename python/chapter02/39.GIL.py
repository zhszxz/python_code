"""
GIL (Global Interpreter Lock) - 全局解释器锁

1. GIL概念:
   - GIL是CPython解释器中的一个互斥锁，确保同一时刻只有一个线程在执行Python字节码
   - 它不是Python语言的特性，而是CPython解释器的实现细节

2. GIL的作用:
   - 保证了解释器层面的线程安全
   - 简化了CPython的内存管理，特别是引用计数机制
   - 使得C扩展更容易编写，不需要考虑线程安全问题

3. GIL的影响:
   - CPU密集型任务: 线程执行前必须获取GIL，多线程无法真正并行，性能不会提升
   - I/O密集型任务: 多线程仍然有效，因为I/O操作会释放GIL
   - 多核CPU利用率: 单个Python进程无法充分利用多核优势

4. GIL的工作原理:
   - 线程获取GIL后才能执行Python代码
   - 执行一定时间片后主动释放GIL
   - 或者在I/O操作时释放GIL
   - 其他线程竞争获取GIL

5. 解决GIL限制的方法:
   - 使用multiprocessing模块创建多进程
   - 使用concurrent.futures.ProcessPoolExecutor
   - 使用C扩展释放GIL(如numpy)
   - 使用其他Python实现(Jython, IronPython)
   - Python 3.13+ 提供了无GIL的实验性选项

6. 实际建议:
   - I/O密集型: 使用threading或asyncio
   - CPU密集型: 使用multiprocessing或多进程池
   - 混合场景: 根据具体需求选择合适的并发模型
"""

import threading
import time
from multiprocessing import Process


# 示例1: 演示GIL对CPU密集型任务的影响
def cpu_bound_task(n):
    """CPU密集型任务"""
    count = 0
    for i in range(n):
        count += i * i
    return count


def thread_cpu_bound():
    """多线程执行CPU密集型任务"""
    start_time = time.time()

    t1 = threading.Thread(target=cpu_bound_task, args=(10 ** 7,))
    t2 = threading.Thread(target=cpu_bound_task, args=(10 ** 7,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    end_time = time.time()
    print(f"多线程CPU密集型耗时: {end_time - start_time:.4f}秒")


def process_cpu_bound():
    """多进程执行CPU密集型任务"""
    start_time = time.time()

    p1 = Process(target=cpu_bound_task, args=(10 ** 7,))
    p2 = Process(target=cpu_bound_task, args=(10 ** 7,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    end_time = time.time()
    print(f"多进程CPU密集型耗时: {end_time - start_time:.4f}秒")


# 示例2: 演示GIL对I/O密集型任务的影响
def io_bound_task():
    """I/O密集型任务"""
    time.sleep(1)  # 模拟I/O操作


def thread_io_bound():
    """多线程执行I/O密集型任务"""
    start_time = time.time()

    threads = []
    for _ in range(5):
        t = threading.Thread(target=io_bound_task)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()
    print(f"多线程I/O密集型耗时: {end_time - start_time:.4f}秒")


def process_io_bound():
    """多进程执行I/O密集型任务"""
    start_time = time.time()

    processes = []
    for _ in range(5):
        p = Process(target=io_bound_task)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end_time = time.time()
    print(f"多进程I/O密集型耗时: {end_time - start_time:.4f}秒")


if __name__ == "__main__":
    print("=== GIL影响演示 ===")

    print("\n--- CPU密集型任务 ---")
    thread_cpu_bound()
    process_cpu_bound()

    print("\n--- I/O密集型任务 ---")
    thread_io_bound()
    process_io_bound()

    print("\n结论:")
    print("- CPU密集型: 多进程优于多线程(GIL限制)")
    print("- I/O密集型: 多线程和多进程效果相近(I/O时释放GIL)")
