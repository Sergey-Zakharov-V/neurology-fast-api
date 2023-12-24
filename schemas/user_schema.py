from datetime import date

from pydantic import BaseModel, json
from typing import Optional


class UserSchema(BaseModel):
    key: Optional[str] = None
    user_id: Optional[str] = None
    username: str
    transcripts: Optional[int] = None

    class Config:
        from_attributes = True


class UserData(BaseModel):
    day: int
    month: int
    year: int
    name: str
    gender: str


class UserFullSchema(BaseModel):
    key: Optional[str] = None
    user_id: Optional[str] = None
    username: str
    transcripts: Optional[int] = None
    day: int
    month: int
    year: int
    name: str
    gender: str

    class Config:
        from_attributes = True


class PaymentSchema(BaseModel):
    username: str
    price: Optional[float] = None
    description: Optional[str] = None
    data: json
    date: Optional[date] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
