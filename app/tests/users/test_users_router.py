"""
TODO test_create_invalid_users(invalid_user)
TODO test_invalid_patching(user) Try changing username or email
"""

from fastapi import status
from app.tests.conftest import client


def test_create_and_delete_user():
    """
    Using the "user" fixture, for each user case
    a user is created and deleted implicitly.
    """


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
    response = client.get(f"users/?username={user['username']}")
    assert response.status_code == status.HTTP_200_OK


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
