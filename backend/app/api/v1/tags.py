from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.machine import TagCreate, TagUpdate, TagResponse
from app.services.tag_service import TagService

router = APIRouter()


@router.get("", response_model=List[TagResponse], summary="获取标签列表")
def get_tags(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """获取所有标签列表"""
    tags = TagService.get_tags(db, skip=skip, limit=limit)
    return tags


@router.get("/{tag_id}", response_model=TagResponse, summary="获取标签详情")
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    """根据ID获取标签详情"""
    tag = TagService.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    return tag


@router.post("", response_model=TagResponse, status_code=201, summary="创建标签")
def create_tag(tag_in: TagCreate, db: Session = Depends(get_db)):
    """创建新标签"""
    # 检查标签名称是否已存在
    existing = TagService.get_tag_by_name(db, tag_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="标签名称已存在")

    tag = TagService.create_tag(db, tag_in)
    return tag


@router.put("/{tag_id}", response_model=TagResponse, summary="更新标签")
def update_tag(tag_id: int, tag_in: TagUpdate, db: Session = Depends(get_db)):
    """更新标签信息"""
    # 如果更新名称，检查是否与其他标签冲突
    if tag_in.name:
        existing = TagService.get_tag_by_name(db, tag_in.name)
        if existing and existing.id != tag_id:
            raise HTTPException(status_code=400, detail="标签名称已存在")

    tag = TagService.update_tag(db, tag_id, tag_in)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    return tag


@router.delete("/{tag_id}", summary="删除标签")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """删除标签（软删除）"""
    success = TagService.delete_tag(db, tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="标签不存在")
    return {"success": True, "message": "删除成功"}
