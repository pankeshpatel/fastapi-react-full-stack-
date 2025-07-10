from backend.test.utils import (
    get_user_token_headers,
    client,
    random_email,
    random_lower_string,
)
from backend.config.config import settings
from backend.database.db import UserCreate, User
from backend.core.crud import create_user, get_user_by_email, verify_password
from sqlmodel import select


def test_get_users_superuser_me() -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=get_user_token_headers())
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == "pankeshpatel@example.com"


def test_get_existing_user(session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = create_user(session=session, user_create=user_in)
    user_id = user.id
    response = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=get_user_token_headers(),
    )

    print(response.json())
    api_user = response.json()

    existing_user = get_user_by_email(session=session, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_get_existing_user_current_user(session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = create_user(session=session, user_create=user_in)
    user_id = user.id

    login_data = {
        "username": username,
        "password": password,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = get_user_by_email(session=session, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_create_user_existing_username(session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    create_user(session=session, user_create=user_in)
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=get_user_token_headers(),
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_retrieve_users(session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    create_user(session=session, user_create=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    create_user(session=session, user_create=user_in2)

    r = client.get(f"{settings.API_V1_STR}/users/", headers=get_user_token_headers())
    all_users = r.json()

    assert len(all_users["data"]) > 1
    assert "count" in all_users
    for item in all_users["data"]:
        assert "email" in item


def test_update_password_me_incorrect_password() -> None:
    new_password = random_lower_string()
    data = {"current_password": new_password, "new_password": new_password}
    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=get_user_token_headers(),
        json=data,
    )
    assert r.status_code == 400
    updated_user = r.json()
    assert updated_user["detail"] == "Incorrect password"


def test_register_user(session) -> None:
    username = random_email()
    password = random_lower_string()
    full_name = random_lower_string()
    data = {"email": username, "password": password, "full_name": full_name}
    r = client.post(
        f"{settings.API_V1_STR}/users/signup",
        json=data,
    )
    assert r.status_code == 200
    created_user = r.json()
    assert created_user["email"] == username
    assert created_user["full_name"] == full_name

    user_query = select(User).where(User.email == username)
    user_db = session.exec(user_query).first()
    assert user_db
    assert user_db.email == username
    assert user_db.full_name == full_name
    assert verify_password(password, user_db.hashed_password)


def test_register_user_already_exists_error() -> None:
    password = random_lower_string()
    full_name = random_lower_string()
    data = {
        "email": "pankeshpatel@example.com",
        "password": password,
        "full_name": full_name,
    }
    r = client.post(
        f"{settings.API_V1_STR}/users/signup",
        json=data,
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "The user with this email already exists in the system"
