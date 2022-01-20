from os import environ

import uvicorn
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from app.models.database import database
from app.routers import users
from app.routers import posts

load_dotenv(find_dotenv())


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


