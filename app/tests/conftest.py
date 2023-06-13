"""
This is a special module that gets detected
by pytest and automatically imports the fixtures
to the other test suites. 

We also define test configurations were needed. 
"""
import json
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from app.main import app
from app.security import create_access_token
from app.tests.cases.user_cases import users
from app.tests.cases.tweet_cases import tweets


client = TestClient(app)


@pytest.fixture(params=users, name="user")
def temp_user(request):
    """
    Creates a temp user before a test that uses this 
    fixture and when the test ends, the user
    gets deleted.
    """
    # Setup
    token = user_setup(user := request.param)
    client.headers["Authorization"] = f"Bearer {token}"

    yield user

    # Teardown:
    response = client.delete("/users/")
    assert response.status_code == status.HTTP_204_NO_CONTENT, \
        f"User deletion failed! {response.content}"


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


@pytest.fixture(params=tweets, name="tweet")
def temp_tweet(request):
    """
    Creates a temp tweet -for each tweet in the fixture params-
    before a test that uses this fixture and when the test ends,
    the user gets deleted.

    It should be used together with the temp_user fixture on tests.
    """
    tweet = request.param
    response = client.post("tweets/", json=tweet)
    assert response.status_code == status.HTTP_201_CREATED

    tweet = json.loads(response.content.decode('utf-8'))
    yield tweet

    response = client.delete(f"tweets/{tweet['id']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, "Failed to delete tweet!"


@pytest.fixture
def multiple_temp_tweets():
    """
    Creates multiple tweets so that a user can have many at once.
    Then when the test ends, the tweets get deleted (teardown step). 
    """
    created_tweets = []
    for tweet in tweets:
        response = client.post("tweets/", json=tweet)
        assert response.status_code == status.HTTP_201_CREATED
        created_tweet = json.loads(response.content.decode('utf-8'))
        created_tweets.append(created_tweet)

    yield created_tweets

    # Teardown
    for created_tweet in created_tweets:
        tweet_id = created_tweet["id"]
        response = client.delete(f"tweets/{tweet_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT, "Failed to delete tweet!"
