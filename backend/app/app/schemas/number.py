from typing import Optional

from pydantic import BaseModel


# Shared properties
class NumberBase(BaseModel):
    number: Optional[str] = None
    number_in_english: Optional[str] = None


# Properties to receive on Number creation
class NumberCreate(NumberBase):
    number: str


# Properties to receive on Number update
class NumberUpdate(NumberBase):
    pass


# Properties shared by models stored in DB
class NumberInDBBase(NumberBase):
    id: int
    number: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Number(NumberInDBBase):
    pass


# Properties properties stored in DB
class NumberInDB(NumberInDBBase):
    pass
