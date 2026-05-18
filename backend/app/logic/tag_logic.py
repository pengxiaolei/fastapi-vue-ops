"""
标签管理业务逻辑层
负责处理标签相关的核心业务逻辑
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.schemas.machine import TagCreate, TagUpdate, TagResponse
from app.services.tag_service import TagService


class TagLogic:
    """标签管理业务逻辑"""

    @staticmethod
    def get_tag_list(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[TagResponse]:
        """获取标签列表业务逻辑"""
        return TagService.get_tags(db, skip=skip, limit=limit)

    @staticmethod
    def get_tag_detail(db: Session, tag_id: int) -> TagResponse:
        """获取标签详情业务逻辑"""
        return TagService.get_tag(db, tag_id)

    @staticmethod
    def create_tag(db: Session, data: TagCreate) -> TagResponse:
        """创建标签业务逻辑"""
        return TagService.create_tag(db, data)

    @staticmethod
    def update_tag(db: Session, tag_id: int, data: Dict[str, Any]) -> TagResponse:
        """更新标签业务逻辑"""
        update_data = TagUpdate(**{k: v for k, v in data.items() if k != "id"})
        return TagService.update_tag(db, tag_id, update_data)

    @staticmethod
    def delete_tag(db: Session, tag_id: int) -> Dict[str, Any]:
        """删除标签业务逻辑"""
        TagService.delete_tag(db, tag_id)
        return {"success": True, "message": "删除成功"}
