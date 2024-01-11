import databases
import sqlalchemy
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
from sqlalchemy.types import DateTime

DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)
metadata = MetaData()


async def create_user(username: str, password: str):
    query = users.insert().values(username=username, password=password)
    return await database.execute(query)

async def get_user(username: str):
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)

async def create_quiz(title: str, description: str, duration_min: int, max_attempts: int,
                      status_id: int, category_id: int, visibility_id: int, admin_id: int):
    query = Quizz.insert().values(
        title=title,
        description=description,
        duration_min=duration_min,
        maxNbrAttempts=max_attempts,
        date_creation=datetime.now(),
        dateLastModif=int(datetime.now().timestamp()),
        status_id=status_id,
        category_id=category_id,
        visibility_id=visibility_id,
        admin_id=admin_id
    )
    return await database.execute(query)

async def get_quiz(quiz_id: int):
    query = Quizz.select().where(Quizz.c.quiz_id == quiz_id)
    return await database.fetch_one(query)

async def get_quizzes_by_category(category_id: int):
    query = Quizz.select().where(Quizz.c.category_id == category_id)
    return await database.fetch_all(query)

async def get_quizzes_by_status(status_id: int):
    query = Quizz.select().where(Quizz.c.status_id == status_id)
    return await database.fetch_all(query)

async def get_quizzes_by_visibility(visibility_id: int):
    query = Quizz.select().where(Quizz.c.visibility_id == visibility_id)
    return await database.fetch_all(query)

async def get_user_quizzes(admin_id: int):
    query = Quizz.select().where(Quizz.c.admin_id == admin_id)
    return await database.fetch_all(query)

async def create_question(question_text: str):
    query = question.insert().values(question_text=question_text)
    return await database.execute(query)

async def get_question(question_id: int):
    query = question.select().where(question.c.question_id == question_id)
    return await database.fetch_one(query)

async def create_answer(answer_text: str, quest_id: int):
    query = answer.insert().values(answer_text=answer_text, quest_id=quest_id)
    return await database.execute(query)

async def get_answers_for_question(quest_id: int):
    query = answer.select().where(answer.c.quest_id == quest_id)
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

async def get_user_quiz_attempts(user_id: int):
    query = take.select().where(take.c.user_id == user_id)
    return await database.fetch_all(query)