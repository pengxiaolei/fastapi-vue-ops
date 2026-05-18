from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import ApiRequest, ApiResponse
from app.schemas.machine import TagCreate, TagUpdate, TagResponse
from app.services.tag_service import TagService

router = APIRouter()


@router.post("", response_model=ApiResponse)
async def tag_operations(
    request: ApiRequest[dict],
    db: Session = Depends(get_db),
):
    """
    标签管理统一入口

    action 功能标识:
    - tag.list: 获取标签列表
    - tag.get: 获取标签详情
    - tag.create: 创建标签
    - tag.update: 更新标签
    - tag.delete: 删除标签
    """
    action = request.action
    data = request.data or {}

    # 获取标签列表
    if action == "tag.list":
        skip = data.get("skip", 0)
        limit = data.get("limit", 100)
        tags = TagService.get_tags(db, skip=skip, limit=limit)
        return ApiResponse.ok(data=tags, action=action)

    # 获取标签详情
    elif action == "tag.get":
        tag_id = data.get("id")
        tag = TagService.get_tag(db, tag_id)
        return ApiResponse.ok(data=tag, action=action)

    # 创建标签
    elif action == "tag.create":
        tag_data = TagCreate(**data)
        tag = TagService.create_tag(db, tag_data)
        return ApiResponse.ok(data=tag, message="创建成功", action=action)

    # 更新标签
    elif action == "tag.update":
        tag_id = data.get("id")
        update_data = TagUpdate(**{k: v for k, v in data.items() if k != "id"})
        tag = TagService.update_tag(db, tag_id, update_data)
        return ApiResponse.ok(data=tag, message="更新成功", action=action)

    # 删除标签
    elif action == "tag.delete":
        tag_id = data.get("id")
        TagService.delete_tag(db, tag_id)
        return ApiResponse.ok(message="删除成功", action=action)

    else:
        return ApiResponse.error(message=f"未知的操作类型: {action}", code=400, action=action)
