import json
import pytest

from app.main import app

from fastapi.testclient import TestClient

from .fixtures import fixture_context
from .test_user_opers import USER_DATA


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


def test_create_habit_ok(fixture_context):
    print("Running the test")
    with TestClient(app) as client:
        user_data = USER_DATA.copy()
        user_data.pop("telegram_id")
        print("user_data=================================", user_data)

        response = client.post(
            url="api/auth/token",
            data=user_data,
        )

        access_token = response.json().get("access_token")
        assert response.status_code == 200


# def test_get_token_invalid_username(fixture_context):
#     with TestClient(app) as client:
#         user_data = USER_DATA.copy()
#         user_data.pop("telegram_id")
#         user_data["username"] = "33"
#
#         response = client.post(
#             url="api/auth/token",
#             data=user_data,
#         )
#         assert response.status_code == 401
#
#
# def test_get_token_invalid_password(fixture_context):
#     with TestClient(app) as client:
#         user_data = USER_DATA.copy()
#         user_data.pop("telegram_id")
#         user_data["password"] = "33"
#
#         response = client.post(
#             url="api/auth/token",
#             data=user_data,
#         )
#         assert response.status_code == 401
