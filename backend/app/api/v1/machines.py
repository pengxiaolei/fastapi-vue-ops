from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.machine import (
    MachineCreate,
    MachineUpdate,
    MachineResponse,
    MachineListResponse,
    ConnectionTestRequest,
    ConnectionTestResponse,
    MachineStatusResponse,
)
from app.services.machine_service import MachineService

router = APIRouter()


# ==================== 机器列表 ====================
@router.post("/list", response_model=ApiResponse[MachineListResponse], summary="获取机器列表")
async def get_machine_list(
    params: dict = {},
    db: Session = Depends(get_db),
):
    """获取机器列表，支持分页和筛选"""
    page = params.get("page", 1)
    page_size = params.get("page_size", 20)
    keyword = params.get("keyword")
    status = params.get("status")
    environment = params.get("environment")

    skip = (page - 1) * page_size
    machines, total = MachineService.get_machines(
        db, skip=skip, limit=page_size, keyword=keyword,
        status=status, environment=environment
    )

    result = MachineListResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
        data=machines
    )
    return ApiResponse.ok(data=result, action="machine.list")


# ==================== 机器详情 ====================
@router.post("/get", response_model=ApiResponse[MachineResponse], summary="获取机器详情")
async def get_machine_detail(
    params: dict,
    db: Session = Depends(get_db),
):
    """根据ID获取机器详情"""
    machine_id = params.get("id")
    machine = MachineService.get_machine(db, machine_id)
    return ApiResponse.ok(data=machine, action="machine.get")


# ==================== 创建机器 ====================
@router.post("/create", response_model=ApiResponse[MachineResponse], summary="创建机器")
async def create_machine(
    data: MachineCreate,
    db: Session = Depends(get_db),
):
    """创建新机器"""
    machine = MachineService.create_machine(db, data)
    return ApiResponse.ok(data=machine, message="创建成功", action="machine.create")


# ==================== 更新机器 ====================
@router.post("/update", response_model=ApiResponse[MachineResponse], summary="更新机器")
async def update_machine(
    data: dict,
    db: Session = Depends(get_db),
):
    """更新机器信息"""
    machine_id = data.get("id")
    update_data = MachineUpdate(**{k: v for k, v in data.items() if k != "id"})
    machine = MachineService.update_machine(db, machine_id, update_data)
    return ApiResponse.ok(data=machine, message="更新成功", action="machine.update")


# ==================== 删除机器 ====================
@router.post("/delete", response_model=ApiResponse, summary="删除机器")
async def delete_machine(
    params: dict,
    db: Session = Depends(get_db),
):
    """删除机器（软删除）"""
    machine_id = params.get("id")
    MachineService.delete_machine(db, machine_id)
    return ApiResponse.ok(message="删除成功", action="machine.delete")


# ==================== 测试连接（不保存） ====================
@router.post("/test-connection", response_model=ApiResponse[ConnectionTestResponse], summary="测试SSH连接")
async def test_connection(
    data: ConnectionTestRequest,
    db: Session = Depends(get_db),
):
    """测试SSH连接，不保存机器信息"""
    success, message, sys_info = MachineService.test_connection(
        hostname=data.hostname,
        port=data.port,
        username=data.username,
        auth_type=data.auth_type,
        password=getattr(data, "password", None),
        private_key=getattr(data, "private_key", None),
    )

    result = ConnectionTestResponse(
        success=success,
        message=message,
        **sys_info
    )
    return ApiResponse.ok(data=result, action="machine.test_connection")


# ==================== 测试已保存机器的连接 ====================
@router.post("/test-saved-connection", response_model=ApiResponse[ConnectionTestResponse], summary="测试已保存机器的连接")
async def test_saved_connection(
    params: dict,
    db: Session = Depends(get_db),
):
    """测试已保存机器的SSH连接"""
    machine_id = params.get("id")
    success, message, sys_info = MachineService.test_machine_connection(db, machine_id)
    result = ConnectionTestResponse(
        success=success,
        message=message,
        **sys_info
    )
    return ApiResponse.ok(data=result, action="machine.test_saved_connection")


# ==================== 刷新机器状态 ====================
@router.post("/refresh-status", response_model=ApiResponse[MachineStatusResponse], summary="刷新机器状态")
async def refresh_machine_status(
    params: dict,
    db: Session = Depends(get_db),
):
    """刷新机器状态，获取最新的资源使用情况"""
    machine_id = params.get("id")
    success, message = MachineService.refresh_machine_status(db, machine_id)
    machine = MachineService.get_machine(db, machine_id)
    result = MachineStatusResponse(
        success=success,
        message=message,
        status=machine.status if machine else None,
        cpu_usage=machine.cpu_usage if machine else None,
        memory_usage=machine.memory_usage if machine else None,
        disk_usage=machine.disk_usage if machine else None,
    )
    return ApiResponse.ok(data=result, action="machine.refresh_status")


# ==================== 添加标签到机器 ====================
@router.post("/add-tag", response_model=ApiResponse, summary="给机器添加标签")
async def add_tag_to_machine(
    params: dict,
    db: Session = Depends(get_db),
):
    """给机器添加标签"""
    machine_id = params.get("machine_id")
    tag_id = params.get("tag_id")
    MachineService.add_tag_to_machine(db, machine_id, tag_id)
    return ApiResponse.ok(message="添加标签成功", action="machine.add_tag")


# ==================== 移除机器标签 ====================
@router.post("/remove-tag", response_model=ApiResponse, summary="移除机器标签")
async def remove_tag_from_machine(
    params: dict,
    db: Session = Depends(get_db),
):
    """移除机器的标签"""
    machine_id = params.get("machine_id")
    tag_id = params.get("tag_id")
    MachineService.remove_tag_from_machine(db, machine_id, tag_id)
    return ApiResponse.ok(message="移除标签成功", action="machine.remove_tag")


# ==================== 添加机器到分组 ====================
@router.post("/add-to-group", response_model=ApiResponse, summary="将机器添加到分组")
async def add_machine_to_group(
    params: dict,
    db: Session = Depends(get_db),
):
    """将机器添加到指定分组"""
    machine_id = params.get("machine_id")
    group_id = params.get("group_id")
    MachineService.add_machine_to_group(db, machine_id, group_id)
    return ApiResponse.ok(message="添加到分组成功", action="machine.add_to_group")


# ==================== 从分组移除机器 ====================
@router.post("/remove-from-group", response_model=ApiResponse, summary="将机器从分组移除")
async def remove_machine_from_group(
    params: dict,
    db: Session = Depends(get_db),
):
    """将机器从指定分组移除"""
    machine_id = params.get("machine_id")
    group_id = params.get("group_id")
    MachineService.remove_machine_from_group(db, machine_id, group_id)
    return ApiResponse.ok(message="从分组移除成功", action="machine.remove_from_group")
