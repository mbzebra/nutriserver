from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.db.consumption import (
    get_consumption,
    retrieve_diaries,
    add_consumption,
    delete_consumption,
    update_consumption
)

from app.server.models.consumption import (
    ErrorResponseModel,
    ResponseModel,
    ConsumptionSchema,
    UpdateConsumptionModel
)

router = APIRouter()

@router.post("/", response_description="Consumption Data Added to the Database")
async def add_consumption_data(consumption: ConsumptionSchema = Body(...)):
    print('Inside post', consumption)
    consumption = jsonable_encoder(consumption)
    new_consumption = await add_consumption(consumption)
    return ResponseModel(new_consumption, "Consumption Added Successfully")

@router.get("/", response_description="Consumption Data retrieved")
async def get_diaries():
    diaries = await retrieve_diaries()
    if diaries:
        return ResponseModel(diaries, "Consumption Data  retrieved successfully")
    return ResponseModel(diaries, "Empty list returned")


@router.get("/{id}", response_description="Consumption Data retrieved")
async def get_consumption_data(id):
    consumption = await get_consumption(id)
    if consumption:
        return ResponseModel(consumption, "Consumption Data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Consumption doesn't exist.")

@router.put("/{id}", response_description="Consumption Data updated")
async def update_consumption_data(id:str, req:UpdateConsumptionModel=Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_consumption = await update_consumption(id, req)
    if updated_consumption:
        return ResponseModel(
            "Consumption with ID: {} name update is successful".format(id),
            "Consumption name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the consumption data.",
    )


@router.delete("/{id}", response_description="Consumption data deleted from the database")
async def delete_consumption_data(id: str):
    deleted_consumption = await delete_consumption(id)
    if deleted_consumption:
        return ResponseModel(
            "Consumption with ID: {} removed".format(id), "Consumption deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Consumption with id {0} doesn't exist".format(id)
    )