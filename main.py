from os import environ

import uvicorn
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
import databases
from sqlalchemy import select, desc
from app.models.users import users_table
from app.models.posts import posts_table
from app.routers import users
from app.routers import posts

load_dotenv(find_dotenv())

DB_USER = environ.get("DB_USER", "user")
DB_PASSWORD = environ.get("DB_PASS", "password")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_NAME = environ.get("DB_NAME", "async_blog")
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)

database = databases.Database(SQLALCHEMY_DATABASE_URL)

app = FastAPI()


@app.on_event("startup")
async def startup():
    """когда приложение запускается устанавливаем соединение с БД"""
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """когда приложение останавливается разрываем соединение с БД"""
    await database.disconnect()


app.include_router(users.router)
app.include_router(posts.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


