# 作用域

# 定义全局变量
num = 100


def func_a():
    # 函数内尝试修改全局变量,实际上是重新定义了一个局部变量
    num = 10000
    print("func_a num = ", num)


func_a()
print("num = ", num)


def func_b():
    # 声明函数接下来使用的是全局变量 num
    global num
    # 此时就是修改全局变量
    num = 10000
    print("func_b num = ", num)


func_b()
print("num = ", num)


# 传参方式
def reg_stu(name, age, gender, city):
    print(f"注册成功, 姓名: {name}, 年龄: {age}, 性别: {gender}, 城市: {city}")
    return {"name": name, "age": age, "gender": gender, "city": city}


# 方式一: 位置参数,形参与实参顺序对应,数量一致
stu = reg_stu("张三", 18, "男", "北京")
print(stu)

# 方式二: 关键字参数,实参顺序无要求
stu = reg_stu(age=20, gender="女", city="北京", name="李慕婉")
print(stu)

# 传参方式三: 混合使用,要求位置参数在前, 关键字参数在后
stu = reg_stu("李慕婉", 20, gender="女", city="北京")
print(stu)


# 参数默认值
def reg_stu(name, age, gender="男", city="北京"):  # 为参数指定默认值
    print(f"注册成功, 姓名: {name}, 年龄: {age}, 性别: {gender}, 城市: {city}")
    return {"name": name, "age": age, "gender": gender, "city": city}


stu = reg_stu("王林", 20)
print(stu)

stu = reg_stu("李慕婉", 18, "女")
print(stu)

stu = reg_stu("韩立", 22, city="上海")
print(stu)


# 可变位置参数:使用 *参数名 来接收不定长的位置参数,这些参数最终被封装为元组
def calc_data(*args):
    print(type(args))
    min_data = min(args)
    max_data = max(args)
    avg_data = sum(args) / len(args)
    return min_data, max_data, round(avg_data, 1)


print(calc_data(2, 7, 9, 10, 45))


# 可变关键字参数:使用 **参数名 来接收不定长的关键字参数,这些参数最终被封装为字典
# 可变位置参数 与 可变关键字参数 同时存在, 可变位置参数 在前, 可变关键字参数 在后
def calc_data(*args, **kwargs):
    print(type(kwargs))
    min_data = min(args)
    max_data = max(args)
    avg_data = sum(args) / len(args)

    if kwargs.get("round") is not None:
        avg_data = round(avg_data, kwargs.get("round"))

    if kwargs.get("print"):
        print(f"计算出来的最小值: {min_data}, 最大值: {max_data}, 平均值:{avg_data}")

    return min_data, max_data, avg_data


print(calc_data(2, 7, 9, 10, 45, round=3, print=True))

print(calc_data(2, 7, 9, 10, 45, 73, 37, 93, 92, 111, 222, round=4, print=False))
