from functools import cached_property

from sqlalchemy.orm import Session
from strawberry.extensions import SchemaExtension
from strawberry.fastapi import BaseContext
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType

from app.db.database import SessionLocal
from app.db.user import UserModel
from app.services.auth.authentication import get_current_user


class Context(BaseContext):
    db: Session

    @cached_property
    def authenticated_user(self) -> UserModel | None:
        if not self.request:
            return None

        authorization = self.request.headers.get("Authorization", None)
        if not authorization:
            return None
        token = authorization.replace("Bearer: ", "")

        current_user = get_current_user(token, self.db)
        if current_user:
            print("Current user set:", current_user)
        return current_user


class SQLAlchemySession(SchemaExtension):
    def on_operation(self):
        self.execution_context.context.db = SessionLocal()
        yield
        self.execution_context.context.db.close()


Info = _Info[Context, RootValueType]


async def get_context() -> Context:
    return Context()
