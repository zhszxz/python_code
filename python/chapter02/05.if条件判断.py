# 1.if单分支结构
socre = 688
if socre > 680:
    print("恭喜你进入清华学习")
    print("即将步入精彩的大学生活")
print("--------------------")

# 2.if ... else ... 双分支结构
year = int(input("请输入年份:"))
if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
    print(f"{year}是闰年")
else:
    print(f"{year}是平年")

# 3.if ... elif ... else ... 多分支结构
num = int(input("请输入整数:"))
if num > 0:
    print(f"{num}是正数")
elif num < 0:
    print(f"{num}是负数")
else:
    print(f"{num}是0")
