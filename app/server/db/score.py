from bson.objectid import ObjectId
from app.server.db.database import score_collection
# Helpers

def score_helper(score) -> dict:
    return {
        "id": str(score["_id"]),
        "name": score["name"],
        "userid": score["userid"]
    }


# Retrieve all scores present

async def retrieve_diaries():
    scores = []
    async for score in score_collection.find():
        scores.append(score_helper(score))
    return scores


async def add_score(score_data:dict) -> dict:
    score = await score_collection.insert_one(score_data)
    new_score = await score_collection.find_one({"_id": score.inserted_id})
    return score_helper(new_score)


async def get_score(id:str) -> dict:
    score = await score_collection.find_one({"_id": ObjectId(id)})
    if score:
        return score_helper(score)

# Update a score with a matching ID
async def update_score(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    score = await score_collection.find_one({"_id": ObjectId(id)})
    if score:
        updated_score = await score_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_score:
            return True
        return False

# Delete a score from the database
async def delete_score(id: str):
    score = await score_collection.find_one({"_id": ObjectId(id)})
    if score:
        await score_collection.delete_one({"_id": ObjectId(id)})
        return True