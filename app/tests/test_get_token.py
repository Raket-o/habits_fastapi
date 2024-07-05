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


class TestDemo(object):
    def setup_method(self):
        print("Setup_Method")
        with TestClient(app) as client:
            response = client.post(
                url="api/users",
                json=USER_DATA,

            )

        self.id = response.json()["id"]
        self.username = response.json()["username"]



        with TestClient(app) as client:
            user_data = USER_DATA.copy()
            # user_data = user_data.pop("telegram_id")
            user_data.pop("telegram_id")
            print("user_data=================================", user_data)

            response = client.post(
                url="api/auth/token",
                json=user_data,
                # data=user_data,

            )
            print(response.json())
            # assert response.status_code == 200
            self.access_token = response.json()["access_token"]


    def test_get_token_ok(self):
        with TestClient(app) as client:
            print("test_get_token_ok", self.id, self.username, self.access_token)

            user_data = USER_DATA.copy()
            # user_data = user_data.pop("telegram_id")
            user_data.pop("telegram_id")
            print("user_data=================================", user_data)

            response = client.post(
                url="api/auth/token",
                # json=user_data,
                data=user_data,
                # auth=user_data
            )
            print(response.json())
            assert response.status_code == 200

    def teardown_method(self):
        # print("Execute Teardown_Method", self.id, self.username)
        print("Execute Teardown_Method")


        # print("Execute test case 1")

        # assert 1 + 1 == 2

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
