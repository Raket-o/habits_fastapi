import json

from app.main import app

from fastapi.testclient import TestClient


# from fastapi import FastAPI
# app = FastAPI()

from .test_user_opers import USER_DATA

# USER_DATA = {
#     "username": "test",
#     "password": "test_password",
#     "telegram_id": 177
# }

TOKEN_DATA: str = ""


# def setup_function():
#     print("Execute Setup_function")


# def test_create_user_ok():
# def setup_function():
#     with TestClient(app) as client:
#         response = client.post(
#             url="api/users",
#             json=USER_DATA,
#
#         )
#
#     # print(response.json())
#     # assert response.status_code == 201
#     # assert response.json()["username"] == USER_DATA.get("username")
#     # assert response.json()["telegram_id"] == USER_DATA.get("telegram_id")
#
#
# def test_get_token_ok():
#     with TestClient(app) as client:
#         user_data = USER_DATA.copy()
#         # user_data = user_data.pop("telegram_id")
#         user_data.pop("telegram_id")
#         print("user_data=================================",user_data)
#
#         response = client.post(
#             url="api/auth/token",
#             # json=user_data,
#             data=user_data
#             # auth=user_data
#         )
#
#     print(response.json())
#     # assert response.status_code == 200
# #     # assert response.json()["username"] == USER_DATA.get("username")
# #     # assert response.json()["telegram_id"] == USER_DATA.get("telegram_id")





import pytest


# class TestDemo(object):
#     def setup_method(self):
#         print("Setup_Method")
#         with TestClient(app) as client:
#             response = client.post(
#                 url="api/users",
#                 json=USER_DATA,
#
#             )
#
#         self.id = response.json()["id"]
#         self.username = response.json()["username"]
#
#
#
#         with TestClient(app) as client:
#             user_data = USER_DATA.copy()
#             # user_data = user_data.pop("telegram_id")
#             user_data.pop("telegram_id")
#             print("user_data=================================", user_data)
#
#             response = client.post(
#                 url="api/auth/token",
#                 json=user_data,
#                 # data=user_data,
#
#             )
#             print(response.json())
#             # assert response.status_code == 200
#             self.access_token = response.json()["access_token"]
#
#
#     def test_get_token_ok(self):
#         with TestClient(app) as client:
#             print("test_get_token_ok", self.id, self.username, self.access_token)
#
#             user_data = USER_DATA.copy()
#             # user_data = user_data.pop("telegram_id")
#             user_data.pop("telegram_id")
#             print("user_data=================================", user_data)
#
#             response = client.post(
#                 url="api/auth/token",
#                 # json=user_data,
#                 data=user_data,
#                 # auth=user_data
#             )
#             print(response.json())
#             assert response.status_code == 200
#
#     def teardown_method(self):
#         # print("Execute Teardown_Method", self.id, self.username)
#         print("Execute Teardown_Method")

import asyncio


async def drop_db():
    from app.database.connect import Base, engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def context():
    """What to do before/after the test."""
    print("Entering !")

    # def setup_method(self):

    print("Setup_Method")
    with TestClient(app) as client:
        response = client.post(
            url="api/users",
            json=USER_DATA,

        )

    print(response.json())

    id = response.json()["id"]
    username = response.json()["username"]

    yield
    print("Exiting !")
    print(response.json())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(drop_db())


def test_get_token_ok(context):
    """The actual code of your test"""
    print("Running the test")
    with TestClient(app) as client:
        user_data = USER_DATA.copy()
        user_data.pop("telegram_id")
        print("user_data=================================", user_data)

        response = client.post(
            url="api/auth/token",
            data=user_data,
        )
        print(response.json())

        access_token = response.json().get("access_token")
        assert response.status_code == 200


def test_get_token_invalid_username(context):
    """The actual code of your test"""
    print("Running the test")

    # def test_get_token_ok(self):
    with TestClient(app) as client:
        user_data = USER_DATA.copy()
        user_data.pop("telegram_id")
        user_data["username"] = "33"

        response = client.post(
            url="api/auth/token",
            data=user_data,
        )
        # print(response.json())
        assert response.status_code == 401


def test_get_token_invalid_password(context):
    """The actual code of your test"""
    print("Running the test")

    # def test_get_token_ok(self):
    with TestClient(app) as client:
        user_data = USER_DATA.copy()
        user_data.pop("telegram_id")
        user_data["password"] = "33"

        response = client.post(
            url="api/auth/token",
            data=user_data,
        )
        # print(response.json())
        assert response.status_code == 401


    # def test_case2(self):
    #     print("Execute test case 2")
    #     assert 1 + 3 == 4
    #
    # def test_case3(self):
    #     print("Execute test 3")
    #     assert 1 + 5 == 6

#
# def test_create_user_not_field_username():
#     with TestClient(app) as client:
#         response = client.post(
#             url="api/users",
#             json=USER_DATA.pop("username"),
#
#         )
#
#     print(response.json())
#     assert response.status_code == 422
#     assert response.json()["detail"][0]["msg"] == "Input should be a valid dictionary or object to extract fields from"
#
#
# def test_create_user_not_field_password():
#     with TestClient(app) as client:
#         response = client.post(
#             url="api/users",
#             json=USER_DATA.pop("password"),
#
#         )
#
#     print(response.json())
#     assert response.status_code == 422
#     assert response.json()["detail"][0]["msg"] == "Input should be a valid dictionary or object to extract fields from"
#
#
# def test_create_user_not_field_telegram_id():
#     with TestClient(app) as client:
#         response = client.post(
#             url="api/users",
#             json=USER_DATA.pop("telegram_id"),
#
#         )
#
#     print(response.json())
#     assert response.status_code == 422
#     assert response.json()["detail"][0]["msg"] == "Input should be a valid dictionary or object to extract fields from"
