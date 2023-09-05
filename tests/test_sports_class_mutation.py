from fastapi.testclient import TestClient

from app.constants import UserRole
from app.db.database import get_session
from app.db.sportclass import SportClassModel
from app.db.user import UserModel
from tests.fixtures.helpers import mock_authenticated_user


def test_mutation(client: TestClient, seed_sports_classes: None, mocker):
    with get_session() as db:
        num_sport_classes = db.query(SportClassModel).count()
        admin_user = (
            db.query(UserModel).filter(UserModel.role == UserRole.ADMIN.value).first()
        )

        mock_authenticated_user(mocker, admin_user)

        mutation = """
            mutation CreateSportsClass {
                createSportsClass(
                    sportClass: {sportId: 1, ageGroup: CHILDREN, description: "Desc"}
                ) {
                    id
                    ageGroup
                    description
                }
            }
        """
        payload = {
            "operationName": "CreateSportsClass",
            "query": mutation,
            "variables": {},
        }

        res = client.post(
            "/graphql",
            json=payload,
            headers={"Authorization": "Bearer mocked_access_token"},
        )

    assert res.status_code == 200

    json = res.json()
    assert json["data"]["createSportsClass"]["description"] == "Desc"

    with get_session() as db:
        assert num_sport_classes + 1 == db.query(SportClassModel).count()
