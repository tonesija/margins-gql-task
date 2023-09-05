import pytest

from app.constants import AgeGroup
from app.db.database import get_session
from app.db.sportclass import SportClassModel
from app.scripts.seed_sports import seed_sports as seed_sports_db


@pytest.fixture
def seed_sports():
    seed_sports_db()
