from strawberry import BasePermission

from app.constants import UserRole
from app.schema.gql_context import Info


class IsAuthenticated(BasePermission):
    message = "User is not authorized"

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        # TODO: check verified (won't for the sake of demonstrations)
        if info.context.authenticated_user:
            return True
        else:
            return False


class IsAdmin(BasePermission):
    message = "User is not authorized"

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        if (
            info.context.authenticated_user
            and info.context.authenticated_user.role == UserRole.ADMIN.value
        ):
            return True
        else:
            return False
