import asyncio

import aiohttp
import time


async def download_picture(session, url):
    print(f'开始下载图片：{url}')
    response = await session.get(url)
    content = await response.read()
    with open(f'./image/{int(time.time() * 1000)}.jpg', 'wb') as f:
        f.write(content)
    print(f'图片下载完成')
    await response.release()


async def main():
    url_list = [
        'https://pic.616pic.com/phototwo/00/07/67/619766a57f5df3279.jpg',
        'https://imgs.699pic.com/images/601/741/485.jpg!list1x.v2',
        'https://img.17sucai.com/upload/534358/2016-06-11/e367aa3fcaaae99a7479dd3f5c5fbcc8.jpg?x-oss-process=style/lessen'

    ]

    start = time.time()

    session = aiohttp.ClientSession()
    coroutine_list = [download_picture(session, url) for url in url_list]
    await  asyncio.gather(*coroutine_list)

    print(f'耗时：{time.time() - start:.2f}秒')

    await  session.close()


if __name__ == '__main__':
    asyncio.run(main())
