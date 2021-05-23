from bson.objectid import ObjectId
from app.server.db.database import diary_collection
# Helpers

def diary_helper(diary) -> dict:
    return {
        "id": str(diary["_id"]),
        "name": diary["name"],
        "userid": diary["userid"]
    }


# Retrieve all diarys present

async def retrieve_diaries():
    diarys = []
    async for diary in diary_collection.find():
        diarys.append(diary_helper(diary))
    return diarys


async def add_diary(diary_data:dict) -> dict:
    diary = await diary_collection.insert_one(diary_data)
    new_diary = await diary_collection.find_one({"_id": diary.inserted_id})
    return diary_helper(new_diary)


async def get_diary(id:str) -> dict:
    diary = await diary_collection.find_one({"_id": ObjectId(id)})
    if diary:
        return diary_helper(diary)

# Update a diary with a matching ID
async def update_diary(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    diary = await diary_collection.find_one({"_id": ObjectId(id)})
    if diary:
        updated_diary = await diary_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_diary:
            return True
        return False

# Delete a diary from the database
async def delete_diary(id: str):
    diary = await diary_collection.find_one({"_id": ObjectId(id)})
    if diary:
        await diary_collection.delete_one({"_id": ObjectId(id)})
        return True