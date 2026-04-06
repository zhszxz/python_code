# 操作csv
# 1.文件操作原始方式
import csv

with open("csv_data/01.csv", "w", encoding="utf-8") as f:
    f.write("姓名,年龄,性别,爱好\n")  # 写入表头
    f.write("小王,18,男,'football,Java'\n")  # 写入数据
    f.write("小李,18,女,Python\n")
    f.write("小张,18,男,C++\n")
    f.write("小王,20,男,Go\n")

with open("csv_data/01.csv", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())

# 2.csv模块
with open("csv_data/02.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, ["姓名", "年龄", "性别", "爱好"])
    writer.writeheader()  # 写入表头
    writer.writerow({"姓名": "小王", "年龄": 18, "性别": "男", "爱好": "football,Java"})  # 写入行数据
    writer.writerow({"姓名": "小李", "年龄": 18, "性别": "女", "爱好": "Python"})
    writer.writerow({"姓名": "小张", "年龄": 18, "性别": "男", "爱好": "C++"})
    writer.writerow({"姓名": "小杨", "年龄": 20, "性别": "男", "爱好": "Go"})

with  open("csv_data/02.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for line in reader:
        print(line)
