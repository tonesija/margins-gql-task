from datetime import datetime

from sqlalchemy.orm import Session

from app.db.sportclass import SportClassModel
from app.db.sportclassevent import SportClassEventModel
from app.schema.types.sport_class_types import SportClassEventInput


def get_sport_class_events_service(
    sport_class: SportClassModel, date_start: datetime, date_end: datetime, db: Session
) -> list[SportClassEventModel]:
    query = db.query(SportClassEventModel).filter(
        SportClassEventModel.sport_class_id == sport_class.id
    )
    if date_start:
        query = query.filter(SportClassEventModel.starts_at > date_start)
    if date_end:
        query = query.filter(SportClassEventModel.starts_at < date_end)

    return query.all()


def create_sports_class_event_service(
    sport_class_event: SportClassEventInput, db: Session
) -> SportClassEventModel:
    sport_class_event_db = SportClassEventModel(
        sport_class_id=sport_class_event.sports_class_id,
        duration=sport_class_event.duration,
        starts_at=sport_class_event.starts_at,
    )
    db.add(sport_class_event_db)
    db.commit()
    return sport_class_event_db


def delete_sports_class_event_service(sport_class_event_id: int, db: Session) -> int:
    num = (
        db.query(SportClassEventModel)
        .filter(SportClassEventModel.id == sport_class_event_id)
        .delete()
    )
    db.commit()
    return num
