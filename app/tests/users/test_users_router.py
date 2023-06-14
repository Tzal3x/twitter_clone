import pytest
from fastapi import status
from app.tests.conftest import client
from app.tests.cases.user_cases import invalid_users_validator_fail


@pytest.mark.usefixtures("user")
def test_create_and_delete_user():
    """
    Using the "user" fixture, for each user case
    a user is created and deleted implicitly.
    """


@pytest.mark.usefixtures("user")
def test_get_current():
    """
    Create user, test get user, delete user.
    """
    response = client.get("users/me")
    assert response.status_code == status.HTTP_200_OK


def test_get_specific_user(user):
    """
    Create user, test get specific user, delete user.
    """
    response = client.get("users/?username=%s" % user["username"])
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.usefixtures("user")
def test_update_current_user_info():
    """
    Create user, test update current user, delete user.
    """
    response = client.patch("users/",
                            json={
                                "first_name": "Updated Name",
                                "last_name": "Updated Last Name",
                                "birth": "1994-03-01",
                                "bio": "Updated bio"
                            })
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.parametrize("invalid_user", invalid_users_validator_fail)
def test_create_invalid_user(invalid_user):
    response = client.post("/users", json=invalid_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
