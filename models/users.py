from datetime import datetime

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, Integer, String, Date, Boolean, Float
from database import Base


class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    username = Column(String, nullable=True)
    transcripts = Column(Integer, nullable=False, default=0)
    register_at = Column(Date, nullable=False, default=datetime.utcnow)
    super_user = Column(Boolean, nullable=False, default=False)


class Payments(Base):
    __tablename__ = "Payments"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False, default=datetime.utcnow)
    status = Column(String, nullable=False)
