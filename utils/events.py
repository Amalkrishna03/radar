from utils.source import SupabaseClient
from utils.storage import CreatePublicURL
from pydantic import BaseModel
from typing import Optional

class Event(BaseModel):
    id: str
    text: Optional[str] = None
    url: str
    timestamp: float
    extraData: Optional[dict] = None

def GetEvents() -> list[Event]:
    response = SupabaseClient.table("events").select("*").order("timestamp", desc=True).execute()

    return response.data

def GetEvent(id: str) -> Event:
    response = SupabaseClient.table("events").select("*").eq("id", id).execute()
    
    if len(response.data):
        data = response.data[0] | CreatePublicURL(id)
        return data
        
    return {}