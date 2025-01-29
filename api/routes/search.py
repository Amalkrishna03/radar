from fastapi import HTTPException, status
from typing import Union

from fastapi import APIRouter

from utils.situation import RunSearchSituation

router = APIRouter(prefix="/search")


@router.get("/")
async def search(q: Union[str, None] = None):
    if q and len(q) >= 5:
        data = RunSearchSituation(q)
        if data is None:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No data found"
            )
            
        
        return data
    
    return []
