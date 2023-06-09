import pytest
from fastapi import status
import app.tests.tweets.tweet_cases as cases
from app.schemas import TweetReturn
from app.tests.conftest import client


@pytest.mark.parametrize("tweet", cases.tweets)
@pytest.mark.usefixtures("user")
def test_create_tweet(tweet):
    res = client.post("tweets/", json=tweet)
    pytest.last_created_tweet_id = TweetReturn(**res.json()).id
    assert res.status_code == status.HTTP_201_CREATED


def test_get_tweet_details(tweet):
    res = client.get(f"tweets/{tweet['id']}")
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.usefixtures("tweet")
def test_get_tweets_of_logged_in_user():
    res = client.get(f"tweets/per_user/me")
    
    assert res.status_code == status.HTTP_200_OK
    

# @pytest.mark.depends(on=['test_create_tweet'])
# def test_update_tweet_title(client):
#     id = pytest.last_created_tweet_id
#     res = client.put(
#         f"tweets/{id}",
#         json={
#             "title": "Updated title",
#             "body": "Updated content",
#         },
#         headers=create_header(pytest.test_user_1_username))
    
#     updated_tweet = TweetReturn(**res.json())
#     assert updated_tweet.title == "Updated title"
#     assert updated_tweet.body == "Updated content"
    

# @pytest.mark.depends(on=['test_create_tweet'])
# def test_delete_tweet(client):
#     id = pytest.last_created_tweet_id - 1
#     res = client.delete(
#         f"tweets/{id}",
#         headers=create_header(pytest.test_user_1_username))
    
#     assert res.status_code == status.HTTP_204_NO_CONTENT
    

# @pytest.mark.depends(on=['test_delete_tweet'])
# def test_get_deleted_tweet_details(client):
#     id = pytest.last_created_tweet_id - 1
#     res = client.get(
#         f"tweets/{id}",
#         headers=create_header(pytest.test_user_1_username))
    
#     assert res.status_code == status.HTTP_404_NOT_FOUND