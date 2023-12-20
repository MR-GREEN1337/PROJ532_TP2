import databases
import sqlalchemy
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table

DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), unique=True, index=True),
    Column("password", String),
)


async def create_user(username: str, password: str):
    query = users.insert().values(username=username, password=password)
    return await database.execute(query)


async def get_user(username: str):
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)
