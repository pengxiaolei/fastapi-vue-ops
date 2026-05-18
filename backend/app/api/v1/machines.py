"""
机器管理 API 层
只负责路由和参数处理，业务逻辑委托给 Logic 层
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.machine import (
    MachineCreate,
    MachineResponse,
    MachineListResponse,
    ConnectionTestRequest,
    ConnectionTestResponse,
    MachineStatusResponse,
)
from app.logic.machine_logic import MachineLogic

router = APIRouter()


# ==================== 机器列表 ====================
@router.post("/list", response_model=ApiResponse[MachineListResponse], summary="获取机器列表")
async def get_machine_list(
    params: dict = {},
    db: Session = Depends(get_db),
):
    """获取机器列表，支持分页和筛选"""
    result = MachineLogic.get_machine_list(
        db,
        page=params.get("page", 1),
        page_size=params.get("page_size", 20),
        keyword=params.get("keyword"),
        status=params.get("status"),
        environment=params.get("environment"),
    )
    return ApiResponse.ok(data=result, action="machine.list")


# ==================== 机器详情 ====================
@router.post("/get", response_model=ApiResponse[MachineResponse], summary="获取机器详情")
async def get_machine_detail(
    params: dict,
    db: Session = Depends(get_db),
):
    """根据ID获取机器详情"""
    result = MachineLogic.get_machine_detail(db, params.get("id"))
    return ApiResponse.ok(data=result, action="machine.get")


# ==================== 创建机器 ====================
@router.post("/create", response_model=ApiResponse[MachineResponse], summary="创建机器")
async def create_machine(
    data: MachineCreate,
    db: Session = Depends(get_db),
):
    """创建新机器"""
    result = MachineLogic.create_machine(db, data)
    return ApiResponse.ok(data=result, message="创建成功", action="machine.create")


# ==================== 更新机器 ====================
@router.post("/update", response_model=ApiResponse[MachineResponse], summary="更新机器")
async def update_machine(
    data: dict,
    db: Session = Depends(get_db),
):
    """更新机器信息"""
    result = MachineLogic.update_machine(db, data.get("id"), data)
    return ApiResponse.ok(data=result, message="更新成功", action="machine.update")


# ==================== 删除机器 ====================
@router.post("/delete", response_model=ApiResponse, summary="删除机器")
async def delete_machine(
    params: dict,
    db: Session = Depends(get_db),
):
    """删除机器（软删除）"""
    result = MachineLogic.delete_machine(db, params.get("id"))
    return ApiResponse.ok(message=result["message"], action="machine.delete")


# ==================== 测试连接（不保存） ====================
@router.post("/test-connection", response_model=ApiResponse[ConnectionTestResponse], summary="测试SSH连接")
async def test_connection(
    data: ConnectionTestRequest,
    db: Session = Depends(get_db),
):
    """测试SSH连接，不保存机器信息"""
    result = MachineLogic.test_connection(data)
    return ApiResponse.ok(data=result, action="machine.test_connection")


# ==================== 测试已保存机器的连接 ====================
@router.post("/test-saved-connection", response_model=ApiResponse[ConnectionTestResponse], summary="测试已保存机器的连接")
async def test_saved_connection(
    params: dict,
    db: Session = Depends(get_db),
):
    """测试已保存机器的SSH连接"""
    result = MachineLogic.test_saved_connection(db, params.get("id"))
    return ApiResponse.ok(data=result, action="machine.test_saved_connection")


# ==================== 刷新机器状态 ====================
@router.post("/refresh-status", response_model=ApiResponse[MachineStatusResponse], summary="刷新机器状态")
async def refresh_machine_status(
    params: dict,
    db: Session = Depends(get_db),
):
    """刷新机器状态，获取最新的资源使用情况"""
    result = MachineLogic.refresh_machine_status(db, params.get("id"))
    return ApiResponse.ok(data=result, action="machine.refresh_status")


# ==================== 添加标签到机器 ====================
@router.post("/add-tag", response_model=ApiResponse, summary="给机器添加标签")
async def add_tag_to_machine(
    params: dict,
    db: Session = Depends(get_db),
):
    """给机器添加标签"""
    result = MachineLogic.add_tag_to_machine(db, params.get("machine_id"), params.get("tag_id"))
    return ApiResponse.ok(message=result["message"], action="machine.add_tag")


# ==================== 移除机器标签 ====================
@router.post("/remove-tag", response_model=ApiResponse, summary="移除机器标签")
async def remove_tag_from_machine(
    params: dict,
    db: Session = Depends(get_db),
):
    """移除机器的标签"""
    result = MachineLogic.remove_tag_from_machine(db, params.get("machine_id"), params.get("tag_id"))
    return ApiResponse.ok(message=result["message"], action="machine.remove_tag")


# ==================== 添加机器到分组 ====================
@router.post("/add-to-group", response_model=ApiResponse, summary="将机器添加到分组")
async def add_machine_to_group(
    params: dict,
    db: Session = Depends(get_db),
):
    """将机器添加到指定分组"""
    result = MachineLogic.add_machine_to_group(db, params.get("machine_id"), params.get("group_id"))
    return ApiResponse.ok(message=result["message"], action="machine.add_to_group")


# ==================== 从分组移除机器 ====================
@router.post("/remove-from-group", response_model=ApiResponse, summary="将机器从分组移除")
async def remove_machine_from_group(
    params: dict,
    db: Session = Depends(get_db),
):
    """将机器从指定分组移除"""
    result = MachineLogic.remove_machine_from_group(db, params.get("machine_id"), params.get("group_id"))
    return ApiResponse.ok(message=result["message"], action="machine.remove_from_group")
