from app.schema.gql_context import Info
from app.schema.types.response_types import (
    CreateSportClassEventResponse,
    DeleteSportClassEventResponse,
    GetSportClassResponse,
    SportCallEventDeleted,
    SportClassEventNotExists,
    SportClassNotExists,
    UpdateSportClassResponse,
)
from app.schema.types.sport_class_types import (
    Sport,
    SportClassEventInput,
    SportClassFilterInput,
    SportClassInput,
    SportClassUpdateInput,
    SportsClass,
    SportsClassEvent,
)
from app.services.exceptions import SportClassNotFound
from app.services.sport_class_event_service import (
    create_sports_class_event_service,
    delete_sports_class_event_service,
)
from app.services.sport_class_service import (
    create_sport_class_service,
    get_sport_class_service,
    get_sports_classes_service,
    get_sports_service,
    update_sport_class_service,
)


def get_sports_resolver(info: Info) -> list[Sport]:
    sports_db = get_sports_service(info.context.db)
    return [Sport.from_orm(sport_db) for sport_db in sports_db]


def get_sports_classes_resolver(
    sport_class_filter: SportClassFilterInput, info: Info
) -> list[SportsClass]:
    sport_classes_db = get_sports_classes_service(sport_class_filter, info.context.db)
    return [SportsClass.from_orm(sport_class_db) for sport_class_db in sport_classes_db]


def get_sport_class_resolver(sport_class_id: int, info: Info) -> GetSportClassResponse:
    try:
        sport_class_db = get_sport_class_service(sport_class_id, info.context.db)
    except SportClassNotFound:
        return SportClassNotExists()

    return SportsClass.from_orm(sport_class_db)


def create_sport_class_resolver(
    sport_class: SportClassInput, info: Info
) -> SportsClass:
    sport_class_db = create_sport_class_service(sport_class, info.context.db)
    return SportsClass.from_orm(sport_class_db)


def update_sport_class_resolver(
    sport_class: SportClassUpdateInput, info: Info
) -> UpdateSportClassResponse:
    try:
        sport_class_db = update_sport_class_service(sport_class, info.context.db)
    except SportClassNotFound:
        return SportClassNotExists()

    return SportsClass.from_orm(sport_class_db)


def create_sports_class_event_resolver(
    sport_class_event: SportClassEventInput, info: Info
) -> CreateSportClassEventResponse:
    sport_class_event_db = create_sports_class_event_service(
        sport_class_event, info.context.db
    )
    return SportsClassEvent.from_orm(sport_class_event_db)


def delete_sports_class_event_resolver(
    sport_class_event_id: int, info: Info
) -> DeleteSportClassEventResponse:
    if delete_sports_class_event_service(sport_class_event_id, info.context.db):
        return SportCallEventDeleted()
    else:
        return SportClassEventNotExists()
