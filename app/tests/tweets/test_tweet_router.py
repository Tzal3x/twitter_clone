"""
Tweet related tests.
"""
import pytest
from fastapi import status
from app.schemas import TweetReturn
from app.tests.conftest import client


@pytest.mark.usefixtures("user", "multiple_temp_tweets")
def test_create_and_delete_tweet():
    """
    Create user, create multiple tests, delete the tests
    and then delete the users. 

    All those steps are happening implicitly by just 
    calling the fixtures.
    """


@pytest.mark.usefixtures("user")
def test_get_tweet_details(tweet):
    """
    Create user, create tweet, get tweet, delete user 
    (and delete tweet due to CASCADE.)
    """
    res = client.get(f"tweets/{tweet['id']}")
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.usefixtures("user", "multiple_temp_tweets")
def test_get_tweets_of_logged_in_user():
    """
    Create users, create multiple tweets for each user, 
    test get tweets of users, delete tweets, delete users. 
    """
    res = client.get("tweets/per_user/me")
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.usefixtures("user")
def test_update_tweet_title(tweet):
    """
    Create user, create a tweet, test update tweet, 
    delete tweet, delete user.
    """
    res = client.put(
        f"tweets/{tweet['id']}",
        json={
            "title": "Updated title",
            "body": "Updated content",
        })
    assert res.status_code == status.HTTP_200_OK
    updated_tweet = TweetReturn(**res.json())
    assert updated_tweet.title == "Updated title"
    assert updated_tweet.body == "Updated content"

#TODO: create fixtures to test on porpose false
# requests such as get_deleted_tweet
