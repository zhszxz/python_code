# 闭包: 函数 + 它引用的外部变量
def outer():
    x = 10

    def inner():
        print(x)  # 使用外部变量

    return inner


f = outer()
f()  # 输出 10


# 案例: 计数器
def counter():
    count = 0

    def add():
        # nonlocal: 如果想修改外部函数变量,必须先声明
        nonlocal count
        count += 1
        return count

    return add


c = counter()

print(c())  # 1
print(c())  # 2
print(c())  # 3


# 装饰器: 增强函数功能的函数
def decorator(func):
    def wrapper():
        print("开始")
        func()
        print("结束")

    return wrapper


# 等价于 test = decorator(test)
@decorator
def test():
    print("执行 test")


test()


# 多层装饰器
def d1(func):
    def wrapper():
        print("d1")
        func()

    return wrapper


def d2(func):
    def wrapper():
        print("d2")
        func()

    return wrapper


@d1
@d2
def test():
    print("test")


test()

# 案例: 统计函数执行时间
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"耗时: {end - start}")
        return result

    return wrapper


@timer
def slow():
    time.sleep(1)


slow()
