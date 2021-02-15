import motor.motor_asyncio
from decouple import config

MONGO_DETAILS = config("MONGO_DETAILS")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS, ssl=True, ssl_cert_reqs='CERT_NONE')
# client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.nutri

user_collection = database.get_collection("users_collection")
diary_collection = database.get_collection("diary_collection")
nutrition_collection = database.get_collection("nutrition_collection")
