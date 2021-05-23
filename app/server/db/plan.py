from bson.objectid import ObjectId
from app.server.db.database import plan_collection
# Helpers

def plan_helper(plan) -> dict:
    return {
        "id": str(plan["_id"]),
        "name": plan["name"],
        "userid": plan["userid"]
    }


# Retrieve all plans present

async def retrieve_diaries():
    plans = []
    async for plan in plan_collection.find():
        plans.append(plan_helper(plan))
    return plans


async def add_plan(plan_data:dict) -> dict:
    plan = await plan_collection.insert_one(plan_data)
    new_plan = await plan_collection.find_one({"_id": plan.inserted_id})
    return plan_helper(new_plan)


async def get_plan(id:str) -> dict:
    plan = await plan_collection.find_one({"_id": ObjectId(id)})
    if plan:
        return plan_helper(plan)

# Update a plan with a matching ID
async def update_plan(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    plan = await plan_collection.find_one({"_id": ObjectId(id)})
    if plan:
        updated_plan = await plan_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_plan:
            return True
        return False

# Delete a plan from the database
async def delete_plan(id: str):
    plan = await plan_collection.find_one({"_id": ObjectId(id)})
    if plan:
        await plan_collection.delete_one({"_id": ObjectId(id)})
        return True