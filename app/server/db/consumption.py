from bson.objectid import ObjectId
from app.server.db.database import consumption_collection
# Helpers

def consumption_helper(consumption) -> dict:
    return {
        "id": str(consumption["_id"]),
        "name": consumption["name"],
        "userid": consumption["userid"]
    }


# Retrieve all consumptions present

async def retrieve_diaries():
    consumptions = []
    async for consumption in consumption_collection.find():
        consumptions.append(consumption_helper(consumption))
    return consumptions


async def add_consumption(consumption_data:dict) -> dict:
    consumption = await consumption_collection.insert_one(consumption_data)
    new_consumption = await consumption_collection.find_one({"_id": consumption.inserted_id})
    return consumption_helper(new_consumption)


async def get_consumption(id:str) -> dict:
    consumption = await consumption_collection.find_one({"_id": ObjectId(id)})
    if consumption:
        return consumption_helper(consumption)

# Update a consumption with a matching ID
async def update_consumption(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    consumption = await consumption_collection.find_one({"_id": ObjectId(id)})
    if consumption:
        updated_consumption = await consumption_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_consumption:
            return True
        return False

# Delete a consumption from the database
async def delete_consumption(id: str):
    consumption = await consumption_collection.find_one({"_id": ObjectId(id)})
    if consumption:
        await consumption_collection.delete_one({"_id": ObjectId(id)})
        return True