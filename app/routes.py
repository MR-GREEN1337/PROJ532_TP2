from fastapi import UploadFile, File, Form, APIRouter, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from database import get_user, create_user, create_quiz, get_quiz, get_quizzes_by_category, get_quizzes_by_status, get_quizzes_by_visibility, get_user_quizzes, create_question, get_question, create_answer, get_answers_for_question, record_quiz_attempt, get_user_quiz_attempts

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Dummy quiz questions for illustration purposes
quiz_questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Paris", "Madrid", "Rome"],
        "correct_answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Mars", "Jupiter", "Venus", "Saturn"],
        "correct_answer": "Mars"
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
        "correct_answer": "Blue Whale"
    }
]

@router.get("/signup", response_class=HTMLResponse)
async def sign_up(request: Request, user = Depends(get_user)):
    return templates.TemplateResponse("/app/templates/sign-up.html", {"request": request, "title": "Quiz", "questions": quiz_questions})

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
