import pytest

from app.constants import AgeGroup
from app.db.database import get_session
from app.db.sportclass import SportClassModel


@pytest.fixture
def seed_sports_classes(seed_users, seed_sports):
    with get_session() as db:
        sports_classes = [
            SportClassModel(description="Good", age_group=AgeGroup.ADULT, sport_id=1),
            SportClassModel(
                description="Bad", age_group=AgeGroup.YOUNG_ADULT, sport_id=2
            ),
            SportClassModel(description="Ok", age_group=AgeGroup.YOUTH, sport_id=3),
        ]

        for sport_class in sports_classes:
            db.add(sport_class)
        db.commit()
