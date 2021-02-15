from bson.objectid import ObjectId
from app.server.db.database import nutrition_collection
# Helpers

def nutrition_helper(nutrition) -> dict:
    return {
        "id": str(nutrition["_id"]),
        "name": nutrition["name"],
        "nutritionid": nutrition["userid"],
    }


# Retrieve all nutritions present

async def retrieve_nutritions():
    nutritions = []
    async for nutrition in nutrition_collection.find():
        nutritions.append(nutrition_helper(nutrition))
    return nutritions


async def add_nutrition(nutrition_data:dict) -> dict:
    nutrition = await nutrition_collection.insert_one(nutrition_data)
    new_nutrition = await nutrition_collection.find_one({"_id": nutrition.inserted_id})
    return nutrition_helper(new_nutrition)


async def get_nutrition(id:str) -> dict:
    nutrition = await nutrition_collection.find_one({"_id": ObjectId(id)})
    if nutrition:
        return nutrition_helper(nutrition)

# Update a nutrition with a matching ID
async def update_nutrition(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    nutrition = await nutrition_collection.find_one({"_id": ObjectId(id)})
    if nutrition:
        updated_nutrition = await nutrition_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_nutrition:
            return True
        return False

# Delete a nutrition from the database
async def delete_nutrition(id: str):
    nutrition = await nutrition_collection.find_one({"_id": ObjectId(id)})
    if nutrition:
        await nutrition_collection.delete_one({"_id": ObjectId(id)})
        return True