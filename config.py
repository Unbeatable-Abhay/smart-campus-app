import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URL = os.environ.get("DATABASE_URL")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

    PORT = os.environ.get("PORT")
    if PORT is not None:
        PORT = int(PORT)
    else:
        PORT = 5000

    FLASK_ENV = os.environ.get("FLASK_ENV")
    if FLASK_ENV is None:
        FLASK_ENV = "development"