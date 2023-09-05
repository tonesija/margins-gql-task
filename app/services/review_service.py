from typing import Optional

from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.db.sportclassreview import SportClassReviewModel
from app.schema.types.sport_class_types import SportsClassReviewInput
from app.services.exceptions import SportClassNotFound


def create_review_service(
    sport_class_review: SportsClassReviewInput, db: Session
) -> SportClassReviewModel:
    try:
        sport_class_review_db = SportClassReviewModel(
            comment=sport_class_review.comment,
            rating=sport_class_review.rating,
            sport_class_id=sport_class_review.sports_class_id,
        )
        db.add(sport_class_review_db)
        db.commit()
    except exc.NoResultFound:
        raise SportClassNotFound()
    return sport_class_review_db


def get_average_ratings_service(sport_class_id: int, db: Session) -> Optional[float]:
    reviews_db = (
        db.query(SportClassReviewModel)
        .filter(SportClassReviewModel.sport_class_id == sport_class_id)
        .all()
    )
    if reviews_db:
        return sum([review.rating for review in reviews_db]) / len(reviews_db)
    else:
        return None
