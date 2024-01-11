from fastapi import UploadFile, File, Form, APIRouter, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from app.database import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

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

@router.get("/quiz", response_class=HTMLResponse)
async def get_quiz(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("quiz.html", {"request": request, "title": "Quiz", "questions": quiz_questions})

@router.post("/submit_answer")
async def submit_answer(question_index: int, answer: str, user: User = Depends(get_current_user)):
    try:
        question = quiz_questions[question_index - 1]
    except IndexError:
        raise HTTPException(status_code=404, detail="Question not found")

    correct_answer = question["correct_answer"]
    is_correct = answer == correct_answer

    # TODO: Store user's answers or score in the database if needed

    return {"is_correct": is_correct}
