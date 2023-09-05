from typing import Annotated, Union

import strawberry

from app.schema.types.sport_class_types import (
    SportsClass,
    SportsClassEvent,
    SportsClassReview,
)
from app.schema.types.user_types import User


@strawberry.type
class AccessToken:
    access_token: str


@strawberry.type
class IncorrectLoginCredentials:
    message: str = "Email or password not correct"


@strawberry.type
class UserExists:
    message: str = "User already exists"


@strawberry.type
class UserNotExists:
    message: str = "User does not exist"


@strawberry.type
class UserDeleted:
    message: str = "User deleted"


@strawberry.type
class Unauthorized:
    message: str = "Unauthorized"


@strawberry.type
class SportClassNotExists:
    message: str = "Sports class does not exist"


@strawberry.type
class SportClassEventDeleted:
    message: str = "Sport class event deleted"


@strawberry.type
class SportClassEventNotExists:
    message: str = "Sports class event does not exist"


@strawberry.type
class UserAlreadyEnrolled:
    message: str = "User is already enrolled in that class"


@strawberry.type
class UserNotEnrolled:
    message: str = "User is not enrolled in that class"


@strawberry.type
class ClassFull:
    message: str = "Class already has 10 members"


@strawberry.type
class UserMaxEnrolled:
    message: str = "User is already enrolled in 2 classes"


@strawberry.type
class UserDifferentAgeGroup:
    message: str = "User is not the same age group as the class"


LoginResponse = Annotated[
    Union[AccessToken, IncorrectLoginCredentials],
    strawberry.union("LoginResponse"),
]

RegisterResponse = Annotated[
    Union[AccessToken, UserExists],
    strawberry.union("RegisterResponse"),
]


GetUserResponse = Annotated[
    Union[User, UserNotExists],
    strawberry.union("GetUserResponse"),
]


DeleteUserResponse = Annotated[
    Union[UserDeleted, UserNotExists],
    strawberry.union("DeleteUserResponse"),
]

EnrollResponse = Annotated[
    Union[
        User,
        UserAlreadyEnrolled,
        UserMaxEnrolled,
        ClassFull,
        UserDifferentAgeGroup,
        SportClassNotExists,
        UserNotExists,
    ],
    strawberry.union("EnrollResponse"),
]
UnEnrollResponse = Annotated[
    Union[User, UserNotExists, UserNotEnrolled, SportClassNotExists],
    strawberry.union("UnEnrollResponse"),
]

GetSportClassResponse = Annotated[
    Union[SportsClass, SportClassNotExists], strawberry.union("GetSportClassResponse")
]
UpdateSportClassResponse = Annotated[
    Union[SportsClass, SportClassNotExists],
    strawberry.union("UpdateSportClassResponse"),
]

CreateSportClassEventResponse = Annotated[
    Union[SportsClassEvent, SportClassNotExists],
    strawberry.union("CreateSportClassEventResponse"),
]

DeleteSportClassEventResponse = Annotated[
    Union[SportClassEventDeleted, SportClassEventNotExists],
    strawberry.union("DeleteSportClassEventResponse"),
]

SportClassReviewResponse = Annotated[
    Union[SportsClassReview, SportClassNotExists],
    strawberry.union("SportClassReviewResponse"),
]
