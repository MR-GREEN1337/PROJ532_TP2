import databases
import sqlalchemy
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table, ForeignKey, Boolean
from sqlalchemy.types import DateTime
from datetime import datetime

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

async def create_quiz(title: str, description: str, duration_min: int, max_attempts: int,
                      status_id: int, category_id: int, visibility_id: int, admin_id: int):
    query = quiz.insert().values(
        categoryName=title,
        description=description,
        duration_min=duration_min,
        maxNbrAttempts=max_attempts,
        dateCreation=datetime.now(),
        dateLastModif=int(datetime.now().timestamp()),
        statusID=status_id,
        visibilityID=visibility_id,
        adminID=admin_id
    )
    return await database.execute(query)

async def get_quiz(quiz_id: int):
    query = quiz.select().where(quiz.c.quizID == quiz_id)
    return await database.fetch_one(query)

async def get_quizzes_by_category(category_id: int):
    query = quiz.select().where(quiz.c.categoryName == category_id)
    return await database.fetch_all(query)

async def get_quizzes_by_status(status_id: int):
    query = quiz.select().where(quiz.c.statusID == status_id)
    return await database.fetch_all(query)

async def get_quizzes_by_visibility(visibility_id: int):
    query = quiz.select().where(quiz.c.visibilityID == visibility_id)
    return await database.fetch_all(query)

async def get_user_quizzes(admin_id: int):
    query = quiz.select().where(quiz.c.adminID == admin_id)
    return await database.fetch_all(query)

async def create_question(question_text: str):
    query = question.insert().values(questText=question_text)
    return await database.execute(query)

async def get_question(question_id: int):
    query = question.select().where(question.c.questID == question_id)
    return await database.fetch_one(query)

async def create_answer(answer_text: str, quest_id: int, is_correct: bool):
    query = answer.insert().values(AnswerText=answer_text, questID=quest_id, isCorrectAnswer=is_correct)
    return await database.execute(query)

async def get_answers_for_question(quest_id: int):
    query = answer.select().where(answer.c.questID == quest_id)
    return await database.fetch_all(query)

async def record_quiz_attempt(user_id: int, quiz_id: int, date_passage: str, score: int, nbr_attempts: int):
    query = take.insert().values(
        user_id=user_id,
        quiz_id=quiz_id,
        date_passage=date_passage,
        score=score,
        nbr_attempts=nbr_attempts
    )
    return await database.execute(query)

async def record_quiz_attempt(user_id: int, quiz_id: int, date_passage: str, score: int, nbr_attempts: int):
    query = take.insert().values(
        userID=user_id,
        quizID=quiz_id,
        date_passage=date_passage,
        score=score,
        nbrAttempts=nbr_attempts
    )
    return await database.execute(query)

async def get_user_quiz_attempts(user_id: int):
    query = take.select().where(take.c.userID == user_id)
    return await database.fetch_all(query)