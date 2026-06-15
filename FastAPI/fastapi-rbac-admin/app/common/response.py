from typing import Any

from pydantic import BaseModel


class ApiResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Any = None


def ok(data: Any = None, message: str = "success") -> ApiResponse:
    """统一成功响应，方便前端按固定结构处理接口结果。"""

    return ApiResponse(code=0, message=message, data=data)
