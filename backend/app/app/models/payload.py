from pydantic import BaseModel


class NumberToEnglishPayload(BaseModel):
    number: int
