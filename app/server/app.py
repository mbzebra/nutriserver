from fastapi import FastAPI, Request

from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from app.server.routes.user import router as UserRouter
from app.server.routes.diary import router as DiaryRouter
from app.server.routes.nutrition import router as NutritionRouter
from app.server.routes.goal import router as GoalRouter
from app.server.routes.plan import router as PlanRouter
from app.server.routes.score import router as ScoreRouter
from app.server.routes.consumption import router as ConsumptionRouter
from app.server.routes.recommend import router as RecommendRouter
from app.server.routes.search import router as SearchRouter


from fastapi.testclient import TestClient


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

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="templates")


app.include_router(UserRouter, tags=["user"], prefix="/user" )
app.include_router(DiaryRouter, tags=["diary"], prefix="/diary" )
app.include_router(PlanRouter, tags=["plan"], prefix="/plan" )
app.include_router(NutritionRouter, tags=["nutrition"], prefix="/nutrition" )
app.include_router(GoalRouter, tags=["goal"], prefix="/goal" )
app.include_router(SearchRouter, tags=["search"], prefix="/search" )
app.include_router(ConsumptionRouter, tags=["consumption"], prefix="/consumption" )
app.include_router(ScoreRouter, tags=["score"], prefix="/score" )
app.include_router(RecommendRouter, tags=["recommend"], prefix="/recommend" )



@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Nutri Diary"}

@app.get('/files', tags=["Files"])
async def read_files():
    from pathlib import Path

    entries = Path('../tests')
    myentries = []
    for entry in entries.iterdir():
        myentry = {
            "fileId" : entry.name,
            "fileType" : 'File' if entry.is_file() else 'Dir',
            "fileName" : entry.name
        }
        myentries.append(myentry)

    return {"hits" : myentries}

    # return {"hits": [{"url": "http://www.test.com", "objectID": "23325319", "title": "Guerrilla Public Service Redux (2017)"}, {"url": "http://www.test.com", "objectID": "23325319", "title": "Guerrilla Public Service Redux (2017)"}]}


client = TestClient(app)



def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


@app.get("/.well-known/acme-challenge/i8bAW8juwarmmEDjwmPVqyoRSTt2mVm6XHw1L70OLdA")
async def serve_home(request: Request):
    return templates.TemplateResponse("certfile.html", {"request": request})


