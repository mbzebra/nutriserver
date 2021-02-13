import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config



# MONGO_DETAILS = "mongodb://localhost:27017"
MONGO_DETAILS = config("MONGO_DETAILS")


# client = pymongo.MongoClient("mongodb+srv://dbadmin:<password>@cluster0.eausz.mongodb.net/<dbname>?retryWrites=true&w=majority")
# db = client.test


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS, ssl=True, ssl_cert_reqs='CERT_NONE')

database = client.users

user_collection = database.get_collection("users_collection")

# Helpers


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "email": user["email"],
        "userid": user["userid"],
    }


# Retrieve all users present

async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


async def add_user(user_data:dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


async def get_user(id:str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)

