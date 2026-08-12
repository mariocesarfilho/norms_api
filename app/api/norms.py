from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import db.schema
from db.database import Session, engine

router = APIRouter()

@router.get("/norms", tags=["norms"])
async def read_norms():
    return