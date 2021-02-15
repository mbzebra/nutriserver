from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.db.nutrition import (
    get_nutrition,
    retrieve_nutritions,
    add_nutrition,
    delete_nutrition,
    update_nutrition
)

from app.server.models.nutrition import (
    ErrorResponseModel,
    ResponseModel,
    NutritionSchema,
    UpdateNutritionModel
)

router = APIRouter()

@router.post("/", response_description="Nutrition Data Added to the Database")
async def add_nutrition_data(nutrition: NutritionSchema = Body(...)):
    nutrition = jsonable_encoder(nutrition)
    new_nutrition = await add_nutrition(nutrition)
    return ResponseModel(new_nutrition, "Nutrition Added Successfully")


@router.get("/", response_description="Nutrition Data retrieved")
async def get_nutritions():
    nutritions = await retrieve_nutritions()
    if nutritions:
        return ResponseModel(nutritions, "Nutrition Data  retrieved successfully")
    return ResponseModel(nutritions, "Empty list returned")


@router.get("/{id}", response_description="Nutrition Data retrieved")
async def get_nutrition_data(id):
    nutrition = await get_nutrition(id)
    if nutrition:
        return ResponseModel(nutrition, "Nutrition Data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Nutrition doesn't exist.")

@router.put("/{id}", response_description="Nutrition Data updated")
async def update_nutrition_data(id:str, req:UpdateNutritionModel=Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_nutrition = await update_nutrition(id, req)
    if updated_nutrition:
        return ResponseModel(
            "Nutrition with ID: {} name update is successful".format(id),
            "Nutrition name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the nutrition data.",
    )


@router.delete("/{id}", response_description="Nutrition data deleted from the database")
async def delete_nutrition_data(id: str):
    deleted_nutrition = await delete_nutrition(id)
    if deleted_nutrition:
        return ResponseModel(
            "Nutrition with ID: {} removed".format(id), "Nutrition deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Nutrition with id {0} doesn't exist".format(id)
    )