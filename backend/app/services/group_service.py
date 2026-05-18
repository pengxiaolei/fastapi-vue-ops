from typing import Optional, List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.machine import MachineGroup
from app.schemas.machine import GroupCreate, GroupUpdate


class GroupService:
    """分组服务类"""

    @staticmethod
    def get_group(db: Session, group_id: int) -> Optional[MachineGroup]:
        """根据ID获取分组"""
        return db.query(MachineGroup).filter(
            and_(MachineGroup.id == group_id, MachineGroup.is_deleted == False)
        ).first()

    @staticmethod
    def get_group_by_name(db: Session, name: str) -> Optional[MachineGroup]:
        """根据名称获取分组"""
        return db.query(MachineGroup).filter(
            and_(MachineGroup.name == name, MachineGroup.is_deleted == False)
        ).first()

    @staticmethod
    def get_groups(db: Session, skip: int = 0, limit: int = 100) -> List[MachineGroup]:
        """获取分组列表"""
        return db.query(MachineGroup).filter(
            MachineGroup.is_deleted == False
        ).order_by(MachineGroup.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def create_group(db: Session, group_in: GroupCreate) -> MachineGroup:
        """创建分组"""
        group = MachineGroup(**group_in.model_dump())
        db.add(group)
        db.commit()
        db.refresh(group)
        return group

    @staticmethod
    def update_group(db: Session, group_id: int, group_in: GroupUpdate) -> Optional[MachineGroup]:
        """更新分组"""
        group = GroupService.get_group(db, group_id)
        if not group:
            return None

        update_data = group_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(group, field, value)

        db.commit()
        db.refresh(group)
        return group

    @staticmethod
    def delete_group(db: Session, group_id: int) -> bool:
        """删除分组（软删除）"""
        group = GroupService.get_group(db, group_id)
        if not group:
            return False

        group.is_deleted = True
        db.commit()
        return True
