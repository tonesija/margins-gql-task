from app.db.database import get_session
from app.db.sport import SportModel


def seed_sports():
    with get_session() as db:
        sports = [
            SportModel(id=1, name="Baseball"),
            SportModel(id=2, name="Basketball"),
            SportModel(id=3, name="Football"),
            SportModel(id=4, name="Boxing"),
            SportModel(id=5, name="Cycling"),
            SportModel(id=6, name="Fitness"),
            SportModel(id=7, name="Golf"),
            SportModel(id=8, name="Running"),
            SportModel(id=9, name="Swimming"),
            SportModel(id=10, name="Tennis"),
            SportModel(id=11, name="Triathlon"),
            SportModel(id=12, name="Volleyball"),
        ]

        try:
            for sport in sports:
                db.add(sport)
            db.commit()
        except Exception:
            db.rollback()
            print("Already seeded sports")
