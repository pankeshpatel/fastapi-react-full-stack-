# from sqlmodel import Session, create_engine, select, SQLModel
# from backend.config.config import settings
# from backend.models.models import User, UserCreate
# from backend.core.crud import create_user
# from backend.database.db import engine
# import pytest


# engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# def init_db(session: Session) -> None:
#     SQLModel.metadata.create_all(engine)

#     user = session.exec(
#         select(User).where(User.email == settings.FIRST_SUPERUSER)
#     ).first()
#     if not user:
#         user_in = UserCreate(
#             email=settings.FIRST_SUPERUSER,
#             password=settings.FIRST_SUPERUSER_PASSWORD,
#             is_superuser=True,
#         )
#         user = create_user(session=session, user_create=user_in)


import pytest
from backend.database.db import engine
from sqlmodel import Session
from backend.config.config import settings
from fastapi.testclient import TestClient
from backend.main import app
import random
import string

client = TestClient(app)


def get_user_token_headers():
    login_data = {
        "username": "pankeshpatel@example.com",
        "password": "pankesh@example.com",
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


@pytest.fixture()
def session() -> Session:
    with Session(engine) as s:
        yield s
