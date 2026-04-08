"""
继承
"""


# 师傅类
class Master:
    def __init__(self):
        self.kongfu = "[古法摊煎饼果子配方]"

    def make_cake(self):
        print(f"运用{self.kongfu}制作煎饼果子")


# 学校类
class School(object):
    def __init__(self):
        self.kongfu = "[黑马AI煎饼果子配方]"

    def make_cake(self):
        print(f"运用{self.kongfu}制作煎饼果子")


# 徒弟类
class Prentice(Master, School):  # 多继承
    def __init__(self):
        self.kongfu = "[自创独家煎饼果子配方]"

    def make_cake(self):
        print(f"运用{self.kongfu}制作煎饼果子")

    def make_master_cake(self):
        # 访问父类方式一:super 按照父类顺序依次查找
        super().__init__()
        super().make_cake()

    def make_school_cake(self):
        # 访问父类方式二:父类名.成员 可以精确访问
        School.__init__(self)
        School.make_cake(self)


xm = Prentice()
xm.make_cake()

xm.make_master_cake()
xm.make_school_cake()

# mro机制: Prentice -> Master -> School -> object
print(Prentice.__mro__)
Prentice.mro()

print("-" * 30)

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

print("-" * 30)

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

print("-" * 30)

"""
抽象类
"""


# 包含抽象方法的类就是抽象类,也叫接口
class AC:
    # 空实现的方法就是抽象方法
    def cool_wind(self):
        """制冷"""
        pass

    def hot_wind(self):
        """制热"""
        pass

    def swing_l_r(self):
        """左右摆风"""
        pass


class XiaoMiAC(AC):
    def cool_wind(self):
        print("小米空调核心制冷技术")

    def hot_wind(self):
        print("小米空调核心制热技术")

    def swing_l_r(self):
        print("小米空调正在左右摆风")


class GeLiAC(AC):
    def cool_wind(self):
        print("格力空调核心制冷技术")

    def hot_wind(self):
        print("格力空调核心制热技术")

    def swing_l_r(self):
        print("格力空调正在左右摆风")


xm = XiaoMiAC()
gl = GeLiAC()
xm.cool_wind()
xm.hot_wind()
xm.swing_l_r()

gl.cool_wind()
gl.hot_wind()
gl.swing_l_r()

print("-" * 30)

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

print("-" * 30)

"""
静态方法
"""


class MathTool:

    @staticmethod
    def add(a, b):
        return a + b


print(MathTool.add(3, 5))
