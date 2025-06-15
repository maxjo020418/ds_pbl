from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./docker/.env")

# CSE keys
CX = os.getenv("CX")
KEY = os.getenv("KEY")

# SQL server creds
DB_USER = os.getenv("DB_USER")
DB_PW = os.getenv("DB_PW")

# Format: dialect+driver://username:password@host:port/database
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PW}"
    "@localhost:3306/datascience_pbl"
)

def connect():
    engine = create_engine(DATABASE_URL, echo=True, future=True)
    session = sessionmaker(bind=engine)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT DATABASE();"))
        print("Connected to database:", result.scalar())

    return engine, session
