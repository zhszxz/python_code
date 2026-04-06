# 字符串str:字符的容器,不可变,有序,可迭代
s = "Hello-Python"
print(type(s))

# 访问
print(s[5])  # 正向索引
print(s[-7])  # 反向索引

# 字符串不可变, 'str' object does not support item assignment
# s[5] = "X"

# 遍历,python中没有字符,长度为1仍是字符串
for i in s:
    print(f"type:{type(i)}, value:{i}")

# 切片,与list基本一致
print(s[0:5:1])
print(s[:5:1])
print(s[:5:])
print(s[:5])

print(s[6:12:1])
print(s[6::1])

# 负步长的作用:从后往前截取字符串
print(s[-1:-7:-1])
print(s[::-1])  # 反转字符串

# str常用方法
s = 'Hello_World_Hello_Python'

# find:查找子串第一次出现的索引,不存在返回-1
index = s.find('_')
print(index)

# count:统计子串出现次数
print(s.count('o'))

# upper:转大写
print(s.upper())

# lower:转小写
print(s.lower())

# split:按指定子串分割字符串,返回list
list = s.split('_')
print(list)

# strip:去除头尾空字符或指定子串
print(s.strip('H'))

# replace:替换子串
print(s.replace('_', '-'))

# startswith/endswith:判断字符串是否以指定子串开头/结尾
print(s.startswith("Hello"))
print(s.endswith("Python"))

# 案例:验证邮箱,需要包含一个 '@' 和至少一个 '.'
mail = input("请输入邮箱:")
if mail.count('@') == 1 and '.' in mail:
    print(f"{mail}是合法的邮箱")
else:
    print(f"{mail}是非法的邮箱")

# 案例:接收输入的10个字符串,转大写反转后存在列表中后输出
str_list = []
for i in range(10):
    str_list.append(input("请输入str:").upper()[::-1])

for s in str_list:
    print(s)
