from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.machine import GroupCreate, GroupUpdate, GroupResponse
from app.services.group_service import GroupService

router = APIRouter()


@router.get("", response_model=List[GroupResponse], summary="获取分组列表")
def get_groups(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """获取所有分组列表"""
    groups = GroupService.get_groups(db, skip=skip, limit=limit)
    return groups


@router.get("/{group_id}", response_model=GroupResponse, summary="获取分组详情")
def get_group(group_id: int, db: Session = Depends(get_db)):
    """根据ID获取分组详情"""
    group = GroupService.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="分组不存在")
    return group


@router.post("", response_model=GroupResponse, status_code=201, summary="创建分组")
def create_group(group_in: GroupCreate, db: Session = Depends(get_db)):
    """创建新分组"""
    # 检查分组名称是否已存在
    existing = GroupService.get_group_by_name(db, group_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="分组名称已存在")

    group = GroupService.create_group(db, group_in)
    return group


@router.put("/{group_id}", response_model=GroupResponse, summary="更新分组")
def update_group(group_id: int, group_in: GroupUpdate, db: Session = Depends(get_db)):
    """更新分组信息"""
    # 如果更新名称，检查是否与其他分组冲突
    if group_in.name:
        existing = GroupService.get_group_by_name(db, group_in.name)
        if existing and existing.id != group_id:
            raise HTTPException(status_code=400, detail="分组名称已存在")

    group = GroupService.update_group(db, group_id, group_in)
    if not group:
        raise HTTPException(status_code=404, detail="分组不存在")
    return group


@router.delete("/{group_id}", summary="删除分组")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    """删除分组（软删除）"""
    success = GroupService.delete_group(db, group_id)
    if not success:
        raise HTTPException(status_code=404, detail="分组不存在")
    return {"success": True, "message": "删除成功"}
