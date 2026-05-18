from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean


class BaseModelMixin:
    """基础模型混入类，提供通用字段"""

    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    is_deleted = Column(Boolean, default=False, comment="是否删除")
