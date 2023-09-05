from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class SportClassReviewModel(Base):
    __tablename__ = "sportclassreviews"

    id: int = Column(Integer, primary_key=True, index=True)
    comment: str = Column(String)
    rating: int = Column(Integer, nullable=False)

    sport_class_id: int = Column(ForeignKey("sportclasses.id"), nullable=False)
    sport_class = relationship(
        "SportClassModel", uselist=False, back_populates="sport_class_reviews"
    )
