from fastapi import HTTPException, status
from typing import Union

from fastapi import APIRouter

from utils.events import GetEvents, GetEvent

router = APIRouter(prefix="/events")


@router.get("/")
async def events(q: Union[str, None] = None):
    data = GetEvents()

    events = {}
    for event in data:
        events[str(event["timestamp"])] = event

    return events


@router.get("/{id}")
async def event(id: str, q: Union[str, None] = None):
    data = GetEvent(id)

    return data
