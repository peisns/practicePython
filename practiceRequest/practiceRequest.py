# 1. request 라이브러리를 사용해보겠습니다
# request는 HTTP 요청을 보내고 응답을 처리하는 기본 라이브러리입니다
# GET, POST, PUT, DELETE 등의 요청을 쉽게 수행할 수 있도록 도와줍니다

# HTTP 요청을 테스트하기위해 https://www.jsontest.com/, https://reqres.in/ 플랫폼을 사용했습니다

# 2-2. Endpoint 열거형에서 전방 선언 없이 자기자신을 참조하기 위해 __future__모듈의 anonotations을 가져옵니다 -> 3. 이동
from __future__ import annotations

# 1-1. request 모듈 가져오기 -> 2. 이동
import requests


# 2. Endpoint를 관리하기 위해 간단하게 열거형을 사용합니다
# 열거형 모듈을 가져옵니다
# Endpoint가 중복되지 않기 위해 unique 데코레이터도 가져옵니다
from enum import Enum, unique

# 3-1. request 후 요청이 실패했을 때, None값이 반환될 수 있습니다
# None이 반환되는 것을 Optional을 통해 명시할 수 있도록 typing 모듈을 가져옵니다
import typing

# 아래와 같이 사용하고자 하는 타입만 따로 명시할 수도 있습니다
# from typing import List, Optional

# request 후 실패했을 때, 로그를 남기기 위해 logging 모듈을 가져옵니다
import logging
from logging import handlers


# 3-2. log format을 설정합니다
log_format = (
    """
%(asctime)s
[%(levelname)s] %(filename)s on line %(lineno)d
%(message)s
"""
    + "-" * 60
)

# 3-3. loggging 환경설정
logging.basicConfig(
    format=log_format,
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        handlers.RotatingFileHandler(
            "practicePython.log", maxBytes=2000, backupCount=2
        ),
    ],
)


# 2-1.
@unique
class Endpoint(Enum):
    """
    Endpoint를 관리하기 위한 열거형을 정의합니다

    Args:
        __Enum__ _URL(BASE, SUB)_:
        URL을 만들기 위해 __Base, str(subdomain 또는 subpath)을 변수로 갖는 NamedTuple을 value로 갖습니다
    """

    @unique
    class __Base(Enum):
        JSONTEST_COM = "jsontest.com"
        REQRES_IN = "https://reqres.in/api/"

    class URL(typing.NamedTuple):
        BASE: Endpoint.__Base
        SUB: str

    IP = URL(__Base.JSONTEST_COM, "ip")
    VALIDATION = URL(__Base.JSONTEST_COM, "validate")
    USERS = URL(__Base.REQRES_IN, "users/{user_id}")

    @classmethod
    def get_full_URL(
        cls,
        endpoint: Endpoint,
        data_list: typing.Optional[list[dict[str, typing.Any]]] = None,
        id: typing.Optional[int] = None,
    ) -> str:
        """
        classmethod 데코레이터를 사용해서 URL을 반환하는 메서드를 정의합니다
        http://sub_domain.jsontest.com 형태의 URL을 반환합니다
        예시1: `Endpoint.get_full_URL(Endpoint.VALIDATION, data_list=data_for_POST)`
        예시2:  `Endpoint.get_full_URL(Endpoint.USERS,id=2)

        Args:
            endpoint (Endpoint): 열거형 Endpoint의 멤버를 파라미터로 갖습니다
            data_list (typing.Optional[list[dict[str, typing.Any]]], optional):
                string을 key로, Any를 value로 갖는 Dict가 있습니다. 이 Dict를 element로 갖는 list입니다, Defaults to None
            id (typing.Optional[int], optional): int 타입의 id값입니다

        Returns:
            str: URL 주소를 반환합니다
        """

        if endpoint.value.BASE == cls._Endpoint__Base.value.JSONTEST_COM:
            url = f"http://{endpoint.value.SUB}.{endpoint.value.BASE.value}"

            if data_list is not None and len(data_list) > 0:
                filtered_data = [
                    element_data
                    for element_data in data_list
                    if all(isinstance(key, str) for key in element_data.keys())
                ]

                url += "/?json=[" + ", ".join(map(str, filtered_data)) + "]"

            return url
        else:
            url = f"{endpoint.value.BASE.value}"
            url += (
                f"{endpoint.value.SUB.format(user_id=id)}"
                if id is not None
                else f"{endpoint.value.SUB.split('/{')[0]}"
            )
            return url


