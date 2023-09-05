from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class EmailVerificationTokenModel(Base):
    __tablename__ = "emailverificationtokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)

    user_id = Column(ForeignKey("users.id"))
    user = relationship(
        "UserModel",
        back_populates="email_verification_tokens",
        uselist=False,
        post_update=True,
    )
