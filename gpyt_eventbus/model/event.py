import datetime
import uuid
from typing import Any, Dict

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
            "timestamp": str(self.timestamp),
            "aggregate_name": self.aggregate_name,
            "revision": self.revision,
        }

    @staticmethod
    def from_dict(event_dict: Dict[Any, Any]) -> "Event":
        event = Event()
        event.aggregate_id = event_dict["aggregate_id"]
        event.data = event_dict["data"]
        event.meta_data = event_dict["meta_data"]
        if "timestamp" in event_dict.keys():
            event.timestamp = datetime.datetime.strptime(
                event_dict["timestamp"], "%Y-%m-%d %H:%M:%S.%f"
            )
        event.aggregate_name = event_dict["aggregate_name"]
        event.revision = event_dict["revision"]
        return event
