import time

import asyncio


async def work(n, delay):
    print(f'work{n}开始')
    print(f'work{n}执行中')
    await asyncio.sleep(delay)
    print(f'work{n}结束')
    return f'work{n}返回值'


async def main():
    print('main开始')

    start = time.time()

    task1 = asyncio.create_task(work(1, 2))
    task2 = asyncio.create_task(work(2, 2))
    task3 = asyncio.create_task(work(3, 2))

    res1 = await task1
    print(res1)
    res2 = await task2
    print(res2)
    res3 = await task3
    print(res3)

    end = time.time()
    print(f'耗时：{end - start:.2f}秒')

    print('main结束')
    return 'main返回值'


asyncio.run(main())
