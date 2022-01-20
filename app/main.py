from os import environ

from dotenv import load_dotenv
from fastapi import FastAPI
import databases
from sqlalchemy import select, desc
from app.models.users import users_table
from app.models.posts import posts_table
from app.routers import users

load_dotenv()

DB_USER = environ.get("DB_USER", "user")
DB_PASSWORD = environ.get("DB_PASS", "password")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_NAME = environ.get("DB_NAME", "async_blog")
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)

database = databases.Database(SQLALCHEMY_DATABASE_URL)

app = FastAPI()

app.include_router(users.router)


@app.on_event("startup")
async def startup():
    # когда приложение запускается устанавливаем соединение с БД
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    # когда приложение останавливается разрываем соединение с БД
    await database.disconnect()


@app.get("/")
async def read_root():
    query = (
        select(
            [
                posts_table.c.id,
                posts_table.c.create_at,
                posts_table.c.title,
                posts_table.c.content,
                posts_table.c.user_id,
                users_table.c.name.label('user_name'),
            ]

        )
        .select_from(posts_table.join(users_table))
        .order_by(desc(posts_table.c.create_at))
    )
    return await database.fetch_all(query)
