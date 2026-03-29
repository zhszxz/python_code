import re

s1 = "18809090000是我的手机号, 你记住了吗? 我的另一个手机号是18800008888，QQ号是177998992你记住了吗?"
s2 = "我的手机号是18809090000, 你记住了吗? 我的另一个手机号是18800008888，QQ号是177998992你记住了吗?"

# match: 从字符串开头匹配,返回match对象
result = re.match(r"1[3-9]\d{9}", s1)
print(result.group())
result = re.match(r"1[3-9]\d{9}", s2)
print(result)

# search: 从字符串任意位置匹配,返回第一个匹配的match对象
result = re.search(r"1[3-9]\d{9}", s1)
print(result.group())
result = re.search(r"1[3-9]\d{9}", s2)
print(result.group())

# findall: 从字符串任意位置匹配,返回所有匹配结果的list
result = re.findall(r"1[3-9]\d{9}", s1)
print(type(result))
result = re.findall(r"1[3-9]\d{9}", s2)
print(result)
