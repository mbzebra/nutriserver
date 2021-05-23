from bson.objectid import ObjectId
from app.server.db.database import recommend_collection
# Helpers

def recommend_helper(recommend) -> dict:
    return {
        "id": str(recommend["_id"]),
        "name": recommend["name"],
        "userid": recommend["userid"]
    }


# Retrieve all recommends present

async def retrieve_diaries():
    recommends = []
    async for recommend in recommend_collection.find():
        recommends.append(recommend_helper(recommend))
    return recommends


async def add_recommend(recommend_data:dict) -> dict:
    recommend = await recommend_collection.insert_one(recommend_data)
    new_recommend = await recommend_collection.find_one({"_id": recommend.inserted_id})
    return recommend_helper(new_recommend)


async def get_recommend(id:str) -> dict:
    recommend = await recommend_collection.find_one({"_id": ObjectId(id)})
    if recommend:
        return recommend_helper(recommend)

# Update a recommend with a matching ID
async def update_recommend(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    recommend = await recommend_collection.find_one({"_id": ObjectId(id)})
    if recommend:
        updated_recommend = await recommend_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_recommend:
            return True
        return False

# Delete a recommend from the database
async def delete_recommend(id: str):
    recommend = await recommend_collection.find_one({"_id": ObjectId(id)})
    if recommend:
        await recommend_collection.delete_one({"_id": ObjectId(id)})
        return True