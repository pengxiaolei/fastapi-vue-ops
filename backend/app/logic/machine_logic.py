"""
机器管理业务逻辑层
负责处理机器相关的核心业务逻辑
"""
from typing import Tuple, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.schemas.machine import (
    MachineCreate,
    MachineUpdate,
    MachineResponse,
    MachineListResponse,
    ConnectionTestRequest,
    ConnectionTestResponse,
    MachineStatusResponse,
)
from app.services.machine_service import MachineService


class MachineLogic:
    """机器管理业务逻辑"""

    @staticmethod
    def get_machine_list(
        db: Session,
        page: int = 1,
        page_size: int = 20,
        keyword: Optional[str] = None,
        status: Optional[str] = None,
        environment: Optional[str] = None,
    ) -> MachineListResponse:
        """获取机器列表业务逻辑"""
        skip = (page - 1) * page_size
        machines, total = MachineService.get_machines(
            db, skip=skip, limit=page_size, keyword=keyword,
            status=status, environment=environment
        )

        return MachineListResponse(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size,
            data=machines
        )

    @staticmethod
    def get_machine_detail(db: Session, machine_id: int) -> MachineResponse:
        """获取机器详情业务逻辑"""
        return MachineService.get_machine(db, machine_id)

    @staticmethod
    def create_machine(db: Session, data: MachineCreate) -> MachineResponse:
        """创建机器业务逻辑"""
        return MachineService.create_machine(db, data)

    @staticmethod
    def update_machine(db: Session, machine_id: int, data: Dict[str, Any]) -> MachineResponse:
        """更新机器业务逻辑"""
        update_data = MachineUpdate(**{k: v for k, v in data.items() if k != "id"})
        return MachineService.update_machine(db, machine_id, update_data)

    @staticmethod
    def delete_machine(db: Session, machine_id: int) -> Dict[str, Any]:
        """删除机器业务逻辑"""
        MachineService.delete_machine(db, machine_id)
        return {"success": True, "message": "删除成功"}

    @staticmethod
    def test_connection(data: ConnectionTestRequest) -> ConnectionTestResponse:
        """测试SSH连接业务逻辑"""
        success, message, sys_info = MachineService.test_connection(
            hostname=data.hostname,
            port=data.port,
            username=data.username,
            auth_type=data.auth_type,
            password=getattr(data, "password", None),
            private_key=getattr(data, "private_key", None),
        )

        return ConnectionTestResponse(
            success=success,
            message=message,
            **sys_info
        )

    @staticmethod
    def test_saved_connection(db: Session, machine_id: int) -> ConnectionTestResponse:
        """测试已保存机器的连接业务逻辑"""
        success, message, sys_info = MachineService.test_machine_connection(db, machine_id)
        return ConnectionTestResponse(
            success=success,
            message=message,
            **sys_info
        )

    @staticmethod
    def refresh_machine_status(db: Session, machine_id: int) -> MachineStatusResponse:
        """刷新机器状态业务逻辑"""
        success, message = MachineService.refresh_machine_status(db, machine_id)
        machine = MachineService.get_machine(db, machine_id)

        return MachineStatusResponse(
            success=success,
            message=message,
            status=machine.status if machine else None,
            cpu_usage=machine.cpu_usage if machine else None,
            memory_usage=machine.memory_usage if machine else None,
            disk_usage=machine.disk_usage if machine else None,
        )

    @staticmethod
    def add_tag_to_machine(db: Session, machine_id: int, tag_id: int) -> Dict[str, Any]:
        """给机器添加标签业务逻辑"""
        MachineService.add_tag_to_machine(db, machine_id, tag_id)
        return {"success": True, "message": "添加标签成功"}

    @staticmethod
    def remove_tag_from_machine(db: Session, machine_id: int, tag_id: int) -> Dict[str, Any]:
        """移除机器标签业务逻辑"""
        MachineService.remove_tag_from_machine(db, machine_id, tag_id)
        return {"success": True, "message": "移除标签成功"}

    @staticmethod
    def add_machine_to_group(db: Session, machine_id: int, group_id: int) -> Dict[str, Any]:
        """将机器添加到分组业务逻辑"""
        MachineService.add_machine_to_group(db, machine_id, group_id)
        return {"success": True, "message": "添加到分组成功"}

    @staticmethod
    def remove_machine_from_group(db: Session, machine_id: int, group_id: int) -> Dict[str, Any]:
        """将机器从分组移除业务逻辑"""
        MachineService.remove_machine_from_group(db, machine_id, group_id)
        return {"success": True, "message": "从分组移除成功"}
