"""
继承Process类
"""

from multiprocessing import Process
import time


class CodingProcess(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        for i in range(10):
            print(f"{self.name}正在敲第{i}遍代码。。。")
            time.sleep(0.1)


class MusicProcess(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        for i in range(10):
            print(f"{self.name}正在听第{i}首歌。。。")
            time.sleep(0.1)


if __name__ == '__main__':
    p1 = CodingProcess('希特勒')
    p2 = MusicProcess('墨索里尼')
    p1.start()
    p2.start()
    p1.join()
    p2.join()
