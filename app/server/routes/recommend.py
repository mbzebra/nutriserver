from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.db.recommend import (
    get_recommend,
    retrieve_diaries,
    add_recommend,
    delete_recommend,
    update_recommend
)

from app.server.models.recommend import (
    ErrorResponseModel,
    ResponseModel,
    RecommendSchema,
    UpdateRecommendModel
)

router = APIRouter()

@router.post("/", response_description="Recommend Data Added to the Database")
async def add_recommend_data(recommend: RecommendSchema = Body(...)):
    print('Inside post', recommend)
    recommend = jsonable_encoder(recommend)
    new_recommend = await add_recommend(recommend)
    return ResponseModel(new_recommend, "Recommend Added Successfully")

@router.get("/", response_description="Recommend Data retrieved")
async def get_diaries():
    diaries = await retrieve_diaries()
    if diaries:
        return ResponseModel(diaries, "Recommend Data  retrieved successfully")
    return ResponseModel(diaries, "Empty list returned")


@router.get("/{id}", response_description="Recommend Data retrieved")
async def get_recommend_data(id):
    recommend = await get_recommend(id)
    if recommend:
        return ResponseModel(recommend, "Recommend Data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Recommend doesn't exist.")

@router.put("/{id}", response_description="Recommend Data updated")
async def update_recommend_data(id:str, req:UpdateRecommendModel=Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_recommend = await update_recommend(id, req)
    if updated_recommend:
        return ResponseModel(
            "Recommend with ID: {} name update is successful".format(id),
            "Recommend name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the recommend data.",
    )


@router.delete("/{id}", response_description="Recommend data deleted from the database")
async def delete_recommend_data(id: str):
    deleted_recommend = await delete_recommend(id)
    if deleted_recommend:
        return ResponseModel(
            "Recommend with ID: {} removed".format(id), "Recommend deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Recommend with id {0} doesn't exist".format(id)
    )