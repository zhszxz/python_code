# while循环打印十次:人生苦短,我用python
i = 0
while i < 10:
    print("人生苦短,我用python")
    i += 1
else:
    print("循环正常结束")

# 案例:统计1-100之间所有偶数之和
total = 0
i = 1
while i <= 100:
    if i % 2 == 0:
        total += i
    i += 1
print(f"1-100之间所有偶数的和是:{total}")

# 案例:猜数字
import random

random_number = random.randint(1, 100)  # 生成一个[1,100]的随机数
print("已生成[1,100]的随机数")
count = 0
while True:
    count += 1
    number = int(input("请输入猜测的数字:"))
    if number == random_number:
        print(f"恭喜你在第{count}次猜中了!")
        break
    if number > random_number:
        print("猜大了!")
    else:
        print("猜小了!")
