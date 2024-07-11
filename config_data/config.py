"""the config module is used to check whether the environment has been created"""
import os

from dotenv import find_dotenv, load_dotenv


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "192.168.55.4"
DB_PORT = os.getenv("DB_PORT")
DB_NAME = "habits"
DB_TESTS = True if os.getenv("DB_TESTS") == "True" else False

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

BOT_TOKEN = os.getenv("BOT_TOKEN")
LOCAL_UTC = os.getenv("LOCAL_UTC")
