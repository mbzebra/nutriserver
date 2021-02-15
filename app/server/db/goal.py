from bson.objectid import ObjectId
from app.server.db.database import goal_collection
# Helpers

def goal_helper(goal) -> dict:
    return {
        "id": str(goal["_id"]),
        "name": goal["name"],
        "userid": goal["userid"]
    }


# Retrieve all goals present

async def retrieve_goals():
    goals = []
    async for goal in goal_collection.find():
        goals.append(goal_helper(goal))
    return goals


async def add_goal(goal_data:dict) -> dict:
    goal = await goal_collection.insert_one(goal_data)
    new_goal = await goal_collection.find_one({"_id": goal.inserted_id})
    return goal_helper(new_goal)


async def get_goal(id:str) -> dict:
    goal = await goal_collection.find_one({"_id": ObjectId(id)})
    if goal:
        return goal_helper(goal)

# Update a goal with a matching ID
async def update_goal(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    goal = await goal_collection.find_one({"_id": ObjectId(id)})
    if goal:
        updated_goal = await goal_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_goal:
            return True
        return False

# Delete a goal from the database
async def delete_goal(id: str):
    goal = await goal_collection.find_one({"_id": ObjectId(id)})
    if goal:
        await goal_collection.delete_one({"_id": ObjectId(id)})
        return True