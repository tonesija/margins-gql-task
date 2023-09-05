from datetime import datetime

from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.db.enrollment import EnrollmentModel
from app.db.sport import SportModel
from app.db.sportclass import SportClassModel
from app.schema.types.sport_class_types import (
    SportClassFilterInput,
    SportClassInput,
    SportClassUpdateInput,
)
from app.services.exceptions import SportClassNotFound


def create_sport_class_service(
    sport_class: SportClassInput, db: Session
) -> SportClassModel:
    sport_class_db = SportClassModel(
        sport_id=sport_class.sport_id,
        description=sport_class.description,
        age_group=sport_class.age_group,
    )
    db.add(sport_class_db)
    db.commit()
    return sport_class_db


def update_sport_class_service(
    sport_class: SportClassUpdateInput, db: Session
) -> SportClassModel:
    """
    Raises:
        SportClassNotFound
    """
    try:
        sport_class_db: SportClassModel = (
            db.query(SportClassModel)
            .filter(SportClassModel.id == sport_class.sport_class_id)
            .one()
        )
        sport_class_db.age_group = sport_class.age_group.value
        sport_class_db.description = sport_class.description
        sport_class_db.sport_id = sport_class.sport_id
        db.commit()
    except exc.NoResultFound:
        raise SportClassNotFound()
    return sport_class_db


def get_sports_classes_service(
    sport_class_filter: SportClassFilterInput, db: Session
) -> list[SportClassModel]:
    query = db.query(SportClassModel)

    if sport_class_filter.age_groups:
        query = query.filter(
            SportClassModel.age_group.in_(sport_class_filter.age_groups)
        )
    if sport_class_filter.sport_ids:
        query = query.filter(SportClassModel.sport_id.in_(sport_class_filter.sport_ids))

    return query.all()


def get_sport_class_service(sport_class_id: int, db: Session) -> SportClassModel:
    """
    Raises:
        SportClassNotFound
    """
    try:
        sport_class_db = (
            db.query(SportClassModel).filter(SportClassModel.id == sport_class_id).one()
        )
    except exc.NoResultFound:
        raise SportClassNotFound()
    return sport_class_db


def get_sports_service(db: Session) -> list[SportModel]:
    return db.query(SportModel).all()


def get_sport_class_enrollments_service(
    sport_class: SportClassModel, date_start: datetime, date_end: datetime, db: Session
):
    query = db.query(EnrollmentModel).filter(
        EnrollmentModel.sport_class_id == sport_class.id
    )
    if date_start:
        query = query.filter(EnrollmentModel.created_at > date_start)
    if date_end:
        query = query.filter(EnrollmentModel.created_at < date_end)

    return query.all()
