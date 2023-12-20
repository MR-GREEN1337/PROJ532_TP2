from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from app.database import create_user, get_user, database

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
