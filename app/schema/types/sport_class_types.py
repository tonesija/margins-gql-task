"""GQL Types:
    - Sport
    - SportsClass
    - SportsClassEvent
    - SportsClassRating
    - Enrollment
"""
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Annotated, List, Optional

import strawberry

from app.db.enrollment import EnrollmentModel
from app.db.sport import SportModel
from app.db.sportclass import SportClassModel
from app.db.sportclassevent import SportClassEventModel
from app.db.sportclassreview import SportClassReviewModel
from app.schema.gql_context import Info
from app.services.auth.authorization import IsAdmin

if TYPE_CHECKING:
    from app.schema.types.user_types import User


@strawberry.type
class Sport:
    id: strawberry.ID
    name: str

    @strawberry.field
    def classes(self) -> list["SportsClass"]:
        return [
            SportsClass.from_orm(sport_class_db)
            for sport_class_db in self.instance.sport_classes
        ]

    instance: strawberry.Private[SportModel]

    @classmethod
    def from_orm(cls, sport_db: SportModel):
        return cls(id=sport_db.id, name=sport_db.name, instance=sport_db)


@strawberry.enum
class AgeGroup(str, Enum):
    CHILDREN = "children"
    YOUTH = "youth"
    YOUNG_ADULT = "young_adult"
    ADULT = "adult"


@strawberry.type
class SportsClass:
    id: strawberry.ID
    sport: Sport
    age_group: AgeGroup
    description: str

    @strawberry.field
    def average_rating(self, info: Info) -> Optional[float]:
        from app.services.review_service import get_average_ratings_service

        return get_average_ratings_service(self.id, info.context.db)

    @strawberry.field
    def sports_class_events(
        self,
        info: Info,
        date_start: Optional[datetime] = None,
        date_end: Optional[datetime] = None,
    ) -> list["SportsClassEvent"]:
        from app.services.sport_class_event_service import (
            get_sport_class_events_service,
        )

        sport_class_events_db = get_sport_class_events_service(
            self.instance, date_start, date_end, info.context.db
        )
        return [
            SportsClassEvent.from_orm(sports_class_event)
            for sports_class_event in sport_class_events_db
        ]

    @strawberry.field(permission_classes=[IsAdmin])
    def users(
        self,
    ) -> list[Annotated["User", strawberry.lazy("app.schema.types.user_types")]]:
        from app.schema.types.user_types import User

        return [User.from_orm(user) for user in self.instance.users]

    @strawberry.field(permission_classes=[IsAdmin])
    def ratings(self) -> list["SportsClassRating"]:
        return [
            SportsClassRating.from_orm(sport_class_rating_db)
            for sport_class_rating_db in self.instance.sport_class_reviews
        ]

    @strawberry.field(permission_classes=[IsAdmin])
    def enrollments(
        self,
        info: Info,
        date_start: Optional[datetime] = None,
        date_end: Optional[datetime] = None,
    ) -> list["Enrollment"]:
        from app.services.sport_class_service import get_sport_class_enrollments_service

        enrollments_db = get_sport_class_enrollments_service(
            self.instance, date_start, date_end, info.context.db
        )
        return [Enrollment.from_orm(enrollment_db) for enrollment_db in enrollments_db]

    instance: strawberry.Private[SportClassModel]

    @classmethod
    def from_orm(cls, sport_class: SportClassModel) -> "SportsClass":
        return cls(
            id=sport_class.id,
            description=sport_class.description,
            age_group=sport_class.age_group,
            sport=Sport.from_orm(sport_class.sport),
            instance=sport_class,
        )


@strawberry.type
class SportsClassEvent:
    id: strawberry.ID
    sports_class: SportsClass
    starts_at: datetime
    duration: Optional[int]

    @classmethod
    def from_orm(cls, sport_class_event: SportClassEventModel) -> "SportsClass":
        return cls(
            id=sport_class_event.id,
            starts_at=sport_class_event.starts_at,
            duration=sport_class_event.duration,
            sports_class=SportsClass.from_orm(sport_class_event.sport_class),
        )


@strawberry.type
class SportsClassRating:
    id: strawberry.ID
    sports_class: "SportsClass"
    rating: int
    comment: str

    @classmethod
    def from_orm(cls, sport_class_review_db: SportClassReviewModel):
        return cls(
            id=sport_class_review_db.id,
            comment=sport_class_review_db.comment,
            rating=sport_class_review_db.rating,
            sports_class=SportsClass.from_orm(sport_class_review_db.sport_class),
        )


@strawberry.type
class Enrollment:
    id: strawberry.ID
    enroll: bool
    created_at: datetime
    user: Annotated["User", strawberry.lazy("app.schema.types.user_types")]

    @classmethod
    def from_orm(cls, enrollment: EnrollmentModel):
        from app.schema.types.user_types import User

        return cls(
            id=enrollment.id,
            enroll=enrollment.enroll,
            created_at=enrollment.created_at,
            user=User.from_orm(enrollment.user),
        )


@strawberry.input
class SportClassInput:
    sport_id: strawberry.ID
    age_group: AgeGroup
    description: str


@strawberry.input
class SportClassFilterInput:
    age_groups: List[AgeGroup]
    sport_ids: List[strawberry.ID]


@strawberry.input
class SportClassUpdateInput:
    sport_class_id: strawberry.ID
    sport_id: strawberry.ID
    age_group: AgeGroup
    description: str


@strawberry.input
class SportClassEventInput:
    sports_class_id: strawberry.ID
    starts_at: datetime
    duration: Optional[int]


@strawberry.input
class SportsClassRatingInput:
    sports_class_id: strawberry.ID
    rating: int
    comment: str
