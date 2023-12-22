from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, Boolean
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
