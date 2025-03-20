from fastapi import FastAPI

from src.api import welcome_router, auth_router, root_router


app = FastAPI()


app.include_router(welcome_router)
app.include_router(auth_router)
app.include_router(root_router)


