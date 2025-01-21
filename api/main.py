from fastapi import APIRouter

from api.routes import status, search

api_router = APIRouter()
api_router.include_router(status.router)
api_router.include_router(search.router)