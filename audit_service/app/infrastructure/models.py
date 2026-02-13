# audit_service/app/infrastructure/models.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class EventLog(Base):
    __tablename__ = "event_logs"
    id = Column(Integer, primary_key=True)
    service = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now())
