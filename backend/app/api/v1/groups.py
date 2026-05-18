"""
分组管理 API 层
只负责路由和参数处理，业务逻辑委托给 Logic 层
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.machine import GroupCreate, GroupResponse
from app.logic.group_logic import GroupLogic

router = APIRouter()


# ==================== 获取分组列表 ====================
@router.post("/list", response_model=ApiResponse[List[GroupResponse]], summary="获取分组列表")
async def get_group_list(
    params: dict = {},
    db: Session = Depends(get_db),
):
    """获取所有分组列表"""
    result = GroupLogic.get_group_list(
        db,
        skip=params.get("skip", 0),
        limit=params.get("limit", 100),
    )
    return ApiResponse.ok(data=result, action="group.list")


# ==================== 获取分组详情 ====================
@router.post("/get", response_model=ApiResponse[GroupResponse], summary="获取分组详情")
async def get_group_detail(
    params: dict,
    db: Session = Depends(get_db),
):
    """根据ID获取分组详情"""
    result = GroupLogic.get_group_detail(db, params.get("id"))
    return ApiResponse.ok(data=result, action="group.get")


# ==================== 创建分组 ====================
@router.post("/create", response_model=ApiResponse[GroupResponse], summary="创建分组")
async def create_group(
    data: GroupCreate,
    db: Session = Depends(get_db),
):
    """创建新分组"""
    result = GroupLogic.create_group(db, data)
    return ApiResponse.ok(data=result, message="创建成功", action="group.create")


# ==================== 更新分组 ====================
@router.post("/update", response_model=ApiResponse[GroupResponse], summary="更新分组")
async def update_group(
    data: dict,
    db: Session = Depends(get_db),
):
    """更新分组信息"""
    result = GroupLogic.update_group(db, data.get("id"), data)
    return ApiResponse.ok(data=result, message="更新成功", action="group.update")


# ==================== 删除分组 ====================
@router.post("/delete", response_model=ApiResponse, summary="删除分组")
async def delete_group(
    params: dict,
    db: Session = Depends(get_db),
):
    """删除分组（软删除）"""
    result = GroupLogic.delete_group(db, params.get("id"))
    return ApiResponse.ok(message=result["message"], action="group.delete")
