from typing import Optional, List, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.machine import Machine, MachineStatus, AuthType
from app.schemas.machine import MachineCreate, MachineUpdate, ConnectionTestRequest
from app.utils.encryption import encryption_util
from app.utils.ssh_client import SSHClient


class MachineService:
    """机器服务类"""

    @staticmethod
    def get_machine(db: Session, machine_id: int) -> Optional[Machine]:
        """根据ID获取机器"""
        return db.query(Machine).filter(
            and_(Machine.id == machine_id, Machine.is_deleted == False)
        ).first()

    @staticmethod
    def get_machines(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        keyword: Optional[str] = None,
        status: Optional[MachineStatus] = None,
        environment: Optional[str] = None,
    ) -> Tuple[List[Machine], int]:
        """获取机器列表，支持分页和筛选"""
        query = db.query(Machine).filter(Machine.is_deleted == False)

        if keyword:
            query = query.filter(
                Machine.name.contains(keyword) | Machine.hostname.contains(keyword)
            )

        if status:
            query = query.filter(Machine.status == status)

        if environment:
            query = query.filter(Machine.environment == environment)

        total = query.count()
        machines = query.order_by(Machine.created_at.desc()).offset(skip).limit(limit).all()

        return machines, total

    @staticmethod
    def create_machine(db: Session, machine_in: MachineCreate) -> Machine:
        """创建机器"""
        machine_data = machine_in.model_dump()

        # 加密敏感信息
        if machine_data.get("password"):
            machine_data["password"] = encryption_util.encrypt(machine_data["password"])
        if machine_data.get("private_key"):
            machine_data["private_key"] = encryption_util.encrypt(machine_data["private_key"])

        machine = Machine(**machine_data)
        db.add(machine)
        db.commit()
        db.refresh(machine)
        return machine

    @staticmethod
    def update_machine(db: Session, machine_id: int, machine_in: MachineUpdate) -> Optional[Machine]:
        """更新机器"""
        machine = MachineService.get_machine(db, machine_id)
        if not machine:
            return None

        update_data = machine_in.model_dump(exclude_unset=True)

        # 加密敏感信息
        if "password" in update_data and update_data["password"]:
            update_data["password"] = encryption_util.encrypt(update_data["password"])
        if "private_key" in update_data and update_data["private_key"]:
            update_data["private_key"] = encryption_util.encrypt(update_data["private_key"])

        for field, value in update_data.items():
            setattr(machine, field, value)

        db.commit()
        db.refresh(machine)
        return machine

    @staticmethod
    def delete_machine(db: Session, machine_id: int) -> bool:
        """删除机器（软删除）"""
        machine = MachineService.get_machine(db, machine_id)
        if not machine:
            return False

        machine.is_deleted = True
        db.commit()
        return True

    @staticmethod
    def test_connection(
        hostname: str,
        port: int,
        username: str,
        auth_type: AuthType,
        password: Optional[str] = None,
        private_key: Optional[str] = None,
    ) -> Tuple[bool, str, dict]:
        """测试SSH连接"""
        try:
            with SSHClient(
                hostname=hostname,
                port=port,
                username=username,
                auth_type=auth_type,
                password=password,
                private_key=private_key,
            ) as client:
                system_info = client.get_system_info()
                return True, "连接成功", system_info
        except Exception as e:
            return False, str(e), {}

    @staticmethod
    def test_machine_connection(db: Session, machine_id: int) -> Tuple[bool, str, dict]:
        """测试已保存机器的连接"""
        machine = MachineService.get_machine(db, machine_id)
        if not machine:
            return False, "机器不存在", {}

        # 解密敏感信息
        password = None
        private_key = None

        if machine.password:
            password = encryption_util.decrypt(machine.password)
        if machine.private_key:
            private_key = encryption_util.decrypt(machine.private_key)

        return MachineService.test_connection(
            hostname=machine.hostname,
            port=machine.port,
            username=machine.username,
            auth_type=machine.auth_type,
            password=password,
            private_key=private_key,
        )

    @staticmethod
    def refresh_machine_status(db: Session, machine_id: int) -> Tuple[bool, str]:
        """刷新机器状态"""
        machine = MachineService.get_machine(db, machine_id)
        if not machine:
            return False, "机器不存在"

        success, message, system_info = MachineService.test_machine_connection(db, machine_id)

        from datetime import datetime
        machine.last_heartbeat = datetime.now()

        if success:
            machine.status = MachineStatus.ONLINE
            if system_info.get("os_type"):
                machine.os_type = system_info["os_type"]
            if system_info.get("cpu_cores"):
                machine.cpu_cores = system_info["cpu_cores"]
            if system_info.get("memory_total"):
                machine.memory_total = system_info["memory_total"]
            if system_info.get("disk_total"):
                machine.disk_total = system_info["disk_total"]
            if system_info.get("cpu_usage") is not None:
                machine.cpu_usage = system_info["cpu_usage"]
            if system_info.get("memory_usage") is not None:
                machine.memory_usage = system_info["memory_usage"]
            if system_info.get("disk_usage") is not None:
                machine.disk_usage = system_info["disk_usage"]
        else:
            machine.status = MachineStatus.OFFLINE

        db.commit()
        db.refresh(machine)
        return success, message

    @staticmethod
    def add_tag_to_machine(db: Session, machine_id: int, tag_id: int) -> bool:
        """给机器添加标签"""
        from app.models.machine import MachineTag

        machine = MachineService.get_machine(db, machine_id)
        tag = db.query(MachineTag).filter(MachineTag.id == tag_id).first()

        if not machine or not tag:
            return False

        if tag not in machine.tags:
            machine.tags.append(tag)
            db.commit()

        return True

    @staticmethod
    def remove_tag_from_machine(db: Session, machine_id: int, tag_id: int) -> bool:
        """移除机器标签"""
        from app.models.machine import MachineTag

        machine = MachineService.get_machine(db, machine_id)
        tag = db.query(MachineTag).filter(MachineTag.id == tag_id).first()

        if not machine or not tag:
            return False

        if tag in machine.tags:
            machine.tags.remove(tag)
            db.commit()

        return True

    @staticmethod
    def add_machine_to_group(db: Session, machine_id: int, group_id: int) -> bool:
        """将机器添加到分组"""
        from app.models.machine import MachineGroup

        machine = MachineService.get_machine(db, machine_id)
        group = db.query(MachineGroup).filter(MachineGroup.id == group_id).first()

        if not machine or not group:
            return False

        if group not in machine.groups:
            machine.groups.append(group)
            db.commit()

        return True

    @staticmethod
    def remove_machine_from_group(db: Session, machine_id: int, group_id: int) -> bool:
        """将机器从分组移除"""
        from app.models.machine import MachineGroup

        machine = MachineService.get_machine(db, machine_id)
        group = db.query(MachineGroup).filter(MachineGroup.id == group_id).first()

        if not machine or not group:
            return False

        if group in machine.groups:
            machine.groups.remove(group)
            db.commit()

        return True
