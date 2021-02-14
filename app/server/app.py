from fastapi import FastAPI

from app.server.routes.user import router as UserRouter
from app.server.routes.diary import router as DiaryRouter

app = FastAPI()

app.include_router(UserRouter, tags=["User"], prefix="/user" )
app.include_router(DiaryRouter, tags=["Diary"], prefix="/diary" )


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Nutri Diary"}

@app.get("/.well-known/acme-challenge/qEKih7qVga3bTnfBdsekEUJFWykfvdK_Os5BeDsb0b4")
async def read_cert_file():
    return "qEKih7qVga3bTnfBdsekEUJFWykfvdK_Os5BeDsb0b4.tt1YMtJf3FWnozhjY1DTPVIL1i7YUhUuz4ue6FUbgsk"

