import json
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from app.main import app
from app.security import create_access_token
from app.tests.user_cases import users
from app.tests.tweets.tweet_cases import tweets


client = TestClient(app)


@pytest.fixture(params=users, name="user")
def temp_user(request):
    """
    Creates a temp user before a test that uses this 
    fixture and when the test ends, the user
    gets deleted.
    """
    # Setup
    token = user_setup(user:=request.param)
    client.headers["Authorization"] = "Bearer %s" % token

    yield user

    # Teardown:
    response = client.delete("/users/")
    assert response.status_code == status.HTTP_204_NO_CONTENT, "User deletion failed!"


def user_setup(user: dict) -> str:
    """
    Given a user dict, creates the user entry in the database
    using the corresponding endpoint and returns an access token.
    """
    response = client.post("/users/", json=user)
    assert response.status_code == status.HTTP_201_CREATED, "User creation failed!"

    token = create_access_token(
        {'sub': user["username"]}
        )
    return token


# FIXME: user fixture is not seen by this one!
@pytest.mark.usefixtures("user")
@pytest.fixture(params=tweets, name="tweet")
def temp_tweet(request):
    tweet = request.param
    response = client.post("tweets/", json=tweet)
    assert response.status_code == status.HTTP_201_CREATED

    tweet = json.loads(response.content.decode('utf-8'))
    yield tweet

    response = client.delete(f"tweets/{tweet['id']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
