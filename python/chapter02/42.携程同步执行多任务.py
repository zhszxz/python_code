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

    coroutine1 = work(1, 2)
    coroutine2 = work(2, 2)
    coroutine3 = work(3, 2)

    res1 = await coroutine1
    print(res1)
    res2 = await coroutine2
    print(res2)
    res3 = await coroutine3
    print(res3)

    end = time.time()
    print(f'耗时：{end - start:.2f}秒')

    print('main结束')


asyncio.run(main())
