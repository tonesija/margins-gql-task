from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class SportModel(Base):
    __tablename__ = "sports"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False)

    sport_classes = relationship("SportClassModel", back_populates="sport")
