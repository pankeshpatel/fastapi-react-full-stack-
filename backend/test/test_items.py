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
import uuid


def test_read_item_not_found() -> None:
    response = client.get(
        f"{settings.API_V1_STR}/items/{uuid.uuid4()}",
        headers=get_user_token_headers(),
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"
