from fastapi import APIRouter, Depends
from app.config.config import Configuration, get_config

router = APIRouter()

@router.get("/config")
def read_config(config: Configuration = Depends(get_config)):
    return {
    }

