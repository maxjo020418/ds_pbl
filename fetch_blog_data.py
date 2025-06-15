import os
import time
import pickle
from typing import Dict, List

import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from parser import to_postprint, get_span
from utils.poisson_rng import rng


load_dotenv(dotenv_path="./docker/.env")

CX = os.getenv("CX")
KEY = os.getenv("KEY")
DB_USER = os.getenv("DB_USER")
DB_PW = os.getenv("DB_PW")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PW}@localhost:3306/datascience_pbl"
)

def fetch_library_names() -> List[str]:
    engine = create_engine(DATABASE_URL, future=True)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT `도서관명` FROM library_data"))
        return [row[0] for row in result]

def google_search(name: str) -> List[str]:
    params = {
        "cx": CX,
        "key": KEY,
        "exactTerms": name,
    }
    r = requests.get(
        "https://customsearch.googleapis.com/customsearch/v1",
        params=params,
    )
    if r.ok:
        data = r.json()
        return [item.get("link") for item in data.get("items", [])]
    return []

def fetch_naver_posts(links: List[str], file_handle) -> None:
    for url in links:
        pp = to_postprint(url)
        if not pp:
            continue
        time.sleep(rng() / 10)
        try:
            text_content = get_span(pp)
        except Exception as exc:
            print(f"failed to fetch {pp}: {exc}")
            continue
        file_handle.write(pp + "\n")
        file_handle.write(text_content + "\n\n")

def main() -> None:
    libraries = fetch_library_names()
    all_links: Dict[str, List[str]] = {}

    for name in libraries:
        all_links[name] = google_search(name)

    with open("./data/google_links.pkl", "wb") as f:
        pickle.dump(all_links, f)

    with open("./data/naver_posts.txt", "w", encoding="utf-8") as out:
        for links in all_links.values():
            fetch_naver_posts(links, out)

if __name__ == "__main__":
    main()