# 3.
def process_response(response: requests.Response) -> dict:
    """
    request후 응답받은 response를 처리합니다

    Args:
        response (requests.Response): request 후 응답받은 response

    Raises:
        ConnectionError: statu code가 200미만, 299초과일 때 발생합니다
        ValueError: result가 None일 때 발생합니다

    Returns:
        typing.Optional[dict]: json 형태의 dict를 반환합니다
    """
    status_code = response.status_code
    if status_code < 200 or status_code > 299:
        raise ConnectionError(f"status code is {str(status_code)}.")
    elif status_code != 200:
        print("STATUS CODE:", status_code)
        return {}

    result = response.json()

    if result is None:
        raise ValueError("result is None")

    return result


# 3-1. GET 요청하기
# 3-4. 요청합니다 -> 4. 이동
response = requests.get(Endpoint.get_full_URL(Endpoint.IP))

result = process_response(response)
if result is not None:
    print("GET RESPONSE:", result)
    # GET RESPONSE: {'ip': '218.123.456.789'}
else:
    logging.info("Response result is None")

# 4. POST요청하기
# 서버에 보내고자 하는 데이터를 json형식을 요소로 하는 List으로 선언합니다
data_for_POST = [
    {"userID": 1, "title": "ID1_TITLE_VALUE", "body": "ID1_BODY_VALUE"},
    {"userID": 2, "title": "ID2_TITLE_VALUE", "body": "ID2_BODY_VALUE"},
    {"userID": 3, "title": "ID3_TITLE_VALUE", "body": "ID3_BODY_VALUE"},
    {"userID": 4, "title": "ID4_TITLE_VALUE", "body": "ID4_BODY_VALUE"},
    # 테스트를 위한 잘못된 데이터 추가
    {"userID": 5, "title": "ID5_TITLE_VALUE", 11: "ID5_BODY_VALUE"},
]

# 4-1. 요청합니다 -> 5. 이동
response = requests.post(
    Endpoint.get_full_URL(Endpoint.VALIDATION, data_list=data_for_POST)
)
result = process_response(response=response)

if result is not None:
    print("POST RESPONSE:", result)
else:
    logging.info("Response result is None")

# 5. PUT 요청하기 -> 6. 이동
# update를 위한 이름과 직업 정보 선언
data = {"name": "morpheus", "job": "zion resident"}

id = 2
response = requests.put(Endpoint.get_full_URL(Endpoint.USERS, id=id), json=data)
result = process_response(response=response)
if result is not None:
    print("PUT RESPONSE:", result)
    # PUT RESPONSE: {'name': 'morpheus', 'job': 'zion resident', 'updatedAt': '2024-07-12T22:55:53.550Z'}
else:
    logging.info("Response result is None")

# 6. DELETE 요청하기 -> 7. 이동
response = requests.delete(Endpoint.get_full_URL(Endpoint.USERS, id=id))
result = process_response(response)
if result is not None:
    print("DELETE RESPONSE:", result)
    # DELETE RESPONSE: {'name': 'morpheus', 'job': 'zion resident', 'updatedAt': '2024-07-12T23:01:37.967Z'}
else:
    logging.info("Response result is None")


# 7. 파라미터를 추가하기
params = {"page": 2, "per_page": 5}

response = requests.get(Endpoint.get_full_URL(Endpoint.USERS), params=params)
result = process_response(response)
if result is not None:
    print("GET RESPONSE WITH Parameters:", result)
    """
    GET RESPONSE WITH PARAMETERS:
    {
        'page': 2, 
        'per_page': 5, 
        'total': 12, 
        'total_pages': 3, 
        'data': [{
            'id': 6, 
            'email': 'tracey.ramos@reqres.in', 
            'first_name': 'Tracey', 
            'last_name': 'Ramos', 
            'avatar': 'https://reqres.in/img/faces/6-image.jpg'
            }, {
            'id': 7, 
            'email': 'michael.lawson@reqres.in', 
            'first_name': 'Michael', 
            'last_name': 'Lawson', 
            'avatar': 'https://reqres.in/img/faces/7-image.jpg'
            }, ..., {
            'id': 10, 
            'email': 'byron.fields@reqres.in', 
            'first_name': 'Byron', 
            'last_name': 'Fields', 
            'avatar': 'https://reqres.in/img/faces/10-image.jpg'
            }], 
        'support': 
        {
            'url': 'https://reqres.in/#support-heading', 
            'text': 'To keep ReqRes free, contributions towards server costs are appreciated!'
            }
    }
    """
else:
    logging.info("Response result is None")
