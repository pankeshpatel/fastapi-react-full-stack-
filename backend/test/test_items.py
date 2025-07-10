from backend.test.utils import (
    get_user_token_headers,
    client,
)
from backend.config.config import settings
import uuid


def test_read_item_not_found() -> None:
    response = client.get(
        f"{settings.API_V1_STR}/items/{uuid.uuid4()}",
        headers=get_user_token_headers(),
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"
