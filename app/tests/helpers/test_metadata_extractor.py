import pytest
from app.helpers import MetadataExtractor


@pytest.fixture
def mock_tweet():
    return {
        "title": "Hello world! #greeting",
        "body": "This is a tweet body. #testing #pytest"
    }


def test_extract_hashtags(mock_tweet):
    expected_hashtags_set = {"greeting", "testing", "pytest"}
    hashtags = MetadataExtractor.extract_hashtags(mock_tweet)
    assert set(hashtags) == expected_hashtags_set


def test_extract_hashtags_no_hashtags(mock_tweet):
    mock_tweet["title"] = "Hello world!"
    mock_tweet["body"] = "This is a tweet body."
    hashtags = MetadataExtractor.extract_hashtags(mock_tweet)
    assert hashtags == []


def test_extract_hashtags_empty_tweet():
    mock_tweet = {"title": "", "body": ""}
    hashtags = MetadataExtractor.extract_hashtags(mock_tweet)
    assert hashtags == []
