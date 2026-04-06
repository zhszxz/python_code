# 定义类
class Car:
    pass


# 创建对象
c1 = Car()
# 动态的为对象添加属性
c1.color = "red"
c1.brand = "BMW"
c1.name = "X5"
c1.price = 500000

print(c1)
print(c1.brand)
# 对象的所有属性,实际上是存储在字典 __dict__ 中
print(c1.__dict__)


class Car:
    # __init__ 初始化方法: 对象创建时自动调用
    # self: 表示当前创建的实例对象
    def __init__(self, c_color, c_brand, c_name, c_price):
        self.color = c_color
        self.brand = c_brand
        self.name = c_name
        self.price = c_price


c1 = Car("红色", "BMW", "X7", 800000)
print(c1.__dict__)

c2 = Car("白色", "奔驰", "E300", 450000)
print(c2.__dict__)


# 实例方法
class Car:
    def __init__(self, c_color, c_brand, c_name, c_price):
        self.color = c_color
        self.brand = c_brand
        self.name = c_name
        self.price = c_price

    # 定义在类中的函数就是方法
    def running(self):
        print(f"{self.brand} {self.name} 正在高速行驶中....")

    def total_cost(self, discount, rate=0.1):
        total_cost = self.price * discount + rate * self.price
        return total_cost


c1 = Car("红色", "BMW", "X7", 800000)

c1.running()
total1 = c1.total_cost(0.9, 0.1)
print("提车的总费用1为: ", total1)

total2 = c1.total_cost(0.9)
print("提车的总费用2为: ", total2)


# 魔法方法:python提供的类中以双下划线开头和结尾的特殊方法,如: __init__ , __str__ , __eq__
class Car:
    # 初始化方法
    def __init__(self, c_color, c_brand, c_name, c_price):
        self.color = c_color
        self.brand = c_brand
        self.name = c_name
        self.price = c_price

    # 对象的字符串表示
    def __str__(self):
        return f"{self.color} {self.brand} {self.name} {self.price}"

    # 对象判相等
    def __eq__(self, other):
        return self.color == other.color and self.brand == other.brand and self.name == other.name and self.price == other.price

    # 对象小于比较
    def __lt__(self, other):
        return self.price < other.price


c1 = Car("白色", "BYD", "汉", 180000)
print(c1)

c2 = Car("白色", "BYD", "汉", 180001)
print(c2)

print(c1 == c2)

print(c1 < c2)


# 实例属性 与 类属性
class Car:
    # 类属性 (所有实例对象共享)
    wheel = 4  # 轮胎数量
    tax_rate = 0.1  # 购置税税率

    def __init__(self, c_color, c_brand, c_name, c_price):
        # 实例属性
        self.color = c_color
        self.brand = c_brand
        self.name = c_name
        self.price = c_price


c1 = Car("白色", "BYD", "汉", 180000)
print(c1.brand)

# 通过实例对象查找属性,先查找实例属性,实例属性不存在,再查找类属性
print(c1.wheel)

# 通过类名访问类属性
print(Car.wheel)
