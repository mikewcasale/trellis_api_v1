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


@router.post("/num_in_english", response_model=NumberToEnglishResult, name="num_in_english")
def post_num_in_english(
    request: Request,
    authenticated: bool = Depends(security.validate_request),
    block_data: NumberToEnglishPayload = 1000
) -> NumberToEnglishResult:
    try:
        model: NumberToEnglishTransformer = NumberToEnglishTransformer
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
    block_data: NumberToEnglishPayload = 1000
) -> NumberToEnglishResult:
    try:
        model: NumberToEnglishTransformer = NumberToEnglishTransformer
        num_in_english: NumberToEnglishResult = model.transform(block_data)
        item = {"status":"ok", "num_in_english":num_in_english}
        json_compatible_item_data = jsonable_encoder(item)
        return JSONResponse(content=json_compatible_item_data)
    except:
        item = {"status": "failed", "num_in_english": "processing failed please check the payload formatting and try again"}
        json_compatible_item_data = jsonable_encoder(item)
        return JSONResponse(content=json_compatible_item_data)

# @router.get("/", response_model=List[schemas.Item])
# def read_items(
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Retrieve items.
#     """
#     if crud.user.is_superuser(current_user):
#         items = crud.item.get_multi(db, skip=skip, limit=limit)
#     else:
#         items = crud.item.get_multi_by_owner(
#             db=db, owner_id=current_user.id, skip=skip, limit=limit
#         )
#     return items
#
#
# @router.post("/", response_model=schemas.Item)
# def create_item(
#     *,
#     db: Session = Depends(deps.get_db),
#     item_in: schemas.ItemCreate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Create new item.
#     """
#     item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
#     return item
#
#
# @router.put("/{id}", response_model=schemas.Item)
# def update_item(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     item_in: schemas.ItemUpdate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update an item.
#     """
#     item = crud.item.get(db=db, id=id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
#     return item
#
#
# @router.get("/{id}", response_model=schemas.Item)
# def read_item(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Get item by ID.
#     """
#     item = crud.item.get(db=db, id=id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     return item
#
#
# @router.delete("/{id}", response_model=schemas.Item)
# def delete_item(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Delete an item.
#     """
#     item = crud.item.get(db=db, id=id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     item = crud.item.remove(db=db, id=id)
#     return item


