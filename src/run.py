from uvicorn import run

if __name__ == '__main__':
    run("src.backend.api.main:app", port=1111, reload=True)