from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class SportClassEventModel(Base):
    __tablename__ = "sportclassevents"

    id: int = Column(Integer, primary_key=True, index=True)
    starts_at: datetime = Column(DateTime, nullable=False)
    duration: int = Column(Integer)

    sport_class_id: int = Column(ForeignKey("sportclasses.id"), nullable=False)
    sport_class = relationship(
        "SportClassModel", uselist=False, back_populates="sport_class_events"
    )
