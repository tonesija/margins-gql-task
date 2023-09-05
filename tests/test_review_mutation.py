from fastapi.testclient import TestClient

from app.db.database import get_session
from app.db.sportclass import SportClassModel
from app.db.sportclassreview import SportClassReviewModel
from app.db.user import UserModel
from tests.fixtures.helpers import mock_authenticated_user


def test_review_mutation(client: TestClient, seed_sports_classes, mocker):
    with get_session() as db:
        num_sport_class_reviews = db.query(SportClassReviewModel).count()
        sport_class = db.query(SportClassModel).first()
        user = db.query(UserModel).first()

        mock_authenticated_user(mocker, user)

        mutation = (
            """
            mutation Review {
            rateSportsClass(
                sportClassReview: {sportsClassId: "%s", rating: 3, comment: "Heyoo"}
            ) {
                ... on SportsClassRating {
                id
                sportsClass {
                    id
                }
                }
                ... on SportClassNotExists {
                __typename
                }
            }
            }

        """
            % sport_class.id
        )
        payload = {"operationName": "Review", "query": mutation, "variables": {}}

        res = client.post(
            "/graphql",
            json=payload,
            headers={"Authorization": "Bearer mocked_access_token"},
        )

    assert res.status_code == 200

    json = res.json()
    assert json["data"]["rateSportsClass"]["sportsClass"]["id"] == str(sport_class.id)

    with get_session() as db:
        assert num_sport_class_reviews + 1 == db.query(SportClassReviewModel).count()
