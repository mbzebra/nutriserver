from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.db.goal import (
    get_goal,
    retrieve_goals,
    add_goal,
    delete_goal,
    update_goal
)

from app.server.models.goal import (
    ErrorResponseModel,
    ResponseModel,
    GoalSchema,
    UpdateGoalModel
)

router = APIRouter()

@router.post("/", response_description="Goal Data Added to the Database")
async def add_goal_data(goal: GoalSchema = Body(...)):
    goal = jsonable_encoder(goal)
    new_goal = await add_goal(goal)
    return ResponseModel(new_goal, "Goal Added Successfully")


@router.get("/", response_description="Goal Data retrieved")
async def get_goals():
    goals = await retrieve_goals()
    if goals:
        return ResponseModel(goals, "Goal Data  retrieved successfully")
    return ResponseModel(goals, "Empty list returned")


@router.get("/{id}", response_description="Goal Data retrieved")
async def get_goal_data(id):
    goal = await get_goal(id)
    if goal:
        return ResponseModel(goal, "Goal Data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Goal doesn't exist.")

@router.put("/{id}", response_description="Goal Data updated")
async def update_goal_data(id:str, req:UpdateGoalModel=Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_goal = await update_goal(id, req)
    if updated_goal:
        return ResponseModel(
            "Goal with ID: {} name update is successful".format(id),
            "Goal name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the goal data.",
    )


@router.delete("/{id}", response_description="Goal data deleted from the database")
async def delete_goal_data(id: str):
    deleted_goal = await delete_goal(id)
    if deleted_goal:
        return ResponseModel(
            "Goal with ID: {} removed".format(id), "Goal deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Goal with id {0} doesn't exist".format(id)
    )