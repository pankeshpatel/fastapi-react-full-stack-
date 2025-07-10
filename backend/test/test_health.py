from fastapi import status
from backend.test.utils import client


def test_healthcheck():
    response = client.get(f"/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is True
