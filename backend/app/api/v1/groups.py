from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import ApiRequest, ApiResponse
from app.schemas.machine import GroupCreate, GroupUpdate, GroupResponse
from app.services.group_service import GroupService

router = APIRouter()


@router.post("", response_model=ApiResponse)
async def group_operations(
    request: ApiRequest[dict],
    db: Session = Depends(get_db),
):
    """
    分组管理统一入口

    action 功能标识:
    - group.list: 获取分组列表
    - group.get: 获取分组详情
    - group.create: 创建分组
    - group.update: 更新分组
    - group.delete: 删除分组
    """
    action = request.action
    data = request.data or {}

    # 获取分组列表
    if action == "group.list":
        skip = data.get("skip", 0)
        limit = data.get("limit", 100)
        groups = GroupService.get_groups(db, skip=skip, limit=limit)
        return ApiResponse.ok(data=groups, action=action)

    # 获取分组详情
    elif action == "group.get":
        group_id = data.get("id")
        group = GroupService.get_group(db, group_id)
        return ApiResponse.ok(data=group, action=action)

    # 创建分组
    elif action == "group.create":
        group_data = GroupCreate(**data)
        group = GroupService.create_group(db, group_data)
        return ApiResponse.ok(data=group, message="创建成功", action=action)

    # 更新分组
    elif action == "group.update":
        group_id = data.get("id")
        update_data = GroupUpdate(**{k: v for k, v in data.items() if k != "id"})
        group = GroupService.update_group(db, group_id, update_data)
        return ApiResponse.ok(data=group, message="更新成功", action=action)

    # 删除分组
    elif action == "group.delete":
        group_id = data.get("id")
        GroupService.delete_group(db, group_id)
        return ApiResponse.ok(message="删除成功", action=action)

    else:
        return ApiResponse.error(message=f"未知的操作类型: {action}", code=400, action=action)
