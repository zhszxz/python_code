# for循环遍历输入字符串
content = input("请输入字符串:")
for s in content:
    print(s)
else:
    print("遍历结束")

# 案例:计算1-100奇数的累加和
total = 0
# for n in range(1, 101):  # range:生成指定规则数字集
#     if n % 2 == 1:
#         total += n

# 方式二:通过步长
for n in range(1, 101, 2):
    total += n
print(f"1-100奇数的累加和是:{total}")

# 案例:计算100-500所有三的倍数的累加和
total = 0
for n in range(102, 501, 3):
    total += n
print(f"100-500所有3的倍数的累加和是:{total}")

# 案例:打印 m * n 的矩阵
m = int(input("请输入矩阵行数:"))
n = int(input("请输入矩阵列数:"))
for i in range(m):
    for j in range(n):
        print("*", end="")  # end:指定print打印以什么结束,默认是\n,设置为""表示不换行
    print()

# 案例:打印九九乘法表
for i in range(1, 10):
    for j in range(1, 10):
        if i >= j:
            print(f"{j} * {i} = {j * i}\t", end="")
    print()
