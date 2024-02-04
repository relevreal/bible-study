from fastapi import FastAPI

from app.core.config import config
from app.api.api import api_router


app = FastAPI(
    title=config.PROJECT_NAME,
    openapi_prefix=config.OPENAPI_PREFIX,
)

app.include_router(
    api_router,
    prefix=config.API_PREFIX,
)
