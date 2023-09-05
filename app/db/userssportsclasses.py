from sqlalchemy import Column, ForeignKey, Table

from app.db.database import Base

users_sports_classes = Table(
    "users_sports_classes",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("sport_class_id", ForeignKey("sportclasses.id"), primary_key=True),
)
