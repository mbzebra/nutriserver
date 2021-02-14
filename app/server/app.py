from fastapi import FastAPI

from app.server.routes.user import router as UserRouter
from app.server.routes.diary import router as DiaryRouter

app = FastAPI()

app.include_router(UserRouter, tags=["User"], prefix="/user" )
app.include_router(DiaryRouter, tags=["Diary"], prefix="/diary" )


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Nutri Diary"}

@app.get("/.well-known/acme-challenge/06UuuU9jzNVZ1uR-CAy148QVbtgVXiUh2M1PWgxL5TI")
async def read_cert_file():
    return "06UuuU9jzNVZ1uR-CAy148QVbtgVXiUh2M1PWgxL5TI.tt1YMtJf3FWnozhjY1DTPVIL1i7YUhUuz4ue6FUbgsk"

