import json

from app.main import app

from fastapi.testclient import TestClient


# from fastapi import FastAPI
# app = FastAPI()

USER_DATA = {
    "username": "test",
    "password": "test_password",
    "telegram_id": 177
}


def test_create_user_ok():
    with TestClient(app) as client:
        response = client.post(
            url="api/users",
            json=USER_DATA,

        )

    assert response.status_code == 201
    assert response.json()["username"] == USER_DATA.get("username")
    assert response.json()["telegram_id"] == USER_DATA.get("telegram_id")


def test_create_user_not_field_username():
    with TestClient(app) as client:
        response = client.post(
            url="api/users",
            json=USER_DATA.pop("username"),

        )

    print(response.json())
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid dictionary or object to extract fields from"


def test_create_user_not_field_password():
    with TestClient(app) as client:
        response = client.post(
            url="api/users",
            json=USER_DATA.pop("password"),

        )

    print(response.json())
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid dictionary or object to extract fields from"


def test_create_user_not_field_telegram_id():
    with TestClient(app) as client:
        response = client.post(
            url="api/users",
            json=USER_DATA.pop("telegram_id"),

        )

    print(response.json())
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid dictionary or object to extract fields from"
