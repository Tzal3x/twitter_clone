# Twitter Clone 🐦 👥

A Twitter clone implemented using Python's FastAPI library for educational purposes.

## Features (In Progress 👷🔧) 

- User Registration: Create accounts and login. 
- Post Tweets: Share short messages, including text, images, links, and hashtags.
- Following: Stay updated by following other accounts and seeing their tweets.
- Retweeting: Share someone else's tweet with your followers.
- Liking: Show appreciation or agreement by liking a tweet.
- Replying: Engage in conversations by replying to tweets.
- Hashtags: Categorize tweets and make them discoverable by adding hashtags.
- Mentions: Tag other accounts in tweets using "@" to initiate communication.
- Timeline: View a chronological feed of tweets from accounts you follow.
- Search: Find specific topics, hashtags, or accounts to discover relevant tweets.

## Requirements

- Python 3.10 +
- PostgreSQL 14.8 +

## Installation

Use the following command to install the required dependencies:

```shell
pip install -r requirements.txt
```

## Setup

1. Create a `configs.env` file in the project's directory.
2. Specify the following fields in the `configs.env` file:

   ```shell
   DB_SERVICE = ******
   DB_USERNAME = ******
   DB_PASSWORD = ******
   DB_HOST = ******
   DB_NAME = ******

   TOKEN_CREATION_SECRET_KEY = ******
   ACCESS_TOKEN_EXPIRE_MINUTES = ******
   HASH_ALGORITHM = ******
   ```

## Testing

To run the tests, execute the following command:

```shell
pytest -v
```
⚠️ *A database is needed to run the tests!*

## Running the Application

To run the application, being on the root project directory `/twitter_clone` use the following command:

```shell
uvicorn app.main:app
```
