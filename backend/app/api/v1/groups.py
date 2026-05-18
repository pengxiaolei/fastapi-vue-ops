from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.machine import GroupCreate, GroupUpdate, GroupResponse
from app.services.group_service import GroupService

router = APIRouter()


# ==================== 获取分组列表 ====================
@router.post("/list", response_model=ApiResponse[List[GroupResponse]], summary="获取分组列表")
async def get_group_list(
    params: dict = {},
    db: Session = Depends(get_db),
):
    """获取所有分组列表"""
    skip = params.get("skip", 0)
    limit = params.get("limit", 100)
    groups = GroupService.get_groups(db, skip=skip, limit=limit)
    return ApiResponse.ok(data=groups, action="group.list")


# ==================== 获取分组详情 ====================
@router.post("/get", response_model=ApiResponse[GroupResponse], summary="获取分组详情")
async def get_group_detail(
    params: dict,
    db: Session = Depends(get_db),
):
    """根据ID获取分组详情"""
    group_id = params.get("id")
    group = GroupService.get_group(db, group_id)
    return ApiResponse.ok(data=group, action="group.get")


# ==================== 创建分组 ====================
@router.post("/create", response_model=ApiResponse[GroupResponse], summary="创建分组")
async def create_group(
    data: GroupCreate,
    db: Session = Depends(get_db),
):
    """创建新分组"""
    group = GroupService.create_group(db, data)
    return ApiResponse.ok(data=group, message="创建成功", action="group.create")


# ==================== 更新分组 ====================
@router.post("/update", response_model=ApiResponse[GroupResponse], summary="更新分组")
async def update_group(
    data: dict,
    db: Session = Depends(get_db),
):
    """更新分组信息"""
    group_id = data.get("id")
    update_data = GroupUpdate(**{k: v for k, v in data.items() if k != "id"})
    group = GroupService.update_group(db, group_id, update_data)
    return ApiResponse.ok(data=group, message="更新成功", action="group.update")


# ==================== 删除分组 ====================
@router.post("/delete", response_model=ApiResponse, summary="删除分组")
async def delete_group(
    params: dict,
    db: Session = Depends(get_db),
):
    """删除分组（软删除）"""
    group_id = params.get("id")
    GroupService.delete_group(db, group_id)
    return ApiResponse.ok(message="删除成功", action="group.delete")
