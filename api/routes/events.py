from fastapi import HTTPException, status
from typing import Union

from fastapi import APIRouter

from utils.events import GetEvents, GetEvent
from utils.storage import CreatePublicURL

router = APIRouter(prefix="/events")


@router.get("/")
async def events(q: Union[str, None] = None):
    data = GetEvents()

    events = {}
    for e in data:
        events[str(e["timestamp"])] = e

    return events

@router.get("/images")
async def eventsWithImages(q: Union[str, None] = None):
    data = GetEvents()

    for e in data:
        e["url"] = CreatePublicURL(e["id"])

    return data




@router.get("/{id}")
async def event(id: str, q: Union[str, None] = None):
    data = GetEvent(id)

    return data
