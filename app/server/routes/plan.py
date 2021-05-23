from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.db.plan import (
    get_plan,
    retrieve_diaries,
    add_plan,
    delete_plan,
    update_plan
)

from app.server.models.plan import (
    ErrorResponseModel,
    ResponseModel,
    PlanSchema,
    UpdatePlanModel
)

router = APIRouter()

@router.post("/", response_description="Plan Data Added to the Database")
async def add_plan_data(plan: PlanSchema = Body(...)):
    print('Inside post', plan)
    plan = jsonable_encoder(plan)
    new_plan = await add_plan(plan)
    return ResponseModel(new_plan, "Plan Added Successfully")

@router.get("/", response_description="Plan Data retrieved")
async def get_diaries():
    diaries = await retrieve_diaries()
    if diaries:
        return ResponseModel(diaries, "Plan Data  retrieved successfully")
    return ResponseModel(diaries, "Empty list returned")


@router.get("/{id}", response_description="Plan Data retrieved")
async def get_plan_data(id):
    plan = await get_plan(id)
    if plan:
        return ResponseModel(plan, "Plan Data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Plan doesn't exist.")

@router.put("/{id}", response_description="Plan Data updated")
async def update_plan_data(id:str, req:UpdatePlanModel=Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_plan = await update_plan(id, req)
    if updated_plan:
        return ResponseModel(
            "Plan with ID: {} name update is successful".format(id),
            "Plan name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the plan data.",
    )


@router.delete("/{id}", response_description="Plan data deleted from the database")
async def delete_plan_data(id: str):
    deleted_plan = await delete_plan(id)
    if deleted_plan:
        return ResponseModel(
            "Plan with ID: {} removed".format(id), "Plan deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Plan with id {0} doesn't exist".format(id)
    )