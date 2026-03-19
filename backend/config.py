"""应用配置模块，从环境变量加载所有配置项。"""

import logging
import os
import warnings
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

logger = logging.getLogger(__name__)


def _safe_int(value: str | None, default: int) -> int:
    """安全地将环境变量转为 int，非法值时回退默认值。"""
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        logger.warning("环境变量值 '%s' 无法转为整数，使用默认值 %d", value, default)
        return default


class Settings:
    """全局配置，从 .env 文件读取。"""

    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    DEEPSEEK_MODEL: str = "deepseek-chat"

    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT: int = _safe_int(os.getenv("MYSQL_PORT"), 3306)
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "nl2sql_platform")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-me-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = _safe_int(os.getenv("JWT_EXPIRE_MINUTES"), 1440)

    def __init__(self) -> None:
        if self.JWT_SECRET_KEY == "change-me-in-production":
            warnings.warn(
                "JWT_SECRET_KEY 使用默认值，请在 .env 中设置安全密钥",
                stacklevel=2,
            )

    @property
    def database_url(self) -> str:
        """构建 SQLAlchemy 数据库连接 URL。"""
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
            "?charset=utf8mb4"
        )


settings = Settings()
