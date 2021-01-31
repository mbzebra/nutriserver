from fastapi import FastAPI
from enum import Enum
import uvicorn


class FoodType(str, Enum):
    food = "food"
    medicine = "medicine"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/nutrition/{type}")
async def root(type):
    if type == FoodType.food:
        return {"message": "It's Food Catgory"}

    elif type == FoodType.medicine:
        return {"message": "It's Medicine Catgory"}

    else:
        return {"message": "No Category Selected"}

@app.post('/users/{user_id}')
async def create_nutri_diary(user_id:int):
    return {"message": "Nutrition Diary Created for {}".format(user_id)}

@app.put('/')
async def update_nutri_diary():
    return {"message": "Your Diary Updated"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7070)