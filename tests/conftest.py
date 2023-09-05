import pytest
import strawberry
from fastapi.testclient import TestClient
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.db.database import Base, engine, get_session
from app.main import app
from app.schema.gql_schema import schema as app_schema
from tests.fixtures.seed_sport_classes import seed_sports_classes
from tests.fixtures.seed_sports import seed_sports
from tests.fixtures.seed_users import seed_users


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    if not database_exists(engine.url):
        create_database(engine.url)

    yield
    drop_database(engine.url)


@pytest.fixture(autouse=True)
def clean_database():
    yield
    with get_session() as db:
        for tbl in reversed(Base.metadata.sorted_tables):
            db.execute(tbl.delete())
        db.commit()
