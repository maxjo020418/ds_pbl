import re
import requests
from bs4 import BeautifulSoup

import re
from urllib.parse import urlparse, parse_qs

def get_se_fs(url: str) -> str:
    # 1. Fetch the page and ensure it's valid
    url = url
    response = requests.get(url)  # Sends a GET request
    response.raise_for_status()  # Raises an exception for HTTP errors

    # 2. Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')  # Uses the built-in parser

    # 3a. Find all <span> tags with a class token starting with "se-fs-"
    spans_regex = soup.find_all(
        'span',
        class_=re.compile(r'^se-fs-')  # Matches any individual class that begins with se-fs-
    )

    # 3b. (Alternative) Use CSS prefix selectors
    spans_css = soup.select(
        'span[class^="se-fs-"], span[class*=" se-fs-"]'
    )  # Covers both first-token and subsequent-token cases

    # 4. Extract and print text
    texts = ''
    for span in set(spans_regex + spans_css):
        text = span.get_text(strip=True)  # Strips surrounding whitespace
        texts += text

    return texts

def get_span(url: str) -> str:
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    # grab every span, regardless of class
    spans = soup.find_all('span')

    # concatenate non-empty text in document order
    return '\n'.join(s.get_text(strip=True) for s in spans if s.get_text(strip=True))


def to_postprint(url: str) -> str | None:
    """
    다음 형태로 url 변형하여 출력, 호환 불가일 경우 None 배출
    "https://blog.naver.com/PostPrint.naver?blogId={blogId}&logNo={logNo}"
    """
    p = urlparse(url)

    # 1) /{blogId}/{logNo} pattern
    m = re.fullmatch(r'/([^/]+)/(\d+)', p.path)
    if m:
        blogId, logNo = m.groups()
    else:
        return None
    
    return f"https://blog.naver.com/PostPrint.naver?blogId={blogId}&logNo={logNo}"
