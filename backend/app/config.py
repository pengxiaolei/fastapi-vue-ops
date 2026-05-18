from typing import List
from pydantic_settings import BaseSettings


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

    # 数据库配置 - MySQL
    database_url: str = "mysql+pymysql://root:root@192.168.110.64:31481/devops_db?charset=utf8mb4"

    # 加密配置 - 用于加密SSH密码和私钥
    encryption_key: str = "BDSyZyOldk20hQHyD1Vr3mTmmJveQy1i9dtLJNe8TGM="

    # SSH配置
    ssh_timeout: int = 10
    ssh_banner_timeout: int = 30

    # CORS配置
    cors_allow_origins: str | List[str] = "*"
    cors_allow_credentials: bool = True
    cors_allow_methods: str | List[str] = "*"
    cors_allow_headers: str | List[str] = "*"

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

    def get_cors_origins(self) -> List[str]:
        """获取CORS允许的源列表"""
        if isinstance(self.cors_allow_origins, str):
            if self.cors_allow_origins == "*":
                return ["*"]
            return [origin.strip() for origin in self.cors_allow_origins.split(",")]
        return self.cors_allow_origins

    def get_cors_methods(self) -> List[str]:
        """获取CORS允许的方法列表"""
        if isinstance(self.cors_allow_methods, str):
            if self.cors_allow_methods == "*":
                return ["*"]
            return [method.strip() for method in self.cors_allow_methods.split(",")]
        return self.cors_allow_methods

    def get_cors_headers(self) -> List[str]:
        """获取CORS允许的头列表"""
        if isinstance(self.cors_allow_headers, str):
            if self.cors_allow_headers == "*":
                return ["*"]
            return [header.strip() for header in self.cors_allow_headers.split(",")]
        return self.cors_allow_headers


# 创建设置实例
settings = Settings()
