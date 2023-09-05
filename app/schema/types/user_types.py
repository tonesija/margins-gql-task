"""GQL Types:
    - User
"""
from datetime import datetime
from enum import Enum
from typing import Optional

import strawberry

from app.db.user import UserModel
from app.schema.gql_context import Info
from app.schema.types.sport_class_types import AgeGroup, Enrollment, SportsClass


@strawberry.enum
class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str
    age_group: AgeGroup

    @strawberry.field
    def enrolled_classes(self) -> list[SportsClass]:
        return [
            SportsClass.from_orm(sport_class)
            for sport_class in self.instance.sport_classes
        ]

    @strawberry.field
    def enrollments(self) -> list["Enrollment"]:
        return [
            Enrollment.from_orm(enrollment_db)
            for enrollment_db in self.instance.enrollments
        ]

    @strawberry.field
    def enrollments(
        self,
        info: Info,
        date_start: Optional[datetime] = None,
        date_end: Optional[datetime] = None,
    ) -> list["Enrollment"]:
        from app.services.user_service import get_user_enrollments_service

        enrollments_db = get_user_enrollments_service(
            self.instance, date_start, date_end, info.context.db
        )
        return [Enrollment.from_orm(enrollment_db) for enrollment_db in enrollments_db]

    instance: strawberry.Private[UserModel]

    @classmethod
    def from_orm(cls, user_db: UserModel):
        return cls(
            id=user_db.id,
            name=user_db.name,
            email=user_db.email,
            instance=user_db,
            age_group=user_db.age_group,
        )


@strawberry.input
class UserInput:
    name: str
    email: str
    password: str
    age_group: AgeGroup


@strawberry.input
class LoginInput:
    email: str
    password: str
