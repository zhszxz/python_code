"""
Queue
"""
import time
from multiprocessing import Queue, Process

q1 = Queue(3)

# put: 向队列中添加数据,默认是阻塞的,可指定阻塞时间
q1.put(10)
q1.put(20)
q1.put(30)
# q1.put(40, timeout=2)

# full: 判断队列是否已满
print(q1.full())

# get: 从队列中获取数据
print(q1.get())
print(q1.get())
print(q1.get())

# empty: 判断队列是否为空
print(q1.empty())

# qsize: 获取队列中数据个数
print(q1.qsize())

q1.put(10)
q1.put(20)
q1.put(30)
# put_nowait: 向队列中添加数据,如果队列已满,则添加失败
q1.put_nowait(40)


def test(queue):
    queue.put('故垒西边，人道是三国周郎赤壁')
    while not queue.empty():
        print(queue.get())


if __name__ == '__main__':
    q1 = Queue(2)
    q1.put('大江东去浪淘尽')
    q1.put('千古风流人物')
    print(q1.full())

    p = Process(target=test, args=(q1,))
    p.start()

    time.sleep(3)

    print(f'主进程取出一个元素：{q1.get()}')
