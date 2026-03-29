# 元组tuple:元组是不可变的序列,类似list但是无法修改
t1 = (80, 95, 78, 50, 75, 80, 85, 20)
print(type(t1))
print(t1)

# 访问
print(t1[0])
print(t1[-1])

# 修改:TypeError: 'tuple' object does not support item assignment
# t1[0] = 100

# 切片
print(t1[:5])

# count:统计元素出现次数
print(t1.count(80))

# index:统计第一次出现的索引,不存在则报错
print(t1.index(80))

# 单元素的元组,为避免歧义,必须加 ','
t2 = (100,)
print(type(t2))

# 组包与解包
t1 = (5, 7, 9, 1, 13)  # 定义元组就是组包
t1 = 5, 7, 9, 1, 13  # 括号可以省略

# 基础解包,变量数需与元组长度一致
a, b, c, d, e = t1
print(a, b, c, d, e)

# * :收集未知数量的元素,返回list
first, *other, last = t1
print(type(other))
print(other)

# 案例:交换元素
a, b = 10, 20
# 隐含了组包和解包的过程
a, b = b, a
print(a, b)