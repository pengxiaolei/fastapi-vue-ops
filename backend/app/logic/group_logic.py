"""
分组管理业务逻辑层
负责处理分组相关的核心业务逻辑
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.schemas.machine import GroupCreate, GroupUpdate, GroupResponse
from app.services.group_service import GroupService


class GroupLogic:
    """分组管理业务逻辑"""

    @staticmethod
    def get_group_list(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[GroupResponse]:
        """获取分组列表业务逻辑"""
        return GroupService.get_groups(db, skip=skip, limit=limit)

    @staticmethod
    def get_group_detail(db: Session, group_id: int) -> GroupResponse:
        """获取分组详情业务逻辑"""
        return GroupService.get_group(db, group_id)

    @staticmethod
    def create_group(db: Session, data: GroupCreate) -> GroupResponse:
        """创建分组业务逻辑"""
        return GroupService.create_group(db, data)

    @staticmethod
    def update_group(db: Session, group_id: int, data: Dict[str, Any]) -> GroupResponse:
        """更新分组业务逻辑"""
        update_data = GroupUpdate(**{k: v for k, v in data.items() if k != "id"})
        return GroupService.update_group(db, group_id, update_data)

    @staticmethod
    def delete_group(db: Session, group_id: int) -> Dict[str, Any]:
        """删除分组业务逻辑"""
        GroupService.delete_group(db, group_id)
        return {"success": True, "message": "删除成功"}
