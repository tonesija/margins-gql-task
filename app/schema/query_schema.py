import strawberry

from app.resolvers.sports_class_resolvers import (
    get_sport_class_resolver,
    get_sports_classes_resolver,
    get_sports_resolver,
)
from app.resolvers.user_resolvers import (
    get_me_resolver,
    get_user_by_id_resolver,
    get_users_resolver,
)
from app.schema.types.response_types import GetSportClassResponse, GetUserResponse
from app.schema.types.sport_class_types import Sport, SportsClass
from app.schema.types.user_types import User
from app.services.auth.authorization import IsAdmin, IsAuthenticated


@strawberry.type
class Query:
    # --- User queries ---

    sports: list["Sport"] = strawberry.field(
        resolver=get_sports_resolver, permission_classes=[IsAuthenticated]
    )

    sports_classes: list[SportsClass] = strawberry.field(
        resolver=get_sports_classes_resolver, permission_classes=[IsAuthenticated]
    )

    sports_class: GetSportClassResponse = strawberry.field(
        resolver=get_sport_class_resolver, permission_classes=[IsAuthenticated]
    )

    me: User = strawberry.field(
        resolver=get_me_resolver, permission_classes=[IsAuthenticated]
    )

    # --- Admin queries ---

    user: GetUserResponse = strawberry.field(
        resolver=get_user_by_id_resolver, permission_classes=[IsAdmin]
    )

    users: list[User] = strawberry.field(
        resolver=get_users_resolver, permission_classes=[IsAdmin]
    )
