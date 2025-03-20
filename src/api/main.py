from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api import welcome_router, auth_router, root_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(welcome_router)
app.include_router(auth_router)
app.include_router(root_router)
