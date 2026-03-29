# match ... case
day = input("请输入星期数(1-7):")
match day:
    case "1":
        print("周一:工作会议日")
    case "2":
        print("周二:学习培训日")
    case "3":
        print("周三:项目开发日")
    case "4":
        print("周四:代码审查日")
    case "5":
        print("周五:总结规划日")
    case "6" | "7":
        print("周末:休息日")
    case _:
        print("输入有误")

# 案例:实现简易计算器
n1 = float(input("请输入操作数1:"))
n2 = float(input("请输入操作数2:"))
oper = input("请输入运算符:")
match oper:
    case "+":
        print(f"{n1} + {n2} = {n1 + n2}")
    case "-":
        print(f"{n1} - {n2} = {n1 - n2}")
    case "*":
        print(f"{n1} * {n2} = {n1 * n2}")
    case "/" if n2 != 0:
        print(f"{n1} / {n2} = {n1 / n2}")
    case _:
        print("非法的操作!")
