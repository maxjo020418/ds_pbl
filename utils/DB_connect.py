from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Engine
import subprocess

load_dotenv(dotenv_path="./docker/.env")

N_ID = os.getenv("N_ID")
N_PW = os.getenv("N_PW")

def get_access_token() -> str:
    result = subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True
    )
    return result.stdout.strip()

DB_USER = os.getenv("DB_USER")
DB_PW = os.getenv("DB_PW")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PW}@localhost:3306/datascience_pbl"
)

def get_engine() -> Engine:
    return create_engine(DATABASE_URL, future=True)

def get_cred() -> tuple:
    return get_access_token(), N_ID, N_PW, DB_USER, DB_PW