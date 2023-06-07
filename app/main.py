from fastapi import FastAPI
from app.routers import users, login, tweets

app = FastAPI()
app.include_router(users.router)
app.include_router(login.router)
app.include_router(tweets.router)

@app.get('/')
def root():
    return { "message": "Welcome to our Twitter Clone! Go to '/docs' for the API documentation." }
