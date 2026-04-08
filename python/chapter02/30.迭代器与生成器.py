"""
迭代器: 一个可以被 next() 不断取值的对象
"""
import sys

nums = [1, 2, 3]

it = iter(nums)  # 获取迭代器

print(next(it))  # 1
print(next(it))  # 2
print(next(it))  # 3
# print(next(it))  # 报错 StopIteration

print("-" * 30)

"""
自定义迭代器
    1.重写__iter__() 方法: 返回自身
    2.重写__next__() 方法: 每次调用返回下一个值，没有就抛出 StopIteration
"""


class MyIterator:
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.end:
            self.current += 1
            return self.current - 1
        else:
            raise StopIteration


it = MyIterator(1, 6)

for x in it:
    print(x)

print("-" * 30)

"""
生成器
    按需生成数据的迭代器,不会一次生成全部数据,使用一个,生成一个,节省内存
    实现方式:
        1.推导式
        2.yield
"""

# 推导式
my_generator = (x for x in range(1, 6))
print(type(my_generator))

print(next(my_generator))  # 1
print(next(my_generator))  # 2
for x in my_generator:  # 3 4 5
    print(x)

# 验证生成器可以减少内存占用
my_list = [x for x in range(1, 10000000)]
my_gt = (x for x in range(1, 10000000))
print(f"my_list 内存占用: {sys.getsizeof(my_list)}")
print(f"my_gt 内存占用: {sys.getsizeof(my_gt)}")

print("-" * 30)

"""
yield 做了哪些事?
    1.返回一个值
    2.暂停函数执行
    3.保存现场
"""


def my_func():
    for x in range(1, 6):
        yield x


my_gt2 = my_func()
print(type(my_gt2))
print(next(my_gt2))
for x in my_gt2:
    print(x)
