from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.machine import TagCreate, TagUpdate, TagResponse
from app.services.tag_service import TagService

router = APIRouter()


# ==================== 获取标签列表 ====================
@router.post("/list", response_model=ApiResponse[List[TagResponse]], summary="获取标签列表")
async def get_tag_list(
    params: dict = {},
    db: Session = Depends(get_db),
):
    """获取所有标签列表"""
    skip = params.get("skip", 0)
    limit = params.get("limit", 100)
    tags = TagService.get_tags(db, skip=skip, limit=limit)
    return ApiResponse.ok(data=tags, action="tag.list")


# ==================== 获取标签详情 ====================
@router.post("/get", response_model=ApiResponse[TagResponse], summary="获取标签详情")
async def get_tag_detail(
    params: dict,
    db: Session = Depends(get_db),
):
    """根据ID获取标签详情"""
    tag_id = params.get("id")
    tag = TagService.get_tag(db, tag_id)
    return ApiResponse.ok(data=tag, action="tag.get")


# ==================== 创建标签 ====================
@router.post("/create", response_model=ApiResponse[TagResponse], summary="创建标签")
async def create_tag(
    data: TagCreate,
    db: Session = Depends(get_db),
):
    """创建新标签"""
    tag = TagService.create_tag(db, data)
    return ApiResponse.ok(data=tag, message="创建成功", action="tag.create")


# ==================== 更新标签 ====================
@router.post("/update", response_model=ApiResponse[TagResponse], summary="更新标签")
async def update_tag(
    data: dict,
    db: Session = Depends(get_db),
):
    """更新标签信息"""
    tag_id = data.get("id")
    update_data = TagUpdate(**{k: v for k, v in data.items() if k != "id"})
    tag = TagService.update_tag(db, tag_id, update_data)
    return ApiResponse.ok(data=tag, message="更新成功", action="tag.update")


# ==================== 删除标签 ====================
@router.post("/delete", response_model=ApiResponse, summary="删除标签")
async def delete_tag(
    params: dict,
    db: Session = Depends(get_db),
):
    """删除标签（软删除）"""
    tag_id = params.get("id")
    TagService.delete_tag(db, tag_id)
    return ApiResponse.ok(message="删除成功", action="tag.delete")
