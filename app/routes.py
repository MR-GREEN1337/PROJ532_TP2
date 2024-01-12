from fastapi import UploadFile, File, Form, APIRouter, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from database import database, get_user, create_user, create_quiz, get_quiz, get_quizzes_by_category, get_quizzes_by_status, get_quizzes_by_visibility, get_user_quizzes, create_question, get_question, create_answer, get_answers_for_question, record_quiz_attempt, get_user_quiz_attempts

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

'''@router.get("/", response_class=HTMLResponse)
async def home(request: Request ,msg:str = None):
    return templates.TemplateResponse("sign_up.html", {"request": request})

@router.get("/quiz", response_class=HTMLResponse)
async def get_quiz(request: Request, user = Depends(get_user)):
    return templates.TemplateResponse("quiz.html", {"request": request, "title": "Quiz", "questions": quiz_questions})

@router.post("/submit_answer")
async def submit_answer(question_index: int, answer: str, user = Depends(get_user)):
    try:
        question = quiz_questions[question_index - 1]
    except IndexError:
        raise HTTPException(status_code=404, detail="Question not found")

    correct_answer = question["correct_answer"]
    is_correct = answer == correct_answer

    return {"is_correct": is_correct}
'''