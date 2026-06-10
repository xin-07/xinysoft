"""
通用 API 响应模型模块
"""
from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """
    通用 API 响应模型

    用于统一 API 返回格式，包含状态码、消息和数据。
    """
    code: int = Field(200, description="状态码，200 表示成功")
    message: str = Field("success", description="响应消息")
    data: Any = Field(None, description="响应数据")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "success",
                "data": None
            }
        }