from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class EnrollmentModel(Base):
    __tablename__ = "enrollment"

    id: int = Column(Integer, primary_key=True, index=True)
    created_at: datetime = Column(DateTime, nullable=False, default=datetime.utcnow)
    enroll: bool = Column(Boolean, nullable=False)

    user_id: int = Column(ForeignKey("users.id"), nullable=False)
    user = relationship("UserModel", uselist=False, back_populates="enrollments")

    sport_class_id: int = Column(ForeignKey("sportclasses.id"), nullable=False)
    sport_class = relationship(
        "SportClassModel", uselist=False, back_populates="enrollments"
    )
