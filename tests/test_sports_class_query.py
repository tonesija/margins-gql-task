from fastapi.testclient import TestClient

from app.db.database import get_session
from app.db.sportclass import SportClassModel
from app.db.user import UserModel
from tests.fixtures.helpers import mock_authenticated_user


def test_sport_class_query_all(client: TestClient, seed_sports_classes: None, mocker):
    with get_session() as db:
        num_sport_classes = db.query(SportClassModel).count()
        user = db.query(UserModel).first()

        mock_authenticated_user(mocker, user)

        query = """
            query GetSportClasses {
            sportsClasses(sportClassFilter: {ageGroups: [], sportIds: []}) {
                description
                id
                sport {
                id
                name
                }
                }
            }
        """
        payload = {"operationName": "GetSportClasses", "query": query, "variables": {}}

        res = client.post(
            "/graphql",
            json=payload,
            headers={"Authorization": "Bearer mocked_access_token"},
        )

    assert res.status_code == 200

    json = res.json()
    assert num_sport_classes == len(json["data"]["sportsClasses"])
