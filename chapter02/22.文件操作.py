# 文件操作

# 读文件
# 1.打开文件: open("文件路径", "打开模式", encoding="编码")
"""
    r   只读(默认),文件必须存在
    w   覆盖写,不存在会创建
    a   追加写
    b   二进制模式
    +   读写模式
"""
f = open("resources/望庐山瀑布.txt", "r", encoding="utf-8")

# 2.读取文件
content = f.read()  # read:读取所有或指定长度的内容
print(type(content))
print(content)
f.seek(0)  # 重置文件指针

content = f.readline()  # readline:读取一行
print(type(content))
print(content)
f.seek(0)

line_list = f.readlines()  # readlines:读取所有行
print(type(line_list))
print(line_list)

# 3.关闭文件
f.close()

# 写文件
f = open("resources/静夜思.txt", "w", encoding="utf-8")
f.write("静夜思(李白)\n")
f.write("\n")
f.write("窗前明月光，\n")
f.write("疑是地上霜。\n")
f.write("举头望明月，\n")
f.write("低头思故乡。\n")
f.close()

# 确保文件关闭
# 方式一: try ... finally ...
try:
    f = open("resources/静夜思.txt", "w", encoding="utf-8")
    f.write("静夜思(李白)\n")
    f.write("\n")
    f.write("窗前明月光，\n")
    i = 1 / 0
    f.write("疑是地上霜。\n")
    f.write("举头望明月，\n")
    f.write("低头思故乡。\n")
finally:
    print("关闭文件")
    f.close()

# 方式二: with
with open("resources/静夜思.txt", "a", encoding="utf-8") as f:
    f.write("疑是地上霜。\n")
    f.write("举头望明月，\n")
    f.write("低头思故乡。\n")
