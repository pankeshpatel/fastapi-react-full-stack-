from backend.test.utils import (
    get_user_token_headers,
    client,
    random_email,
    random_lower_string,
    session,
)
from backend.config.config import settings
from backend.database.db import UserCreate, User
from backend.core.crud import create_user, get_user_by_email, verify_password
from sqlmodel import sql, select


def test_create_user(session) -> None:

    email = random_email()

    r = client.post(
        f"{settings.API_V1_STR}/private/users/",
        json={
            "email": email,
            "password": "password123",
            "full_name": "Pollo Listo",
        },
    )

    assert r.status_code == 200

    data = r.json()

    user = session.exec(select(User).where(User.id == data["id"])).first()

    assert user
    assert user.email == email
    assert user.full_name == "Pollo Listo"
