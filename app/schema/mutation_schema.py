import strawberry

from app.resolvers.review_resolvers import review_sports_classes_resolver
from app.resolvers.sports_class_resolvers import (
    create_sport_class_resolver,
    create_sports_class_event_resolver,
    delete_sports_class_event_resolver,
    update_sport_class_resolver,
)
from app.resolvers.user_resolvers import (
    delete_user_resolver,
    enroll_user_id_sports_class_resolver,
    enroll_user_sports_class_resolver,
    login_user_resolver,
    register_user_resolver,
    unenroll_id_user_sports_class_resolver,
    unenroll_user_sports_class_resolver,
    verify_email_resolver,
)
from app.schema.types.response_types import (
    CreateSportClassEventResponse,
    DeleteSportClassEventResponse,
    DeleteUserResponse,
    EnrollResponse,
    LoginResponse,
    RegisterResponse,
    SportClassReviewResponse,
    UnEnrollResponse,
    UpdateSportClassResponse,
)
from app.schema.types.sport_class_types import SportsClass
from app.services.auth.authorization import IsAdmin, IsAuthenticated


@strawberry.type
class Mutation:
    register_user: RegisterResponse = strawberry.field(resolver=register_user_resolver)
    verify_email: bool = strawberry.field(resolver=verify_email_resolver)
    login_user: LoginResponse = strawberry.field(resolver=login_user_resolver)

    # --- User mutations ---

    enroll_sports_class: EnrollResponse = strawberry.field(
        resolver=enroll_user_sports_class_resolver, permission_classes=[IsAuthenticated]
    )
    unenroll_sports_class: UnEnrollResponse = strawberry.field(
        resolver=unenroll_user_sports_class_resolver,
        permission_classes=[IsAuthenticated],
    )
    rate_sports_class: SportClassReviewResponse = strawberry.field(
        resolver=review_sports_classes_resolver, permission_classes=[IsAuthenticated]
    )

    # --- Admin mutations ---

    delete_user: DeleteUserResponse = strawberry.field(
        resolver=delete_user_resolver, permission_classes=[IsAdmin]
    )

    enroll_some_user_sports_class: EnrollResponse = strawberry.field(
        resolver=enroll_user_id_sports_class_resolver, permission_classes=[IsAdmin]
    )

    unenroll_some_user_sports_class: UnEnrollResponse = strawberry.field(
        resolver=unenroll_id_user_sports_class_resolver, permission_classes=[IsAdmin]
    )

    create_sports_class: SportsClass = strawberry.field(
        resolver=create_sport_class_resolver, permission_classes=[IsAdmin]
    )

    update_sports_class: UpdateSportClassResponse = strawberry.field(
        resolver=update_sport_class_resolver, permission_classes=[IsAdmin]
    )

    create_sports_class_event: CreateSportClassEventResponse = strawberry.field(
        resolver=create_sports_class_event_resolver, permission_classes=[IsAdmin]
    )

    delete_sports_class_event: DeleteSportClassEventResponse = strawberry.field(
        resolver=delete_sports_class_event_resolver, permission_classes=[IsAdmin]
    )
