from uvicorn import run

from src.api.main import app


if __name__ == '__main__':
    run(app, port=1111)
