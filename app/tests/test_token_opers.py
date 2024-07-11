"""the token test module"""
from fastapi.testclient import TestClient

from app.main import app

from .test_user_opers import USER_DATA
from .fixtures import fixture_create_user


def test_get_token_ok(fixture_create_user) -> None:
    with TestClient(app) as client:
        user_data = USER_DATA.copy()
        user_data.pop("telegram_id")

        response = client.post(
            url="api/auth/token",
            data=user_data,
        )

    assert response.status_code == 200


def test_get_token_invalid_username(fixture_create_user) -> None:
    with TestClient(app) as client:
        user_data = USER_DATA.copy()
        user_data.pop("telegram_id")
        user_data["username"] = "33"

        response = client.post(
            url="api/auth/token",
            data=user_data,
        )

    assert response.status_code == 401


def test_get_token_invalid_password(fixture_create_user) -> None:
    with TestClient(app) as client:
        user_data = USER_DATA.copy()
        user_data.pop("telegram_id")
        user_data["password"] = "33"

        response = client.post(
            url="api/auth/token",
            data=user_data,
        )

    assert response.status_code == 401
