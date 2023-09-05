from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.db.userssportsclasses import users_sports_classes


class UserModel(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String, nullable=False)
    age_group: str = Column(String, nullable=False)
    role: str = Column(String, nullable=False, default="user")
    verified: bool = Column(Boolean, nullable=False, default=False)

    enrollments = relationship(
        "EnrollmentModel", back_populates="user", cascade="all,delete"
    )

    sport_classes = relationship(
        "SportClassModel", secondary=users_sports_classes, back_populates="users"
    )

    email_verification_tokens = relationship(
        "EmailVerificationTokenModel", cascade="all,delete"
    )
