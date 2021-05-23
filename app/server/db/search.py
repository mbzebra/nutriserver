from bson.objectid import ObjectId
from app.server.db.database import search_collection
# Helpers

def search_helper(search) -> dict:
    return {
        "id": str(search["_id"]),
        "name": search["name"],
        "userid": search["userid"]
    }


# Retrieve all searchs present

async def retrieve_diaries():
    searchs = []
    async for search in search_collection.find():
        searchs.append(search_helper(search))
    return searchs


async def add_search(search_data:dict) -> dict:
    search = await search_collection.insert_one(search_data)
    new_search = await search_collection.find_one({"_id": search.inserted_id})
    return search_helper(new_search)


async def get_search(id:str) -> dict:
    search = await search_collection.find_one({"_id": ObjectId(id)})
    if search:
        return search_helper(search)

# Update a search with a matching ID
async def update_search(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    search = await search_collection.find_one({"_id": ObjectId(id)})
    if search:
        updated_search = await search_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_search:
            return True
        return False

# Delete a search from the database
async def delete_search(id: str):
    search = await search_collection.find_one({"_id": ObjectId(id)})
    if search:
        await search_collection.delete_one({"_id": ObjectId(id)})
        return True