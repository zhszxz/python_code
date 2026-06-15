from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """项目配置：学习项目默认使用 SQLite，生产环境可通过环境变量覆盖。"""

    app_name: str = "FastAPI RBAC Admin"
    api_prefix: str = "/api/v1"
    database_url: str = f"sqlite:///{BASE_DIR / 'rbac.db'}"
    secret_key: str = "change-this-secret-key-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 8
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
