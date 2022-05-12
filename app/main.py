from fastapi import FastAPI, Depends, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from routers import desk_router, card_router, column_router
from fastapi import APIRouter, Request, Query
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import PlainTextResponse, JSONResponse, RedirectResponse
from config import HOST


from db import database_channel
from classes import Desk
from models import DeskUpdate, DeskDelete, DeskExtractAll

app = FastAPI(
    title='Kanban',
    description='Моя канбан-доска',
    docs_url='/docs',
    redoc_url='/doc'
)

# Добавление поддержки политик CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=["*"]
)

app.include_router(
    desk_router,
    prefix='/desks',
    tags=['desk'],
    dependencies=[]
)
app.include_router(
    card_router,
    prefix='/cards',
    tags=['card'],
    dependencies=[]
)
app.include_router(
    column_router,
    prefix='/columns',
    tags=['column'],
    dependencies=[]
)
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory="templates")


# Перехват ошибок
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return templates.TemplateResponse("error.html",
                                      {"request": request, "detail": str(exc.detail), "status_code": exc.status_code})


@app.get("/test")
def test():
    return "ready!"


@app.get("/dp")
def test22():
    up = Desk.extract_all()
    return up


@app.post("/dp")
def test2(dsk: DeskUpdate):
    # return 'dada'
    up = Desk.update(dsk)
    return up

@app.put("/dp")
def test3(dsk: DeskUpdate):
    # return 'dada'
    up = Desk.update(dsk)
    return up

@app.delete("/dp")
def test4(dsk: DeskDelete):
    # return 'dada'
    up = Desk.delete(dsk)
    return up



@app.get("/")
def index():
    return RedirectResponse(f"{HOST}/desks/all")


@app.on_event('startup')
async def startup():
    await database_channel.connect()


@app.on_event('shutdown')
async def shutdown():
    await database_channel.disconnect()
