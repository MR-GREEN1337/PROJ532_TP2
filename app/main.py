from fastapi import FastAPI, Depends, HTTPException, Form
from routes import router as quiz_router
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
import database
from database import get_user
import secrets
import uvicorn

app = FastAPI()

secret_key = secrets.token_urlsafe(32)
app.add_middleware(SessionMiddleware, secret_key=secret_key)

app.include_router(quiz_router, prefix="/quiz", tags=["quiz"])
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
async def startup_event():
    await database.database.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await database.disconnect()

@app.get("/sign-up")
async def sign_up(request: Request, user=Depends(get_user)):
    response = await quiz_router.sign_up(request, user)
    return response

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
