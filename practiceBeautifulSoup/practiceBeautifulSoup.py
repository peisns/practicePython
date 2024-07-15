# HTML Fetch하기위해 https://en.wikipedia.org/wiki/Main_Page 페이지를 사용했습니다.
import logging
from logging import handlers
import requests
import sys

# 1. bs4 모듈에서 BeautifulSoup 클래스 모듈을 가져옵니다
from bs4 import BeautifulSoup

# log configure
log_format = """
------------------------------------------------------------
%(asctime)s
[%(levelname)s] %(filename)s on line %(lineno)d
%(message)s
------------------------------------------------------------
"""

logging.basicConfig(
    format=log_format,
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(),
        handlers.RotatingFileHandler(
            "practicePython.log", maxBytes=2000, backupCount=2
        ),
    ],
)


def isNone(subject) -> bool:
    if subject is None:
        logging.error(ValueError)
        sys.exit()


# 2. HTML 가져오기
wikipediaURL = "https://en.wikipedia.org/wiki/Main_Page"
response = requests.get(wikipediaURL)
HTML = response.text if response.status_code == 200 else None
# print("HTML:", HTML)

isNone(HTML)

# BeautifulSoup 객체를 생성합니다
soup = BeautifulSoup(HTML, "html.parser")

# 찾고자 하는 태그와 속성을 지정합니다
target_dict = {"h2": "mp-tfa-h2", "div": "mp-tfa"}

# 파싱
target_contents = [
    soup.find(key, id=value).get_text() for key, value in target_dict.items()
]
print("target_contents:", target_contents)