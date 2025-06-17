import time
from typing import Dict, List
from tqdm import tqdm

import requests
from dotenv import load_dotenv
from sqlalchemy import text
import pandas as pd

import os
import sys
this_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(this_dir, '..'))
sys.path.insert(0, root_dir)

from utils.parser import to_postprint, get_span
from utils.poisson_rng import rng

from utils.DB_connect import get_engine, get_cred
engine = get_engine()
_, N_ID, N_PW, _, _ = get_cred()

def fetch_library_names() -> List[tuple[int, str, str]]:
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT `id`, `도서관명`, `시군구명` FROM library_data"
            ))
        return [(int(row[0]), row[1], row[2]) for row in result]

def naver_search(name: str, location: str) -> List[tuple[str, str]]:

    url = "https://openapi.naver.com/v1/search/blog.json"

    headers = {
        "X-Naver-Client-Id": N_ID,
        "X-Naver-Client-Secret": N_PW,
        "User-Agent": "curl/7.49.1",
        "Accept": "*/*"
    }

    params = {
        "query": name,
        "display": 5,
        "start": 1
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    if response.ok:
        results = response.json()['items']
        return [(result['link'], result['description']) 
                for result in results]
    else: 
        print(response)
        return []

def fetch_naver_posts(links: List[str], file_handle) -> None:
    print('starting naver fetch...')
    for url in tqdm(links):
        pp = to_postprint(url)
        if not pp:
            continue
        time.sleep(rng() / 10)  # RL avoidance
        try:
            text_content = get_span(pp)
        except Exception as exc:
            print(f"failed to fetch {pp}: {exc}")
            continue

        file_handle.write(text_content + '\n[STOP]\n')  # [STOP]으로 블로그 별 쪼개기

def fetch_blog_url() -> None:

    libraries = fetch_library_names()

    i = 0
    for id, name, location in tqdm(libraries, total=len(libraries)):
        lib_link_data: Dict[str, list] = {
            'id': [],
            'library_id': [],
            'url': [],
            'review': [],
        }

        results = naver_search(name, location)
        for link, desc in results:
            lib_link_data['id'].append(i)
            lib_link_data['library_id'].append(id)
            lib_link_data['url'].append(link)
            lib_link_data['review'].append(desc)
            i += 1
        # time.sleep(.25)

        df_lib_link_data = pd.DataFrame(lib_link_data)
        df_lib_link_data.to_sql(
            name='library_reviews',
            con=engine,
            if_exists='append',  # Options: 'fail', 'replace', 'append'
            index=False
        )

if __name__ == "__main__":
    op = int(input('1. fetch url, 2. fetch all blog'))
    if op == 1:
        fetch_blog_url()
    
    if op == 2:
        '''
        with open("./data/naver_posts.txt", "w", encoding="utf-8") as out:
            for links in all_links.values():
                fetch_naver_posts(links, out)
        '''
        pass
