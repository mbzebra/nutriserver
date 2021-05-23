from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.db.score import (
    get_score,
    retrieve_diaries,
    add_score,
    delete_score,
    update_score
)

from app.server.models.score import (
    ErrorResponseModel,
    ResponseModel,
    ScoreSchema,
    UpdateScoreModel
)

router = APIRouter()

@router.post("/", response_description="Score Data Added to the Database")
async def add_score_data(score: ScoreSchema = Body(...)):
    print('Inside post', score)
    score = jsonable_encoder(score)
    new_score = await add_score(score)
    return ResponseModel(new_score, "Score Added Successfully")

@router.get("/", response_description="Score Data retrieved")
async def get_diaries():
    diaries = await retrieve_diaries()
    if diaries:
        return ResponseModel(diaries, "Score Data  retrieved successfully")
    return ResponseModel(diaries, "Empty list returned")


@router.get("/{id}", response_description="Score Data retrieved")
async def get_score_data(id):
    score = await get_score(id)
    if score:
        return ResponseModel(score, "Score Data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Score doesn't exist.")

@router.put("/{id}", response_description="Score Data updated")
async def update_score_data(id:str, req:UpdateScoreModel=Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_score = await update_score(id, req)
    if updated_score:
        return ResponseModel(
            "Score with ID: {} name update is successful".format(id),
            "Score name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the score data.",
    )


@router.delete("/{id}", response_description="Score data deleted from the database")
async def delete_score_data(id: str):
    deleted_score = await delete_score(id)
    if deleted_score:
        return ResponseModel(
            "Score with ID: {} removed".format(id), "Score deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Score with id {0} doesn't exist".format(id)
    )