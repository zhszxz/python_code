# 算数运算符
print(10 + 4)
print(10 - 4)
print(10 * 4)
print(10 / 4)  # 结果是浮点数
print(10 // 4)  # 整除,向下取整,java默认向0取整
print(10 % 4)
print(10 ** 4)  # 指数

# 赋值运算
num = 85
num += 10  # 95
print("num = ", num)
num -= 10  # 85
print("num = ", num)
num *= 10  # 850
print("num = ", num)
num /= 10  # 85.0
print("num = ", num)
num //= 10  # 8.0
print("num = ", num)
num %= 3  # 2.0
print("num = ", num)
num **= 3  # 8.0
print("num = ", num)

# 关系运算符
print(100 == 100)
print('100' == '100')
print(100 != 100)
print(100 > 100)
print(100 >= 100)
print(100 < 100)
print(100 <= 100)

# 逻辑运算符
num = int(input("请输入一个整数:"))
print(f"{num}在10-20之间吗?", num >= 10 and num <= 20)
print(f"{num}在10-20之间吗?", 10 <= num <= 20)
print(f"{num}不在10-20之间吗?", num < 10 or num > 20)
print(not True)
