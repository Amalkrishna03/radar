
from fastapi import APIRouter

router = APIRouter(prefix="/status")

@router.get("/")
def main():
    return {"status": "OK"}