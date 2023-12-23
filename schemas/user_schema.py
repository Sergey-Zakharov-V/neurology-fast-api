from pydantic import BaseModel
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
