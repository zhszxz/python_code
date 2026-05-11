"""
property: 把方法当属性用
    @property 修饰get方法
    @get方法名.setter 修饰set方法
"""

# class Person:
#     def __init__(self, age):
#         self.__age = age
#
#     @property
#     def age(self):
#         return self.__age
#
#     @age.setter
#     def age(self, age):
#         self.__age = age


"""
扩展:类属性方式
"""


class Person:
    def __init__(self, age):
        self.__age = age

    def get_age(self):
        return self.__age

    def set_age(self, age):
        self.__age = age

    age = property(get_age, set_age)


if __name__ == '__main__':
    p = Person(10)
    print(p.age)
    p.age = 20
    print(p.age)
