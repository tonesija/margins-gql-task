from app.schema.gql_context import Info
from app.schema.types.sport_class_types import SportsClassRating, SportsClassRatingInput
from app.services.review_service import create_review_service


def review_sports_classes_resolver(
    sport_class_review: SportsClassRatingInput, info: Info
) -> SportsClassRating:
    sport_class_review_db = create_review_service(sport_class_review, info.context.db)

    return SportsClassRating.from_orm(sport_class_review_db)
