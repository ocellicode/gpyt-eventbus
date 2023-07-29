from sqlalchemy import Column, String

from gpyt_eventbus.model.base import Base


class Subscriber(Base):
    __tablename__ = "subscriber"

    url = Column(String(255), nullable=False, primary_key=True)
