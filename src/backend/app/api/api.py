from fastapi import APIRouter

from app.api.endpoints import (
    verses,
)

api_router = APIRouter()

api_router.include_router(
    verses.router,
    prefix="/verses",
    tags=["verses"],
)
