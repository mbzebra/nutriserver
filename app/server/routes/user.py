from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.db.database import (
    get_user,
    retrieve_users,
    add_user
)

from app.server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel
)

router = APIRouter()

@router.post("/", response_description="User Data Added to the Database")
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User Added Successfully")


@router.get("/", response_description="User Data retrieved")
async def get_users():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "User Data  retrieved successfully")
    return ResponseModel(users, "Empty list returned")


@router.get("/{id}", response_description="User Data retrieved")
async def get_user_data(id):
    user = await get_user(id)
    if user:
        return ResponseModel(user, "User Data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")
