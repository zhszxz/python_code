from fastapi import FastAPI
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    FileResponse,
    StreamingResponse
)

from pydantic import BaseModel

app = FastAPI()


# ==================== FastAPI 返回数据类型说明 ====================
#
# FastAPI 支持多种响应格式，主要包括：
#
# 1. JSON 响应（默认）- JSONResponse
#    - 自动将 Python 字典/列表转换为 JSON 格式
#    - Content-Type: application/json
#
# 2. HTML 响应 - HTMLResponse
#    - 返回 HTML 页面内容
#    - Content-Type: text/html
#
# 3. 纯文本响应 - PlainTextResponse
#    - 返回纯文本内容
#    - Content-Type: text/plain
#
# 4. 重定向响应 - RedirectResponse
#    - HTTP 重定向到另一个 URL
#    - 状态码通常是 301 或 307
#
# 5. 文件响应 - FileResponse
#    - 返回文件（图片、PDF、视频等）
#    - 自动设置正确的 Content-Type
#
# 6. 流式响应 - StreamingResponse
#    - 用于大数据流或实时数据传输
#    - 支持异步生成器
#
# ================================================================


# -------------------- 1. JSON 响应（默认方式）--------------------
@app.get("/json")
async def return_json():
    """
    默认返回 JSON 格式
    FastAPI 会自动将 dict/list 转换为 JSON
    """
    return {"message": "这是 JSON 响应", "status": "success", "code": 200}


@app.get("/json-response")
async def return_json_response():
    """
    显式使用 JSONResponse
    可以自定义状态码和 headers
    """
    data = {"message": "这是显式的 JSON 响应", "data": [1, 2, 3]}
    return JSONResponse(
        content=data,
        status_code=201,
        headers={"X-Custom-Header": "MyValue"}
    )


class News(BaseModel):
    id: int
    title: str
    content: str


@app.get("/json-custom", response_model=News)
async def return_json_custom():
    """
    使用 response_model 约束返回数据结构
    """
    return {
        "id": 88,
        "title": "特朗普宣布霍尔木兹海峡改名",
        "content": "特朗普：“霍尔木兹海峡”更名为“特朗普海峡”"
    }


# -------------------- 2. HTML 响应 --------------------
@app.get("/html", response_class=HTMLResponse)
async def return_html():
    """
    返回 HTML 页面
    可以使用 response_class 参数或直接返回 HTMLResponse
    """
    html_content = """
    <!DOCTYPE html>
    <html>
        <head><title>FastAPI HTML 示例</title></head>
        <body>
            <h1>Hello from FastAPI!</h1>
            <p>这是一个 HTML 响应</p>
        </body>
    </html>
    """
    return html_content


@app.get("/html-direct")
async def return_html_direct():
    """
    直接返回 HTMLResponse 对象
    """
    return HTMLResponse(
        content="<h1>直接返回 HTML</h1><p>使用 HTMLResponse 类</p>",
        status_code=200
    )


# -------------------- 3. 纯文本响应 --------------------
@app.get("/text", response_class=PlainTextResponse)
async def return_text():
    """
    返回纯文本内容
    """
    return "这是纯文本响应\n第二行文本"


@app.get("/text-direct")
async def return_text_direct():
    """
    直接返回 PlainTextResponse 对象
    """
    return PlainTextResponse(
        content="直接使用 PlainTextResponse\n可以包含特殊字符: @#$%",
        status_code=200
    )


# -------------------- 4. 重定向响应 --------------------
@app.get("/redirect")
async def redirect_example():
    """
    重定向到其他 URL
    默认是临时重定向（307）
    """
    return RedirectResponse(url="/json")


@app.get("/redirect-permanent")
async def redirect_permanent():
    """
    永久重定向（301）
    """
    return RedirectResponse(url="/html", status_code=301)


# -------------------- 5. 文件响应 --------------------
@app.get("/file")
async def return_file():
    """
    返回文件
    需要提供文件的完整路径
    """
    # 示例：返回一个图片文件
    path = "./files/1.jpeg"
    return FileResponse(path)


@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    下载文件并指定文件名
    """
    return FileResponse(
        path=f"./files/{filename}",
        filename=f"download_{filename}",
        media_type="application/octet-stream"
    )


# -------------------- 6. 流式响应 --------------------
def generate_numbers():
    """生成器函数，用于流式传输"""
    for i in range(10):
        yield f"数字: {i}\n"


@app.get("/stream")
async def stream_response():
    """
    流式响应
    适用于大数据量或实时数据传输
    """
    return StreamingResponse(
        generate_numbers(),
        media_type="text/plain"
    )


async def async_generate():
    """异步生成器"""
    for i in range(5):
        yield f"异步数据: {i}\n"


@app.get("/stream-async")
async def stream_async_response():
    """
    异步流式响应
    """
    return StreamingResponse(
        async_generate(),
        media_type="text/plain"
    )


# -------------------- 7. 自定义响应头和内容类型 --------------------
@app.get("/custom-response")
async def custom_response():
    """
    完全自定义响应
    可以控制状态码、headers、content-type 等
    """
    return JSONResponse(
        content={"message": "自定义响应"},
        status_code=202,
        headers={
            "X-Custom-Header": "CustomValue",
            "Cache-Control": "no-cache",
            "Content-Type": "application/json; charset=utf-8"
        }
    )


# -------------------- 8. XML 响应示例 --------------------
@app.get("/xml")
async def return_xml():
    """
    返回 XML 格式数据
    使用 PlainTextResponse 并设置正确的 content-type
    """
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <book>
        <title>FastAPI 教程</title>
        <author>开发者</author>
        <year>2024</year>
    </book>"""
    return PlainTextResponse(
        content=xml_content,
        media_type="application/xml"
    )


# -------------------- 9. CSV 响应示例 --------------------
@app.get("/csv")
async def return_csv():
    """
    返回 CSV 格式数据
    """
    csv_content = "姓名,年龄,城市\n张三,25,北京\n李四,30,上海\n王五,28,广州"
    return PlainTextResponse(
        content=csv_content,
        media_type="text/csv"
    )
