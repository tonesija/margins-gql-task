from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.db.userssportsclasses import users_sports_classes


class SportClassModel(Base):
    __tablename__ = "sportclasses"

    id: int = Column(Integer, primary_key=True, index=True)
    description: str = Column(String)
    age_group: str = Column(String, nullable=False)

    sport_id: int = Column(ForeignKey("sports.id"), nullable=False)
    sport = relationship("SportModel", uselist=False, back_populates="sport_classes")

    enrollments = relationship("EnrollmentModel", back_populates="sport_class")
    sport_class_events = relationship(
        "SportClassEventModel", back_populates="sport_class"
    )
    sport_class_reviews = relationship(
        "SportClassReviewModel", back_populates="sport_class"
    )
    users = relationship(
        "UserModel", secondary=users_sports_classes, back_populates="sport_classes"
    )
