import re
import requests
from bs4 import BeautifulSoup

import re
from urllib.parse import urlparse, parse_qs


def get_se_fs(url: str) -> str:  
    """
    미사용하기로 결정
    쓰지마셈
    """

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
    """Convert various Naver blog URLs to the ``PostPrint`` endpoint.

    This helper normalises a blog post URL so that ``PostPrint.naver``
    directly returns a printer‑friendly page.  ``None`` is returned if the
    URL format is unrecognised.
    """

    p = urlparse(url)

    # Already in PostPrint format
    if p.path.rstrip('/') == '/PostPrint.naver':
        return url

    # Pattern 1: /{blogId}/{logNo}
    m = re.fullmatch(r'/([^/]+)/(\d+)', p.path)
    if m:
        blogId, logNo = m.groups()
    else:
        # Pattern 2: query parameters
        qs = parse_qs(p.query)
        blogId = qs.get('blogId')
        logNo = qs.get('logNo')

        # e.g. https://blog.naver.com/{blogId}?Redirect=Log&logNo=123
        if logNo and not blogId:
            m2 = re.fullmatch(r'/([^/]+)', p.path)
            if m2:
                blogId = [m2.group(1)]

        if not (blogId and logNo):
            print(f'skipping: {url}')
            return None

        blogId, logNo = blogId[0], logNo[0]

    return (
        f"https://blog.naver.com/PostPrint.naver?blogId={blogId}&logNo={logNo}"
    )
