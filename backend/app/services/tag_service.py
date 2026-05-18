from typing import Optional, List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.machine import MachineTag
from app.schemas.machine import TagCreate, TagUpdate


class TagService:
    """标签服务类"""

    @staticmethod
    def get_tag(db: Session, tag_id: int) -> Optional[MachineTag]:
        """根据ID获取标签"""
        return db.query(MachineTag).filter(
            and_(MachineTag.id == tag_id, MachineTag.is_deleted == False)
        ).first()

    @staticmethod
    def get_tag_by_name(db: Session, name: str) -> Optional[MachineTag]:
        """根据名称获取标签"""
        return db.query(MachineTag).filter(
            and_(MachineTag.name == name, MachineTag.is_deleted == False)
        ).first()

    @staticmethod
    def get_tags(db: Session, skip: int = 0, limit: int = 100) -> List[MachineTag]:
        """获取标签列表"""
        return db.query(MachineTag).filter(
            MachineTag.is_deleted == False
        ).order_by(MachineTag.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def create_tag(db: Session, tag_in: TagCreate) -> MachineTag:
        """创建标签"""
        tag = MachineTag(**tag_in.model_dump())
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag

    @staticmethod
    def update_tag(db: Session, tag_id: int, tag_in: TagUpdate) -> Optional[MachineTag]:
        """更新标签"""
        tag = TagService.get_tag(db, tag_id)
        if not tag:
            return None

        update_data = tag_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tag, field, value)

        db.commit()
        db.refresh(tag)
        return tag

    @staticmethod
    def delete_tag(db: Session, tag_id: int) -> bool:
        """删除标签（软删除）"""
        tag = TagService.get_tag(db, tag_id)
        if not tag:
            return False

        tag.is_deleted = True
        db.commit()
        return True
