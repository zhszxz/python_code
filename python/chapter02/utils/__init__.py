# 含有 __init__.py 的文件夹就是一个软件包
# 描述包信息
__version__ = "1.0.0"
__author__ = "zhangsan"

# 指定 from 包名 import *  具体导入的是那些模块
__all__ = ["my_fun", "my_var"]
