from fastapi import status
from backend.test.utils import client
from backend.config.config import settings


def test_healthcheck():
    response = client.get(f"{settings.API_V1_STR}/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is True
