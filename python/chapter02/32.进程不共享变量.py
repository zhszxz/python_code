"""
多进程是不共享内存的,也就不共享变量
"""
from multiprocessing import Process

num = 100


def task1():
    global num
    num += 10
    print(f"task1内,num最新值{num}")


def task2():
    global num
    num -= 10
    print(f"task2内,num最新值{num}")


if __name__ == '__main__':
    p1 = Process(target=task1)
    p2 = Process(target=task2)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(f"主进程,num最新值{num}")
