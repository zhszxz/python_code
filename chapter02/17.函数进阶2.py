# 函数可以作为另一个函数的参数

def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    return x / y


def calc(x, y, oper):
    return oper(x, y)


print(calc(10, 20, multiply))

# 匿名函数: lambda 参数列表 : 函数体
# 匿名函数的函数体只能有一行,会自动返回结果无需 return
out_line = lambda: print("-----------------------------------")
out_line()

add = lambda x, y: x + y
print(add(100, 200))

# 案例:将列表按字符串长度降序排序
data_list = ["C++", "C", "Python", "Jack", "PHP", "Java", "Go", "JavaScript", "Rust"]
print(data_list)

# key:排序规则函数 reverse:是否反转
data_list.sort(key=lambda s: len(s), reverse=True)
print(data_list)


# 案例: 计算n的阶乘
def jc(n):
    if n == 1:
        return 1
    return n * jc(n - 1)


print(jc(10))
