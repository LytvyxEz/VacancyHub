import os
from dotenv import load_dotenv


load_dotenv()


DB_URL: str = os.getenv("DB_URL")
DB_KEY: str = os.getenv("DB_KEY")
