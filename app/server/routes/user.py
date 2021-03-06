from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.db.user import (
    get_user,
    retrieve_users,
    add_user,
    delete_user,
    update_user
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

@router.put("/{id}", response_description="User Data updated")
async def update_user_data(id:str, req:UpdateUserModel=Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(id, req)
    if updated_user:
        return ResponseModel(
            "User with ID: {} name update is successful".format(id),
            "User name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )


@router.delete("/{id}", response_description="User data deleted from the database")
async def delete_user_data(id: str):
    deleted_user = await delete_user(id)
    if deleted_user:
        return ResponseModel(
            "User with ID: {} removed".format(id), "User deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "User with id {0} doesn't exist".format(id)
    )