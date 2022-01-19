from pydantic import BaseModel


class NumberToEnglishResult(BaseModel):
    status: str = 'ok'
    number_in_english: str