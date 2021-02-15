from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates

from app.server.routes.user import router as UserRouter
from app.server.routes.diary import router as DiaryRouter
from app.server.routes.nutrition import router as NutritionRouter

app = FastAPI()

templates = Jinja2Templates(directory="templates")


app.include_router(UserRouter, tags=["User"], prefix="/user" )
app.include_router(DiaryRouter, tags=["Diary"], prefix="/diary" )
app.include_router(NutritionRouter, tags=["Nutrition"], prefix="/nutrition" )


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Nutri Diary"}


@app.get("/.well-known/acme-challenge/i8bAW8juwarmmEDjwmPVqyoRSTt2mVm6XHw1L70OLdA")
async def serve_home(request: Request):
    return templates.TemplateResponse("certfile.html", {"request": request})
