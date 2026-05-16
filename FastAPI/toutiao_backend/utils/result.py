from typing import Any, Optional


class Result:

    def __init__(
            self,
            code: int = 200,
            message: str = "success",
            data: Optional[Any] = None
    ):
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data
        }

    @staticmethod
    def success(data=None, message="success"):
        return Result(
            code=200,
            message=message,
            data=data
        ).to_dict()

    @staticmethod
    def error(message="error", code=500, data=None):
        return Result(
            code=code,
            message=message,
            data=data
        ).to_dict()
