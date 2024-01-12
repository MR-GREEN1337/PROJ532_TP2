from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from routes import router as quiz_router
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
import database
from database import get_user
import secrets
import uvicorn

app = FastAPI()

'''secret_key = secrets.token_urlsafe(32)
app.add_middleware(SessionMiddleware, secret_key=secret_key)
'''
app.include_router(quiz_router, prefix="/quiz", tags=["quiz"])
templates = Jinja2Templates(directory="templates/")


@app.on_event("startup")
async def startup_event():
    database.database.connect()

@app.on_event("shutdown")
async def shutdown_event():
    database.database.disconnect()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, msg: str = "hamiiid"):
    return templates.TemplateResponse("sign_up.html", {"request": request, "msg": msg})

@app.get("/sign-in")
async def sign_in(request: Request):
    return templates.TemplateResponse("sign_in.html", {"request": request, "msg": msg})


@app.get("/quiz", response_class=HTMLResponse)
async def get_quiz(request: Request, user=Depends(get_user)):
    return templates.TemplateResponse("quiz.html", {"request": request, "title": "Quiz", "questions": quiz_questions})

@app.post("/submit_answer")
async def submit_answer(question_index: int, answer: str, user=Depends(get_user)):
    try:
        question = quiz_questions[question_index - 1]
    except IndexError:
        raise HTTPException(status_code=404, detail="Question not found")

    correct_answer = question["correct_answer"]
    is_correct = answer == correct_answer

    return {"is_correct": is_correct}

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
