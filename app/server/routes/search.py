from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.db.search import (
    get_search,
    retrieve_diaries,
    add_search,
    delete_search,
    update_search
)

from app.server.models.search import (
    ErrorResponseModel,
    ResponseModel,
    SearchSchema,
    UpdateSearchModel
)

router = APIRouter()

@router.post("/", response_description="Search Data Added to the Database")
async def add_search_data(search: SearchSchema = Body(...)):
    print('Inside post', search)
    search = jsonable_encoder(search)
    new_search = await add_search(search)
    return ResponseModel(new_search, "Search Added Successfully")

@router.get("/", response_description="Search Data retrieved")
async def get_diaries():
    diaries = await retrieve_diaries()
    if diaries:
        return ResponseModel(diaries, "Search Data  retrieved successfully")
    return ResponseModel(diaries, "Empty list returned")


@router.get("/{id}", response_description="Search Data retrieved")
async def get_search_data(id):
    search = await get_search(id)
    if search:
        return ResponseModel(search, "Search Data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Search doesn't exist.")

@router.put("/{id}", response_description="Search Data updated")
async def update_search_data(id:str, req:UpdateSearchModel=Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_search = await update_search(id, req)
    if updated_search:
        return ResponseModel(
            "Search with ID: {} name update is successful".format(id),
            "Search name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the search data.",
    )


@router.delete("/{id}", response_description="Search data deleted from the database")
async def delete_search_data(id: str):
    deleted_search = await delete_search(id)
    if deleted_search:
        return ResponseModel(
            "Search with ID: {} removed".format(id), "Search deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Search with id {0} doesn't exist".format(id)
    )