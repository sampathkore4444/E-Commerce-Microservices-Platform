# audit_service/app/api/logs.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.infrastructure.models import EventLog
from typing import List

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/logs", response_model=List[dict])
def list_logs(db: Session = Depends(get_db)):
    return [
        l.__dict__ for l in db.query(EventLog).order_by(EventLog.timestamp.desc()).all()
    ]


@router.get("/logs/{service_name}", response_model=List[dict])
def logs_by_service(service_name: str, db: Session = Depends(get_db)):
    return [
        l.__dict__
        for l in db.query(EventLog)
        .filter(EventLog.service == service_name)
        .order_by(EventLog.timestamp.desc())
        .all()
    ]
