from fastapi import APIRouter, Depends
from starlette.requests import Request
from app.core import security
from app.models.payload import NumberToEnglishPayload
from app.models.transformation import NumberToEnglishResult
from app.services.transformer import NumberToEnglishTransformer

router = APIRouter()

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Any, List
from app import crud, models, schemas
from app.api import deps
from sqlalchemy.orm import Session


@router.post("/num_in_english", response_model=NumberToEnglishResult, name="num_in_english")
def post_num_in_english(
    request: Request,
    authenticated: bool = Depends(security.validate_request),
    block_data: NumberToEnglishPayload = {"number": 123456789},
) -> NumberToEnglishResult:
    try:
        model = NumberToEnglishTransformer()
        num_in_english: NumberToEnglishResult = model.transform(block_data)
        item = {"status": "ok", "num_in_english": num_in_english}
        json_compatible_item_data = jsonable_encoder(item)
        return JSONResponse(content=json_compatible_item_data)
    except:
        item = {"status": "failed",
                "num_in_english": "processing failed please check the payload formatting and try again"}
        json_compatible_item_data = jsonable_encoder(item)
        return JSONResponse(content=json_compatible_item_data)


@router.get("/num_in_english", response_model=NumberToEnglishResult, name="num_in_english")
def get_num_in_english(
    request: Request,
    authenticated: bool = Depends(security.validate_request),
    number: int = 123456789,
) -> NumberToEnglishResult:

    try:
        model = NumberToEnglishTransformer()
        block_data: NumberToEnglishPayload = {"number": number}
        num_in_english: NumberToEnglishResult = model.transform(block_data)
        item = {"status":"ok", "num_in_english":num_in_english}
        json_compatible_item_data = jsonable_encoder(item)
        return JSONResponse(content=json_compatible_item_data)
    except:
        item = {"status": "failed",
                "num_in_english": "processing failed please check the payload formatting and try again"}
        json_compatible_item_data = jsonable_encoder(item)
        return JSONResponse(content=json_compatible_item_data)
