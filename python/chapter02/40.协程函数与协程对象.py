"""
================================================================================
   - 协程函数(Coroutine Function): 使用 async def 定义的函数
   - 协程对象(Coroutine Object): 调用协程函数返回的对象
"""

import asyncio


async def work():
    print("Start work")
    print("Working...")
    print("End work")
    return "work done"


# 调用协程函数，不会执行其中的代码，而是得到一个协程对象
coroutine_obj = work()
print(coroutine_obj)

# asyncio.run 做了三件事：
# 1. 创建一个事件循环
# 2. 将协程对象包装成 task 交给事件循环
# 3. 启动事件循环
# 注意：asyncio.run 会阻塞线程，直到 task 结束并获取结果
result = asyncio.run(coroutine_obj)
print(result)
