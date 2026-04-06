# 函数:组织好的,可复用的,实现特定功能的代码片段
import math


def out_line():
    print("----------------------------------")
    print("----------------------------------")


# 函数必须先定义再调用
out_line()


# 函数的参数和返回值
def circle_area(r):
    """
    计算圆的面积
    :param r: 半径
    :return: 圆面积
    """
    area = math.pi * r ** 2
    return area


def rectangle_area(l, w):
    """
    计算矩形面积
    :param l: 长
    :param w: 宽
    :return: 矩形面积
    """
    area = l * w
    return area


print(circle_area(5))
print(rectangle_area(20, 10))


# 函数的多返回值
def circle_area_len(r):
    area = math.pi * r ** 2
    l = 2 * math.pi * r
    return area, l  # 封装在元组中返回


res = circle_area_len(5)
print(type(res))
print(res)
