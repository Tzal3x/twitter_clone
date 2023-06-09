"""
TODO test_create_invalid_users(invalid_user)
TODO test_invalid_patching(user) Try changing username or email
"""

import pytest
from fastapi import status
import app.tests.users.user_cases as cases
from app.tests.conftest import create_header


@pytest.mark.parametrize("user", cases.users)
def test_create_user(user, client):
    response = client.post("users/", json=user)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.depends(on=['test_create_user'])
@pytest.mark.parametrize("user", cases.users)
def test_get_current(user, client):
    response = client.get("users/me",
                          headers=create_header(user["username"]))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.depends(on=['test_create_user'])
@pytest.mark.parametrize("user", cases.users)
def test_get_specific_user(user, client):
    response = client.get("users/?username=%s" % user["username"],
                          headers=create_header(user["username"]))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.depends(on=['test_create_user'])
@pytest.mark.parametrize("user", cases.users[:2])
def test_update_current_user_info(user, client):
    response = client.patch("users/", 
                            json={
                                "first_name": "Updated Name",
                                "last_name": "Updated Last Name",
                                "birth": "1994-03-01",
                                "bio": "Updated bio"
                            },
                            headers=create_header(user["username"]))
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.depends(on=['test_create_user'])
@pytest.mark.parametrize("user", cases.users[:2])
def test_delete_current_account(user, client):
    response = client.delete("users/", headers=create_header(user["username"]))
    assert response.status_code == status.HTTP_204_NO_CONTENT