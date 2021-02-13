from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: str = Field(...)
    userid: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "mariswaran balasubramanian",
                "email": "mbzebradev@gmail.com",
                "userid": "d3f0ae52-bfbd-4a89-b34b-95c6030d3c47"
            }
        }

class UpdateUserModel(BaseModel):
    fullname: Optional[str]
    email: Optional[str]
    userid: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "fullname": "mariswaran balasubramanian",
                "email": "mbzebradev@gmail.com",
                "userid": "d3f0ae52-bfbd-4a89-b34b-95c6030d3c47"
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}