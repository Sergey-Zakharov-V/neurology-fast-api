import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

YOOKASSA_ACCOUNT_ID = os.environ.get("YOOKASSA_ACCOUNT_ID")
YOOKASSA_SECRETKEY = os.environ.get("YOOKASSA_SECRETKEY")