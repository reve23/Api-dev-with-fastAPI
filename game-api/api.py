from fastapi import FastAPI, Path,Depends,BackgroundTasks
from typing import Optional
from pydantic import BaseModel
import models
from sqlalchemy.orm import Session
from database import SessionLocal,engine
from models import Games
import databases
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

DATABASE_URL = "sqlite:///./games.db"
database = databases.Database(DATABASE_URL)
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
@app.on_event("startup")
async def database_connect():
    await database.connect()


@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()

@app.get('/games')
async def all_games():
    query = 'SELECT * FROM Games'
    result =  await database.fetch_all(query=query)
    return result


@app.get('/games/{game_id}')
def all_games(game_id: int):
    db = SessionLocal()
    item = db.query(Games).filter(Games.id == game_id).first()
    return item


class Game(BaseModel):
    name: str
    description: str
    year: int
    image: str

def fetch_games(id: int):
    db = SessionLocal()
    item = db.query(Games).filter(Games.id == id).first()
    db.add(item)
    db.commit()

@app.post('/add-game')
async def add_game(game: Game,background_tasks: BackgroundTasks,db:Session = Depends(get_db)):

    item = Games()
    item.name = game.name
    item.description = game.description
    item.year = game.year
    item.image = game.image
    db.add(item)
    db.commit()

    background_tasks.add_task(fetch_games,item.id)
    return {
        "code":"success",
        "message":"Game added successfully "
    }

