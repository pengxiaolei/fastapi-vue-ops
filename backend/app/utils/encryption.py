from cryptography.fernet import Fernet

from app.config import settings


class EncryptionUtil:
    """加密工具类"""

    def __init__(self):
        self._fernet = Fernet(settings.encryption_key.encode())

    def encrypt(self, plain_text: str) -> str:
        """加密字符串"""
        if not plain_text:
            return plain_text
        return self._fernet.encrypt(plain_text.encode()).decode()

    def decrypt(self, encrypted_text: str) -> str:
        """解密字符串"""
        if not encrypted_text:
            return encrypted_text
        return self._fernet.decrypt(encrypted_text.encode()).decode()


# 全局加密工具实例
encryption_util = EncryptionUtil()
