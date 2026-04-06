import json

# 序列化
data = {
    "name": "Tom",
    "age": 20,
    "skills": ["Python", "Java"]
}

json_str = json.dumps(data)
print(json_str)

# 反序列化
data = json.loads(json_str)
print(data)
print(type(data))  # dict

# 对象写入json文件
user = {
    "name": "张三",
    "age": 18,
    "gender": "男",
    "hobbies": ["reading", "swimming"]
}

with open("resources/user.json", "w", encoding="utf-8") as f:
    # ensure_ascii: 默认为True, 会将非ASCII字符进行转义; False, 非ASCII码保留原样输出
    # indent: 会在输出的json数据中添加缩进(格式化)
    json.dump(user, f, ensure_ascii=False, indent=2)

# json文件解析为对象
with open("resources/user.json", "r", encoding="utf-8") as f:
    user = json.load(f)
    print(type(user))
    print(user)
