# 读取键盘输入:input("提示信息")
total = 10000
password = input("请输入密码:")
print(f"密码是{password}")
jine = input("请输入取款金额:")  # 无论键盘键入什么,input始终返回str
print(f"取款成功!账户余额:{total - int(jine)}")
