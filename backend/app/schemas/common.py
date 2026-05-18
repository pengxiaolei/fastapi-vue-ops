from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

T = TypeVar('T')


class ApiRequest(BaseModel, Generic[T]):
    """统一请求格式"""
    action: str = Field(..., description="功能用途标识，如：machine.list, machine.create")
    data: Optional[T] = Field(None, description="请求业务数据")


class ApiResponse(BaseModel, Generic[T]):
    """统一响应格式"""
    success: bool = Field(True, description="请求是否成功")
    code: int = Field(200, description="响应状态码")
    message: str = Field("success", description="响应消息")
    action: Optional[str] = Field(None, description="对应当前请求的功能标识")
    data: Optional[T] = Field(None, description="响应业务数据")

    @classmethod
    def ok(cls, data: Any = None, message: str = "success", action: str = None):
        return cls(success=True, code=200, message=message, action=action, data=data)

    @classmethod
    def error(cls, message: str = "error", code: int = 400, action: str = None):
        return cls(success=False, code=code, message=message, action=action, data=None)
