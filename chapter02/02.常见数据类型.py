# type():查看字面量或变量的数据类型
print(type(10))
print(type(3.14))
print(type("hello"))
print(type(True))
print(type(None))

num = -100
print(type(num))

# isinstance():判断字面量或变量是否是指定的类型
print(isinstance(num, int))
print(isinstance(num, bool))
print(isinstance(num, str))

# 字符串定义
# 1.使用单引号或双引号,两者是等价的
s1 = 'Hello'
s2 = "Python"
print(s1)
print(s2)
# 2.使用三引号定义多行字符串
s3 = """
白日依山尽
黄河入海流
欲穷千里目
更上一层楼
"""
print(s3)
# 3.转义字符
s4 = 'Let\'s go g2'
print(s4)
s5 = "Hello 的意思是\"你好\""
print(s5)
s6 = "\t欢迎大家学习python\n\t记得一键三连哟"
print(s6)

# 字符串拼接
# 1.使用任意个空格
s7 = "春宵苦短日高起" "," "从此君王不早朝"
print(s7)
# 2.使用+
name = "田所浩二"
age = 24
pro = "学生"
print(name + ":" + str(age) + "岁,是" + pro)  # python不能直接将非字符串与字符串拼接,必须显式转换

# 格式化字符串
# 方式一:占位符
msg = "大家好,我是%s,今年%s岁,是%s" % (name, age, pro)
print(msg)
# 方式二:f"..{变量名/表达式}.."
msg = f"大家好,我是{name},今年{age}岁,不是{pro}"
print(msg)
