import pytest

from app.db.database import get_session
from app.db.user import UserModel


@pytest.fixture
def seed_users():
    with get_session() as db:
        users = [
            UserModel(
                name="Test user",
                email="testemail1",
                hashed_password="pass",
                age_group="youth",
            ),
            UserModel(
                name="Admin user",
                email="admineemail1",
                hashed_password="pass",
                age_group="adult",
                role="admin",
            ),
        ]

        for user in users:
            db.add(user)
        db.commit()
