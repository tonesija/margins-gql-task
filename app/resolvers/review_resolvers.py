from app.schema.gql_context import Info
from app.schema.types.sport_class_types import SportsClassReview, SportsClassReviewInput
from app.services.review_service import create_review_service


def review_sports_classes_resolver(
    sport_class_review: SportsClassReviewInput, info: Info
) -> SportsClassReview:
    sport_class_review_db = create_review_service(sport_class_review, info.context.db)

    return SportsClassReview.from_orm(sport_class_review_db)
