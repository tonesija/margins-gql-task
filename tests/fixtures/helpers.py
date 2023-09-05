from app.db.user import UserModel


def mock_authenticated_user(mocker, user: UserModel):
    mocker.patch(
        "app.schema.gql_context.get_current_user",
        return_value=user,
    )
