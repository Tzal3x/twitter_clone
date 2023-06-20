FROM --platform=x86_64 python:3.10-alpine 

WORKDIR /twitter_clone
COPY ./requirements.txt /twitter_clone/requirements.txt
COPY ./alembic.ini /twitter_clone/alembic.ini
COPY ./migrations /twitter_clone/migrations

RUN pip install --no-cache-dir --upgrade -r /twitter_clone/requirements.txt

COPY ./app /twitter_clone/app 
EXPOSE 80
