import datetime
import uuid

from sqlalchemy import JSON, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    aggregate_id = Column(String, default=str(uuid.uuid4()))
    data = Column(JSON)
    meta_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    aggregate_name = Column(String)
    revision = Column(Integer, default=0)

    def dict(self):
        return {
            "aggregate_id": self.aggregate_id,
            "data": self.data,
            "meta_data": self.meta_data,
            "timestamp": self.timestamp,
            "aggregate_name": self.aggregate_name,
            "revision": self.revision,
        }
