# 列表list:元素有序,可重复,有索引,python列表可以存储不同类型的元素
s = [56, 78, 91, 2.718, 3.14, 6.02, "Hello", "abc", True]
print(type(s))

# 访问
print(s[8])  # 通过正向索引
print(s[-1])  # 通过反向索引

# 修改
s[7] = "python"
print(s)

# 遍历
for item in s:
    print(item)

# 删除
del s[-4]
print(s)

# 切片操作:s[起始索引:结束索引:步长] 获取一个包含元素 s[起始索引,结束索引) 的list,步长默认为1
s = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
print(s)
print(s[0:5:1])
print(s[0:5:])
print(s[0:5])
print(s[:5])  # 都是等价的
print(s[1:-2:2])  # 两种索引混用

# list 的常用方法
s = [56, 90, 88, 65, 90, 100, 209, 72, 145]
# append:在列表尾部追加元素
s.append(108)
print(s)
# insert:在指定索引处插入元素
s.insert(2, 80)
print(s)
# remove:删除列表中第一个匹配上的元素
s.remove(90)
print(s)
# pop:删除并返回指定索引的元素,默认删尾元素
s.pop(1)
print(s)
# sort:排序,要求list元素是同类型
s.sort()
print(s)
# reverse:反转list元素
s.reverse()
print(s)

# 案例:用列表存储键盘输入的10个int,进行排序,计算它们的最大,最小,平均值
s = []
for i in range(10):
    s.append(int(input("请输入一个int:")))
print(s)
s.sort()
print(s)
print(f"最大值:{s[-1]}")
print(f"最大值:{max(s)}")
print(f"最小值:{s[0]}")
print(f"最小值:{min(s)}")
print(f"平均值:{sum(s) / len(s)}")

# 案例:合并两个list并去除其中的重复元素
num_list1 = [19, 23, 54, 64, 875, 20, 109, 232, 123, 54]
num_list2 = [55, 80, 72, 35, 60, 123, 54, 29, 91]

# 解包:将容器解开为一个个元素
num_list = [*num_list1, *num_list2]

new_list = []

for item in num_list:
    if item not in new_list:
        new_list.append(item)

print(new_list)

# 案例:生成[1,20]的平方列表
num_list = []
# 方式1:循环
for i in range(1, 21):
    num_list.append(i ** 2)
print(num_list)

# 方式2:列表推导式 -> 按照规则快速生成列表
num_list = [i ** 2 for i in range(1, 21)]
print(num_list)

# 案例:提取一个列表的所有偶数,计算其平方组成新列表
num_list = [12, 32, 45, 77, 80, 92, 33, 57, 97, 98, 110, 111, 122]
new_list = [i ** 2 for i in num_list if i % 2 == 0]
print(new_list)
