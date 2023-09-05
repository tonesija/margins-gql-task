import strawberry

from app.schema.gql_context import Info
from app.schema.types.response_types import (
    ClassFull,
    DeleteUserResponse,
    EnrollResponse,
    GetUserResponse,
    IncorrectLoginCredentials,
    LoginResponse,
    RegisterResponse,
    SportClassNotExists,
    UnEnrollResponse,
    UserAlreadyEnrolled,
    UserDeleted,
    UserDifferentAgeGroup,
    UserExists,
    UserMaxEnrolled,
    UserNotEnrolled,
    UserNotExists,
)
from app.schema.types.user_types import LoginInput, User, UserInput
from app.services.email_service import verify_email_service
from app.services.exceptions import (
    EmailVerificationFailed,
    LoginError,
    SportClassCapacityReached,
    SportClassNotFound,
    UserAlreadyExists,
    UserAlreadyInClass,
    UserAlreadyMaxEnrolled,
    UserNotFound,
    UserNotInAgeGroup,
    UserNotInClass,
)
from app.services.user_service import (
    delete_user_service,
    enroll_user_sports_class_service,
    get_user_by_id_service,
    get_users_service,
    login_user_service,
    register_user_service,
    unenroll_user_sports_class_service,
)


def register_user_resolver(user: UserInput, info: Info) -> RegisterResponse:
    try:
        return register_user_service(user, info.context.db)
    except UserAlreadyExists:
        return UserExists()


def login_user_resolver(login_data: LoginInput, info: Info) -> LoginResponse:
    try:
        return login_user_service(login_data, info.context.db)
    except LoginError:
        return IncorrectLoginCredentials()


def verify_email_resolver(token: str, info: Info) -> bool:
    try:
        verify_email_service(token, info.context.db)
        return True
    except EmailVerificationFailed:
        return False


def get_users_resolver(info: Info) -> list[User]:
    users_db = get_users_service(info.context.db)
    return [User.from_orm(user_db) for user_db in users_db]


def get_user_by_id_resolver(user_id: int, info: Info) -> GetUserResponse:
    try:
        user_db = get_user_by_id_service(user_id, info.context.db)
    except UserNotFound:
        return UserNotExists()
    return User.from_orm(user_db)


def get_me_resolver(info: Info) -> User:
    return User.from_orm(info.context.authenticated_user)


def delete_user_resolver(user_id: int, info: Info) -> DeleteUserResponse:
    if delete_user_service(user_id, info.context.db):
        return UserDeleted()
    else:
        return UserNotExists()


def enroll_user_sports_class_resolver(
    sports_class_id: strawberry.ID, info: Info
) -> EnrollResponse:
    try:
        user_db = enroll_user_sports_class_service(
            info.context.authenticated_user.id, sports_class_id, info.context.db
        )
    except UserNotFound:
        return UserNotExists()
    except SportClassNotFound:
        return SportClassNotExists()
    except UserAlreadyMaxEnrolled:
        return UserMaxEnrolled()
    except SportClassCapacityReached:
        return ClassFull()
    except UserNotInAgeGroup:
        return UserDifferentAgeGroup()
    except UserAlreadyInClass:
        return UserAlreadyEnrolled()

    return User.from_orm(user_db)


def unenroll_user_sports_class_resolver(
    sports_class_id: strawberry.ID, info: Info
) -> UnEnrollResponse:
    try:
        user_db = unenroll_user_sports_class_service(
            info.context.authenticated_user.id, sports_class_id, info.context.db
        )
    except UserNotFound:
        return UserNotExists()
    except SportClassNotFound:
        return SportClassNotExists()
    except UserNotInClass:
        return UserNotEnrolled()

    return User.from_orm(user_db)


def enroll_user_id_sports_class_resolver(
    user_id: strawberry.ID, sports_class_id: strawberry.ID, info: Info
) -> EnrollResponse:
    try:
        user_db = enroll_user_sports_class_service(
            user_id, sports_class_id, info.context.db
        )
    except UserNotFound:
        return UserNotExists()
    except SportClassNotFound:
        return SportClassNotExists()
    except UserAlreadyMaxEnrolled:
        return UserMaxEnrolled()
    except SportClassCapacityReached:
        return ClassFull()
    except UserNotInAgeGroup:
        return UserDifferentAgeGroup()
    except UserAlreadyInClass:
        return UserAlreadyEnrolled()

    return User.from_orm(user_db)


def unenroll_id_user_sports_class_resolver(
    user_id: strawberry.ID, sports_class_id: strawberry.ID, info: Info
) -> UnEnrollResponse:
    try:
        user_db = unenroll_user_sports_class_service(
            user_id, sports_class_id, info.context.db
        )
    except UserNotFound:
        return UserNotExists()
    except SportClassNotFound:
        return SportClassNotExists()
    except UserNotInClass:
        return UserNotEnrolled()

    return User.from_orm(user_db)
