"""
await 作用

    1.挂起：await 会暂停当前协程执行
    2.等待：await 表示要等待某个对象执行完成，事件循环会立即调度该对象，并且可以拿到执行结果
        关键点：执行 await 后的对象时，分两种情况：
            情况一：遇到了【I/O操作】
            如：网络请求、文件读写等
            CPU控制权就会交给事件循环
            事件循环调度其他任务执行（如果有）

            情况二：不包含任何【I/O操作】
            如：print打印、数学计算
            此时事件循环拿不到CPU，不会发生任务切换
    3.恢复：当 await 等待的对象执行完，事件循环会恢复之前挂起的协程，从挂起的位置继续执行

注意：await 后只能跟【可等待对象】，如：协程、Future、Task
"""

import asyncio


async def work():
    print("Start work")
    print("Working...")
    res = await asyncio.sleep(2)
    print(res)
    print("End work")
    return "work done"


async def main():
    print("Start main")
    result = await work()
    print(result)
    print("End main")
    return "main done"


res = asyncio.run(main())
print(res)
