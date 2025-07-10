from backend.test.utils import (
    client,
    random_email,
)
from backend.config.config import settings
from backend.database.db import User
from sqlmodel import select


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
