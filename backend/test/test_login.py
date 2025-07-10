from backend.config.config import settings
from fastapi import status


from backend.test.utils import (
    client,
    get_user_token_headers,
    random_email,
    random_lower_string,
)
from backend.models.models import User, UserCreate
from backend.core.crud import create_user
from backend.utils.utils import (
    generate_password_reset_token,
)
from backend.test.utils import client


def test_login_access_token():
    login_data = {
        "username": "pankeshpatel@example.com",
        "password": "pankesh@example.com",
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_incorrect_password() -> None:
    login_data = {
        "username": "pankeshpatel@example.com",
        "password": "incorrect",
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 400


# def test_use_access_token() -> None:
#     response = client.post(
#         f"{settings.API_V1_STR}/login/test-token",
#         headers=get_user_token_headers(),
#     )
#     result = response.json()
#     assert response.status_code == 200
#     assert "email" in result
