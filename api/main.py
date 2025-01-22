from fastapi import APIRouter

from api.routes import events, search, status

api_router = APIRouter()
api_router.include_router(status.router)
api_router.include_router(search.router)
api_router.include_router(events.router)