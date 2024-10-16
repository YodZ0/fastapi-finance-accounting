from pathlib import Path

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_DIR = BASE_DIR / "media"
LOGS_DIR = BASE_DIR / "logs"

if not MEDIA_DIR.exists():
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)

if not LOGS_DIR.exists():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"
    categories: str = "/categories"
    periods: str = "/periods"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

    @property
    def bearer_token_url(self) -> str:
        parts = (self.prefix, self.v1.prefix, self.v1.auth, "/login")
        path = "".join(parts)
        return path.removeprefix("/")


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AccessTokenConfig(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class LoggingConfig(BaseModel):
    path: Path = LOGS_DIR
    format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{line} - {message}"
    levels: tuple[str] = (
        "DEBUG",
        "INFO",
        "SUCCESS",
        "WARNING",
        "ERROR",
    )
    rotation: str = "100 KB"
    compression: str = "zip"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        env_file=(".env.template", ".env"),
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DataBaseConfig
    access_token: AccessTokenConfig
    logs: LoggingConfig = LoggingConfig()
    base_dir: Path = BASE_DIR  # ..\fastapi-finance-accounting\backend\
    media_dir: Path = MEDIA_DIR  # ..\fastapi-finance-accounting\backend\media


settings = Settings()
