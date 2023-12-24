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
    price: float | None = None
    description: str | None = None
    data: json
    date: date | None = None
    status: str | None = None

    class Config:
        from_attributes = True
