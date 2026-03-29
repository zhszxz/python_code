# 集合set:无序,可修改,自动去重的容器
s = {0, 1, 1, 2, 10, 99, 99, 1000}
print(s)
print(type(s))

# 定义空set
s = {}  # 错误方式,实际是dict
print(type(s))
s = set()  # 正确方式
print(type(s))

# 常用方法
s = {100, 200, 300, 400, 500, 600, 700, 800}
print(s)

# add:添加元素
s.add(1200)
print(s)

# remove:删除元素,不存在则报错
s.remove(200)
print(s)

# pop:随机删除元素并返回
print(s.pop())
print(s)

# clear:清空set
s.clear()
print(s)

s1 = {'A', 'B', 'C', 'D', 'E', 'X', 'Y'}
s2 = {'C', 'E', 'Y', 'Z'}

# difference:求差集
print(s1.difference(s2))
print(s2.difference(s1))

# union:求并集
print(s1.union(s2))

# intersection:求交集
print(s1.intersection(s2))

# set操作案例
# 选修足球学生名单
football_set = {"王林", "曾牛", "徐立国", "遁天", "天运子", "韩立", "厉飞雨", "乌丑", "紫灵"}
# 选修篮球学生名单
basketball_set = {"张铁", "墨居仁", "王林", "姜老道", "曾牛", "王蝉", "韩立", "天运子", "李化元", "厉飞雨", "云露"}
# 选修法语学生名单
french_set = {"许木", "王卓", "十三", "虎咆", "姜老道", "天运子", "红蝶", "厉飞雨", "韩立", "曾牛"}
# 选修艺术学生名单
art_set = {"遁天", "天运子", "韩立", "虎咆", "姜老道", "紫灵"}

# 1. 找出同时选修了 法语 和 艺术 的学生
# 方式一: intersection
fa_set = french_set.intersection(art_set)
print(fa_set)

# 方式二: &
fa_set = french_set & art_set
print(fa_set)

# 2. 找出同时选修了所有四门课程的学生
all_set = football_set & basketball_set & french_set & art_set
print(all_set)

# 3. 找出选修了足球, 但是没有选修篮球的学生
# 方式一: difference
fnb_set = football_set.difference(basketball_set)
print(fnb_set)

# 方式二: -
fnb_set = football_set - basketball_set
print(fnb_set)

# 方式三: 集合推导式
fnb_set = {n for n in football_set if n not in basketball_set}
print(fnb_set)

# 4. 统计每一个学生选修的课程数量
# 获取学生名单
stu_set = football_set | basketball_set | french_set | all_set
print(stu_set)
# 获取每个学生选修的课程数量
all_list = [*football_set, *basketball_set, *french_set, *all_set]
for stu in stu_set:
    print(f"{stu} 选修了 {all_list.count(stu)} 门课程")
