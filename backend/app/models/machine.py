import enum

from sqlalchemy import Column, Integer, String, Text, Float, BigInteger, DateTime, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import BaseModelMixin


class MachineStatus(str, enum.Enum):
    """机器状态枚举"""
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


class AuthType(str, enum.Enum):
    """认证类型枚举"""
    PASSWORD = "password"
    KEY = "key"


# 机器-标签关联表
machine_tag_relation = Table(
    "machine_tag_relation",
    Base.metadata,
    Column("machine_id", Integer, ForeignKey("machines.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("machine_tags.id"), primary_key=True),
)

# 机器-分组关联表
machine_group_relation = Table(
    "machine_group_relation",
    Base.metadata,
    Column("machine_id", Integer, ForeignKey("machines.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("machine_groups.id"), primary_key=True),
)


class Machine(Base, BaseModelMixin):
    """机器模型"""
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="机器名称")
    hostname = Column(String(255), nullable=False, comment="主机名/IP地址")
    port = Column(Integer, default=22, comment="SSH端口")
    username = Column(String(50), nullable=False, comment="SSH用户名")
    auth_type = Column(Enum(AuthType), default=AuthType.PASSWORD, comment="认证类型")
    password = Column(String(255), comment="密码（加密存储）")
    private_key = Column(Text, comment="私钥内容（加密存储）")
    os_type = Column(String(50), comment="操作系统类型")
    status = Column(Enum(MachineStatus), default=MachineStatus.OFFLINE, comment="机器状态")
    cpu_cores = Column(Integer, comment="CPU核数")
    memory_total = Column(BigInteger, comment="总内存(MB)")
    disk_total = Column(BigInteger, comment="总磁盘(GB)")
    cpu_usage = Column(Float, comment="CPU使用率")
    memory_usage = Column(Float, comment="内存使用率")
    disk_usage = Column(Float, comment="磁盘使用率")
    environment = Column(String(50), comment="所属环境：dev/test/prod")
    last_heartbeat = Column(DateTime, comment="最后心跳时间")
    description = Column(Text, comment="描述")

    # 关联关系
    tags = relationship("MachineTag", secondary=machine_tag_relation, back_populates="machines")
    groups = relationship("MachineGroup", secondary=machine_group_relation, back_populates="machines")

    def __repr__(self):
        return f"<Machine(id={self.id}, name='{self.name}', hostname='{self.hostname}')>"


class MachineGroup(Base, BaseModelMixin):
    """机器分组模型"""
    __tablename__ = "machine_groups"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, comment="分组名称")
    description = Column(Text, comment="分组描述")

    # 关联关系
    machines = relationship("Machine", secondary=machine_group_relation, back_populates="groups")

    def __repr__(self):
        return f"<MachineGroup(id={self.id}, name='{self.name}')>"


class MachineTag(Base, BaseModelMixin):
    """机器标签模型"""
    __tablename__ = "machine_tags"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True, comment="标签名称")
    color = Column(String(7), default="#1890ff", comment="标签颜色")

    # 关联关系
    machines = relationship("Machine", secondary=machine_tag_relation, back_populates="tags")

    def __repr__(self):
        return f"<MachineTag(id={self.id}, name='{self.name}')>"
