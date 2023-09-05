from datetime import datetime

from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.db.enrollment import EnrollmentModel
from app.db.sportclass import SportClassModel
from app.db.user import UserModel
from app.schema.types.response_types import AccessToken
from app.schema.types.user_types import LoginInput, UserInput
from app.services.auth.authentication import (
    create_access_token,
    get_password_hash,
    get_user_by_email,
    verify_password,
)
from app.services.email_service import send_verify_email_and_create_token
from app.services.exceptions import (
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


def get_users_service(db: Session) -> list[UserModel]:
    return db.query(UserModel).all()


def get_user_by_id_service(user_id: int, db: Session) -> UserModel:
    """
    Raises:
        UserNotFound
    """
    try:
        user_db = db.query(UserModel).filter(UserModel.id == user_id).one()
    except exc.NoResultFound:
        raise UserNotFound()
    return user_db


def register_user_service(user: UserInput, db: Session) -> AccessToken:
    """
    Raises:
        UserAlreadyExists
    """
    try:
        user_db = UserModel(
            name=user.name,
            email=user.email,
            hashed_password=get_password_hash(user.password),
            age_group=user.age_group,
        )
        db.add(user_db)
        db.commit()
    except exc.IntegrityError:
        raise UserAlreadyExists()

    access_token = create_access_token({"email": user.email})

    send_verify_email_and_create_token(user_db, db)

    return AccessToken(access_token=access_token)


def login_user_service(login_data: LoginInput, db: Session) -> AccessToken:
    """
    Raises:
        IncorrectLoginCredentials
    """
    user_db: UserModel = get_user_by_email(login_data.email, db)

    if not user_db:
        raise LoginError()

    if not verify_password(login_data.password, user_db.hashed_password):
        raise LoginError()

    access_token = create_access_token({"email": user_db.email})

    return AccessToken(access_token=access_token)


def delete_user_service(user_id: int, db: Session) -> bool:
    try:
        user_db = db.query(UserModel).filter(UserModel.id == user_id).one()
        db.delete(user_db)
        db.commit()
    except exc.NoResultFound:
        return False
    return True


def enroll_user_sports_class_service(
    user_id: int, sports_class_id: int, db: Session
) -> UserModel:
    """
    Raises:
        UserNotFound
        SportClassNotFound
        UserNotInAgeGroup
        UserAlreadyMaxEnrolled
        SportClassCapacityReached
        UserAlreadyInClass
    """
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).one()
    except exc.NoResultFound:
        raise UserNotFound()
    try:
        sport_class = (
            db.query(SportClassModel)
            .filter(SportClassModel.id == sports_class_id)
            .one()
        )
    except exc.NoResultFound:
        raise SportClassNotFound()

    if user.age_group != sport_class.age_group:
        raise UserNotInAgeGroup()
    if len(user.sport_classes) == 2:
        raise UserAlreadyMaxEnrolled()
    if len(sport_class.users) == 10:
        raise SportClassCapacityReached()
    if user in sport_class.users:
        raise UserAlreadyInClass()

    enrollment = EnrollmentModel(
        enroll=True, sport_class_id=sports_class_id, user_id=user.id
    )
    db.add(enrollment)

    sport_class.users.append(user)

    db.commit()
    return user


def unenroll_user_sports_class_service(
    user_id: int, sports_class_id: int, db: Session
) -> UserModel:
    """
    Raises:
        UserNotFound
        SportClassNotFound
        UserNotInClass
    """
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).one()
    except exc.NoResultFound:
        raise UserNotFound()
    try:
        sport_class = (
            db.query(SportClassModel)
            .filter(SportClassModel.id == sports_class_id)
            .one()
        )
    except exc.NoResultFound:
        raise SportClassNotFound()

    if user not in sport_class.users:
        raise UserNotInClass()

    enrollment = EnrollmentModel(
        enroll=False, sport_class_id=sports_class_id, user_id=user.id
    )
    db.add(enrollment)

    sport_class.users.remove(user)

    db.commit()
    return user


def get_user_enrollments_service(
    user: UserModel, date_start: datetime, date_end: datetime, db: Session
):
    query = db.query(EnrollmentModel).filter(EnrollmentModel.user_id == user.id)
    if date_start:
        query = query.filter(EnrollmentModel.created_at > date_start)
    if date_end:
        query = query.filter(EnrollmentModel.created_at < date_end)

    return query.all()
