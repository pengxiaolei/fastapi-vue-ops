from typing import List
from pydantic_settings import BaseSettings
from cryptography.fernet import Fernet

class Settings(BaseSettings):
    """应用配置类"""
    # 基础配置
    app_name: str = "DevOps Platform"
    app_version: str = "1.0.0"
    debug: bool = True
    # 服务配置
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    # 数据库配置
    database_url: str = "sqlite:///./devops.db"
    # 加密配置 - 用于加密SSH密码和私钥
    encryption_key: str = "BDSyZyOldk20hQHyD1Vr3mTmmJveQy1i9dtLJNe8TGM="
    # SSH配置
    ssh_timeout: int = 10
    ssh_banner_timeout: int = 30

    # CORS配置
    cors_allow_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    # 日志配置
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    # 分页配置
    default_page_size: int = 20
    max_page_size: int = 100
    # 安全配置
    max_login_attempts: int = 5
    jwt_secret_key: str = "your-jwt-secret-key"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24小时

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 创建设置实例
settings = Settings()
