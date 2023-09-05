from fastapi.testclient import TestClient

from app.db.database import get_session
from app.db.sportclass import SportClassModel
from app.db.user import UserModel
from tests.fixtures.helpers import mock_authenticated_user


def test_enroll_user(client: TestClient, seed_sports_classes: None, mocker):
    with get_session() as db:
        sport_class = db.query(SportClassModel).first()
        user = db.query(UserModel).first()
        user.age_group = sport_class.age_group
        sport_class_id = sport_class.id
        db.commit()

        mock_authenticated_user(mocker, user)

        mutation = (
            """
            mutation Enroll {
            enrollSportsClass(sportsClassId: "%s") {
                ... on User {
                email
                id
                enrolledClasses {
                    ageGroup
                    id
                }
                }
            }
            }
        """
            % sport_class_id
        )
        payload = {"operationName": "Enroll", "query": mutation, "variables": {}}

        res = client.post(
            "/graphql",
            json=payload,
            headers={"Authorization": "Bearer mocked_access_token"},
        )

    assert res.status_code == 200

    json = res.json()
    assert json["data"]["enrollSportsClass"]["enrolledClasses"][0]["id"] == str(
        sport_class_id
    )


def test_enroll_user_twice(client: TestClient, seed_sports_classes: None, mocker):
    with get_session() as db:
        sport_class = db.query(SportClassModel).first()
        user = db.query(UserModel).first()
        user.age_group = sport_class.age_group
        sport_class_id = sport_class.id
        db.commit()

        mock_authenticated_user(mocker, user)

        mutation = (
            """
            mutation Enroll {
            enrollSportsClass(sportsClassId: "%s") {
                ... on UserAlreadyEnrolled {
                    __typename
                    message
                }
            }
            }
        """
            % sport_class_id
        )
        payload = {"operationName": "Enroll", "query": mutation, "variables": {}}

        client.post(
            "/graphql",
            json=payload,
            headers={"Authorization": "Bearer mocked_access_token"},
        )
        res = client.post(
            "/graphql",
            json=payload,
            headers={"Authorization": "Bearer mocked_access_token"},
        )

    assert res.status_code == 200

    json = res.json()
    assert (
        json["data"]["enrollSportsClass"]["message"]
        == "User is already enrolled in that class"
    )


def test_enroll_user_sports_class_max_capacity(
    client: TestClient, seed_sports_classes: None, mocker
):
    with get_session() as db:
        sport_class = db.query(SportClassModel).first()
        for i in range(10):
            user_db = UserModel(
                name=f"N{i}",
                email=f"email{i}",
                hashed_password="pass",
                age_group=sport_class.age_group,
            )
            db.add(user_db)
            sport_class.users.append(user_db)

        new_user_db = UserModel(
            name=f"new",
            email=f"email_new",
            hashed_password="pass",
            age_group=sport_class.age_group,
        )
        db.add(new_user_db)
        db.commit()

        sport_class_id = sport_class.id

        mock_authenticated_user(mocker, new_user_db)

        mutation = (
            """
            mutation Enroll {
            enrollSportsClass(sportsClassId: "%s") {
                ... on ClassFull {
                __typename
                message
                }
            }
            }
        """
            % sport_class_id
        )
        payload = {"operationName": "Enroll", "query": mutation, "variables": {}}

        res = client.post(
            "/graphql",
            json=payload,
            headers={"Authorization": "Bearer mocked_access_token"},
        )

    assert res.status_code == 200

    json = res.json()
    assert (
        json["data"]["enrollSportsClass"]["message"] == "Class already has 10 members"
    )


def test_enroll_user_wrong_age_group(
    client: TestClient, seed_sports_classes: None, mocker
):
    with get_session() as db:
        sport_class = db.query(SportClassModel).first()
        user = db.query(UserModel).first()

    mock_authenticated_user(mocker, user)

    mutation = (
        """
        mutation Enroll {
        enrollSportsClass(sportsClassId: "%s") {
            ... on UserDifferentAgeGroup {
            __typename
            message
            }
        }
        }
    """
        % sport_class.id
    )
    payload = {"operationName": "Enroll", "query": mutation, "variables": {}}

    res = client.post(
        "/graphql",
        json=payload,
        headers={"Authorization": "Bearer mocked_access_token"},
    )

    assert res.status_code == 200

    json = res.json()
    assert (
        "User is not the same age group as the class"
        == json["data"]["enrollSportsClass"]["message"]
    )
