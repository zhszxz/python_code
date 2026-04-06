"""
继承
"""


class Car:
    def __init__(self, brand, price):
        self.brand = brand
        self.price = price

    def run(self):
        print(f"{self.brand} 正在行驶")


# 子类
class ElectricCar(Car):
    def __init__(self, brand, price, battery):
        super().__init__(brand, price)  # 调用父类
        self.battery = battery

    def charge(self):
        print(f"{self.brand} 正在充电")


c = ElectricCar("BYD", 200000, 100)
c.run()
c.charge()

"""
多态
"""


class Dog:
    def speak(self):
        print("汪汪")


class Cat:
    def speak(self):
        print("喵喵")


def make_sound(animal):
    animal.speak()


make_sound(Dog())
make_sound(Cat())

"""
封装
"""


class User:
    def __init__(self, name, balance):
        self.name = name
        self.__balance = balance  # 私有属性

    def get_balance(self):
        return self.__balance

    def deposit(self, money):
        if money > 0:
            self.__balance += money


u = User("张三", 1000)
print(u.get_balance())

"""
类方法
"""


class Car:
    count = 0

    def __init__(self):
        Car.count += 1

    @classmethod
    def get_count(cls):
        return cls.count


c1 = Car()
c2 = Car()
print(Car.get_count())

"""
静态方法
"""


class MathTool:

    @staticmethod
    def add(a, b):
        return a + b


print(MathTool.add(3, 5))
