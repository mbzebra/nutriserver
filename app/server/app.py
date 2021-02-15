from fastapi import FastAPI, Request

from fastapi.templating import Jinja2Templates

from app.server.routes.user import router as UserRouter
from app.server.routes.diary import router as DiaryRouter
from app.server.routes.nutrition import router as NutritionRouter
from app.server.routes.goal import router as GoalRouter

tags_metadata = [
    {
        "name": "user",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "diary",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]


app = FastAPI(
    title="The Nutri Project",
    description="All Things Nutrition",
    version="1.0",
    openapi_tags=tags_metadata
)

templates = Jinja2Templates(directory="templates")


app.include_router(UserRouter, tags=["user"], prefix="/user" )
app.include_router(DiaryRouter, tags=["diary"], prefix="/diary" )
app.include_router(NutritionRouter, tags=["nutrition"], prefix="/nutrition" )
app.include_router(GoalRouter, tags=["goal"], prefix="/goal" )


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Nutri Diary"}


@app.get("/.well-known/acme-challenge/i8bAW8juwarmmEDjwmPVqyoRSTt2mVm6XHw1L70OLdA")
async def serve_home(request: Request):
    return templates.TemplateResponse("certfile.html", {"request": request})
