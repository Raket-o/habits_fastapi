import json

from app.main import app

from .fixtures import login, register_user, USER_DATA

from fastapi.testclient import TestClient


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
    data = USER_DATA.copy()
    data = data.pop("username")
    with TestClient(app) as client:
        response = client.post(
            url="api/users",
            json=data,
        )

    print(response.json())
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid dictionary or object to extract fields from"


def test_create_user_not_field_password():
    data = USER_DATA.copy()
    data = data.pop("password")
    with TestClient(app) as client:
        response = client.post(
            url="api/users",
            json=data,
        )

    print(response.json())
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid dictionary or object to extract fields from"


def test_create_user_not_field_telegram_id():
    # data = USER_DATA.pop("telegram_id")
    data = USER_DATA.copy()
    data = data.pop("telegram_id")
    with TestClient(app) as client:
        response = client.post(
            url="api/users",
            json=data,
        )

    print(response.json())
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid dictionary or object to extract fields from"


def test_get_user():
    register_user()
    access_token = login()
    params = {
        "token": access_token
    }
    with TestClient(app) as client:
        response = client.get(
            url="api/users/me",
            params=params,
        )

    print(response.json())
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["username"] == USER_DATA.get("username")
    assert response.json()["telegram_id"] == USER_DATA.get("telegram_id")
