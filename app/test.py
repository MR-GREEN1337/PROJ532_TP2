import databases
import sqlalchemy
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table, ForeignKey, Boolean
from sqlalchemy.types import DateTime
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import fastapi
from fastapi import Request, FastAPI, Depends, HTTPException, Form
import uvicorn

DATABASE_URL = "sqlite:///./db/sqlV2.sqlite"
database = databases.Database(DATABASE_URL)
metadata = MetaData()

users = Table(
    "user",
    metadata,
    Column("userID", Integer, primary_key=True),
    Column("userFiname", String(50), unique=True, index=True),
    Column("userFaname", String(50), unique=True, index=True),
    Column("userPsw", String),
    Column("userMail", String),
    Column("userType", String),
)

take = Table(
    "take",
    metadata,
    Column("userID", Integer, ForeignKey('user.userID'), primary_key=True),
    Column("quizID", Integer, ForeignKey('quiz.quizID'), primary_key=True),
    Column("date_passage", DateTime),
    Column("score", Integer),
    Column("nbrAttempts", Integer)
)

status = Table(
    "status",
    metadata,
    Column("statusID", Integer, primary_key=True),
    Column("label", String),
    Column("description", String)
)

visibility = Table(
    "visibility",
    metadata,
    Column("visibilityID", Integer, primary_key=True),
    Column("label", String),
    Column("description", String)
)

question = Table(
    "question",
    metadata,
    Column("questID", Integer, primary_key=True),
    Column("quizID", Integer, ForeignKey('answer.questID'), primary_key=True),
    Column("questText", String),
)

answer = Table(
    "answer",
    metadata,
    Column("answerID", Integer, primary_key=True),
    Column("AnswerText", String),
    Column("questID", Integer, ForeignKey('question.questID')),
    Column("isCorrectAnswer", Boolean)
)

quiz = Table(
    "quiz",
    metadata,
    Column("quizID", Integer, primary_key=True),
    Column("categoryName", String),
    Column("description", String),
    Column("duration_min", Integer),
    Column("maxNbrAttemps", Integer),
    Column("dateCreation", DateTime),
    Column("dateLastModif", DateTime),
    Column("statusID", Integer, ForeignKey('status.statusID')),
    Column("visibilityID", Integer, ForeignKey('visibility.visibilityID')),
    Column("adminID", Integer, ForeignKey('user.userID')),
)

async def create_user(first_name: str, last_name: str, password: str, email: str, user_type: str):
    query = users.insert().values(userFiname=first_name, userFaname=last_name, userPsw=password, userMail=email, userType=user_type)
    return await database.execute(query)

async def get_user(username: str):
    query = users.select().where(users.c.userFiname == username)
    return await database.fetch_one(query)

async def get_quiz(quiz_id: int):
    query = quiz.select().where(quiz.c.quizID == quiz_id)
    return await database.fetch_one(query)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    database.connect()

@app.on_event("shutdown")
async def shutdown_event():
    database.disconnect()

@app.get("/")
async def get_content(request: Request):
    response = await get_quiz(1)
    return response

if __name__ == '__main__':
    uvicorn.run("test:app", host="127.0.0.1", port=8000, reload=True)
