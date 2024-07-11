import json
import pytest

from app.main import app

from fastapi.testclient import TestClient

from .fixtures import login, register_user, run_async_drop_db
from .test_user_opers import USER_DATA


DATA_HABIT = {
        "habit_name": "name_test",
        "description": "description_test",
        "alert_time": "12:14:03.061Z"
    }


# def register_user():
#     print("Setup_Method")
#     with TestClient(app) as client:
#         _ = client.post(
#             url="api/users",
#             json=USER_DATA,
#         )
#
# def login():
#     with TestClient(app) as client:
#         user_data = USER_DATA.copy()
#         user_data.pop("telegram_id")
#         print("user_data=================================", user_data)
#
#         response = client.post(
#             url="api/auth/token",
#             data=user_data
#         )
#         return response.json()["access_token"]

def create_habit(access_token):
    params = {
        "token": access_token,
    }

    with TestClient(app) as client:
        user_data = USER_DATA.copy()
        user_data.pop("telegram_id")
        # print("user_data=================================", user_data)

        response = client.post(
            url="api/habits",
            params=params,
            json=DATA_HABIT,
        )
        return response



class TestCreatedHabit(object):
    def setup_method(self):
        register_user()
        self.access_token = login()

    @classmethod
    def teardown_method(cls):
        print("Execute Teardown_Method")
        run_async_drop_db()

    def test_create_habit_ok(self):
        response = create_habit(self.access_token)
        self.habit_id = response.json()["id"]
        assert response.status_code == 201
        assert response.json()["habit_name"] == DATA_HABIT.get("habit_name")
        assert response.json()["description"] == DATA_HABIT.get("description")




    def test_get_habit_ok(self):
        response = create_habit(self.access_token)
        habit_id = response.json()["id"]
        print("test_get_habit_ok=================================")

        params = {
            "token": self.access_token,
            "habit_id":  habit_id

        }

        with TestClient(app) as client:
            response = client.get(
                url="api/habits/<int:habit_id>",
                params=params,
            )
            print("response==================", response.json())
            assert response.status_code == 200
            assert response.json()["habit_name"] == DATA_HABIT.get("habit_name")
            assert response.json()["description"] == DATA_HABIT.get("description")

    def test_path_habit_ok(self):
        response = create_habit(self.access_token)
        habit_id = response.json()["id"]
        print("test_path_habit_ok=================================")

        params = {
            "token": self.access_token,
            "habit_id":  habit_id

        }

        # data = {"alert_time": str(alert_time)}
        data = {
            "habit_name": "name_test_edit",
            "description": "name_test_edit",
            "alert_time": "12:10:03.061Z"
        }

        with TestClient(app) as client:
            response = client.patch(
                url="api/habits/<int:habit_id>",
                params=params,
                json=data,
            )
            print("response==================", response.json())
            assert response.status_code == 201
            assert response.json()["habit_name"] == data.get("habit_name")
            assert response.json()["description"] == data.get("description")

    def test_comp_habit_ok(self):
        response = create_habit(self.access_token)
        habit_id = response.json()["id"]
        print("test_path_habit_ok=================================")

        params = {
            "token": self.access_token,
            "habit_id":  habit_id

        }

        with TestClient(app) as client:
            response = client.post(
                url="api/habits/<int:habit_id>/fulfilling",
                params=params,
            )
            print("response==================", response.json())
            assert response.status_code == 201
            assert response.json()["count"] == 1

    def test_delete_habit_ok(self):
        response = create_habit(self.access_token)
        habit_id = response.json()["id"]
        print("test_path_habit_ok=================================")

        params = {
            "token": self.access_token,
            "habit_id":  habit_id

        }

        with TestClient(app) as client:
            response = client.delete(
                url="api/habits/<int:habit_id>",
                params=params,
            )
            assert response.status_code == 204