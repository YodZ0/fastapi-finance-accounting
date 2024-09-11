from pathlib import Path

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_DIR = BASE_DIR / "media"


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    # add v1 blocks here
    auth: str = "/auth"
    users: str = "/users"
    categories: str = "/categories"
    roles: str = "/roles"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    # add versions here
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
    base_dir: Path = BASE_DIR  # ..\fastapi-finance-accounting\backend
    media_dir: Path = MEDIA_DIR  # ..\fastapi-finance-accounting\backend\media


settings = Settings()
