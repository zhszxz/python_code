"""
进程通信方式一：Queue
"""
import time
from multiprocessing import Process, Queue, Pipe


def test1(queue):
    for i in range(5):
        queue.put(i)
        print(f"生产者放入:{i}")
        time.sleep(1)


def test2(queue):
    for i in range(5):
        data = queue.get()
        print(f"消费者取出:{data}")
        time.sleep(0.5)


"""
进程通信方式二：Pipe
"""


def child(conn):
    conn.send("你好！我是子进程")
    print(f"子进程收到消息：{conn.recv()}")


if __name__ == '__main__':
    # q = Queue()
    # p1 = Process(target=test1, args=(q,))
    # p2 = Process(target=test2, args=(q,))
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()

    conn1, conn2 = Pipe()
    p = Process(target=child, args=(conn2,))
    p.start()
    print(f"父进程收到消息：{conn1.recv()}")
    conn1.send("你好！我是父进程")
    p.join()
