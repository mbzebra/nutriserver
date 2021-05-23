from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.db.diary import (
    get_diary,
    retrieve_diaries,
    add_diary,
    delete_diary,
    update_diary
)

from app.server.models.diary import (
    ErrorResponseModel,
    ResponseModel,
    DiarySchema,
    UpdateDiaryModel
)

router = APIRouter()

@router.post("/", response_description="Diary Data Added to the Database")
async def add_diary_data(diary: DiarySchema = Body(...)):
    print('Inside post', diary)
    diary = jsonable_encoder(diary)
    new_diary = await add_diary(diary)
    return ResponseModel(new_diary, "Diary Added Successfully")


# @router.post("/", response_description="Diary Data Added to the Database")
# async def add_diary_data(diary: DiarySchema = Body(...)):
#     print('Inside post')
#     diary = jsonable_encoder(diary)
#     new_diary = await add_diary(diary)
#     return ResponseModel(new_diary, "Diary Added Successfully")
#

@router.get("/", response_description="Diary Data retrieved")
async def get_diaries():
    diaries = await retrieve_diaries()
    if diaries:
        return ResponseModel(diaries, "Diary Data  retrieved successfully")
    return ResponseModel(diaries, "Empty list returned")


@router.get("/{id}", response_description="Diary Data retrieved")
async def get_diary_data(id):
    diary = await get_diary(id)
    if diary:
        return ResponseModel(diary, "Diary Data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Diary doesn't exist.")

@router.put("/{id}", response_description="Diary Data updated")
async def update_diary_data(id:str, req:UpdateDiaryModel=Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_diary = await update_diary(id, req)
    if updated_diary:
        return ResponseModel(
            "Diary with ID: {} name update is successful".format(id),
            "Diary name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the diary data.",
    )


@router.delete("/{id}", response_description="Diary data deleted from the database")
async def delete_diary_data(id: str):
    deleted_diary = await delete_diary(id)
    if deleted_diary:
        return ResponseModel(
            "Diary with ID: {} removed".format(id), "Diary deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Diary with id {0} doesn't exist".format(id)
    )