# 字典dict:存储 key - value 型数据的容器,key是唯一的
# 定义空字典
dict1 = {}
print(type(dict1))
dict2 = dict()
print(type(dict2))

# dict的key必须是不可变类型,不能是list,set,dict
dict = {"韩立": 688, "李化元": 560, "紫灵": 670, "梅凝": 511}
print(dict)

# 访问
print(dict["韩立"])

# 修改
dict["紫灵"] = 700
print(dict)

# dict常用方法

# 添加或修改
dict["玄骨"] = 500  # key不存在添加
print(dict)
dict["玄骨"] = 660  # key存在修改
print(dict)

# 查询
print(dict["玄骨"])
print(dict.get("玄骨"))

# keys:获取所有key
print(dict.keys())
# values:获取所有值
print(dict.values())
# items:获取所有键值对
print(dict.items())

# 删除
del dict["韩立"]
# pop:删除key并返回值
print(dict.pop("玄骨"))
print(dict)

# 遍历
for key in dict.keys():  # 遍历key获取value
    print(f"{key}: {dict[key]}")

for item in dict.items():  # 遍历items
    print(f"{item[0]}: {item[1]}")

for key, value in dict.items():  # 利用解包
    print(f"{key}: {value}")

# 案例:购物车管理系统，实现商品信息的增删改查
shopping_cart = {}
menu = """
########### 购物车系统 ##########
#         1. 添加购物车         #
#         2. 修改购物车         #
#         3. 删除购物车         #
#         4. 查询购物车         #
#         5. 退出购物车         #
###############################
"""
print("欢迎使用购物车管理系统 ~")
print(menu)

while True:
    choice = input("请选择要执行的操作(1-5):")
    match choice:
        case "1":
            goods_name = input("请输入商品名称:")
            if goods_name in shopping_cart:
                print("商品已存在,请重新选择")
                continue
            goods_price = float(input("请输入商品价格:"))
            goods_num = int(input("请输入商品数量:"))
            shopping_cart[goods_name] = {"price": goods_price, "num": goods_num}
            print("添加成功!")
        case "2":
            goods_name = input("请输入商品名称:")
            if goods_name not in shopping_cart:
                print("商品不存在,请重新选择")
                continue
            goods_price = float(input("请输入商品价格:"))
            goods_num = int(input("请输入商品数量:"))
            shopping_cart[goods_name] = {"price": goods_price, "num": goods_num}
            print("修改成功!")
        case "3":
            goods_name = input("请输入商品名称:")
            if goods_name not in shopping_cart:
                print("商品不存在,请重新选择")
                continue
            del shopping_cart[goods_name]
            print("删除成功!")
        case "4":
            for goods_name, goods_info in shopping_cart.items():
                print(f"商品名称:{goods_name} 商品价格:{goods_info["price"]} 商品数量:{goods_info["num"]}")
        case "5":
            print("欢迎下次光临!")
            break
        case _:
            print("输入有误!")
