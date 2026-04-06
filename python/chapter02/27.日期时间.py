"""
datetime 模块核心类：

date	    只表示日期（年-月-日）
time	    只表示时间（时:分:秒）
datetime	日期 + 时间（最常用）
timedelta	时间差
"""

from datetime import datetime, timedelta

# 1.获取当前时间
now = datetime.now()
print(now)

# 2.创建指定日期时间对象
dt = datetime(2026, 3, 27, 10, 30, 0)
print(dt)

# 3.获取日期时间的部分
print(now.year)  # 年
print(now.month)  # 月
print(now.day)  # 日
print(now.hour)  # 时
print(now.minute)  # 分
print(now.second)  # 秒

# 4.格式化时间
s = now.strftime("%Y %m %d %H:%M:%S")  # 时间 -> 字符串
print(s)
dt = datetime.strptime(s, "%Y %m %d %H:%M:%S")
print(dt)

# 5.时间运算

# 加 1 天
print(now + timedelta(days=1))
# 减 2 小时
print(now - timedelta(hours=2))
# 时间差计算
t1 = datetime(2026, 3, 27)
t2 = datetime(2026, 3, 20)
delta = t1 - t2
print(delta.days)  # 7

# 6.时间戳

# 时间转时间戳(秒级)
ts = now.timestamp()
print(ts)
# 时间戳转时间
dt = datetime.fromtimestamp(ts)
print(dt)
