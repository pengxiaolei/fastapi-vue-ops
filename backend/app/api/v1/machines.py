from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.machine import (
    MachineCreate,
    MachineUpdate,
    MachineResponse,
    MachineDetailResponse,
    MachineListResponse,
    ConnectionTestRequest,
    ConnectionTestResponse,
    MachineStatusResponse,
)
from app.services.machine_service import MachineService

router = APIRouter()


@router.get("", response_model=MachineListResponse, summary="获取机器列表")
def get_machines(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="搜索关键词（机器名称/主机名）"),
    status: Optional[str] = Query(None, description="机器状态筛选"),
    environment: Optional[str] = Query(None, description="环境筛选"),
    db: Session = Depends(get_db),
):
    """获取机器列表，支持分页和筛选"""
    skip = (page - 1) * page_size
    machines, total = MachineService.get_machines(
        db, skip=skip, limit=page_size, keyword=keyword, status=status, environment=environment
    )

    total_pages = (total + page_size - 1) // page_size

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": machines,
    }


@router.get("/{machine_id}", response_model=MachineDetailResponse, summary="获取机器详情")
def get_machine(machine_id: int, db: Session = Depends(get_db)):
    """根据ID获取机器详情"""
    machine = MachineService.get_machine(db, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="机器不存在")
    return machine


@router.post("", response_model=MachineResponse, status_code=201, summary="创建机器")
def create_machine(machine_in: MachineCreate, db: Session = Depends(get_db)):
    """创建新机器"""
    machine = MachineService.create_machine(db, machine_in)
    return machine


@router.put("/{machine_id}", response_model=MachineResponse, summary="更新机器")
def update_machine(machine_id: int, machine_in: MachineUpdate, db: Session = Depends(get_db)):
    """更新机器信息"""
    machine = MachineService.update_machine(db, machine_id, machine_in)
    if not machine:
        raise HTTPException(status_code=404, detail="机器不存在")
    return machine


@router.delete("/{machine_id}", summary="删除机器")
def delete_machine(machine_id: int, db: Session = Depends(get_db)):
    """删除机器（软删除）"""
    success = MachineService.delete_machine(db, machine_id)
    if not success:
        raise HTTPException(status_code=404, detail="机器不存在")
    return {"success": True, "message": "删除成功"}


@router.post("/test-connection", response_model=ConnectionTestResponse, summary="测试SSH连接")
def test_connection(request: ConnectionTestRequest):
    """测试SSH连接（不保存机器信息）"""
    success, message, system_info = MachineService.test_connection(
        hostname=request.hostname,
        port=request.port,
        username=request.username,
        auth_type=request.auth_type,
        password=request.password,
        private_key=request.private_key,
    )

    return {
        "success": success,
        "message": message,
        **system_info,
    }


@router.post("/{machine_id}/test-connection", response_model=ConnectionTestResponse, summary="测试机器连接")
def test_machine_connection(machine_id: int, db: Session = Depends(get_db)):
    """测试已保存机器的SSH连接"""
    success, message, system_info = MachineService.test_machine_connection(db, machine_id)
    if not success and "不存在" in message:
        raise HTTPException(status_code=404, detail=message)

    return {
        "success": success,
        "message": message,
        **system_info,
    }


@router.post("/{machine_id}/refresh-status", response_model=MachineStatusResponse, summary="刷新机器状态")
def refresh_machine_status(machine_id: int, db: Session = Depends(get_db)):
    """刷新机器状态，获取最新的资源使用情况"""
    machine = MachineService.get_machine(db, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="机器不存在")

    success, message = MachineService.refresh_machine_status(db, machine_id)

    return {
        "success": success,
        "message": message,
        "status": machine.status,
        "cpu_usage": machine.cpu_usage,
        "memory_usage": machine.memory_usage,
        "disk_usage": machine.disk_usage,
    }


@router.post("/{machine_id}/tags/{tag_id}", summary="给机器添加标签")
def add_tag_to_machine(machine_id: int, tag_id: int, db: Session = Depends(get_db)):
    """给机器添加标签"""
    success = MachineService.add_tag_to_machine(db, machine_id, tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="机器或标签不存在")
    return {"success": True, "message": "添加标签成功"}


@router.delete("/{machine_id}/tags/{tag_id}", summary="移除机器标签")
def remove_tag_from_machine(machine_id: int, tag_id: int, db: Session = Depends(get_db)):
    """移除机器的标签"""
    success = MachineService.remove_tag_from_machine(db, machine_id, tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="机器或标签不存在")
    return {"success": True, "message": "移除标签成功"}


@router.post("/{machine_id}/groups/{group_id}", summary="将机器添加到分组")
def add_machine_to_group(machine_id: int, group_id: int, db: Session = Depends(get_db)):
    """将机器添加到指定分组"""
    success = MachineService.add_machine_to_group(db, machine_id, group_id)
    if not success:
        raise HTTPException(status_code=404, detail="机器或分组不存在")
    return {"success": True, "message": "添加到分组成功"}


@router.delete("/{machine_id}/groups/{group_id}", summary="将机器从分组移除")
def remove_machine_from_group(machine_id: int, group_id: int, db: Session = Depends(get_db)):
    """将机器从指定分组移除"""
    success = MachineService.remove_machine_from_group(db, machine_id, group_id)
    if not success:
        raise HTTPException(status_code=404, detail="机器或分组不存在")
    return {"success": True, "message": "从分组移除成功"}
