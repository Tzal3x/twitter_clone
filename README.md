# Twitter Clone 🐦 👥

A Twitter clone implemented using Python's FastAPI library for educational purposes.

## Features (In Progress 👷🔧) 

 - 👤 **User Registration**: Create accounts and login. 

- ✉️ **Post Tweets**: Share short messages, including text, images, links, and hashtags.

- 👀 **Following**: Stay updated by following other accounts and seeing their tweets.

- 🔄 **Retweeting**: Share someone else's tweet with your followers.

- 💙 **Liking**: Show appreciation or agreement by liking a tweet.

- 💬 **Replying**: Engage in conversations by replying to tweets with comments.

- #️⃣ **Hashtags**: Categorize tweets and make them discoverable by adding hashtags.

- 🔔 **Mentions**: Tag other accounts in tweets using "@" to initiate communication.

- 🕒 **Timeline**: View a chronological feed of tweets from accounts you follow.

- 🔎 **Search**: Find specific topics, hashtags, or accounts to discover relevant tweets.

## Project setup

Create a `.env` file in the project directory. This file should contain the following fields:

```
DB_SERVICE=postgresql
DB_USERNAME=postgres
DB_PASSWORD=mysupersecretpassword
DB_NAME=twitter_clone
DB_PORT=5432
DB_HOST=postgres:5432
HASH_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
TOKEN_CREATION_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
GRAYLOG_PASSWORD_SECRET=mysupersecretpassword
GRAYLOG_ROOT_PASSWORD_SHA2=a7fdfe53e2a13cb602def10146388c65051c67e60ee55c051668a1c709449111
```

**Warning!** The field values are examples. You should use different values for safety purposes.

### Setup using Docker
Requirements: 
- Docker version 24.0.4+

Setup the project with: 

`$ docker compose up -d` 

Teardown the project with: 

`$ docker compose down` 

**Note that currently we are using volumes to have persistent data**. If you need to delete all volumes run `$ docker compose down --volumes`


### Access the API 

You can access the API on http://0.0.0.0:80.

The API documentation can be found on http://0.0.0.0:80/docs or http://0.0.0.0:80/redoc.

### Testing with Docker

To run the tests, execute the following command:

```shell
$ docker exec -it twitter_clone_web_server sh -c "pytest"
```

## Local Setup (useful for debugging) 🐛

Requirements:
- Python 3.10.6+
- PostgreSQL 14

Create a python virtual environment:

```shell
$ python3 -m venv .venv
```

Activate the virtual environment:

For Linux/MacOS:
```shell
$ source .venv/bin/activate
```

For Windows (PowerShell):
```shell
$ .venv\Scripts\Activate.ps1
```

Install the requirements:

```shell
$ pip install -r requirements.txt
```

Then run the migrations with:

```shell
$ alembic upgrade head
```

**⚠️ Important note!** You need to have already setup a `twitter_clone` database in **PostgreSQL**. This is important because if no database exists, running the migrations will fail. The credentials and any other crucial information about the database should be included in the corresponding fields of the `.env` file.  

### Running the local app

To run the application, being on the root project directory `/twitter_clone` use the following command:

```shell
$ uvicorn app.main:app --reload --host "127.0.0.1" --port 80 
```

The `reload` flag is useful while debugging because it will recompile the server on the spot every time it detects a change in the code, without needing for you to stop and re-run your program all the time.


### Testing on the local setup

For the tests we are using the pytest framework.

To run the tests use the following command:
```shell
$ pytest -v
```

Happy tweeting! 🙇‍♂️
