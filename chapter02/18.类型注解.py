# 不使用类型注解,python解释器会自动推断
a = 596
score = 98.5
hobby = "Python"
flag = True
pic = None

names = ["A", "C", "E", 100]
phones = {"13309091111", "15209101902", "18809019201"}
options = {"count": 2, "total": 10}
goods = ("手机", 6999, 1)

names.append(10010.0)

print(names)

# 使用类型注解
a2: int = 596
score2: float = 98.5
hobby2: str = "Python"
flag2: bool = True
pic2: None = None

names2: list[str | int] = ["A", "C", "E"]
phones2: set[str] = {"13309091111", "15209101902", "18809019201"}
options2: dict[str, int] = {"count": 2, "total": 10}
goods2: tuple[str, int, int] = ("手机", 6999, 1)

names2.append("X")
names2.append(10010)
# 类型注解只是提示不是约束,不会改变python动态类型特性
names2.append(10010.0)


# 函数类型注解
def circle_area_len(r: float) -> tuple[float, float]:
    return round(3.14 * r ** 2, 2), round(2 * 3.14 * r, 2)


print(circle_area_len(8.5))
