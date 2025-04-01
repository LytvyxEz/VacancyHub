from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from src.backend.api import root_router, auth_router, parser_route

app = FastAPI()


base_dir = Path(__file__).resolve().parent.parent
static_path = base_dir / "static"


app.mount("/static", StaticFiles(directory=static_path), name="static")


app.include_router(root_router)
app.include_router(auth_router)
app.include_router(parser_route)