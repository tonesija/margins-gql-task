import asyncio
import secrets
from hashlib import sha256

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.db.emailverificationtoken import EmailVerificationTokenModel
from app.db.user import UserModel
from app.services.exceptions import EmailVerificationFailed
from app.settings import get_settings

conf = ConnectionConfig(
    MAIL_USERNAME=get_settings().mail_username,
    MAIL_PASSWORD=get_settings().mail_password,
    MAIL_FROM=get_settings().mail_from,
    MAIL_PORT=get_settings().mail_port,
    MAIL_SERVER=get_settings().mail_server,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


def verify_email_service(token: str, db: Session):
    """
    Raises:
        EmailVerificationFailed: _description_
    """
    hashed_email_recovery_token = sha256(token.encode("utf-8")).hexdigest()

    try:
        email_recovery_token_db = (
            db.query(EmailVerificationTokenModel)
            .filter(EmailVerificationTokenModel.token == hashed_email_recovery_token)
            .first()
        )

        user_db: UserModel = (
            db.query(UserModel)
            .filter(UserModel.id == email_recovery_token_db.user_id)
            .one()
        )

        db.query(EmailVerificationTokenModel).filter(
            EmailVerificationTokenModel.user_id == user_db.id
        ).delete()

        user_db.verified = True

        db.commit()
    except exc.NoResultFound:
        raise EmailVerificationFailed()


def send_verify_email_and_create_token(user: UserModel, db: Session):
    raw_email_verification_token = secrets.token_urlsafe(64)
    hashed_email_verification_token = sha256(
        raw_email_verification_token.encode("utf-8")
    ).hexdigest()

    email_verification_token = EmailVerificationTokenModel(
        token=hashed_email_verification_token,
        user_id=user.id,
    )
    db.add(email_verification_token)
    db.commit()

    message = MessageSchema(
        subject="Test",
        recipients=[user.email],
        body=f"Email verification token: {raw_email_verification_token}",
        subtype=MessageType.plain,
    )

    asyncio.get_running_loop().create_task(send_email(message))


async def send_email(message: MessageSchema):
    fm = FastMail(conf)
    await fm.send_message(message)
