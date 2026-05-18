"""
标签管理 API 层
只负责路由和参数处理，业务逻辑委托给 Logic 层
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.machine import TagCreate, TagResponse
from app.logic.tag_logic import TagLogic

router = APIRouter()


# ==================== 获取标签列表 ====================
@router.post("/list", response_model=ApiResponse[List[TagResponse]], summary="获取标签列表")
async def get_tag_list(
    params: dict = {},
    db: Session = Depends(get_db),
):
    """获取所有标签列表"""
    result = TagLogic.get_tag_list(
        db,
        skip=params.get("skip", 0),
        limit=params.get("limit", 100),
    )
    return ApiResponse.ok(data=result, action="tag.list")


# ==================== 获取标签详情 ====================
@router.post("/get", response_model=ApiResponse[TagResponse], summary="获取标签详情")
async def get_tag_detail(
    params: dict,
    db: Session = Depends(get_db),
):
    """根据ID获取标签详情"""
    result = TagLogic.get_tag_detail(db, params.get("id"))
    return ApiResponse.ok(data=result, action="tag.get")


# ==================== 创建标签 ====================
@router.post("/create", response_model=ApiResponse[TagResponse], summary="创建标签")
async def create_tag(
    data: TagCreate,
    db: Session = Depends(get_db),
):
    """创建新标签"""
    result = TagLogic.create_tag(db, data)
    return ApiResponse.ok(data=result, message="创建成功", action="tag.create")


# ==================== 更新标签 ====================
@router.post("/update", response_model=ApiResponse[TagResponse], summary="更新标签")
async def update_tag(
    data: dict,
    db: Session = Depends(get_db),
):
    """更新标签信息"""
    result = TagLogic.update_tag(db, data.get("id"), data)
    return ApiResponse.ok(data=result, message="更新成功", action="tag.update")


# ==================== 删除标签 ====================
@router.post("/delete", response_model=ApiResponse, summary="删除标签")
async def delete_tag(
    params: dict,
    db: Session = Depends(get_db),
):
    """删除标签（软删除）"""
    result = TagLogic.delete_tag(db, params.get("id"))
    return ApiResponse.ok(message=result["message"], action="tag.delete")
