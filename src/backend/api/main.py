from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from src.backend.data import handlers_manager

from src.backend.api import root_router, auth_router, parser_route
from src.backend.api import auth_middleware

app = FastAPI(debug=True)


base_dir = Path(__file__).resolve().parent.parent.parent

static_path = base_dir / 'frontend/static'
app.mount("/static", StaticFiles(directory=static_path), name="static")
<<<<<<< HEAD

app.middleware("http")(auth_middleware)
=======
# app.middleware("http")(auth_middleware)
>>>>>>> cafa16c1a0e2c61e884da29504e721d609358106
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:1111", "http://127.0.0.1:1111"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)
app.include_router(auth_router)
app.include_router(parser_route)
