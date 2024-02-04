from typing import (
    Annotated,
    Any,
)

from pydantic import (
    AnyHttpUrl,
    UrlConstraints,
    field_validator,
    ValidationInfo,
)
from pydantic_core import Url
from pydantic_settings import BaseSettings

SqliteDsn = Annotated[
    Url,
    UrlConstraints(
        host_required=False,
        allowed_schemes=[
            "sqlite",
            "sqlite+pysqlite",
        ],
        default_path=":memory:",
    ),
]


class Config(BaseSettings):
    PROJECT_NAME: str = "bible-study-api"
    OPENAPI_PREFIX: str = ""
    API_PREFIX: str = "/api"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000"]
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> str | list[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [o.strip() for o in v.split(",")]
        elif isinstance(v, str | list):
            return v
        raise ValueError(v)

    SQLITE_DB: str = "bible.db"
    SQLALCHEMY_DATABASE_URI: SqliteDsn | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI")
    @classmethod
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return SqliteDsn.build(
            scheme="sqlite+pysqlite",
            host="",
            path=f"{info.data.get('SQLITE_DB', ':memory:')}",
        )


config = Config()
