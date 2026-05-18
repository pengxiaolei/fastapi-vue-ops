from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from app.models.machine import MachineStatus, AuthType


# ==================== 标签相关Schema ====================
class TagBase(BaseModel):
    name: str = Field(..., max_length=50, description="标签名称")
    color: Optional[str] = Field("#1890ff", max_length=7, description="标签颜色")


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50, description="标签名称")
    color: Optional[str] = Field(None, max_length=7, description="标签颜色")


class TagResponse(TagBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== 分组相关Schema ====================
class GroupBase(BaseModel):
    name: str = Field(..., max_length=100, description="分组名称")
    description: Optional[str] = Field(None, description="分组描述")


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="分组名称")
    description: Optional[str] = Field(None, description="分组描述")


class GroupResponse(GroupBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== 机器相关Schema ====================
class MachineBase(BaseModel):
    name: str = Field(..., max_length=100, description="机器名称")
    hostname: str = Field(..., max_length=255, description="主机名/IP地址")
    port: int = Field(22, ge=1, le=65535, description="SSH端口")
    username: str = Field(..., max_length=50, description="SSH用户名")
    auth_type: AuthType = Field(AuthType.PASSWORD, description="认证类型")
    os_type: Optional[str] = Field(None, max_length=50, description="操作系统类型")
    environment: Optional[str] = Field(None, max_length=50, description="所属环境：dev/test/prod")
    description: Optional[str] = Field(None, description="描述")


class MachineCreate(MachineBase):
    password: Optional[str] = Field(None, description="SSH密码")
    private_key: Optional[str] = Field(None, description="SSH私钥内容")


class MachineUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="机器名称")
    hostname: Optional[str] = Field(None, max_length=255, description="主机名/IP地址")
    port: Optional[int] = Field(None, ge=1, le=65535, description="SSH端口")
    username: Optional[str] = Field(None, max_length=50, description="SSH用户名")
    auth_type: Optional[AuthType] = Field(None, description="认证类型")
    password: Optional[str] = Field(None, description="SSH密码")
    private_key: Optional[str] = Field(None, description="SSH私钥内容")
    os_type: Optional[str] = Field(None, max_length=50, description="操作系统类型")
    environment: Optional[str] = Field(None, max_length=50, description="所属环境：dev/test/prod")
    description: Optional[str] = Field(None, description="描述")
    status: Optional[MachineStatus] = Field(None, description="机器状态")


class MachineResponse(MachineBase):
    id: int
    status: MachineStatus
    cpu_cores: Optional[int] = None
    memory_total: Optional[int] = None
    disk_total: Optional[int] = None
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    disk_usage: Optional[float] = None
    last_heartbeat: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    tags: List[TagResponse] = Field(default_factory=list)
    groups: List[GroupResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class MachineDetailResponse(MachineResponse):
    """机器详情，包含更多信息"""
    pass


# ==================== 连接测试相关Schema ====================
class ConnectionTestRequest(BaseModel):
    hostname: str = Field(..., max_length=255, description="主机名/IP地址")
    port: int = Field(22, ge=1, le=65535, description="SSH端口")
    username: str = Field(..., max_length=50, description="SSH用户名")
    auth_type: AuthType = Field(AuthType.PASSWORD, description="认证类型")
    password: Optional[str] = Field(None, description="SSH密码")
    private_key: Optional[str] = Field(None, description="SSH私钥内容")


class ConnectionTestResponse(BaseModel):
    success: bool
    message: str
    os_type: Optional[str] = None
    cpu_cores: Optional[int] = None
    memory_total: Optional[int] = None
    disk_total: Optional[int] = None
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    disk_usage: Optional[float] = None


# ==================== 机器状态刷新Schema ====================
class MachineStatusResponse(BaseModel):
    success: bool
    message: str
    status: Optional[MachineStatus] = None
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    disk_usage: Optional[float] = None


# ==================== 批量操作Schema ====================
class BatchOperationRequest(BaseModel):
    machine_ids: List[int] = Field(..., description="机器ID列表")
    operation: str = Field(..., description="操作类型：delete/add_tag/remove_tag")
    tag_id: Optional[int] = Field(None, description="标签ID（标签操作时需要）")


class BatchOperationResponse(BaseModel):
    success: bool
    message: str
    processed_count: int
    failed_count: int


# ==================== 分页Schema ====================
class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int


class MachineListResponse(PaginatedResponse):
    data: List[MachineResponse]
